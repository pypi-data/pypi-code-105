#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A Bot for Minecraft: Bedrock Edition programmed in python using websocket"""

__author__ = "phoenixR"
__version__ = "0.0.1b3"
__license__ = "MIT"


############################################
# Notes

    # overload
    # check for too many args
    # try if it works on console by joining on phone
    # list of commands sorted by tags
    # don't include convert.py, rather show them in the docs


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

from .tools.case import snakecase_to_pascalcase, pascalcase_to_snakecase
from .tools.chat import Color, Style
from .tools.context import (
    BotContext,
    CommandContext,
    CommandResponseContext,
    ConnectContext,
    DisconnectContext,
    MessageContext,
    MissingArgumentsContext,
    UnknownCommandContext,
    WebsocketContext
)
import .tools.minecraft_output as mo


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
        tuple(),
        set(),
        "",
        b""
    )

def chunk(l: list, size: int) -> list:
    return [l[i:i+size] for i in range(0, len(l), size)]

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
        "brief": brief or overwrite["brief"],
        "tags": tags + overwrite["tags"], # tags get extended so you can e. g. use default tags
        "description": description or overwrite["description"],
        "usage": usage or overwrite["usage"],
        "return": returns or overwrite["returns"]
    }

def get_command_attrs(string: str) -> Tuple[str, Tuple[str, ...]]:
    """Splits command parameters"""
    pattern = "[^\"' ]+|(?P<quote>[\"']).*?(?P=quote)"
    # arguments in quotes become one
    # every argument is split by any amount of spaces
    
    arguments = [m.group() for m in re.finditer(pattern, string)]
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



def convert_type(func: callable, *args: str):
    """The arguments get converted to the annotations of the arguments."""
    ant = func.__annotations__
    new_args = []
    for arg, conv in zip(args, ant.values()):
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
        tests_prefix: str = "@",
        tests_active: bool = False
    ) -> None:
        
        if prefix == tests_prefix:
            raise NameError("prefix and test prefix can't be the same")
        
        # bot metadata
        self.name = name
        self.prefix = prefix
        self.tests_prefix = tests_prefix
        self.case_sensitive = case_sensitive
        self.help_commands = ["help","?"]
        self.output_level = output_level
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
            self.test_handlers[tstname] = tst
        
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
                BotContext(**cfg).raw("") # update
            
            
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
                    #logger.debug(f"response: {response}")
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
                                message = message[len(self.prefix):] # remove prefix
                                test_name, test_arguments = get_command_attrs(message)
                                if not self.case_sensitive:
                                    test_name = test_name.lower()
                                
                                if not self.authorized(author):
                                    await BotContext(**cfg).err(predefinded["not_authorized"], target = author)
                                else:
                                    try:
                                        if self.tests_active:
                                            test = self.test_handlers[test_name]
                                            await test(CommandContext(properties, **cfg), *convert_type(test, *test_arguments))
                                        else:
                                            await BotContext(**cfg).err(predefinded["tests_disabled"], target = author)
                                    except KeyError: # test not found
                                        e = self._event_prefix + "unknown_command"
                                        if e in self.event_handlers:
                                            ctx = UnknownCommandContext(test_name, **cfg)
                                            await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                                    except TypeError: # missing argument(s)
                                        required = []
                                        params = signature(test).parameters
                                        for param in params.values():
                                            if all((
                                                param.default == Parameter.empty,                                   # no default given
                                                param.kind not in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD) # not *arg nor **kwarg
                                            )):
                                                required.append(param.name)
                                        not_given = required[len(test_arguments) + 1:] # +1 for the ctx argument
                                        e = self._event_prefix + "missing_arguments"
                                        if e in self.event_handlers:
                                            ctx = MissingArgumentsContext(test_name, not_given, **cfg)
                                            await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                            
                            # command
                            elif message.startswith(self.prefix):
                                message = message[len(self.prefix):] # remove prefix
                                command_name, command_arguments = get_command_attrs(message)
                                if not self.case_sensitive:
                                    command_name = command_name.lower()
                                
                                if not self.authorized(author):
                                    await BotContext(**cfg).err(predefinded["not_authorized"], target = author)
                                else:
                                    try:
                                        command = self.command_handlers[command_name]
                                        await command["function"](CommandContext(properties, **cfg), *convert_type(command["function"], *command_arguments))
                                    except KeyError: # command not found
                                        e = self._event_prefix + "unknown_command"
                                        if e in self.event_handlers:
                                            ctx = UnknownCommandContext(command_name, **cfg)
                                            await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                                    except TypeError: # missing argument(s)
                                        required = []
                                        params = signature(command["function"]).parameters
                                        for param in params.values():
                                            if all((
                                                param.default == Parameter.empty,                                   # no default given
                                                param.kind not in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD) # not *arg nor **kwarg
                                            )):
                                                required.append(param.name)
                                        not_given = required[len(command_arguments) + 1:] # +1 for the ctx argument
                                        e = self._event_prefix + "missing_arguments"
                                        if e in self.event_handlers:
                                            ctx = MissingArgumentsContext(command_name, not_given, **cfg)
                                            await Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                        
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
                        logger.debug(f"req id {req_id}")
                        if req_id in self.awaited_queue:
                            logger.debug(f"deleting {req_id} from awaited_queue...")
                            del self.awaited_queue[req_id]
                        
                        e = self._event_prefix + "commandresponse"
                        if e in self.event_handlers:
                            ctx = CommandResponseContext(success, message, content, **cfg)
                            Bot._try_async_function(self.event_handlers[e], ctx = ctx)
                    
                    count = min(
                        COMMAND_REQUEST_LIMIT - len(self.awaited_queue), # free space
                        len(self.send_queue)                             # need to send
                    )
                    logger.debug(f"# send queue: {len(self.send_queue)}")
                    logger.debug(f"# awaited queue: {len(self.awaited_queue)}")
                    logger.debug(f"# of next excutes: {count}")
                    for _ in range(count): # send a maximum of 100 commands
                        cmd = self.send_queue.pop(0)
                        await ws.send(cmd.data)
                        self.awaited_queue[cmd.request_id] = cmd.data
            
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