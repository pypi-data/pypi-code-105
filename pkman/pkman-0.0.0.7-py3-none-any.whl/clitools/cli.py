import os
import sys
from .utils import CmdUtil
os.environ['ANSI_COLORS_DISABLED']="1"
import fire
from . import apis




class CLI:
    def hi(cls):
        print('Hi, welcome to use pkman !'.center(50, '*'))

    @classmethod
    def cmd(cls, *args, **kwargs):
        CmdUtil.run_command(sys.argv[2:])
    @classmethod
    def build(cls):
        pass
    @classmethod
    def config(cls):
        pass
    @classmethod
    def docs(cls):
        pass
    @classmethod
    def init(cls):
        apis.init()
    @classmethod
    def install(cls):
        pass
    @classmethod
    def list(cls):
        pass
    @classmethod
    def ls(cls):
        pass
    @classmethod
    def login(cls):
        pass
    @classmethod
    def logout(cls):
        pass
    @classmethod
    def publish(cls):
        pass
    @classmethod
    def run(cls):
        pass
    @classmethod
    def search(cls):
        pass
    @classmethod
    def uninstall(cls):
        pass
    @classmethod
    def unpublish(cls):
        pass
    @classmethod
    def update(cls):
        pass
    @classmethod
    def version(cls):
        pass


    @classmethod
    def testsysargv(cls, *args, **kwargs):
        import sys
        print("sys.argv:", sys.argv)
        print("executable:", sys.executable)

def main():
    fire.Fire(CLI())

if __name__ == '__main__':
    main()