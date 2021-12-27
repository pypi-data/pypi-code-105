import os
from typing import Type, TypeVar

from domdf_python_tools.paths import PathPlus, WindowsPathPlus, PosixPathPlus

_PPP = TypeVar("_PPP", bound="PathPlusPlus")

class PathPlusPlus(PathPlus):
	def __new__(cls: Type[_PPP], *args, **kwargs) -> _PPP:
		if cls is PathPlusPlus:
			cls = WindowsPathPlusPlus if os.name == "nt" else PosixPathPlusPlus
		return super().__new__(*args, **kwargs)

	def is_newer_than(self, other: PathPlus):
		return self.stat().st_mtime > other.stat().st_mtime


class WindowsPathPlusPlus(PathPlusPlus, WindowsPathPlus):
	...


class PosixPathPlusPlus(PathPlusPlus, PosixPathPlus):
	...
