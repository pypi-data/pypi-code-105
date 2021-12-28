__version__ = "0.0.4"
__host__ = "http://172.32.4.219/puppy_test"

# __host__="http://r4735hqh7.hn-bkt.clouddn.com"
import os
import warnings
from urllib import request


def to_int(version):
    a = version.replace(".", "")
    return int(a)


def get_server_version() -> str:
    """从服务器取到最新的版本"""
    global __host__
    try:
        puppy_version_url = __host__ + "/version.txt"
        request.urlretrieve(puppy_version_url, "puppy_version.txt")
        with open("puppy_version.txt") as file:
            for line in file.readlines():
                version = line.strip()
        os.remove("puppy_version.txt")
        return version
    except:
        return None


def get_version() -> str:
    """获取当前框架版本"""
    global __version__
    return __version__


def upgrade_puppy_test():
    global __host__
    version = get_server_version()
    if version is None:
        return
    puppy_test_url = __host__ + "/puppy_test-{}.tar.gz".format(version)
    request.urlretrieve(puppy_test_url, "puppy_test.tar.gz")
    os.system("pip install puppy_test.tar.gz")
    os.remove("puppy_test.tar.gz")


def check_version(version):
    if to_int(version) > to_int(get_version()):
        warnings.warn("puppy_test框架版本落后于脚本版本，请升级puppy_test版本！", UserWarning)
    if to_int(version) < to_int(get_version()):
        warnings.warn('puppy_test框架版本高于脚本版本，请使用puppya update命令进行升级！', UserWarning)
