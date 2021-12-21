import json
from uuid import uuid4

from chat import Color, Style
import minecraft_output as mo
import minecraft_properties as mp

class _CommandRequest:
    def __init__(self, data, request_id):
        self.data = data
        self.request_id = request_id

class BotContext:
    def __init__(self, send_queue, style, name, output_level = mo.DEBUG):
        self.send_queue = send_queue
        self.style = style
        self.name = name
        self.output_level = output_level
    
    def _generate_rawtext(self, header_info: str, header_color: str, content_color: str, message: str) -> str:
        return json.dumps({
           "rawtext": [{
                "text": f"{self.style['header']}[{self.name}]{Style.RESET.value} {header_color}{Style.BOLD.value}{header_info}\n{content_color}{message}"
            }]
        })
    
    def cmd(self, command: str) -> None:
        if command.startswith("/"):
            command = command[1:] # remove slash prefix
        req_id = str(uuid4())
        send = json.dumps({
            "header": {
                "version": 1,
                "requestId": req_id,
                "messagePurpose": "commandRequest",
                "messageType": "commandRequest"
            },
            "body": {
                "version": 1,
                "commandLine": command,
                "origin": {
                    "type": "player"
                }
            }
        })
        self.send_queue.append(_CommandRequest(send, req_id))
        
    command = cmd
    execute = cmd
    
    def raw(self, message: str, target: str = "@a") -> None:
        rawtext = json.dumps({
            "rawtext": [{
                "text": message
             }]
        })
        self.cmd(f"tellraw {target} {rawtext}")
    
    def message(self, message: str, target: str = "@a") -> None:
        rawtext = json.dumps({
            "rawtext": [{
                "text": f"{self.style['header']}[{self.name}]{self.style['default']}\n{message}"
             }]
        })
        self.cmd(f"tellraw {target} {rawtext}")
    msg = message
    
    def debug(self, message: str, target: str = "@a") -> None:
        if self.output_level <= mo.DEBUG:
            header_color = Color.AQUA.value
            header_info = "Debug"
            content_color = self.style["debug"]
            rawtext = self._generate_rawtext(header_info, header_color, content_color, message)
            self.cmd(f"tellraw {target} {rawtext}")
    
    def info(self, message: str, target: str = "@a") -> None:
        if self.output_level <= mo.INFO:
            header_color = Color.YELLOW.value
            header_info = "Info"
            content_color = self.style["info"]
            rawtext = self._generate_rawtext(header_info, header_color, content_color, message)
            self.cmd(f"tellraw {target} {rawtext}")
    
    def warning(self, message: str, target: str = "@a") -> None:
        if self.output_level <= mo.WARNING:
            header_color = Color.DARK_YELLOW.value
            header_info = "Warning"
            content_color = self.style["warning"]
            rawtext = self._generate_rawtext(header_info, header_color, content_color, message)
            self.cmd(f"tellraw {target} {rawtext}")
    warn = warning
    
    def error(self, message: str, target: str = "@a") -> None:
        if self.output_level <= mo.ERROR:
            header_color = Color.RED.value
            header_info = "Error"
            content_color = self.style["error"]
            rawtext = self._generate_rawtext(header_info, header_color, content_color, message)
            self.cmd(f"tellraw {target} {rawtext}")
    err = error
    
    def critical(self, message: str, target: str = "@a") -> None:
        if self.output_level <= mo.CRITICAL:
            header_color = Color.DARK_RED.value
            header_info = "Critical"
            content_color = self.style["critical"]
            rawtext = self._generate_rawtext(header_info, header_color, content_color, message)
            self.cmd(f"tellraw {target} {rawtext}")
    fatal = critical

class ConnectContext(BotContext):
    def __init__(self, *ctx_args, **ctx_kwargs):
        super().__init__(*ctx_args, **ctx_kwargs)

class DisconnectContext:
    def __init__(self, exception):
        if exception.sent is None:
            self.code = self.reason = None
        else:
            self.code = exception.sent.code
            self.reason = exception.sent.reason
        
        if exception.recv is None:
            self.code = self.recv = None
        else:
            self.code = exception.recv.code
            self.reason = exception.recv.reason

class CommandContext(BotContext):
    def __init__(self, properties, *ctx_args, **ctx_kwargs):
        super().__init__(*ctx_args, **ctx_kwargs)
        self.author = properties["Sender"]
        self.biome = mp.Biome(properties["Biome"])
        self.difficulty = properties["Difficulty"] # difficulty name (uppercase)
        self.gamemode = mp.Gamemode(properties["Mode"]) # the gamemode id
        self.build = properties["Build"] # the minecraft version the player uses

class MessageContext(BotContext):
    def __init__(self, properties, *ctx_args, **ctx_kwargs):
        super().__init__(*ctx_args, **ctx_kwargs)
        self.message = properties["Message"]
        self.author = properties["Sender"]
        self.biome = mp.Biome(properties["Biome"])
        self.difficulty = properties["Difficulty"] # difficulty name (uppercase)
        self.gamemode = mp.Gamemode(properties["Mode"]) # the gamemode id
        self.build = properties["Build"] # the minecraft version the player uses

class CommandResponseContext(BotContext):
    def __init__(self, success, message, content, *ctx_args, **ctx_kwargs):
        super().__init__(*ctx_args, **ctx_kwargs)
        self.success = success
        self.response = message
        self.content = content

class UnknownCommandContext(BotContext):
    def __init__(self, command, *ctx_args, **ctx_kwargs):
        super().__init__(*ctx_args, **ctx_kwargs)
        self.command = command

class MissingArgumentsContext(BotContext):
    def __init__(self, command, arguments, *ctx_args, **ctx_kwargs):
        super().__init__(*ctx_args, **ctx_kwargs)
        self.command = command
        self.arguments = arguments

class WebsocketContext:
    def __init__(self, host, port):
        self.host = host
        self.port = port