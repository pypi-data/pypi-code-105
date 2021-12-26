from msteamswebhook.base import *
from msteamswebhook.AdaptiveCard import AdaptiveCard

class Action_OpenUrl(SelectAction):
    _type = "Action.OpenUrl"

    def __init__(self,
    url: str,
    #Action
    title: str=None,
    iconUrl: str=None,
    style: ActionStyle=None,
    fallback: Union[IAction, FallbackOption]=None):
        super().__init__(title, iconUrl, style, fallback)
        self._url = url
    
class Action_ShowCard(Action):
    _type = "Action.ShowCard"

    def __init__(self,
    card: AdaptiveCard=None,
    #Action
    title: str=None,
    iconUrl: str=None,
    style: ActionStyle=None,
    fallback: Union[IAction, FallbackOption]=None):
        super().__init__(title, iconUrl, style, fallback)
        self._card = card

class Action_Submit(SelectAction):
    _type = "Action.Submit"

    def __init__(self,
    data: Union[str, object]=None,
    associatedInputs: AssociatedInputs=None,
    #Action
    title: str=None,
    iconUrl: str=None,
    style: ActionStyle=None,
    fallback: Union[IAction, FallbackOption]=None):
        super().__init__(title, iconUrl, style, fallback)
        self._data = data
        self._associatedInputs = associatedInputs

class Action_ToggleVisibility(SelectAction):
    _type = "Action.ToggleVisibility"

    def __init__(self,
    targetElements: List[ Union[str, TargetElement] ],
    #Action
    title: str=None,
    iconUrl: str=None,
    style: ActionStyle=None,
    fallback: Union[IAction, FallbackOption]=None):
        super().__init__(title, iconUrl, style, fallback)
        self._targetElements = targetElements

