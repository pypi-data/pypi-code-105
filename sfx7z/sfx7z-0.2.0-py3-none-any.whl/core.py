from omnitools import p
import multivolumefile
import py7zr
import os


SFX_TYPE_CLASSIC_GUI = 0x00
SFX_TYPE_CLASSIC_CONSOLE = 0x01
SFX_TYPE_INSTALLER_GUI = 0x02
SFX_TYPE_INSTALLER_GUI_LEGACY = 0x03


# https://olegscherbakov.github.io/7zSFX/
# noinspection PyPep8Naming
def Installer_Config(
        *,
        Title: str = "This SFX is built with sfx7z by foxe6",
        BeginPrompt: str = "Click 'yes' to continue.",
        Progress: str = "yes",
        RunProgram: str = None,
        Directory: str = "",
        ExecuteFile: str = None,
        ExecuteParameters: str = None,
        **kwargs
):
    if RunProgram is None and ExecuteFile is None:
        raise ValueError("missing RunProgram or ExecuteFile")
    START = b";!@Install@!UTF-8!"
    END = b";!@InstallEnd@!"
    config = []
    config.append(START)
    if kwargs:
        p("following config may not be supported: {}".format(", ".join(k for k, _ in kwargs.items())), error=True)
    kwargs.update({
        "Title": Title,
        "BeginPrompt": BeginPrompt,
        "Progress": Progress,
        "RunProgram": RunProgram,
        "Directory": Directory,
        "ExecuteFile": ExecuteFile,
        "ExecuteParameters": ExecuteParameters,
    })
    for k, v in kwargs.items():
        if v is not None:
            config.append("{}=\"{}\"".format(k, v.replace("\"", "\\\"")).encode())
    config.append(END)
    return b"\n".join(config)


class Builder(py7zr.SevenZipFile):
    def __init__(
            self,
            file,
            mode: str = "w",
            *,
            sfx_type: int = SFX_TYPE_CLASSIC_GUI,
            sfx_installer_config: bytes = b"",
            sfx_bundle: bool = False,
            **kwargs
    ):
        if sfx_bundle:
            if isinstance(file, multivolumefile.MultiVolume):
                raise TypeError("sfx_bundle does not support type '{}'".format(type(file).__name__))
            if hasattr(file, "write"):
                pass
            elif isinstance(file, str):
                if file.endswith(".7z"):
                    file = file[:-2]+"exe"
                elif not file.endswith(".exe"):
                    file += ".exe"
                file = open(file, "wb")
            else:
                raise TypeError("type '{}' not supported".format(type(file).__name__))
            if not isinstance(file, multivolumefile.MultiVolume):
                write_o = file.write
                def write(*args, **kwargs):
                    if file.tell() == 0:
                        self.write_sfx(sfx_type, sfx_installer_config, write_o)
                    return write_o(*args, **kwargs)
                file.write = write
        else:
            if sfx_type in [SFX_TYPE_INSTALLER_GUI, SFX_TYPE_INSTALLER_GUI_LEGACY]:
                raise TypeError("sfx_type '{}' requires sfx_bundle".format(sfx_type))
            if hasattr(file, "name"):
                fo = open(os.path.splitext(file.name)[0]+".exe", "wb")
            elif isinstance(file, str):
                fo = open(os.path.splitext(file)[0]+".exe", "wb")
            else:
                raise TypeError("type '{}' not supported".format(type(file).__name__))
            self.write_sfx(sfx_type, sfx_installer_config, fo.write)
            fo.close()
        super().__init__(file, "w", **kwargs)

    def write_sfx(self, sfx_type, sfx_installer_config, write):
        cwd = os.path.dirname(os.path.abspath(__file__))
        if sfx_type == SFX_TYPE_CLASSIC_GUI:
            fn = "7z.sfx"
            sfx_installer_config = b""
        elif sfx_type == SFX_TYPE_CLASSIC_CONSOLE:
            fn = "7zCon.sfx"
            sfx_installer_config = b""
        elif sfx_type == SFX_TYPE_INSTALLER_GUI:
            fn = "7zSD.sfx"
        elif sfx_type == SFX_TYPE_INSTALLER_GUI_LEGACY:
            fn = "7zS.sfx"
        else:
            raise ValueError("unknown sfx_type '{}'".format(sfx_type))
        sfx_fp = os.path.join(cwd, "pkg_data", fn)
        sfx_fo = open(sfx_fp, "rb")
        while True:
            buf = sfx_fo.read(8192)
            if not buf:
                break
            write(buf)
        write(sfx_installer_config)
        sfx_fo.close()


