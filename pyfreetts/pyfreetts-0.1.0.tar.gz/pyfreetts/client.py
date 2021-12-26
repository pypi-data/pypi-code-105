from sqlite3 import Connection
from tempfile import TemporaryDirectory
from typing import Dict, Any, Tuple, List
from .const import GET_VOICES_BY_LANGUAGE, INIT_DATABASE, INLINE_OPTION
import json


def get_payload(voice: Tuple[str, str, str, int], text):
    retval1 = (
        ("Language", voice[1]),
        ("Voice", voice[0]),
        ("TextMessage", text),
        ("id", voice[0]),
        ("type", "1"),
    )
    retval2 = (
        ("Language", voice[1]),
        ("Voice", voice[0]),
        ("TextMessage", text),
        ("type", "0"),
    )
    if voice[3] == 1:
        return retval1
    else:
        return retval2


def get_voice_with_index(
    voices: List[Tuple[str, str, str, int]], index: int
) -> Tuple[str, str, str, int]:
    return voices[index - 1]


def choice_voice(voices: List[Tuple[str, str, str, int]]) -> Tuple[str, str, str, int]:
    __choice__ = 0
    __count__ = 0
    for voice in voices:
        __count__ += 1
        __type__ = "SAPI5" if voice[3] == 1 else "SAPI4"
        print(
            INLINE_OPTION.format(
                index=__count__, voice=voice[0], gender=voice[2], type=__type__
            )
        )
    while __choice__ == 0:
        try:
            __choice__ = int(input("Make your choice: "))
        except ValueError:
            print("Please input the numeric only.")
            __choice__ = 0
        else:
            if __choice__ not in range(1, __count__ + 1):
                print("Out of range! Please choice the valid option.")
                __choice__ = 0
    return voices[__choice__ - 1]


class API:
    """API of Text to Speech"""

    def __init__(self):
        self.__folder__ = TemporaryDirectory(dir="./")
        self.__filename__ = f"{self.__folder__.name}/temp.db"
        self.conn = Connection(self.__filename__)
        self.cur = self.conn.cursor()
        self.cur.executescript(INIT_DATABASE)
        self.conn.commit()

    def setup_voice(self, language: str, index: int = 0) -> None:
        self.cur.execute(GET_VOICES_BY_LANGUAGE, (language,))
        voices = self.cur.fetchall()
        if index in range(1, len(voices) + 1):
            self.__voice__ = get_voice_with_index(voices, index)
        else:
            print("All voices for your language: ")
            self.__voice__ = choice_voice(voices)

    def freetts_api(self, text: str) -> Dict[str, Any]:
        __query__ = get_payload(self.__voice__, text)
        __user__ = "Mozilla/5.0"
        __api__ = {
            "URL1": "https://freetts.com/Home/PlayAudio",
            "HEAD1": {
                "User-Agent": __user__,
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "X-Requested-With": "XMLHttpRequest",
                "Alt-Used": "freetts.com",
                "Connection": "keep-alive",
                "Referer": "https://freetts.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "TE": "trailers",
            },
            "PAYLOAD": __query__,
            "URL2": "https://freetts.com/audio/{path}",
            "HEAD2": {
                "authority": "freetts.com",
                "sec-ch-ua": "^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^",
                "sec-ch-ua-mobile": "?0",
                "upgrade-insecure-requests": "1",
                "user-agent": __user__,
                "accept": "*/*",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "no-cors",
                "sec-fetch-user": "?1",
                "sec-fetch-dest": "video",
                "accept-language": "en-US,en;q=0.9,vi;q=0.8",
                "referer": "https://freetts.com/audio/",
                "range": "bytes=0-",
            },
        }
        return __api__

    def voicemaker_api(self, text: str) -> Dict[str, Any]:
        __query__ = {
            "Engine": "standard",
            "Provider": "ai101",
            "SpeechName": self.__voice__[0],
            "OutputFormat": "mp3",
            "VoiceId": self.__voice__[0],
            "LanguageCode": self.__voice__[1],
            "SampleRate": "24000",
            "effect": "default",
            "master_VC": "advanced",
            "speed": "0",
            "master_volume": "2",
            "pitch": "0",
            "Text": text,
            "TextType": "text",
            "fileName": "",
        }
        __data__ = json.dumps(__query__)
        __user__ = "Mozilla/5.0 Gecko/20100101 Firefox/94.0"
        __accpt = "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,"
        __accept__ = __accpt + "application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5"
        __api__ = {
            "URL1": "https://voicemaker.in/voice/standard",
            "HEAD1": {
                "user-agent": __user__,
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.5",
                "referer": "https://voicemaker.in/",
                "content-type": "application/json; charset=utf-8",
                "csrf-token": "",
                "x-requested-with": "XMLHttpRequest",
                "origin": "https://voicemaker.in",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "te": "trailers",
            },
            "PAYLOAD": __data__,
            "URL2": "https://voicemaker.in{path}",
            "HEAD2": {
                "user-agent": __user__,
                "accept": __accept__,
                "accept-language": "en-US,en;q=0.5",
                "referer": "https://voicemaker.in/",
                "range": "bytes=0-",
                "sec-fetch-dest": "audio",
                "sec-fetch-mode": "no-cors",
                "sec-fetch-site": "same-origin",
                "te": "trailers",
            },
        }
        return __api__

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
