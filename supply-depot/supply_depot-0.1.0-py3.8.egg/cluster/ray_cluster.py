from typing import Any, Callable, Dict, List, Union

import ray
from ray.util import ActorPool

from supply_depot.cluster import Cluster, Execution


class RayCluster(Cluster):
    def __init__(self):
        ray.init()

    def shutdown(self) -> None:
        ray.shutdown()

    def execute(
        self,
        execution: Union[List[Execution], Execution],
        execution_args: Union[List[Dict[str, Any]], Dict[str, Any]],
    ) -> Union[List[Any], Any]:
        if isinstance(execution, list):
            pool = ActorPool(execution)
            return list(pool.map(lambda a, i: a.execute.remote(**i), execution_args))
        return ray.get(execution.execute.remote(**execution_args))

    def create_execution(self, execution_class: Callable, *args, **kwargs) -> Execution:
        return ray.remote(execution_class).remote(*args, **kwargs)
