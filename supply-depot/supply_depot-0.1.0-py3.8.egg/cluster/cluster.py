from __future__ import annotations

import abc
from typing import Any, Callable, Dict, List, Union


class Cluster:
    def shutdown(self):
        pass

    def execute(
        self,
        execution: Union[List[Execution], Execution],
        execution_args: Union[List[Dict[str, Any]], Dict[str, Any]],
    ) -> Union[List[Any], Any]:
        return execution(**execution_args)

    def create_execution(self, execution_class: Callable, *args, **kwargs) -> Execution:
        return execution_class(*args, **kwargs)


class Execution(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
            Main execution function
        """

    def __call__(self, *args, **kwargs) -> Any:
        return self.execute(*args, **kwargs)
