__version__ = "0.1.0"

from functools import update_wrapper


def register(base):
    def wrapped(cls):
        from .generic import ModelViewSet

        assert issubclass(cls, ModelViewSet)
        assert base

        from .views.django_apps import router

        cls.register_to_router(router, base)

        return cls

    return wrapped


def register_func(action, base):
    assert action.lower() in ["get", "post"]

    def wrapped(func):
        from .views.django_apps import router

        if action.lower() == "get":
            handler = router.get(base)(func)
        else:
            handler = router.post(base)(func)

        update_wrapper(handler, func)
        return handler

    return wrapped
