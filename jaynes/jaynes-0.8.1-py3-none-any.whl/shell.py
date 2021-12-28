import subprocess


def popen(cmd, *args, verbose=False, **kwargs):
    if verbose:
        print(cmd, *args)
    return subprocess.Popen(cmd, *args, **kwargs)


def c(cmd, *args, verbose=False, **kwargs):
    if verbose:
        print(cmd, *args)
    return subprocess.call(cmd, *args, **kwargs)


def ck(cmd, *args, verbose=False, **kwargs) -> object:
    if verbose:
        print(cmd, *args)
    try:
        return subprocess.check_call(cmd, *args, **kwargs)
    except subprocess.CalledProcessError as e:
        print(e)


def run(cmd, *args, verbose=False, **kwargs) -> str:
    if verbose:
        print(cmd, *args)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    return process.communicate()
