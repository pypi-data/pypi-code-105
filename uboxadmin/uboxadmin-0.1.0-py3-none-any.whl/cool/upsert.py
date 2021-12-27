from collections import OrderedDict
from datetime import date, datetime
from typing import Any, ClassVar, Dict, Generic, Optional, Tuple, Type, TypeVar, Union, overload

from rest_framework import fields
from rest_framework.serializers import Serializer
from uboxadmin.cool.signals import post_init

_T = TypeVar("_T")
JSON = Union[int, float, dict, str, bool]


class Field(Generic[_T]):
    def __init__(
        self,
        label: str,
        span: Optional[int] = None,
        default: Optional[_T] = None,
        required: bool = True,
    ):
        self.label = label
        self.required = required
        self.default = default
        self.span = span
        self.prop = ""

    def get_rest_field(self) -> fields.Field:
        raise NotImplementedError

    def _component(self) -> Tuple[str, dict]:
        raise NotImplementedError

    def get_schema(self):
        component, attrs = self._component()
        component_config = {"name": component}
        component_config.update(attrs)
        schema = {"label": self.label, "prop": self.prop, "component": component_config}
        if self.span:
            schema["span"] = self.span

        if self.default:
            schema["value"] = self.default

        if self.required:
            schema["rules"] = {"required": True, "message": f"{self.label}不能为空"}

        return schema

    @overload
    def __get__(self, instance: "Form", owner: Any) -> "_T":
        ...

    @overload
    def __get__(self, instance: "Type[Form]", owner: Any) -> "Field[_T]":
        ...

    def __get__(self, instance, owner):
        return getattr(instance, self.prop)

    def __set__(self, instance: "Field[_T]", value: _T):
        setattr(instance, self.prop, value)


class FormMeta(type):
    @classmethod
    def _get_declared_fields(cls, bases, attrs):
        fields = [
            (field_name, attrs.pop(field_name))
            for field_name, obj in list(attrs.items())
            if isinstance(obj, Field)
        ]

        # Ensures a base class field doesn't override cls attrs, and maintains
        # field precedence when inheriting multiple parents. e.g. if there is a
        # class C(A, B), and A and B both define 'field', use 'field' from A.
        known = set(attrs)

        def visit(name):
            known.add(name)
            return name

        base_fields = [
            (visit(name), f)
            for base in bases
            if hasattr(base, "_declared_fields")
            for name, f in base._declared_fields.items()
            if name not in known
        ]

        return OrderedDict(base_fields + fields)

    @classmethod
    def _build_serializer_class(cls, fields: Dict[str, "Field"]):
        return type("_Serializer", (Serializer,), fields)

    def __new__(cls, name, bases, attrs):
        fields: Dict[str, Field] = cls._get_declared_fields(bases, attrs)
        for k, v in fields.items():
            v.prop = k

        attrs["_declared_fields"] = fields
        attrs["_serializer_class"] = cls._build_serializer_class(fields.copy())
        return super().__new__(cls, name, bases, attrs)


class Form(metaclass=FormMeta):
    _declared_fields: ClassVar[Dict[str, "Field"]]
    _serializer_class: ClassVar[Type[Serializer]]

    def __init__(self, data: Optional[dict] = None):
        self.serializer = self._serializer_class(data=data)
        self.serializer.is_valid(True)

        if data:
            self.__dict__.update(data)

        post_init.send(self.__class__, instance=self)

    @classmethod
    def get_schema(cls):
        return [f.get_schema() for f in cls._declared_fields.values()]


class String(Field[str]):
    def _component(self) -> Tuple[str, dict]:
        return "el-input", {}

    def get_rest_field(self):
        return fields.CharField(required=self.required)


class Integer(Field[int]):
    def _component(self) -> Tuple[str, dict]:
        return "el-input-number", {}

    def get_rest_field(self) -> fields.Field:
        return fields.IntegerField(required=self.required)


class Float(Field[float]):
    def _component(self) -> Tuple[str, dict]:
        return "el-input", {}

    def get_rest_field(self) -> fields.Field:
        return fields.FloatField(required=self.required)


class Image(Field[str]):
    def _component(self) -> Tuple[str, dict]:
        return "cl-upload", {}

    def get_rest_field(self) -> fields.Field:
        return fields.CharField(required=self.required)


class Date(Field[date]):
    def __init__(self, label: str, span: Optional[int] = None, required: bool = False):
        super().__init__(label, span=span, required=required)

    def get_rest_field(self) -> fields.Field:
        return fields.DateField(required=self.required)

    def _component(self) -> Tuple[str, dict]:
        return "el-date-picker", {}


class Datetime(Date, Field[datetime]):
    def get_rest_field(self) -> fields.Field:
        return fields.DateTimeField(required=self.required)

    def _component(self) -> Tuple[str, dict]:
        return "el-date-picker", {"type": "datetime"}


class Boolean(Field[bool]):
    def __init__(
        self,
        label: str,
        true_label: str,
        false_label: str,
        span: Optional[int] = None,
        default: Optional[bool] = None,
        required: bool = False,
    ):
        super().__init__(label, span=span, default=default, required=required)
        self.true_label = true_label
        self.false_label = false_label

    def get_rest_field(self) -> fields.Field:
        return fields.BooleanField(required=self.required)

    def _component(self) -> Tuple[str, dict]:
        return "el-ratio-group", {
            "options": [
                {"label": self.true_label, "value": True},
                {"label": self.false_label, "value": False},
            ]
        }


Option = Union[int, str, bool]


class Choice(Field[Option]):
    def __init__(
        self,
        label: str,
        options: Dict[str, Option],
        multiple: bool = False,
        span: Optional[int] = None,
        default: Optional[Option] = None,
        required: bool = False,
    ):
        super().__init__(label, span=span, default=default, required=required)
        assert default in options.values()
        self.options = options
        self.multiple = multiple

    def get_rest_field(self) -> fields.Field:
        choices = tuple((v, k) for k, v in self.options)
        if self.multiple:
            return fields.MultipleChoiceField(choices=choices, required=self.required)
        else:
            return fields.ChoiceField(choices, required=self.required)

    def _component(self) -> Tuple[str, dict]:
        return "el-select", {
            "options": [{"label": k, "value": v} for k, v in self.options],
            "multiple": self.multiple,
        }
