from py7zr.properties import *
from subprocess import run


def lzma_filter(**kwargs) -> dict:
    return kwargs


def new_multi_volume_fo(name, **kwargs):
    import multivolumefile
    if not name.endswith(".7z"):
        name += ".7z"
    return multivolumefile.MultiVolume(name, "wb", **kwargs)


def change_sfx_icon(exe_fp: str, ico_fp: str, resource_hacker_fp: str = r"C:\Program Files (x86)\Resource Hacker\ResourceHacker.exe"):
    run([
        resource_hacker_fp,
        "-open", exe_fp,
        "-save", exe_fp,
        "-action", "addoverwrite",
        "-res", ico_fp,
        "-mask", "ICONGROUP,MAINICON,0"
    ])



