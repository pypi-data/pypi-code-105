class ScallopProvenance:
  """
  Base class for a provenance context. Any class implementing `ScallopProvenance`
  must override the following functions:
  - `base`
  - `zero`
  - `one`
  - `add`
  - `mult`
  """

  def base(self, info):
    """
    Given the base information, generate a tag for the tuple.
    Base information is specified as `I1`, `I2`, ... in the following example:

    ``` python
    ctx.add_facts("RELA", [(I1, T1), (I2, T2), ...])
    ```

    This `base` function should take in info like `I1` and return the base tag.
    """
    raise Exception("Not implemented")

  def disjunction_base(self, infos):
    """
    Given a set of base informations associated with a set of tuples forming a
    disjunction, return the list of tags associated with each of them.
    """
    return [self.base(i) for i in infos]

  def is_valid(self, tag):
    """
    Check if a given tag is valid.
    When a tag is invalid, the tuple associated will be removed during reasoning.
    The default implementation assumes every tag is valid.

    An example of an invalid tag: a probability tag of probability 0.0
    """
    return True

  def zero(self):
    """
    Get the `0` element of the provenance semiring
    """
    raise Exception("Not implemented")

  def one(self):
    """
    Get the `1` element of the provenance semiring
    """
    raise Exception("Not implemented")

  def add(self, t1, t2):
    """
    Perform semiring addition on two tags (`t1` and `t2`)
    """
    raise Exception("Not implemented")

  def mult(self, t1, t2):
    """
    Perform semiring multiplication on two tags (`t1` and `t2`)
    """
    raise Exception("Not implemented")
