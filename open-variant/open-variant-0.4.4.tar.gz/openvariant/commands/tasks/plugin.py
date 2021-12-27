import os
from enum import Enum
from functools import partial


def _add_action(name: str, directory: str) -> None:
    path = directory if directory is not None else os.getcwd()
    if os.path.exists(f"{path}/{name}"):
        raise FileExistsError(f"Directory {path}/{name} already exists.")
    os.mkdir(f"{path}/{name}")
    plugin_name = f"{name.capitalize()}Plugin"
    with open(f"{path}/{name}/__init__.py", 'w') as init_file:
        init_file.write(f"import .{name} from {plugin_name}\n")
        init_file.close()
    with open(f"{path}/{name}/{name}.py", 'w') as plugin_file:
        plugin_file.write(f"from plugins.plugin import Plugin\n\n\n")
        plugin_file.write(f"class {plugin_name}(Plugin):\n")
        plugin_file.write(f"\tdef run(self, row: dict) -> dict:\n")
        plugin_file.write(f"\t\treturn row\n")
'''

class Alteration_typePlugin(Plugin):
    """
    This plugin identifies the alteration type.
    Classifies the alteration type: checking POSITION, REF and ALT fields.
    The result will be store as ALT_TYPE field in the same row.
    """

    def run(self, row: dict):
'''

class PluginActions(Enum):
    ADD = partial(_add_action)
