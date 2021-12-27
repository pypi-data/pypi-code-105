from __future__ import annotations
from typing import List, Union, Tuple, Optional, Any, Dict, Callable

# Try import torch; if not there, delegate to something else
from .torch_importer import *

# Import internals
from .scallopy import InternalScallopContext
from .collection import ScallopCollection
from .provenance import ScallopProvenance
from .io import CSVFileOptions

# Main context
class ScallopContext(Context):
  """
  A Scallop execution context that fosters all compilation and execution.

  Usage:

  ``` python
  ctx = ScallopContext()
  ```

  :param provenance: The type of provenance used during execution.
  Default to "unit", and can be any value from the set
  - `"unit"`, no provenance information associated
  - `"minmaxprob"`, min-max probability
  - `"topkproofs"`, top-k proofs. It is possible to supply a `k` value for this
    provenance
  - `"diffminmaxprob"`, differentiable min-max probability
  - `"difftopkproofs"`, differentiable top-k proofs. It is possible to supply a
    `k` value for this provenance
  """
  def __init__(
    self,
    provenance: str = "unit",
    custom_provenance: Optional[ScallopProvenance] = None,
    k: int = 3,
    train_k: Optional[int] = None,
    test_k: Optional[int] = None,
    fork_from: Optional[ScallopContext] = None
  ):
    super(ScallopContext, self).__init__()

    # Check if we are creating a forked context or not
    if fork_from is None:
      # Validify provenance; differentiable needs PyTorch
      if "diff" in provenance and not use_pytorch:
        raise Exception("Attempting to use differentiable provenance but with no PyTorch imported")

      # Setup
      self.provenance = provenance
      self._internal = InternalScallopContext(provenance=provenance,
                                              custom_provenance=custom_provenance,
                                              k=k)
      self._input_mappings = {}
      self._k = k
      self._train_k = train_k
      self._test_k = test_k
    else:
      # Fork from an existing context
      self.provenance = fork_from.provenance
      self._internal = fork_from._internal.clone()
      self._input_mappings = fork_from._input_mappings
      self._k = fork_from._k
      self._train_k = fork_from._train_k
      self._test_k = fork_from._test_k

  def clone(self) -> ScallopContext:
    """
    Clone the current context. This is useful for incremental execution:

    ``` python
    ctx2 = ctx.clone()
    ctx2.add_rule("...")
    ctx2.run()

    ctx3 = ctx.clone()
    ctx3.add_rule("...")
    ctx3.run()
    ```

    In this example, `ctx2` and `ctx3` will be executed independently,
    but both could inherit the computation already done on `ctx`.
    """
    return ScallopContext(fork_from=self)

  def run(self):
    """
    Execute the code under the current context. This operation is incremental
    and might use as many as previous information as possible.

    ``` python
    ctx.run()
    ```
    """
    self._internal.run()

  def forward_function(
    self,
    output: str,
    output_mapping: List[Tuple],
  ) -> Callable[[Dict[str, Tensor]], Dict[str, Tensor]]:
    """
    Generate a forward function for PyTorch module.
    """
    if not use_pytorch:
      raise Exception("`forward_function` cannot be called when there is no PyTorch import")

    # Needs to be a differentiable context
    if self.provenance == "diffminmaxprob":
      pass
    elif self.provenance == "difftopkproofs":
      pass
    else:
      raise Exception("`forward_function` can only be called on context with differentiable provenance")

    # Store a source context
    source_ctx = self

    # The forward function
    def forward(**input_facts: Dict[str, Tensor]):
      source_ctx._refresh_training_eval_state() # Set train/eval

      # First make sure that all facts share the same batch size
      num_datapoints = None
      for (_, rela_facts) in input_facts.items():
        if num_datapoints is None:
          num_datapoints = len(rela_facts)
        else:
          assert num_datapoints == len(rela_facts)

      # Then execute scallop for each datapoint
      input_tags = []
      output_results = []
      for task_id in range(num_datapoints):

        # Clone a context for scallop execution
        ctx = source_ctx.clone()

        # Put the facts into the context
        for (rela, rela_facts) in input_facts.items():
          fs = list(zip(rela_facts[task_id], ctx._input_mappings[rela]))
          ctx.add_facts(rela, fs)

        # Execute the context
        ctx.run()

        # Get input tags
        input_tags.append(ctx._internal.input_tags())

        # Get the internal collection for each output
        internal_iter = ctx._internal.relation(output)
        internal_result_dict = { tup: tag for (tag, tup) in internal_iter }
        output_results.append([internal_result_dict[t] if t in internal_result_dict else None for t in output_mapping])

      # Integrate the outputs
      v = source_ctx._batched_prob(output_results)
      if source_ctx._has_output_hook() and v.requires_grad:
        v.register_hook(source_ctx._batched_output_hook(input_tags, output_results))
      return v

    # Return the forward function
    return forward

  def _batched_prob(
    self,
    tasks: List[List[Any]],
  ) -> Tensor:
    if self.provenance == "diffminmaxprob":
      tensor_results = []
      for task_results in tasks:
        task_tensor_results = []
        for task_tup_result in task_results:
          if task_tup_result is not None:
            (s, p) = task_tup_result
            if s == 1:
              task_tensor_results.append(p)
            elif s == 0:
              task_tensor_results.append(torch.tensor(p, requires_grad=True))
            else:
              task_tensor_results.append(1 - p)
          else:
            task_tensor_results.append(torch.tensor(0.0, requires_grad=True))
        tensor_results.append(torch.stack(task_tensor_results))
      return torch.stack(tensor_results)
    elif self.provenance == "difftopkproofs":
      tensor_results = []
      for task_results in tasks:
        task_tensor_results = []
        for task_tup_result in task_results:
          if task_tup_result is not None:
            (p, _) = task_tup_result
            task_tensor_results.append(torch.tensor(p, requires_grad=True))
          else:
            task_tensor_results.append(torch.tensor(0.0, requires_grad=True))
        tensor_results.append(torch.stack(task_tensor_results))
      return torch.stack(tensor_results)
    else:
      raise Exception("[Internal Error] Should not happen")

  def _has_output_hook(self):
    if self.provenance == "difftopkproofs":
      return True
    else:
      return False

  def _batched_output_hook(
    self,
    input_tags: Optional[List[List[Any]]],
    tasks: List[List[Any]],
  ) -> Callable:
    if self.provenance == "diffminmaxprob":
      raise Exception("`diffminmaxprob` does not implement batched output hook")
    elif self.provenance == "difftopkproofs":
      return self._difftopkproofs_batched_output_hook(input_tags, tasks)
    else:
      raise Exception("[Internal Error] Should not happen")

  def _difftopkproofs_batched_output_hook(
    self,
    input_tags: List[List[Any]],
    output_batch: List[List[Any]],
  ) -> Callable:
    # Prepare the dimensions
    batch_size = len(output_batch)
    num_inputs = len(input_tags[0])
    num_outputs = len(output_batch[0])

    # mat_i: Input matrix
    mat_i = torch.stack([torch.stack(l) for l in input_tags])

    # mat_w: Weight matrix
    mat_w = torch.zeros(batch_size, num_outputs, num_inputs)
    for (batch_id, task_result) in enumerate(output_batch): # batch_size
      for (output_id, output_tag) in enumerate(task_result): # output_size
        if output_tag is not None:
          (_, deriv) = output_tag
          for (input_id, weight, _) in deriv:
            mat_w[batch_id, output_id, input_id] = weight

    # backward hook
    def hook(grad):
      mat_f = torch.einsum("ikj,ik->ij", mat_w, grad)
      mat_i.backward(mat_f)

    return hook

  def _refresh_training_eval_state(self):
    if self._train_k is not None or self._test_k is not None:
      if self.training: # Coming from nn.Module and `torch.train()` or `torch.eval()`
        if self._train_k is not None:
          self._internal.set_k(self._train_k)
        else:
          self._internal.set_k(self._k)
      else:
        if self._test_k is not None:
          self._internal.set_k(self._test_k)
        else:
          self._internal.set_k(self._k)

  def add_relation(
    self,
    relation_name: str,
    relation_types: Union[Tuple, type, str],
    load_csv: Optional[Union[CSVFileOptions, str]] = None,
    input_mapping: Optional[List[Tuple]] = None,
  ):
    """
    Add a relation to the context, where a relation is defined by its name
    and the tuple types.
    Idiomatic python types such as `str`, `int`, `bool` are supported, while
    internally being transformed into corresponding scallop types.
    (e.g. `int` -> `i32`).

    ``` python
    ctx.add_relation("edge", (int, int))
    ctx.add_relation("path", (int, int))
    ctx.add_relation("digit", int)
    ```

    Note that we usually accept a tuple. When a single element, such as `int`
    is provided, it will be internally transformed into a one-tuple.

    In addition to idiomatic python types, you can use the types provided in
    `types` module to gain access to native Scallop types:

    ``` python
    from scallopy import types
    ctx.add_relation("digit", (types.i8,))
    ```

    Of course, directly feeding type as string is ok too:

    ``` python
    ctx.add_relation("digit", "i8")
    ```

    You can load csv using this function

    ``` python
    ctx.add_relation(
      "edge", (int, int),
      load_csv = "FILE.csv",
    )
    ```

    If you wish to specify properties of CSV such as deliminator, you can
    use the `CSVFile` class

    ``` python
    edge_csv_file = CSVFile("FILE.csv", deliminator="\t")
    ctx.add_relation("edge", (int, int), load_csv=edge_csv_file)
    ```
    """

    # Helper function
    def _type_to_scallop_type_str(ty):
      if ty == str:
        return "Rc<String>"
      elif ty == int:
        return "i32"
      elif ty == bool:
        return "bool"
      elif ty == float:
        return "f32"
      elif type(ty) == str:
        return ty
      else:
        raise Exception(f"Unknown type `{ty}`")

    # Make sure that relation types is a tuple
    if type(relation_types) == tuple:
      relation_types_tuple = relation_types
    elif type(relation_types) == type or type(relation_types) == str:
      relation_types_tuple = (relation_types,)
    else:
      raise Exception(f"Unknown relation types `{relation_types}`")

    # Create the decl str
    types_str = ", ".join([_type_to_scallop_type_str(ty) for ty in relation_types_tuple])
    relation_decl_str = f"{relation_name}({types_str})"

    # Invoke internal's add relation
    inserted_relation_name = self._internal.add_relation(relation_decl_str, load_csv=load_csv)

    # Sanity check
    assert relation_name == inserted_relation_name

    # Store the input mapping
    if input_mapping is not None:
      self._input_mappings[relation_name] = input_mapping

  def add_facts(self, relation: str, elems: List[Tuple]):
    """
    Add facts to the relation under the context. The simple usage is as
    follows:

    ``` python
    ctx.add_facts("edge", [(0, 1), (1, 2)])
    ```

    Note that when adding relation, the relation name must be previously
    defined in the context using `add_relation` or by inferred from other
    rules. The function may throw error if the type does not match.

    When the context is associated with a non-unit provenance context,
    say "minmaxprob", one would need to provide the tag associated with
    each tuple. For "minmaxprob", as an example, one would need to invoke
    the function like this:

    ``` python
    ctx.add_facts("digit", [
      (0.90, (0, 1)),
      (0.01, (0, 2)),
      (0.03, (0, 3)),
    ])
    ```

    Note that there is a probability in the beginning and each tuple
    is now nested.

    :param relation: the name of the relation
    :param elems: the tuple elements
    """
    self._internal.add_facts(relation, elems)

  def add_rule(self, rule: str, tag: Optional[Any] = None):
    """
    Add rule to the context. The rule will be compiled and compilation
    error may be raised.

    ``` python
    ctx.add_rule("path(a, c) = edge(a, b), path(b, c)")
    ```

    In case non-unit provenance is used, a rule can be associated with
    tag. For example, in a probabilistic provenance context, one can
    associate probability with the rule.

    ``` python
    ctx.add_rule("born_in(a, \"china\") :- speaks(a, \"chinese\")", tag = 0.8)
    ```

    :param rule: a rule in scallop syntax
    :param tag: the tag associated with the rule
    """
    self._internal.add_rule(rule, tag=tag)

  def dump_front_ir(self):
    """
    Dump the Scallop front internal representation of the program compiled
    inside this context.
    """
    self._internal.dump_front_ir()

  def relation(self, relation: str) -> ScallopCollection:
    """
    Inspect the (computed) relation in the context. Will return
    a `ScallopCollection` which is iterable.

    ``` python
    for tuple in ctx.relation("edge"):
      print(tuple)
    ```

    :param relation: the name of the relation
    """
    return ScallopCollection(
      self.provenance,
      self._internal.relation(relation),
    )

  def relation_is_computed(self, relation: str) -> bool:
    """
    Check if the relation is computed.
    """
    return self._internal.relation_is_computed(relation)

  def num_relations(self, include_hidden: bool = False) -> int:
    """
    Get the number of relations in the context.
    """
    return self._internal.num_relations(include_hidden=include_hidden)

  def relations(self, include_hidden: bool = False) -> List[str]:
    """
    Get a list of user defined relations in the context.
    If `include_hidden` is specified to be `True`, will also return the auxilliary
    relations (such as sub-formula, permutation, etc) in the list.
    """
    return self._internal.relations(include_hidden=include_hidden)
