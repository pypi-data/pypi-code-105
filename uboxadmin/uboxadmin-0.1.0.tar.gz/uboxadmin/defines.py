from enum import Enum as _Enum, IntEnum
from typing import Any, Callable

from typing_extensions import Protocol


class Override(Protocol):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        ...

    def override(self, constant):
        ...


def OverridedEnumMethod(default_method):
    # type: (Callable) -> Override
    cache = {}

    def _wrapped_func(inst, *args, **kwds):
        try:
            return cache[inst.value](inst, *args, **kwds)
        except KeyError:
            default_method(args, kwds)

    def _override(constant):
        def _method_wrapper(method):
            cache[constant] = method
            return method

        return _method_wrapper

    _wrapped_func.override = _override

    return _wrapped_func


class Enum(_Enum):
    @classmethod
    def as_choices(cls):
        return tuple((v.value, k) for k, v in cls.__members__.items())


class ParamType(Enum):
    STRING = 0
    ARRAY = 1
    MAPPING = 2


class UserStatus(Enum):
    DISABLED = 0
    ENABLED = 1


class ResponseCode(IntEnum):
    OK = 1000, "success"
    BAD_REQUEST = 2000, "bad request"
    ARGS_REQUIRED = 2001, "arguments required"
    BAD_RELATIONS = 2002, "bad relations"
    NOT_FOUND = 4000, "entity not found"
    AUTHENTICATION_FAILED = 4001, "authentication failed"

    description: str

    def __new__(cls, value, description):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.description = description
        return obj

    @classmethod
    def of(cls, code):
        for inst in cls.__members__.values():
            if inst._value_ == code:
                return inst
        return cls._missing_(code)


class ParseErrorCode(Enum):
    NULL = "null"
    UNIQUE = "unique"
    REQUIRED = "required"
    EMPTY = "empty"
    NOT_A_LIST = "not_a_list"
    INVALID = "invalid"

    @classmethod
    def of(cls, code):
        for inst in cls.__members__.values():
            if inst._value_ == code:
                return inst
        return cls._missing_(code)

    @OverridedEnumMethod
    def to_message(self, field_name: str) -> str:
        ...

    @to_message.override(NULL)
    def _(self, field_name: str):  # type: ignore
        return f"没有提供{field_name}"

    @to_message.override(UNIQUE)
    def _(self, field_name: str):  # type: ignore
        return f"{field_name}已存在"

    @to_message.override(EMPTY)
    def _(self, field_name: str):  # type: ignore
        return f"{field_name}为空"

    @to_message.override(NOT_A_LIST)
    def _(self, field_name: str):  # type: ignore
        return f"{field_name}不是一个数组"

    @to_message.override(INVALID)
    def _(self, field_name: str):  # type: ignore
        return f"{field_name}是非法数据"

    @to_message.override(REQUIRED)
    def _(self, field_name: str):  # type: ignore
        return f"{field_name}是必须的"
