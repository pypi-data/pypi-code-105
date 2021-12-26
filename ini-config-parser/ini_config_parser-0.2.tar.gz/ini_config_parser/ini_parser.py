import sys
from configparser import ConfigParser
from typing import List


class IniParserSingleton:
    config_path: str = "config.ini"
    global_section: str = "global"

    environment: str
    available_environments: List[str]
    configparser_obj: ConfigParser

    class IniParserError(Exception):
        pass

    def _init_configparser(self):
        self.configparser_obj = ConfigParser()
        self.configparser_obj.read(self.config_path)

        self.available_environments = self.configparser_obj.sections()
        self.available_environments.remove(self.global_section)

    def __init__(self, config_path: str = "", global_section: str = ""):
        if config_path:
            self.config_path = config_path
        if global_section:
            self.global_section = global_section

        self._init_configparser()

    def _resolve_value(self, key: str):
        environment_config = self.configparser_obj[self.environment]
        if key in environment_config:
            return environment_config[key]

        global_config = self.configparser_obj[self.global_section]
        if key in global_config:
            return global_config[key]

        raise self.IniParserError(
            f"Key `{key}` is not found in `global` section neither `{self.environment}`"
        )

    @property
    def _available_environments_text(self):
        return f" | Available enviroments: {self.available_environments}"

    def get_environment_as_cmd_arg(self):
        args = sys.argv
        if len(args) != 2 or args[1] not in self.available_environments:
            raise self.IniParserError(
                "Usage: python3 [file.py] [enviroment]"
                + self._available_environments_text
            )

        self.environment = args[1]
        return self

    def get_environment_from_file(self, file_path: str):
        try:
            with open(file_path, "r") as f:
                environment = f.read().replace("\n", "")
        except FileNotFoundError:
            raise self.IniParserError(
                f"Please, create file `{file_path}` with available environment"
                + self._available_environments_text
            ) from FileNotFoundError

        if not environment in self.available_environments:
            raise self.IniParserError(
                f"Environment `{environment}` in file `{file_path}` is incorrect"
                + self._available_environments_text
            )

        self.environment = environment
        return self

    def config(self, key: str, converter=None):
        """gets key from config.ini and if converter, returns converter(value) else just value"""
        value = self._resolve_value(key)
        if converter:
            return converter(value)
        return value


if __name__ == "__main__":
    ini_parser_singleton = IniParserSingleton().get_environment_as_cmd_arg()
    config = ini_parser_singleton.config

    ...

    PORT = config("PORT", int)
