from typing import Optional, get_type_hints, List, Callable, Union

import pointy.core as _core
from pointy.marker import Marker

Marker = Marker

ProvideDecorator = Union[
    Callable[[], Optional[_core.TClass]],
    Callable[[Optional[_core.TClass]], Optional[_core.TClass]]
]


def provide(
        the_type: _core.TClass,
        factory: Optional[_core.TFactory] = None,
        singleton: Optional[bool] = False
) -> ProvideDecorator:
    def decorator(the_providing_type: Optional[_core.TClass] = None) -> Optional[_core.TClass]:
        final_factory = factory or the_providing_type or the_type

        if singleton:
            final_factory = _core.SingletonFactory(final_factory).get

        _core.registry[the_type] = final_factory

        return the_providing_type

    return decorator


def inject(target: _core.TClass) -> _core.TClass:
    og_new = getattr(target, "__new__")
    fields: List[_core.Field[Marker]] = list(
        filter(
            lambda f: f.is_marker,
            map(
                lambda t: _core.Field(target, *t),
                get_type_hints(target).items()
            )
        )
    )

    def injecting_new(cls, *args, **kwargs):
        instance = og_new(cls, *args, **kwargs)

        for field in fields:
            factory = _core.registry.get(field.type, None)
            if not callable(factory):
                raise RuntimeError(f"Invalid factory: {factory} ({target})")

            marker = field.value
            if not isinstance(marker, Marker):
                raise RuntimeError(f"Not a marker: {marker} ({target})")

            setattr(instance, field.name, factory(*marker.args, **marker.kwargs))

        return instance

    setattr(target, "__new__", injecting_new)

    return target


def construct(the_type: _core.TClass, *args, **kwargs) -> _core.T:
    return _core.registry[the_type](*args, **kwargs)
