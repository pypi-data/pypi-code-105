# This code was made for SquareCloud (https://squarecloud.app) by Mudinho and NemRela.
# Imports Section
import os
import sys
from warnings import warn


# Bytes converter (RAM Function)
def bytes_to(n: int, formatted: bool = False):
    if formatted:
        for i in ['B', 'KB', 'MB', 'GB']:
            if n < 1024.0:
                return f'{n:3.2f}{i}'
            n /= 1024.0
        return n
    return float(f'{n / 1048576:3.2f}')


# Get_bytes from a directory
def get_bytes_from(path: str) -> int:
    try:
        with open(path, 'r') as b:
            return int(b.read())
    except FileNotFoundError:
        return 0


class Square:
    if os.name != 'posix':
        warn('\n\nAtenção: Esta biblioteca pode não funcionar corretamente no seu sistema operacional.\n')

    class ram:
        def __new__(cls, formatted: bool = False):
            return f'{round(cls.used(raw=True) / 1024 ** 2)}/{cls.total(formatted)}'

        # Returns your used ram
        @staticmethod
        def used(formatted: bool = False, raw: bool = False):
            b: int = get_bytes_from('/sys/fs/cgroup/memory/memory.usage_in_bytes')
            return b if raw else bytes_to(b, formatted)

        # Returns your total ram
        @staticmethod
        def total(formatted: bool = False, raw: bool = False):
            b: int = get_bytes_from('/sys/fs/cgroup/memory/memory.limit_in_bytes')
            return b if raw else bytes_to(b, formatted)

    class ssd:
        def __new__(cls, formatted: bool = False, raw: bool = False):
            folder: str = sys.path[0]
            b: int = 0
            for item in os.listdir(folder):
                if os.path.isdir(f'{os.path.join(folder)}/{item}'):
                    for path, dirs, files in os.walk(f'{os.path.join(folder)}/{item}'):
                        for f in files:
                            fp = os.path.join(path, f)
                            b += float(int(os.path.getsize(fp)))
                else:
                    if not str(item) == 'start.sh':
                        b += float(int(os.path.getsize(f'{os.path.join(folder)}/{item}')))
            return b if raw else bytes_to(b, formatted)
