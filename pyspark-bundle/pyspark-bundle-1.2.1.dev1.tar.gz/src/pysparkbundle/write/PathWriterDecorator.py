from typing import Union
from pysparkbundle.write.PathWriter import PathWriter
from daipecore.decorator.OutputDecorator import OutputDecorator
from injecta.container.ContainerInterface import ContainerInterface
from pyspark.sql import DataFrame


class PathWriterDecorator(OutputDecorator):  # noqa: N801

    _mode: str
    _writer_service: str

    def __init__(self, path: str, partition_by: Union[str, list] = None, options: dict = None):
        self._path = path

        if partition_by is None:
            self._partition_by = []
        elif isinstance(partition_by, str):
            self._partition_by = [partition_by]
        elif isinstance(partition_by, list):
            self._partition_by = partition_by
        else:
            raise Exception(f"Unexpected partition_by type: {type(partition_by)}")

        self._options = options

    def process_result(self, result: DataFrame, container: ContainerInterface):
        path_writer: PathWriter = container.get(self._writer_service)
        path_writer.write(result, self._path, self._mode, self._partition_by, self._options)
