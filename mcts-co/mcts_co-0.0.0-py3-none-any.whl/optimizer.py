from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Optional,
    TypeVar,
    Union,
)
import sys
import time
import math
from .statistical_value import StatisticalValue
from .search_space import SearchSpace

T = TypeVar("T")
State = TypeVar("State")
Action = TypeVar("Action")


class MCTSNode(Generic[Action]):
    def __init__(self):
        self.value = StatisticalValue()
        self.outgoing_arcs: list[MCTSArc[Action]] = []

    def is_leaf(self) -> bool:
        return len(self.outgoing_arcs) == 0


class MCTSArc(Generic[Action]):
    def __init__(self, action: Action, tail: MCTSNode[Action], head: MCTSNode[Action]):
        self.value = StatisticalValue()
        self.action = action
        self.head = head
        tail.outgoing_arcs.append(self)


class MCTSOptimizer(Generic[T, State, Action]):
    def __init__(
        self,
        objective: Callable[[frozenset[T]], float],
        search_space: SearchSpace[T, State, Action],
    ):
        self.objective = objective
        self.scale = 1.0
        self.search_space = search_space
        self.root = MCTSNode[Action]()
        self.transposition_table: Dict[State, MCTSNode[Action]] = {}
        StatisticalValue.use_var = True

    def tree_policy(self, node: MCTSNode[Action], a: float = 2.0, b: float = 1.0):
        best_arc, best_score = None, None
        for arc in node.outgoing_arcs:
            beta = arc.value.beta(count=node.value.count, a=a, b=b)
            score = arc.value.mean() + beta
            if best_score is None or score > best_score:
                best_score = score
                best_arc = arc
        assert best_arc is not None
        return best_arc

    def optimize_once(self):
        state = self.search_space.root()
        node = self.root
        path: list[Union[MCTSNode[Action], MCTSArc[Action]]] = [node]

        # Step 1. Selection
        while not node.is_leaf():
            arc = self.tree_policy(node)
            node = arc.head
            state = self.search_space.move(state, arc.action)
            path += [arc, node]

        # Step 2. Expansion
        actions = self.search_space.actions(state)
        if len(actions) > 0:
            for action in actions:
                new_state = self.search_space.move(state, action)
                if new_state not in self.transposition_table:
                    self.transposition_table[new_state] = MCTSNode()
                head = self.transposition_table[new_state]
                MCTSArc(action, node, head)
            arc = self.tree_policy(node)
            node = arc.head
            state = self.search_space.move(state, arc.action)
            path += [arc, node]

        # Step 3. Simulation
        state = self.search_space.rollout(state)
        solution = self.search_space.as_set(state)
        value = self.objective(solution)
        self.search_space.feedback(state, value)

        # Step 4. Backup
        for node_or_arc in path:
            node_or_arc.value.add(value)

    def optimal_solution(self) -> frozenset[T]:
        state = self.search_space.root()
        node = self.root
        while not node.is_leaf():
            arc = self.tree_policy(node, a=0.0)
            node = arc.head
            state = self.search_space.move(state, arc.action)
        state = self.search_space.rollout(state)
        solution = self.search_space.as_set(state)
        return solution

    def optimize(
        self,
        *,
        time_limit: Optional[float] = None,
        num_iterations: Optional[int] = None,
    ) -> frozenset[T]:
        assert time_limit is not None or num_iterations is not None
        time_limit = time_limit or math.inf
        num_iterations = num_iterations or sys.maxsize

        start_time = time.monotonic()
        for _ in range(num_iterations):
            self.optimize_once()
            if time.monotonic() - start_time >= time_limit:
                break
        return self.optimal_solution()

    def __repr__(self):
        result = "Tree(\n"
        state = [self.search_space.root()]
        depth = 2

        class StackItem:
            def __init__(self, name: str, item: Any):
                self.name = name
                self.item = item

            def unwrap(self) -> tuple[str, Any]:
                return self.name, self.item

        stack: list[StackItem] = [StackItem("Enter", self.root)]
        while len(stack) > 0:
            item = stack.pop()
            if item.name == "Enter":
                node = item.item
                tab = " " * depth
                result += f"{tab}{state[-1]}: {node}\n"
                for arc in node.outgoing_arcs:
                    stack.append(StackItem("Back", arc))
                    stack.append(StackItem("Go", arc))
            elif item.name == "Go":
                arc = item.item
                if arc is not None:
                    state.append(self.search_space.move(state[-1], arc))
                depth += 2
                stack.append(StackItem("Enter", arc.head))
            else:
                arc = item.item
                if arc is not None:
                    state.pop()
                depth -= 2
        return result + ")"
