from .package_installation_magics import PackageInstallationMagics
from .adls_setup_magic import ADLSSetupMagics
from .hostfile_update_magic import HostfileUpdateMagic
from .parallel_shell_magic import ParallelShellMagics


def load_ipython_extension(ipython):
    """
    Register the magics with IPython
    """
    ipython.register_magics(PackageInstallationMagics)
    ipython.register_magics(ADLSSetupMagics)
    ipython.register_magics(HostfileUpdateMagic)
    ipython.register_magics(ParallelShellMagics)


from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
