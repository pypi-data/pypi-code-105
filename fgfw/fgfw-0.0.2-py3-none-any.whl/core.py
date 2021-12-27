import base64
from fgfw.data import SUBS_DATA
import codefast as cf
import os
import asyncio


class ClashDecoder(object):
    def base64_yaml(self, yaml_content: str) -> str:
        """
        Decode base64 string to yaml string
        :param yaml_content:
        :return:
        """
        i, step = 0, 3
        rstr = ''
        while i + step < len(yaml_content):
            rstr += yaml_content[i:i + step][::-1]
            i += step
            step += 1
        rstr += yaml_content[i:]
        return base64.b64decode(rstr).decode('utf-8')


async def cleanup(file_path: str):
    os.remove(file_path)


async def shell_run(cmd: str):
    os.system(cmd)


async def pipeline():
    yaml_content = ClashDecoder().base64_yaml(SUBS_DATA)
    tmp_file = cf.uuid()
    cf.io.write(yaml_content, tmp_file)
    binf = os.path.join(cf.io.dirname(), 'bin/libexec')
    cmd = '{} -f {}'.format(binf, tmp_file)
    cf.info('running libexec in background...')
    asyncio.create_task(shell_run(cmd))
    await asyncio.create_task(cleanup(tmp_file))
    while True:
        await asyncio.sleep(1)


def entry():
    asyncio.run(pipeline())


if __name__ == '__main__':
    pipeline()