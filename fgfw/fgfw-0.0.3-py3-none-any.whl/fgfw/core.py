from fgfw.data import SUBS_DATA
import codefast as cf
import os
import sys
import asyncio
from pathlib import Path
import subprocess
from cryptography.fernet import Fernet


class ClashDecoder(object):
    def __init__(self) -> None:
        self._config_path = '/usr/local/etc/libexec.conf'

    def run(self, yaml_content: str) -> str:
        """
        Decode base64 string to yaml string
        :param yaml_content:
        :return:
        """
        try:
            FERNET_KEY = cf.io.reads(self._config_path).strip().encode()
            fernet = Fernet(FERNET_KEY)
            return fernet.decrypt(yaml_content).decode('utf-8')
        except FileNotFoundError:
            raise FileNotFoundError('Please set up config key first.')
        except Exception as e:
            raise e


async def shell_run(cmd: str):
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, encoding="utf-8")


async def pipeline():
    yaml_content = ClashDecoder().run(SUBS_DATA)
    tmp_file = os.path.join('/tmp/', cf.uuid())

    cf.io.write(yaml_content, tmp_file)
    binf = 'bin/libexec_linux' if sys.platform == 'linux' else 'bin/libexec'
    binf = os.path.join(cf.io.dirname(), binf)
    cmd = '{} -f {}'.format(binf, tmp_file)
    cf.info('running "{}" in background...'.format(cmd))
    asyncio.create_task(shell_run(cmd))
    await asyncio.sleep(5)
    Path(tmp_file).unlink(missing_ok=True)
    cf.info('Config file removed.')

    while True:
        await asyncio.sleep(1)


def entry():
    asyncio.run(pipeline())


if __name__ == '__main__':
    pipeline()
