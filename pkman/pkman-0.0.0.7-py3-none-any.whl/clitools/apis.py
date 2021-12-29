import json
import os.path

from .utils import IoUtil
from .config import PACKGAE_CONFIG_FILENAME
def init():
    def input_field(description, default, keep_empty):
        res = input('%s: (%s)' % (description, default)).strip() if default is not None else input(
            '%s: ' % (description)).strip()
        if res:
            return res
        elif default is not None:
            return default
        elif keep_empty:
            return ""
        else:
            return default

    def field(description, default=None, keep_empty=False):
        return dict(description=description, default=default, keep_empty=keep_empty)

    form = dict(
        name=field(description="package name", default=os.path.basename(os.path.abspath(os.getcwd()))),
        version=field(description="version", default="1.0.0"),
        description=field(description="description", keep_empty=True),
        entry_point=field(description="entry point", default="main.py"),
        test_command=field(description="test command"),
        git_repository=field(description="git repository"),
        keywords=field(description="keywords"),
        anthor=field(description="author", keep_empty=True),
        license=field(description="license", default='MIT'),
    )

    def fill_form(form):
        result = {}
        for k, f in form.items():
            v = input_field(f['description'], f['default'], f["keep_empty"])
            if v is not None:
                result[k] = v
        return result

    info = fill_form(form)
    if "test_command" in info.keys():
        test_command = info.pop("test_command")
    else:
        test_command = 'echo "Error: no test specified"'
    info["scripts"] = {"test": test_command}

    if "git_repository" in info.keys():
        repository = {
            "type": "git",
            "url": info.pop("git_repository")
        }
        info["repository"]=repository
    pkg_config_path=os.path.join(os.getcwd(),PACKGAE_CONFIG_FILENAME)
    IoUtil.json_dump(info,pkg_config_path,indent=2)
    print(IoUtil.read_txt(pkg_config_path))
    return info


