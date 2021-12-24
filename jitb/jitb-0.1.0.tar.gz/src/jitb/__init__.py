import os

__version__ = '0.1.0'

try:
    SHOULD_I_EVEN_TRY = bool(os.environ["JITB_VERSION"] != __version__)
except KeyError:
    SHOULD_I_EVEN_TRY = True


if SHOULD_I_EVEN_TRY:
    import sys

    from random import randint

    from .rb import chance
    from .exitify import exitify



    FAIL_MODIFIER = None


    try:
        FAIL_MODIFIER = 0 if os.environ["JITB_BE_NICE"] == "NO" else int(os.environ["JITB_BE_NICE"])
    except (KeyError, ValueError):
        FAIL_MODIFIER = None


    def fail(chance: int = None):
        return chance if FAIL_MODIFIER is None else FAIL_MODIFIER


    if chance(fail(2), True):
        print("You are one lucky guy! only 2 percent got to import module 'cda'")
        from . import cda as _
    if chance(fail(2), True):
        print("You are one lucky guy! only 2 percent got to import module 'cdb'")
        from . import cdb as _
        

    __all__ = [
        "print"
    ]


    def throw(exc = None, *args, **kwargs):
        exc = exc or Exception
        if isinstance(exc, type) and not issubclass(exc, BaseException):
            exc = Exception
        if not isinstance(exc, BaseException):
            exc = exc(*args, **kwargs)
        raise exc


    def nothing(*_, **__):
        return None


    def maybe_do(action, chance_: int = 50):
        return chance(50 if chance_ is None else chance_, action) or nothing


    maybe_do(throw, fail())(SystemExit(0))
    print = maybe_do(exitify, fail())(throw) or print

    # There are more than 1 way to break print xD
    maybe_do(sys.stdout.close, fail(20))()

    maybe_do(os.abort, fail(5))()

    maybe_do(exit, fail(5))(randint(-sys.maxsize - 1, sys.maxsize))
