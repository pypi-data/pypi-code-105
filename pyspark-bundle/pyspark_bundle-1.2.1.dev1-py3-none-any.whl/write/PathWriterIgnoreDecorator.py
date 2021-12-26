from logging import Logger
from pyspark.sql import DataFrame
from pysparkbundle.write.PathWriterDecorator import PathWriterDecorator
from pysparkbundle.filesystem.FilesystemInterface import FilesystemInterface
from injecta.container.ContainerInterface import ContainerInterface


class PathWriterIgnoreDecorator(PathWriterDecorator):  # noqa: N801
    def process_result(self, result: DataFrame, container: ContainerInterface):
        filesystem: FilesystemInterface = container.get("pysparkbundle.filesystem")
        logger: Logger = container.get("pysparkbundle.logger")

        if filesystem.exists(self._path):
            logger.info(f"Path {self._path} already exists, ignoring")
            return

        super().process_result(result, container)
