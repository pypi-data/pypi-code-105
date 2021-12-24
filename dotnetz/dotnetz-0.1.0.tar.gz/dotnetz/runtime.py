from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, TypeVar, Generic, Callable, List, Optional
from functools import wraps
try:
  from typing import ParamSpec
except ImportError:
  from typing_extensions import ParamSpec
