#!/usr/bin/env python3
# coding=utf-8
# encoding=utf-8
# pylint: disable=W0311
"""Minecraft uses two main systems for formatting text.

The Legacy format uses section symbols and hexadecimal color coding,
while the JSON format uses key-value pairs to color individual parts of text.

JSONTextMC is a module for translating legacy messages to and from JSON-formatted text.
Output is not valid JSON by itself, it must be translated into JSON with :func:`json.loads`.

Strict modes and inheritance of various JSON elements can be controlled.

Legacy -> JSON::

    >>> import jsontextmc
    >>> jsontextmc.to_json("\xa7cRed! \xa7lAnd bold!")
    [{'text': 'Red! ', 'color': 'red'}, {'text': 'And bold!', 'color': 'red', 'bold': True}]
    >>> jsontextmc.to_json("\xa7cRed! \xa7lAnd bold!", inherit_parent=True)
    [{'text': 'Red! ', 'color': 'red'}, {'text': 'And bold!', 'bold': True}]
    >>> jsontextmc.to_json("\xa7l\xa7cBold before red, not anymore", strict=True)
    {'text': 'Bold before red, not anymore', 'color': 'red'}
    >>> jsontextmc.to_json("Simple plain text")
    'Simple plain text'

JSON -> Legacy::

    >>> import jsontextmc
    >>> jsontextmc.from_json(
    ...   [{'text': 'Red! ', 'color': 'red'}, {'text': 'And bold!', 'bold': True}]
    ... )
    '§cRed! §lAnd bold!'
    >>> jsontextmc.from_json('Simple plain text')
    'Simple plain text'
"""

from __future__ import annotations

import re

__version__: str = "3.0"


def tokenize(sectioned: str, separator: str = "\xa7") -> list:
    """
    Split input based on separator.

    Text is searched for the separator and split with the Minecraft color code in front of it.

    :param sectioned: Text to split
    :type sectioned: str
    :param separator: The separator to split on
    :type separator: str
    :return: Split list of tokenized codes
    :rtype: list
    """
    return re.split(
        rf"(?P<named>{separator}[0-9a-frk-o]|{separator}[x#][0-9a-f]{6})",
        sectioned,
        flags=re.IGNORECASE | re.UNICODE,
    )


COLORS: dict = {
    "0": "black",
    "1": "dark_blue",
    "2": "dark_green",
    "3": "dark_aqua",
    "4": "dark_red",
    "5": "dark_purple",
    "6": "gold",
    "7": "gray",
    "8": "dark_gray",
    "9": "blue",
    "a": "green",
    "b": "aqua",
    "c": "red",
    "d": "light_purple",
    "e": "yellow",
    "f": "white",
    "r": "reset",
}

COLORS_REVERSED: dict = {v: k for k, v in COLORS.items()}

FORMATS: dict = {
    "k": "obfuscated",
    "l": "bold",
    "m": "strikethrough",
    "n": "underlined",
    "o": "italic",
}

FORMATS_REVERSED: dict = {v: k for k, v in FORMATS.items()}


def to_json(
    text: str,
    separator: str = "\xa7",
    strict: bool = False,
    inherit_parent: bool = False,
) -> dict | list | str:
    """
    Translate Minecraft color-coded text into a modern JSON format.

    * Standalone text will be returned as-is.
    * Text components with one element will be returned themselves, outside of a list.
    * For all other cases, each element is appended to a list and returned.

    If ``strict`` is true, then formatting codes are not allowed to be declared before color codes.
    If a formatting code appears before any color is applied, it will be ignored and discarded.

    If ``inherit_parent`` is true, formatting from the previous element will not carry over into
    the next one, and so any codes defined before will be reset. The reset code works identically.

    :param text: The text to translate into raw JSON text.
    :type text: str
    :param separator: Character to identify color codes by. Natively, it is §, but others may use &
    :type separator: str
    :param strict: If true, formatting codes will be cleared if they are before a color code
    :type strict: bool
    :param inherit_parent: If true, formatting from previous element will be not be copied ahead
    :type inherit_parent: bool
    :return: List, string, or dictionary of a valid JSON component. Use json to transfer into JSON.
    :rtype: dict or list or str
    """
    exported: list = []
    settings: dict = {"color": None, "format": []}
    tokened: list = [x for x in tokenize(text, separator) if x != ""]
    if len(tokened) != 1:
        for part in tokened:
            # if part is a valid color code (has section sign *and* a valid code after)
            if (
                2 <= len(part) <= 8
                and part[0] == separator
                and part[1].lower() in "0123456789abcdeflmnorx#"
            ):
                # If part is not a reset code
                if part[1].lower() in "0123456789abcdefrlmno":
                    # If part is a color code
                    if part[1].lower() in "0123456789abcdefr":
                        if strict:
                            if settings["format"]:
                                settings["format"] = []
                        settings["color"] = COLORS[part[1].lower()]
                        if part[1].lower() == "r":
                            settings["format"] = []
                    # Else, part must be a format code
                    else:
                        settings["format"].append(FORMATS[part[1].lower()])
                # If part is a hexadecimal color code, starts with x OR #
                elif part[1].lower() in "x#":
                    # Hashtag + 6 digits in hexadecimal color code
                    settings["color"] = "#" + part[1:7].lower()
            else:
                temp: dict = {"text": part}
                # If a setting is present
                if settings["color"] or settings["format"]:
                    if settings["color"]:
                        temp["color"] = settings["color"]
                    if len(settings["format"]) != 0:
                        for option in settings["format"]:
                            temp[option] = True
                # No options, can be stored as plain text
                else:
                    temp = part
                if inherit_parent:
                    settings = {"color": None, "format": []}
                exported.append(temp)
    else:
        if len(tokened) == 0:
            return ""
        return tokened[0]
    if len(exported) == 1:
        return exported[0]
    return exported


def from_json(text: dict | list | str, separator: str = "\xa7") -> str:
    """
    Translate modern JSON text into legacy section-sign text.

    Any extra elements such as clickables, translations, or actions **will be discarded**.
    Only ``"text"``, ``"color"``, and the formatting code booleans are dealt with.

    :param text: JSON component text to transform
    :type text: dict | list | str
    :param separator: Character to use as color code marking
    :type separator: str
    :return: String of legacy-coded text
    :rtype: str
    """
    exported: str = ""
    if isinstance(text, (dict, list)):
        if isinstance(text, dict):
            text: list = [text]
        for entry in text:
            if len(entry.keys()) >= 2 and "text" in entry:
                if "color" in entry:
                    exported += separator + COLORS_REVERSED[entry["color"].lower()]
                for option in FORMATS_REVERSED.keys():
                    if option in entry:
                        exported += separator + FORMATS_REVERSED[option]
            if "text" in entry:
                exported += entry["text"]
    elif isinstance(text, str):
        return text
    return exported
