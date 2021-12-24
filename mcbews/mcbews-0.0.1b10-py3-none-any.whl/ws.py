#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A Bot for Minecraft: Bedrock Edition programmed in python using websocket"""

__author__ = "phoenixR"
__version__ = "0.0.1b10"
__license__ = "MIT"


############################################
# Notes

    # list of commands sorted by tags
    # on_connect only send when event received


############################################
# Future Projects

    # WorldEdit
    # Pixel Art


############################################
# Code

import asyncio
from inspect import cleandoc, getdoc, Parameter, signature
import json
import logging
import re
import sys
import traceback
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from uuid import uuid4

import websockets
from websockets.exceptions import ConnectionClosedError

from .case import snakecase_to_pascalcase, pascalcase_to_snakecase
from .chat import Color, Style
from .context import (
    BotContext,
    CommandContext,
    CommandResponseContext,
    ConnectContext,
    ConvertErrorContext,
    DisconnectContext,
    MessageContext,
    MissingArgumentsContext,
    TooManyArgumentsContext,
    UnknownCommandContext,
    WebsocketContext
)
from . import minecraft_output as mo


class exception:
    class InvalidPrefixError(Exception):
        def __init__(self, prefixes):
            self.prefixes = prefixes
    class ConvertError(Exception):
        def __init__(self, function, argument):
            self.converter = function
            self.argument = argument

logging.basicConfig(
    format = "[{asctime}] {levelname}: {message}",
    style = "{",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)



output_level = mo.DEBUG

COMMAND_REQUEST_LIMIT = 100

predefinded = {
    # add different languages (copy 'not_authorized' from minecraft lang file)
    "not_authorized": "You are not authorized to use this command.",
    "tests_disabled": "Tests are disabled."
}

reserved_command_names = [
    # help
    "help",
    "?",
    
    # test
    "t",
    "test",
    "run"
]


def empty(l: Any) -> bool:
    """Checks if the arguments is empty"""
    return l in (
        list(),
        dict(),
        tuple(),
        set(),
        "",
        b""
    )

def command_doc(doc: str, **overwrite: Any) -> dict:
    """Retrieves the docs of a ws minecraft command"""
    
    _example = """
    Divides a number by 2
    
    This command divides a number by two.
    
    #math #chat
    #bot
    
    [Usage]
    num
        The number to divide
    
    [Return]
    The divided number
    """
    # every section is split by two newlines
    # 
    # In case you want to insert a space but
    # write in two different lines use ' \'.
    
    tags = []
    brief = description = usage = returns = None
    
    if doc is not None:
        
        doc = cleandoc(doc)
        sections = doc.split("\n\n")
        
        
        for section in sections:
            # brief
            if section == sections[0]:
                brief = section
                continue
            
            # description
            if section == sections[1]:
                description = section
                continue
            
            # tags
            if section == sections[2]:
                tags = splittags(section)
                continue
            
            # usage
            pattern = "\[Usage\]\n(?P<content>.*)"
            flags = re.DOTALL
            
            match = re.match(pattern, section, flags = flags)
            if match:
                content = match.group("content")
                pattern = """
                    (
                        (?P<argument>
                            \w+
                        )\n
                        (
                            \s+
                            (?P<description>
                                (.+)
                            \n
                            )+
                        )
                    )
                """
                flags = re.VERBOSE
                usage = {
                    m.group("argument"): m.group("description")
                    for m in re.finditer(pattern, content, flags = flags)
                }
                continue
            
            # return
            pattern = "\[Return\]\n(?P<content>.*)"
            flags = re.DOTALL
            
            match = re.match(pattern, section, flags = flags)
            if match:
                returns = match.group("content")
                continue
        
    return {
        "brief": brief or overwrite.get("brief"),
        "tags": tags + overwrite.get("tags", []), # tags get extended so you can e. g. use default tags
        "description": description or overwrite.get("description"),
        "usage": usage or overwrite.get("usage"),
        "return": returns or overwrite.get("returns")
    }

def get_command_args(string: str) -> Tuple[str, Tuple[str, ...]]:
    """Splits command arguments"""
    quotes = "\"'"
    pattern = f"[^{quotes} ]+|(?P<quote>[{quotes}]).*?(?P=quote)"
    # characters in quotes become one argument
    # every argument is split by any amount of spaces
    
    # return (command_name, command_args)
    arguments = [
        re.sub(
            f"^(?P<quote>[{quotes}])(?P<content>.*?)(?P=quote)$", # remove quotes if exist
            lambda m: m.group("content"),
            m.group()
        ) for m in re.finditer(pattern, string)
    ]
    if len(arguments) == 1:
        return (arguments[0], ())
    return arguments[0], tuple(arguments[1:])

def splittags(tags: Union[str, List[str]]) -> list:
    """
    Splits tags into a list. The format may be one of
    #mytag1  #mytag2#mytag3    #mytag4
    mytag1, mytag2,   mytag3,mytag4
    """
    if isinstance(tags, str):
        tags = tags.replace("\n", ",")
        
        if tags == "": return []
        
        # hashtag-style
        newtags = re.findall("#(\w+)", tags)
        if newtags != []:
            return newtags
        
        # comma seperated
        tags = re.sub("\s", "", tags)
        return tags.split(",")
    return tags

def syntax_format(f: callable) -> str:
    """
    Formats a function into a Minecraft command format.
    Example: async def hello(ctx, greet, name  = "World", *more_names)
                               becomes e. g.
             hello <greet> [name: World] [more_names ...]
    """
    sig = signature(f)
    name = f.__name__
    params = sig.parameters
    
    out = name
    
    for param in params:
        param = param[1]
        hasdefault = param.default == Parameter.empty
        iswildcard = param.kind = Paramter.VAR_POSITIONAL
        if iswildcard:
            out += f"[{param.name} ...]"
        else:
            brackets = "[{0.name}]" if hasdefault else "<{0.name}: {0.default}>" #! if not str()’able?
            out += f" {brackets.format(param)}"
    
    return out

def overlay(list1: Iterable, list2: Iterable) -> tuple:
    """Two lists zipped but single values are seperated"""
    if len(list1) == len(list2):
        return tuple(zip(list1, list2))
    base = list1 if len(list1) > len(list2) else list2
    sub  = list1 if len(list1) < len(list2) else list2
    
    concatenates = []
    single = []
    for i, item in enumerate(base):
        if len(sub) - 1 > i:
            single.append(i)
            continue
        concatenates.append((item, sub[i]))
    
    return (concatenates, single)

def onlykeys(dictionary: dict, keys: List[Any]) -> bool:
    """Checks if a dictionary only has certain keys"""
    return all((
        len(dictionary.keys()) == len(keys),
        all([
            key in dictionary.keys() for key in keys
        ])
    ))

def keep(arg):
    return arg

def convert_type(func: callable, *args: str):
    """The arguments get converted to the annotations of the arguments."""
    stdconvert = keep
    ant = func.__annotations__
    
    ant.pop("ctx", None)
    # there shouldn't be an annotation for ctx
    # since it's not supposed to be converted
    
    ant.pop("return", None)
    # there shouldn't be an annotation for a
    # return value since all commands are
    # courotines
    
    sig = signature(func)
    params = sig.parameters
    for param in params:
        if param not in ant:
            ant[param] = stdconvert
    
    new_args = []
    for arg, conv in zip(args, ant.values()):
        try:
            converted = conv(arg)
        except ValueError as exc:
            raise exception.ConvertError(
                conv, arg
            )# from exc
        new_args.append(conv(arg))
    return tuple(new_args)


class Bot:
    def __init__(
        self,
        name: str,
        prefix: str,
        style: dict = {},
        case_sensitive: bool = True,
        permission: Union[str, List[str]] = [], # an empty list stands for everyone
        output_level: int = mo.DEBUG,
        language: str = "en_US",
        tests_prefix: str = "@",
        tests_active: bool = False
    ) -> None:
        
        if prefix == tests_prefix:
            raise exception.InvalidPrefixError("prefix and test prefix can't be the same")
        
        # bot metadata
        self.name = name
        self.prefix = prefix
        self.tests_prefix = tests_prefix
        self.case_sensitive = case_sensitive
        self.help_commands = ["help","?"]
        self.output_level = output_level
        self.language = language
        self.permission = [permission] if isinstance(permission, str) else permission
        self.tests_active = tests_active
        self._event_prefix = "on_"
        
        # events
        self.listen_events = {"PlayerMessage"}
        
        self.event_handlers = {}
        self.minecraftevent_handlers = {}
        self.test_handlers = {}
        self.command_handlers = {}
        
        # loop
        self.loop = asyncio.get_event_loop()
        
        # style
        default_style = {
            # Tuple of Color and Style
            # None for none
            
            "header": (Color.GOLD, Style.BOLD),
            "default": (None, None),
            
            "critical": (Color.DARK_RED, None),
            "error": (Color.RED, None),
            "warning": (Color.RED, None),
            "info": (None, None),
            "debug": (None, None)
        }
        
        for key, value in default_style.items():
            style.setdefault(key, value)
        
        # queue
        self.send_queue = [] # commands that need to be executed
        self.awaited_queue = {} # commands that got sent, but didn't got a respond
        # After 100 pending requests the bot
        # waits until one requests has been
        # processed.
        
        
        # assign style
        def getstyle(key):
            return Style.RESET.value + "".join([
                "" if s is None else s.value
                for s in style[key]
            ])
        
        self.color_header = getstyle("header")
        self.color_default = getstyle("default")
        
        self.color_critical = getstyle("critical")
        self.color_error = getstyle("error")
        self.color_warning = getstyle("warning")
        self.color_info = getstyle("info")
        self.color_debug = getstyle("debug")
        
        self.style = {
            key: getstyle(key)
            for key in style
        }
    
    async def sleep(self, duration: Union[int, float]) -> None:
        await asyncio.sleep(duration)
    wait = sleep
    
    @staticmethod
    def set_output_level(level: int) -> None:
        self.output_level = level
    
    @staticmethod
    def _on_error(event_method: str) -> None:
        print(f"Ignoring exception in {event_method}", file = sys.stderr)
        traceback.print_exc()
    
    def authorized(self, name: str) -> bool:
        if empty(self.permission) or name in self.permission:
            return True
        else:
            return False
    
    def event(self, evt: callable) -> None:
        def decorator(*args, **kwargs):
            name = evt.__name__
            if name in self.event_handlers:
                raise Exception(f"'{name}' is already registered as event.")
            self.event_handlers[name] = evt
        
        return decorator()
    
    def minecraftevent(self, evt: callable) -> None:
        def decorator(*args, **kwargs):
            name = evt.__name__
            if name in self.minecraftevent_handlers:
                raise Exception(f"'{name}' is already registered as minecraftevent.")
            self.minecraftevent_handlers[name] = evt
            self.listen_events.add(snakecase_to_pascalcase(name))
        
        return decorator()
    
    def test(
        self,
        name: str = "",
        description: str = ""
    ) -> None:
        def decorator(tst):
            tstname = name.lower() or tst.__name__.lower()
            if tstname in self.test_handlers:
                raise Exception(f"'{n}' is already registered as test.")
            self.test_handlers[tstname] = {}
            self.test_handlers[tstname]["function"] = tst
            self.test_handlers[tstname]["command"] = command_doc(tst.__doc__)
        
        return decorator
    
    def command(
        self,
        name: Optional[str] = None,
        aliases: List[str] = [],
        tags: Union[str, List[str]] = [],
        permission: Union[str, List[str]] = [],
        brief: Optional[str] = None,
        description: Optional[str] = None,
        usage: Dict[str, Union[str, Dict[str, str]]] = {},
        returns: Optional[str] = None
    ) -> None:
        tags = splittags(tags)
        def decorator(cmd):
            cmdname = name or cmd.__name__
            cmdname = cmdname.lower()
            names = aliases.copy()
            names.append(cmdname)
            for n in names:
                if n in reserved_command_names:
                    raise Exception (f"'{n}' is a reserved command name.")
                if n in self.command_handlers:
                    raise Exception(f"'{n}' is already registered as command.")
                self.command_handlers[n] = {}
                self.command_handlers[n]["function"] = cmd
                self.command_handlers[n]["command"] = command_doc(
                    cmd.__doc__,
                    brief = brief,
                    description = description,
                    usage = usage,
                    tags = tags,
                    returns = returns
                )
        
        return decorator
    
    @staticmethod
    async def _try_async_function(func: callable, *args: Any, **kwargs: Any) -> None:
        try:
            await func(*args, **kwargs)
        except Exception:
            Bot._on_error(func.__name__)
    
    @staticmethod
    def _try_function(func: callable, *args: Any, **kwargs: Any) -> None:
        try:
            func(*args, **kwargs)
        except Exception:
            Bot._on_error(func.__name__)
    
    '''
    def _configure_help_command(self) -> None:
        async def help_function(ctx, name: str = "*"):
            if name in self.command_handlers:
                doc = self.command_handlers[name]["function"].__doc__
                info = command_doc(doc)
                ctx.info(
                    f"{self.prefix}{name}"
                )
        self.command_handlers[self.help_commands] = help_function
    '''
    
    def stop(self) -> None:
        self.loop.stop()
        self.loop.close()
    
    def run(self, host: str, port: int) -> None:
        async def start(ws):
            
            async def process_requests() -> None:
                count = min(
                    COMMAND_REQUEST_LIMIT - len(self.awaited_queue), # free space
                    len(self.send_queue)                             # need to send
                )
                for _ in range(count): # send a maximum of 100 commands
                    cmd = self.send_queue.pop(0)
                    await ws.send(cmd.data)
                    self.awaited_queue[cmd.request_id] = cmd.data
            
            cfg = { # gets passed in (almost) every context class
                "send_queue": self.send_queue,
                "name": self.name,
                "style": self.style,
                "output_level": self.output_level
            }
            
            e = self._event_prefix + "connect"
            if e in self.event_handlers:
                ctx = ConnectContext(**cfg)
                await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                await process_requests()
            
            async def runcommand(typ: str, message: str, author: str) -> None:
                if typ == "command":
                    message = message[len(self.prefix):]
                    handler = self.command_handlers
                    quit = False
                elif typ == "test":
                    message = message[len(self.tests_prefix):]
                    handler = self.test_handlers
                    quit = not self.tests_active
                
                if not quit:
                    command_name, command_arguments = get_command_args(message)
                    if not self.case_sensitive:
                        command_name = command_name.lower()
                    
                    if not self.authorized(author):
                        e = self._event_prefix + "not_authorized"
                        if e in self.event_handlers:
                            ctx = NotAuthorizedContext(command_name, author, **cfg)
                            await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                    else:
                        command = handler.get(command_name)
                        if command is None:
                            # command not found
                            e = self._event_prefix + "unknown_command"
                            if e in self.event_handlers:
                                ctx = UnknownCommandContext(command_name, **cfg)
                                await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                        else:
                            func = command["function"]
                            sig = signature(func)
                            params = sig.parameters.values()
                            param_names = [p.name for p in params]
                            param_names.remove("ctx")
                            given = [i[1] for i in zip(command_arguments, param_names)]
                            if len(command_arguments) > len(param_names):
                                too_many = command_arguments[len(given):]
                                e = self._event_prefix + "too_many_arguments"
                                if e in self.event_handlers:
                                    ctx = TooManyArgumentsContext(command_name, too_many, **cfg)
                                    await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                            else:
                                missing = []
                                for param in params:
                                    if param.name != "ctx":
                                        required = any((
                                            param.default is Parameter.empty,
                                            param.kind not in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD)
                                        ))
                                        if required:
                                            if param.name not in given:
                                                missing.append(param.name)
                                if not empty(missing):
                                    e = self._event_prefix + "missing_arguments"
                                    if e in self.event_handlers:
                                        ctx = MissingArgumentsContext(command_name, missing, **cfg)
                                        await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                                
                                else:
                                    try:
                                        args = convert_type(command["function"], *command_arguments)
                                    except exception.ConvertError as err:
                                        e = self._event_prefix + "convert_error"
                                        if e in self.event_handlers:
                                            ctx = ConvertErrorContext(err.converter, err.argument, **cfg)
                                            await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                                    else:
                                        await command["function"](CommandContext(properties, **cfg), *args)
        
            
            # sent listener requests to minecraft
            for event in self.listen_events:
                await ws.send(json.dumps({
                    "header": {
                        "version": 1,
                        "requestId": str(uuid4()),
                        "messageType": "commandRequest",
                        "messagePurpose": "subscribe"
                    },
                    "body": {
                        "eventName": event
                    }
                }))
            
            try:
                async for data in ws:
                    data = json.loads(data)
                    response = data["header"].get("messagePurpose") == "commandResponse"
                    if not response:
                        event = data["body"].get("eventName")
                        if event == "PlayerMessage":
                            properties = data["body"]["properties"]
                            message = properties["Message"]
                            author = properties["Sender"]
                            e = self._event_prefix + "message"
                            if e in self.event_handlers:
                                ctx = MessageContext(properties, **cfg)
                                Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                            
                            # test command
                            if message.startswith(self.tests_prefix):
                                await runcommand(
                                    "test",
                                    message = message,
                                    author = author
                                )
                            
                            # command
                            elif message.startswith(self.prefix):
                                await runcommand(
                                    "command",
                                    message = message,
                                    author = author
                                )
                        
                        elif isinstance(event, str):
                            await Bot._try_async_function(self.minecraftevent_handlers[pascalcase_to_snakecase(event)], ctx = data["body"])
                    
                    #endif (not response)
                    else:
                        header = data["header"]
                        req_id = header["requestId"]
                        
                        responsedata = data["body"].copy()
                        success = responsedata.pop("statusCode") != 0
                        message = responsedata.pop("statusMessage", None)
                        content = responsedata
                        if req_id in self.awaited_queue:
                            del self.awaited_queue[req_id]
                        
                        e = self._event_prefix + "commandresponse"
                        if e in self.event_handlers:
                            ctx = CommandResponseContext(success, message, content, **cfg)
                            await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                    
                    await process_requests()
            
            except ConnectionClosedError as exc:
                e = self._event_prefix + "disconnect"
                if e in self.event_handlers:
                    ctx = DisconnectContext(exc)
                    await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
        
        start_server = websockets.serve(start, host = host, port = port)
        
        e = self._event_prefix + "ready"
        if e in self.event_handlers:
            ctx = WebsocketContext(host, port)
            Bot._try_function(self.event_handlers[e], ctx = ctx)
        
        self.loop.run_until_complete(start_server)
        self.loop.run_forever()