import os
import sys
import re
import platform
import getpass
from typing import Any, Dict, List, Tuple, Match

import keyboard

from iinput import utils


class __iinput:
    

    def __init__(self):
        pass


    def __call__(self, prompt: str = ''):
        return input(prompt)


    @staticmethod
    def yn(prompt: str, default: Any = None) -> str:
        inp = None
        while inp not in ['y', 'n']:
            inp = str(input(f"{prompt} [y/n]: ")).strip().lower()
            if not inp and default is not None:
                return default
        return inp


    @staticmethod
    def value(prompt: str, allowed_types: List[type] = [str], default: str = '') -> Any:
        inp = None
        while inp is None:
            inp = str(input(f"{prompt}: ")).strip()
            if not inp and default is not None:
                return default
            inp, = utils.auto_cast([inp], allowed_types=allowed_types)
        return inp


    @staticmethod
    def values(prompt: str, delimiter: str = ',', allowed_types: List[type] = [str], default: list = []) -> list:
        inp = items = None
        while not (inp and items):
            inp = str(input(f"{prompt}: ")).strip()
            if not inp and default is not None:
                return default
            items = utils.split_ws(inp, delimiter)
            items = utils.auto_cast(items, allowed_types)
        return items


    @staticmethod
    def match_value(prompt: str, target: str, max_attempts: int = -1) -> bool:
        target = str(target)
        attempts = 0
        inp = None
        while inp != target and attempts != max_attempts:
            inp = str(input(f"{prompt}: "))
            attempts += 1
        return attempts != max_attempts


    @staticmethod
    def match_values(prompt: str, targets: list, delimiter: str = ',', max_attempts: int = -1) -> bool:
        targets = [str(v) for v in targets]
        attempts = 0
        inps = []
        while sorted(inps) != sorted(targets) and attempts != max_attempts:
            inp = str(input(f"{prompt}: "))
            inps = utils.split_ws(inp, delimiter)
            attempts += 1
        return attempts != max_attempts


    @staticmethod
    def boolean(prompt: str, default: Any = None) -> bool:
        while True:
            inp = str(input(f"{prompt}: ")).strip().lower()
            if not inp and default is not None:
                return default
            if inp in ['0', '1']:
                return inp == '1'
            elif inp in ['false', 'true']:
                return inp == 'true'


    @staticmethod
    def number(prompt: str, default: Any = None) -> int or float:
        inp = ''
        while not (utils.isint(inp) or utils.isfloat(inp)):
            inp = str(input(f"{prompt}: ")).strip()
            if not inp and default is not None:
                return default
        return float(inp) if '.' in inp else int(inp)


    @staticmethod
    def integer(prompt: str, default: Any = None) -> int:
        inp = ''
        while not utils.isint(inp):
            inp = str(input(f"{prompt}: ")).strip()
            if not inp and default is not None:
                return default
        return int(inp)


    @staticmethod
    def floating_point(prompt: str, default: Any = None) -> float:
        inp = ''
        while not utils.isfloat(inp):
            inp = str(input(f"{prompt}: ")).strip()
            if not inp and default is not None:
                return default
        return float(inp)


    @staticmethod
    def character(prompt: str, default: Any = None) -> str:
        inp = ''
        while not utils.ischar(inp):
            inp = str(input(f"{prompt}: "))
            if not inp and default is not None:
                return default
        return inp


    @staticmethod
    def string(prompt: str, default: str = '') -> str:
        inp = ''
        while not inp:
            inp = str(input(f"{prompt}: ")).strip()
            if not inp and default is not None:
                return default
        return inp


    @staticmethod
    def alpha(prompt: str, default: Any = None) -> str:
        inp = ''
        while not inp.isalpha():
            inp = str(input(f"{prompt}: ")).strip()
            if not inp and default is not None:
                return default
        return inp


    @staticmethod
    def alphanumeric(prompt: str, default: Any = None) -> str:
        inp = ''
        while not inp.isalnum():
            inp = str(input(f"{prompt}: ")).strip()
            if not inp and default is not None:
                return default
        return inp


    @staticmethod
    def line(prompt: str, default: str = '') -> str:
        inp = None
        while not inp:
            inp = str(input(f"{prompt}: "))
            if not inp and default is not None:
                return default
        return inp


    @staticmethod
    def lines(prompt: str) -> List[str]:
        print(f"{prompt}: ")
        lines = sys.stdin.readlines()
        lines = [l.rstrip('\n') for l in lines]
        return lines


    @staticmethod
    def selection(menu_options: dict, header: str = "menu", prompt: str = "enter selection", default: Any = None) -> Tuple[str, Any]:
        if header:
            print(header)
        for key, value in menu_options.items():
            print(f"\t[{key}]: {value}")
        print()

        menu_options = {str(k): v for k, v in menu_options.items()}
        selected_key = None
        while selected_key not in menu_options:
            selected_key = str(input(f"{prompt}> ")).strip()
            if not selected_key and default is not None:
                if default in menu_options:
                    return default, menu_options[default]
                else:
                    return default, None
        return selected_key, menu_options[selected_key]


    @staticmethod
    def multiselection(menu_options: dict, header: str = "menu", prompt: str = "enter selection", delimiter: str = ',', default: Any = None) -> Dict[str, Any]:
        if header:
            print(header)
        for key, value in menu_options.items():
            print(f"\t[{key}]: {value}")
        print()

        menu_options = {str(k): v for k, v in menu_options.items()}
        selected_keys = []
        while not selected_keys or any(s not in menu_options.keys() for s in selected_keys):
            inp = str(input(f"{prompt}> "))
            selected_keys = utils.split_ws(inp, delimiter)
            if not selected_keys and default is not None:
                return {k: menu_options.get(k, None) for k in default} 
        return {k: menu_options[k] for k in selected_keys} 


    @staticmethod
    def email(prompt: str, default: str = '') -> str:
        email = None
        while not email:
            inp = str(input(f"{prompt}: ")).strip()
            if not inp and default is not None:
                return default
            email = re.search("[\w\.,]+@[\w\.,]+\.\w+", inp)
        return email.group(0)


    @staticmethod
    def password(prompt: str, default: str = '') -> str:
        pwd = None
        while not pwd:
            pwd = getpass.getpass(prompt=f"{prompt}: ")
            if not pwd and default is not None:
                return default
        return pwd


    @staticmethod
    def match_password(prompt: str, target: str, max_attempts: int = -1) -> bool:
        target = str(target)
        attempts = 0
        pwd = None
        while pwd != target and attempts != max_attempts:
            pwd = getpass.getpass(prompt=f"{prompt}: ")
            attempts += 1
        return attempts != max_attempts

    @staticmethod
    def regex(prompt: str, r: str, flags: int = 0, default: Any = None) -> Match[str]:
        match = None
        while not match:
            inp = str(input(f"{prompt}: "))
            if not inp and default is not None:
                return default
            match = re.search(r, inp, flags=flags)
        return match


    @staticmethod
    def wait_for_key_press(key: str, prompt: str = "press '{}' to continue...") -> None:
        if not utils.ischar(key):
            raise ValueError(f"{key} is not a valid key")

        prompt = prompt.format(key)
        print(f"{prompt} ")
        keyboard.wait(key)


    @staticmethod
    def wait_for_some_key_press(keys: List[str], prompt: str = "press {} to continue...") -> None:
        if any(not utils.ischar(k) for k in keys):
            raise ValueError(f"{keys} are not valid")

        prompt = prompt.format(keys)
        print(f"{prompt} ")
        while True:
            if keyboard.read_key() in keys:
                return


    @staticmethod
    def wait_for_any_key_press(prompt: str = "press any key to continue...") -> None:
        if platform.system() == "Windows":
            print(prompt)
            os.system("pause")
        else:
            os.system(f"read -s -n 1 -p \"{prompt}\"")


    @staticmethod
    def wait_for_enter(prompt: str = "press ENTER to continue...") -> None:
        input(prompt)


iinput = __iinput()
