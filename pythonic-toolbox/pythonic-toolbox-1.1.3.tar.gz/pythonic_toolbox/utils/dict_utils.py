from typing import Any, Callable, Optional


def dict_until(obj, keys: list, terminate: Optional[Callable[[Any], bool]] = None, default=None):
    class Empty:
        pass

    UNSIGNED = Empty()

    if terminate is None:
        terminate = lambda v: v is not UNSIGNED

    from pythonic_toolbox.utils.list_utils import until

    # default is for value
    val = default
    key = until(keys, lambda k: terminate(obj.get(k, UNSIGNED)), default=UNSIGNED)
    if key is not UNSIGNED:
        val = obj[key]
    return val
