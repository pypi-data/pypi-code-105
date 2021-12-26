from msteamswebhook.base import *
from typing import List

@adcard()
class AdaptiveCard:
    _schema = "https://adaptivecards.io/schemas/adaptive-card.json"
    _type = "AdaptiveCard"
    _version = "1.2"

    def __init__(self,    
    body: List[ Element ],
    actions: List[ Action ]=[],
    selectAction: SelectAction=None,
    fallbackText: str=None,
    backgroundImage: str=None,
    minHeight: str=None,
    speak: str=None,
    lang: str=None,
    verticalContentAlignment: str=None):
        self._body = body
        self._actions = actions
        self._selectAction = selectAction
        self._fallbackText = fallbackText
        self._backgroundImage = backgroundImage
        self._minHeight = minHeight
        self._speak = speak
        self._lang = lang
        self._verticalContentAlignment = verticalContentAlignment   
        self._msteams={"width": "Full"}
