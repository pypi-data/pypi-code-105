from py7zr.properties import *
from subprocess import run


def lzma_filter(**kwargs) -> dict:
    return kwargs


def new_multi_volume_fo(*args, **kwargs):
    import multivolumefile
    args = list(args)
    if not args[0].endswith(".7z"):
        args[0] += ".7z"
    return multivolumefile.MultiVolume(*args, **kwargs)


def change_sfx_icon(exe_fp: str, ico_fp: str, resouce_hacker_fp: str = r"C:\Program Files (x86)\Resource Hacker\ResourceHacker.exe"):
    run([
        resouce_hacker_fp,
        "-open", exe_fp,
        "-save", exe_fp,
        "-action", "addoverwrite",
        "-res", ico_fp,
        "-mask", "ICONGROUP,MAINICON,0"
    ])



