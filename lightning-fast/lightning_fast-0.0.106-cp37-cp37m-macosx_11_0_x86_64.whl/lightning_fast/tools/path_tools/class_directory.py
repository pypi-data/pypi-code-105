import pathlib
import re
import sys
from typing import Type


class ClassDirectory:
    """
    处理class本身文件路径的辅助类
    """

    def __init__(self, class_type: Type):
        self.class_type = class_type

    def get_class_path(self) -> pathlib.Path:
        """
        获取某个class所在文件的绝对路径
        """
        class_file_path = sys.modules[self.class_type.__module__].__file__
        class_file_path = pathlib.Path(class_file_path).absolute()
        return class_file_path

    def get_class_root_directory(
        self, source_dir: pathlib.Path, target_dir: pathlib.Path, create: bool = True
    ) -> pathlib.Path:
        """
        从一个python class相对于source_dir的路径中获得相对于另一个target_dir的路径
        比如当前脚本相对于项目为/project_dir/package_dir/a.py, 数据文件目录为/data
        我们想要拿到/data/package_dir/a/这个目录。
        :param source_dir: 源目录
        :param target_dir: 新源目录
        :param create: 是否创建新目录
        :return:
        """
        class_file_path = self.get_class_path()
        relative_source_dir = class_file_path.relative_to(source_dir)
        relative_target_dir = target_dir / relative_source_dir
        relative_target_dir = pathlib.Path(
            re.sub(r"\.[^.\\/]*?$", "", str(relative_target_dir))
        )
        if create:
            relative_target_dir.mkdir(parents=True, exist_ok=True)
        return relative_target_dir
