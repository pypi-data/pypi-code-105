####################################################################################################
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
####################################################################################################

import logging
from enum import Enum, auto, unique
from functools import wraps, singledispatch
from typing import *
import os
import shutil

from . import _lang_python, lang
from .Targets import Target
from .Parameter import *
from .Constants import inf


@singledispatch
def _convert_arg(arg: _lang_python._lang._Valor):
    if arg.layout == _lang_python._MemoryLayout():
        return _lang_python._lang.Scalar(arg)
    else:
        return _lang_python._lang.Array(arg)

@_convert_arg.register(lang.Array)
def _(arg: lang.Array):
    return arg._get_native_array()


@singledispatch
def _resolve_array_shape(source, arr: lang.Array):
    if arr.shape[-1] == inf:
        # TODO: support shape inference for lang.Function, Callable if needed
        raise NotImplementedError(f"Array shape cannot be resolved for {type(source)}")
    return

@_resolve_array_shape.register(lang.Nest)
def _(source, arr: lang.Array):
    from .lang.IntrospectionUtilities import get_array_access_indices

    if arr.shape[-1] == inf:
        # introspect array access index to determine dimensions of the array
        logic_fns = source.get_logic()
        # TODO: support multiple logic fns if needed
        assert len(logic_fns) == 1, "Only one logic function is supported"
        access_indices = get_array_access_indices(arr, logic_fns[0])
        assert len(access_indices) == len(arr.shape), "Access indices and shape must have the same dimensions"
        idx = source.get_indices().index(access_indices[-1])

        # initialize the array with the new shape
        inferred_shape = tuple(arr.shape[:-1] + [source.get_shape()[idx]])
        arr._init_delayed(inferred_shape)

@_resolve_array_shape.register(lang.Schedule)
def _(source, arr: lang.Array):
    _resolve_array_shape(source._nest, arr)

@_resolve_array_shape.register(lang.ActionPlan)
def _(source, arr: lang.Array):
    _resolve_array_shape(source._sched._nest, arr)


def _emit_module(module_to_emit, target, mode, output_dir, name):
    from . import accc
    from .hat import HATFile

    assert target._device_name, "Target is unknown"
    working_dir = os.path.join(output_dir, "_tmp")

    proj = accc.AcceraProject(output_dir=working_dir, library_name=name)
    proj.module_file_sets = [
        accc.ModuleFileSet(name=name, common_module_dir=working_dir)
    ]
    module_to_emit.Save(proj.module_file_sets[0].generated_mlir_filepath)

    proj.generate_and_emit(build_config=mode.value, system_target=target._device_name)

    # Create initial HAT files containing shape and type metadata that the C++ layer has access to
    header_path = os.path.join(output_dir, name + ".hat")
    module_to_emit.WriteHeader(header_path)

    # Complete the HAT file with information we have stored at this layer
    hat_file = HATFile.Deserialize(header_path)
    hat_file.dependencies.link_target = os.path.basename(
        proj.module_file_sets[0].object_filepath
    )
    hat_file.Serialize(header_path)

    # copy HAT package files into output directory
    shutil.copy(proj.module_file_sets[0].object_filepath, output_dir)


class SetActiveModule:
    def __init__(self, module):
        self.module = module

    def __enter__(self):
        _lang_python._ClearActiveModule()
        _lang_python._SetActiveModule(self.module)

    def __exit__(self, exc_type, exc_val, exc_tb):
        _lang_python._ClearActiveModule()
        _lang_python._SetActiveModule(Package._default_module)


class Package:
    "A package of functions that can be built and linked with client code."

    class Format(Enum):
        HAT = auto()  #: HAT package (github.com/microsoft/hat)
        MLIR = auto()  #: Include the intermediate IR along with the HAT package

    class Mode(Enum):
        RELEASE = "Release"  #: Release (maximally optimized)
        DEBUG = "Debug"  #: Debug mode (automatically tests logical equivalence)"

    @unique
    class Platform(Enum):
        # TODO: should we reconcile with HATOperatingSystem?
        HOST = "host"
        WINDOWS = "windows"
        LINUX = "linux"
        MACOS = "mac"
        ANDROID = "android"
        IOS = "ios"
        RASPBIAN = "raspbian"

    # class attribute to track the default module
    _default_module = None

    def __init__(self):
        self._fns: Dict[str, Any] = {}
        self._description = {}

    def _create_gpu_utility_module(
        self, compiler_options, target, mode, output_dir, name="AcceraGPUUtilities"
    ):
        gpu_utility_module = _lang_python._Module(name=name, options=compiler_options)

        with SetActiveModule(gpu_utility_module):
            gpu_init_fn = _lang_python._DeclareFunction("AcceraGPUInitialize")
            gpu_deinit_fn = _lang_python._DeclareFunction("AcceraGPUDeInitialize")

            gpu_init_fn.public(True).decorated(False).headerDecl(True).rawPointerAPI(
                True
            ).addTag("rc_gpu_init")
            gpu_deinit_fn.public(True).decorated(False).headerDecl(True).rawPointerAPI(
                True
            ).addTag("rc_gpu_deinit")

            # No common initialization / de-initialization at this layer, however lowering passes may add steps
            def empty_func(args):
                pass

            gpu_init_fn.define(empty_func)
            gpu_deinit_fn.define(empty_func)

        _emit_module(gpu_utility_module, target, mode, output_dir, name)

    def add_function(
        self,
        source: Union["accera.Nest", "accera.Schedule", "accera.ActionPlan", "accera.Function", Callable],
        args: List["accera.Array"] = None,
        base_name: str = "",
        parameters: dict = {},
        function_opts: dict = {},
        auxiliary: dict = {},
    ) -> "accera.Function":
        """Adds a function to the package.

        Args:
            source: The source which defines the function's implementation.
            args: The order of external-scope arrays to use in the function signature.
            base_name: A base name for the function. The full name for the function will be the
                base name followed by an automatically-generated unique identifier.
            parameters: A value for each parameter if the function's implementation is parameterized.
            function_opts: A dictionary of advanced options to set on the function, e.g. {"no_inline" : True}
            auxiliary: A dictionary of auxiliary metadata to include in the HAT package.
        """

        from secrets import token_hex

        for delayed_param, value in parameters.items():
            delayed_param.set_value(value)

        def validate_target(target: Target):
            # can't use set because targets are mutable (therefore unhashable)
            for f in self._fns.values():
                if not target.is_compatible_with(f.target):
                    raise NotImplementedError(
                        "Function target being added is currently incompatible with existing functions in package"
                    )

        # Function names must begin with an _ or alphabetical character
        name = token_hex(4)
        name = (f"{base_name}_{name}" if base_name else f"_{name}")

        # Resolve any undefined argument shapes based on the source usage pattern
        for arr in args:
            _resolve_array_shape(source, arr)

        if isinstance(source, lang.Nest) or isinstance(source, lang.Schedule):
            # assumption: convenience functions are for host targets only
            source = source.create_action_plan(Target.HOST)
            # fall-through

        if isinstance(source, lang.ActionPlan):
            source = source._create_function(
                args, public=True, no_inline=function_opts.get("no_inline", False)
            )
            # fall-through

        if isinstance(source, lang.Function):
            source: lang.Function

            # due to the fall-through, we only need to validate here
            validate_target(source.target)
            logging.debug("Adding wrapped function")

            native_array_args = [arg._get_native_array() for arg in args]

            assert source.public
            source.name = name
            source.base_name = base_name
            source.auxiliary = auxiliary
            source.param_overrides = parameters
            source.args = tuple(native_array_args)
            source.requested_args = args
            self._fns[source.name] = source
            return source  # for composability

        elif isinstance(source, Callable):

            # due to the fall-through, we only need to validate here
            validate_target(Target.HOST)

            @wraps(source)
            def wrapper_fn(args):
                source(*map(_convert_arg, args))

            logging.debug(f"[API] Added {name}")

            wrapped_func = lang.Function(
                name=name,
                base_name=base_name,
                public=True,
                decorated=function_opts.get("decorated", False),
                no_inline=function_opts.get("no_inline", False),
                args=tuple(map(_convert_arg, args)),
                requested_args=args,
                definition=wrapper_fn,
                auxiliary=auxiliary,
                target=Target.HOST,
            )

            self._fns[name] = wrapped_func
            return wrapped_func  # for composability

        else:
            raise ValueError("Invalid type for source")

    def add_functions(
        self,
        source: Union["accera.Nest", "accera.Schedule", "accera.ActionPlan"],
        args: List["accera.Array"] = None,
        base_name: str = "",
        parameters: List[dict] = None,
        ) -> List["accera.Function"]:
            """Generates functions from a parameter grid and adds them to a package.

            Args:
                source: The source which defines the function's implementation.
                args: The order of external-scope arrays to use in the function signature.
                base_name: A base name for the function. The full name for the function will be the
                    base name followed by an automatically-generated unique identifier.
                parameters: A list of parameters, each element has a value for each parameter if the function's implementation is parameterized.
            """
            return [self.add_function(source=source, args=args, base_name=base_name, parameters=p) for p in parameters]

    def _add_functions_to_module(self, module):
        with SetActiveModule(module):
            for name, wrapped_func in self._fns.items():
                print(f"Building function {name}")
                try:
                    wrapped_func._emit()
                except:
                    print(f"Compiler error when trying to build function {name}")
                    raise

    def _add_debug_utilities(self, tolerance):
        from .Debug import get_args_to_debug, add_debugging_functions

        # add_check_all_close will modify the self._fns dictionary (because
        # it is adding debug functions), to avoid this, we first gather information
        # about the functions to add
        fns_to_add = {name : (wrapped_func, get_args_to_debug(wrapped_func)) \
            for name, wrapped_func in self._fns.items()}

        # only add if there are actually arguments to debug
        return add_debugging_functions(self,
            {name : fn_and_args for name, fn_and_args in fns_to_add.items() if fn_and_args[1]},
            atol=tolerance)

    def _generate_target_options(self, platform: Platform, mode: Mode = Mode.RELEASE):
        from .build_config import BuildConfig

        if len(self._fns) == 0:
            raise RuntimeError("No functions have been added")

        # target consistency is enforced during add_function()
        target = list(self._fns.values())[0].target
        host_target_device = _lang_python._GetTargetDeviceFromName("host")

        if platform in [
            Package.Platform.HOST,
            Package.Platform.LINUX,
            Package.Platform.MACOS,
            Package.Platform.WINDOWS,
        ]:
            target_device = _lang_python._GetTargetDeviceFromName(platform.value)
        else:
            target_device = _lang_python.TargetDevice()

        # Architecture
        if target.architecture == Target.Architecture.HOST:
            target_device.architecture = host_target_device.architecture
            target_device.cpu = host_target_device.cpu
            target_device.features = host_target_device.features

        elif target.architecture == Target.Architecture.ARM:
            # All known targets that are ARM are supported completely
            target_device = _lang_python._GetTargetDeviceFromName(target._device_name)
            target_device.architecture = "arm"

        elif target.architecture == Target.Architecture.X86_64:
            target_device.architecture = "x86_64"

            if "AVX2" in target.extensions or "AVX" in target.extensions:
                target_device.device_name = "avx512"
                target_device.cpu = "skylake-avx512"
                # TODO: make this functionality less hidden
                avx512_feat_str = ",".join(
                    [f"+{feature.lower()}" for feature in target.extensions]
                )

                target_device.features = avx512_feat_str

        elif target.architecture == Target.Architecture.X86:
            target_device.architecture = "x86"

        _lang_python._CompleteTargetDevice(target_device)

        compiler_options = _lang_python.CompilerOptions()
        compiler_options.target_device = target_device
        compiler_options.debug = mode == Package.Mode.DEBUG

        BuildConfig.obj_extension = ".obj" if target_device.is_windows() else ".o"

        return target, target_device, compiler_options

    def build(
        self,
        name: str,
        format: Format = Format.HAT,
        mode: Mode = Mode.RELEASE,
        platform: Platform = Platform.HOST,
        tolerance: float = 1e-5,
        output_dir: str = None,
    ):
        """Builds a HAT package.

        Args:
            name: The package name.
            format: The format of the package.
            mode: The package mode, such as whether it is optimized or used for debugging.
            platform: The platform where the package will run.
            tolerance: The tolerance for correctness checking when `mode = Package.Mode.DEBUG`.
            output_dir: The path to an output directory. Defaults to the current directory if unspecified.
        """

        from . import accc
        from .hat import HATFile
        from .hat import OperatingSystem as HATOperatingSystem

        target, target_device, compiler_options = self._generate_target_options(platform, mode)

        output_dir = output_dir or os.getcwd()
        working_dir = os.path.join(output_dir, "_tmp")
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(working_dir, exist_ok=True)

        # Debug mode: add utility functions for checking results
        debug_utilities = self._add_debug_utilities(tolerance) \
            if mode == Package.Mode.DEBUG else {}

        # Create the package module
        package_module = _lang_python._Module(name=name, options=compiler_options)
        self._add_functions_to_module(package_module)

        # Debug mode: emit the debug function that uses the utility functions
        for fn_name, utilities in debug_utilities.items():
            package_module.EmitDebugFunction(fn_name, utilities)

        # Emit the supporting modules
        self._create_gpu_utility_module(compiler_options, target, mode, output_dir)
        Package._emit_default_module(
            compiler_options, target, mode, output_dir, f"{name}_Globals"
        )

        # Emit the package module
        proj = accc.AcceraProject(output_dir=working_dir, library_name=name)
        proj.module_file_sets = [
            accc.ModuleFileSet(name=name, common_module_dir=working_dir)
        ]
        package_module.Save(proj.module_file_sets[0].generated_mlir_filepath)

        # Enable dumping of IR passes based on build format
        dump_ir = format == Package.Format.MLIR
        proj.generate_and_emit(
            build_config=mode.value,
            system_target=target._device_name,
            dump_all_passes=dump_ir,
            dump_intrapass_ir=dump_ir,
        )

        # Create initial HAT files containing shape and type metadata that the C++ layer has access to
        header_path = os.path.join(output_dir, name + ".hat")
        package_module.WriteHeader(header_path)

        # Complete the HAT file with information we have stored at this layer
        hat_file = HATFile.Deserialize(header_path)
        hat_file.dependencies.link_target = os.path.basename(
            proj.module_file_sets[0].object_filepath
        )
        for fn_name in self._fns:
            if self._fns[fn_name].public:
                hat_func = hat_file.function_map.get(fn_name)
                if hat_func is None:
                    raise ValueError(
                        f"Couldn't find header-declared function {fn_name} in emitted HAT file"
                    )
                hat_func.auxiliary = self._fns[fn_name].auxiliary
        if target_device.is_windows():
            hat_os = HATOperatingSystem.Windows
        elif target_device.is_macOS():
            hat_os = HATOperatingSystem.MacOS
        elif target_device.is_linux():
            hat_os = HATOperatingSystem.Linux
        hat_file.target.required.os = hat_os
        hat_file.target.required.cpu.architecture = target_device.architecture

        # Not all of these features are necessarily used in this module, however we don't currently have a way
        # of determining which are and are not used so to be safe we require all of them
        hat_file.target.required.cpu.extensions = target_device.features.split(",")

        hat_file.description.author = self._description.get("author", "")
        hat_file.description.version = self._description.get("version", "")
        hat_file.description.license_url = self._description.get("license", "")
        if "auxiliary" in self._description:
            hat_file.description.auxiliary = self._description["auxiliary"]

        hat_file.Serialize(header_path)

        # copy HAT package files into output directory
        shutil.copy(proj.module_file_sets[0].object_filepath, output_dir)

        return proj.module_file_sets

    def add_description(
        self,
        author: str = None,
        license: str = None,
        other: dict = {},
        version: str = None,
    ):
        """Adds descriptive metadata to the HAT package.

        Args:
            author: Name of the individual or group that authored the package.
            license: The internet URL of the license used to release the package.
            other: User-specific descriptive metadata.
                If the key already exists, the value will be overwritten
                To remove a key, set its value to None
            version: The package version.
        """
        if other:
            if "auxiliary" not in self._description:
                self._description["auxiliary"] = other
            else:
                self._description["auxiliary"].update(other)

            # remove any keys marked None
            keys_to_remove = [
                k for k, v in self._description["auxiliary"].items() if v is None
            ]
            for k in keys_to_remove:
                del self._description["auxiliary"][k]

        if version is not None:
            self._description["version"] = version
        if author is not None:
            self._description["author"] = author
        if license is not None:
            self._description["license"] = license

    @classmethod
    def _init_default_module(cls):
        # Creates a default module that is initialized once per import
        # This module will hold global data (such as constant Arrays), and will be
        # included in every built package
        cls._default_module = _lang_python._Module(name="PackageGlobals")
        _lang_python._SetActiveModule(cls._default_module)

    @classmethod
    def _emit_default_module(cls, compiler_options, target, mode, output_dir, name):
        # Specializes and then emits the default module
        cls._default_module.SetDataLayout(compiler_options)
        _emit_module(cls._default_module, target, mode, output_dir, name)
