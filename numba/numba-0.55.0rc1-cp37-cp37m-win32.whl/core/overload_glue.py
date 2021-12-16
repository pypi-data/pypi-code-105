"""
Provides wrapper functions for "glueing" together Numba implementations that are
written in the "old" style of a separate typing and lowering implementation.
"""
import types as pytypes
import textwrap
from threading import RLock
from collections import defaultdict

from numba.core import errors


class _OverloadWrapper(object):
    """This class does all the work of assembling and registering wrapped split
    implementations.
    """

    def __init__(self, function, typing_key=None):
        assert function is not None
        self._function = function
        self._typing_key = typing_key
        self._BIND_TYPES = dict()
        self._selector = None
        self._TYPER = None
        # run to register overload, the intrinsic sorts out the binding to the
        # registered impls at the point the overload is evaluated, i.e. this
        # is all lazy.
        self._build()

    def _stub_generator(self, nargs, body_func, kwargs=None):
        """This generates a function that takes "nargs" count of arguments
        and the presented kwargs, the "body_func" is the function that'll
        type the overloaded function and then work out which lowering to
        return"""
        def stub(tyctx):
            # body is supplied when the function is magic'd into life via glbls
            return body(tyctx)  # noqa: F821
        if kwargs is None:
            kwargs = {}
        # create new code parts
        stub_code = stub.__code__
        co_args = [stub_code.co_argcount + nargs + len(kwargs)]

        new_varnames = [*stub_code.co_varnames]
        new_varnames.extend([f'tmp{x}' for x in range(nargs)])
        new_varnames.extend([x for x, _ in kwargs.items()])
        from numba.core import utils
        if utils.PYVERSION >= (3, 8):
            co_args.append(stub_code.co_posonlyargcount)
        co_args.append(stub_code.co_kwonlyargcount)
        co_args.extend([stub_code.co_nlocals + nargs + len(kwargs),
                        stub_code.co_stacksize,
                        stub_code.co_flags,
                        stub_code.co_code,
                        stub_code.co_consts,
                        stub_code.co_names,
                        tuple(new_varnames),
                        stub_code.co_filename,
                        stub_code.co_name,
                        stub_code.co_firstlineno,
                        stub_code.co_lnotab,
                        stub_code.co_freevars,
                        stub_code.co_cellvars
                        ])

        new_code = pytypes.CodeType(*co_args)

        # get function
        new_func = pytypes.FunctionType(new_code, {'body': body_func})
        return new_func

    def wrap_typing(self):
        """
        Use this to replace @infer_global, it records the decorated function
        as a typer for the argument `concrete_function`.
        """
        if self._typing_key is None:
            key = self._function
        else:
            key = self._typing_key

        def inner(typing_class):
            # Note that two templates could be used for the same function, to
            # avoid @infer_global etc the typing template is copied. This is to
            # ensure there's a 1:1 relationship between the typing templates and
            # their keys.
            clazz_dict = dict(typing_class.__dict__)
            clazz_dict['key'] = key
            cloned = type(f"cloned_template_for_{key}", typing_class.__bases__,
                          clazz_dict)
            self._TYPER = cloned
            _overload_glue.add_no_defer(key)
            self._build()
            return typing_class
        return inner

    def wrap_impl(self, *args):
        """
        Use this to replace @lower*, it records the decorated function as the
        lowering implementation
        """
        assert self._TYPER is not None

        def inner(lowerer):
            self._BIND_TYPES[args] = lowerer
            return lowerer
        return inner

    def _assemble(self):
        """Assembles the OverloadSelector definitions from the registered
        typing to lowering map.
        """
        from numba.core.base import OverloadSelector

        if self._typing_key is None:
            key = self._function
        else:
            key = self._typing_key

        _overload_glue.flush_deferred_lowering(key)

        self._selector = OverloadSelector()
        msg = f"No entries in the typing->lowering map for {self._function}"
        assert self._BIND_TYPES, msg
        for sig, impl in self._BIND_TYPES.items():
            self._selector.append(impl, sig)

    def _build(self):
        from numba.core.extending import overload, intrinsic

        @overload(self._function, strict=False,
                  jit_options={'forceinline': True})
        def ol_generated(*ol_args, **ol_kwargs):

            def body(tyctx):
                msg = f"No typer registered for {self._function}"
                if self._TYPER is None:
                    raise errors.InternalError(msg)
                typing = self._TYPER(tyctx)
                sig = typing.apply(ol_args, ol_kwargs)
                if sig is None:
                    # this follows convention of something not typeable
                    # returning None
                    return None
                if self._selector is None:
                    self._assemble()
                lowering = self._selector.find(sig.args)
                msg = (f"Could not find implementation to lower {sig} for ",
                       f"{self._function}")
                if lowering is None:
                    raise errors.InternalError(msg)
                return sig, lowering

            stub = self._stub_generator(len(ol_args), body, ol_kwargs)
            intrin = intrinsic(stub)

            # This is horrible, need to generate a jit wrapper function that
            # walks the ol_kwargs into the intrin with a signature that
            # matches the lowering sig. The actual kwarg var names matter,
            # they have to match exactly.
            arg_str = ','.join([f'tmp{x}' for x in range(len(ol_args))])
            kws_str = ','.join(ol_kwargs.keys())
            call_str = ','.join([x for x in (arg_str, kws_str) if x])
            # NOTE: The jit_wrapper functions cannot take `*args`
            # albeit this an obvious choice for accepting an unknown number
            # of arguments. If this is done, `*args` ends up as a cascade of
            # Tuple assembling in the IR which ends up with literal
            # information being lost. As a result the _exact_ argument list
            # is generated to match the number of arguments and kwargs.
            name = str(self._function)
            # This is to name the function with something vaguely identifiable
            name = ''.join([x if x not in {'>','<',' ','-','.'} else '_'
                            for x in name])
            gen = textwrap.dedent(("""
            def jit_wrapper_{}({}):
                return intrin({})
            """)).format(name, call_str, call_str)
            l = {}
            g = {'intrin': intrin}
            exec(gen, g, l)
            return l['jit_wrapper_{}'.format(name)]


class _Gluer:
    """This is a helper class to make sure that each concrete overload has only
    one wrapper as the code relies on the wrapper being a singleton."""
    def __init__(self):
        self._registered = dict()
        self._lock = RLock()
        # `_no_defer` stores keys that should not defer lowering because typing
        # is already provided.
        self._no_defer = set()
        # `_deferred` stores lowering that must be deferred because the typing
        # has not been provided.
        self._deferred = defaultdict(list)

    def __call__(self, func, typing_key=None):
        with self._lock:
            if typing_key is None:
                key = func
            else:
                key = typing_key
            if key in self._registered:
                return self._registered[key]
            else:
                wrapper = _OverloadWrapper(func, typing_key=typing_key)
                self._registered[key] = wrapper
                return wrapper

    def defer_lowering(self, key, lower_fn):
        """Defer lowering of the given key and lowering function.
        """
        with self._lock:
            if key in self._no_defer:
                # Key is marked as no defer, register lowering now
                lower_fn()
            else:
                # Defer
                self._deferred[key].append(lower_fn)

    def add_no_defer(self, key):
        """Stop lowering to be deferred for the given key.
        """
        with self._lock:
            self._no_defer.add(key)

    def flush_deferred_lowering(self, key):
        """Flush the deferred lowering for the given key.
        """
        with self._lock:
            deferred = self._deferred.pop(key, [])
            for cb in deferred:
                cb()


_overload_glue = _Gluer()
del _Gluer


def glue_typing(concrete_function, typing_key=None):
    """This is a decorator for wrapping the typing part for a concrete function
    'concrete_function', it's a text-only replacement for '@infer_global'"""
    return _overload_glue(concrete_function,
                          typing_key=typing_key).wrap_typing()


def glue_lowering(*args):
    """This is a decorator for wrapping the implementation (lowering) part for
    a concrete function. 'args[0]' is the concrete_function, 'args[1:]' are the
    types the lowering will accept. This acts as a text-only replacement for
    '@lower/@lower_builtin'"""

    def wrap(fn):
        key = args[0]

        def real_call():
            glue = _overload_glue(args[0], typing_key=key)
            return glue.wrap_impl(*args[1:])(fn)

        _overload_glue.defer_lowering(key, real_call)
        return fn
    return wrap
