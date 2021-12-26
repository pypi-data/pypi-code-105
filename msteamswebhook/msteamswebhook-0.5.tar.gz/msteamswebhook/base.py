from enum import Enum
from typing import Union, List, Dict

def adcard():
    def wrapper(K):
        setattr(K, "get_element", get_element)
        return K
    return wrapper

def isFilled(value):
    if value == None:
        return False
    return True

def get_element(self):
    ret = {}
    if self == None:
        return ""
    if self.__class__ in [int, str, bool, dict]:
        return self
    for attr, value in self.__class__.__dict__.items():
        attr_name = attr[1:]
        if attr_name not in ["type", "schema", "version"]:
            continue
        ret[attr_name] = value
    for attr, value in self.__dict__.items():                
        if isFilled(value):
            if "_additionalProperties" == attr:
                for k,v in value.items():
                    ret[k] = v
                continue
            if value.__class__ in [int, str, bool]:
                ret[attr[1:]] = value
            elif value.__class__ == list:
                ret[attr[1:]] = [ get_element(v) for v in value ]
            elif value.__class__ == dict:
                ret[attr[1:]] = value
            elif issubclass(type(value), Enum):
                ret[attr[1:]] = value.name
            else:
                ret[attr[1:]] = value.get_element()
    return ret

##########################################################
class FallbackOption(Enum):
    drop = 1

class BlockElementHeight(Enum):
    auto = 1
    stretch = 2

class BlockElementHeight(Enum):
    auto = 1
    stretch = 2

class Spacing(Enum):
    default = 1
    none = 2
    small = 3
    medium = 4
    large = 5
    extraLarge = 6
    padding = 7

class ContainerStyle(Enum):
    default = 1
    emphasis = 2
    good = 3
    attention = 4
    warning = 5
    accent = 6

class HorizontalAlignment(Enum):
    left = 1
    center = 2
    right = 3

class VerticalContentAlignment(Enum):
    top = 1
    center = 2
    bottom = 3

class ActionStyle(Enum):
    default = 1
    positive = 2
    destructive = 3

class ChoiceInputStyle(Enum):
    compact = 1
    expanded = 2

class TextInputStyle(Enum):
    text = 1
    tel = 2
    url = 3
    email = 4

class AssociatedInputs(Enum):
    auto = 1
    none = 2

class ImageFillMode(Enum):
    cover = 1
    repeatHorizontally = 2
    repeatVertically = 3
    repeat = 4

class VerticalAlignment(Enum):
    top = 1
    center = 2
    bottom = 3

class ImageSize(Enum):
    auto = 1
    stretch = 2
    small = 3
    medium = 4
    large = 5

class ImageStyle(Enum):
    default = 1
    person = 2

class Colors(Enum):
    default = 1
    dark = 2
    light = 3
    accent = 4
    good = 5
    warning = 6
    attention = 7

class FontType(Enum):
    default = 1
    monospace = 2

class FontSize(Enum):
    default = 1
    small = 2
    medium = 3
    large = 4
    extraLarge = 5

class FontWeight(Enum):
    default = 1
    lighter = 2
    bolder = 3

##################################
@adcard()
class Item:
    def __init__(self, additionalProperties: Dict=None):
        self._additionalProperties = additionalProperties

@adcard()
class IAction:
    pass

class Action(IAction):
    def __init__(self,
    title: str=None,
    iconUrl: str=None,
    style: ActionStyle=None,
    fallback: Union[IAction, FallbackOption]=None):
        self._title = title
        self._iconUrl = iconUrl
        self._style = style
        self._fallback = fallback

class SelectAction(Action):
    def __init__(self,
    title: str=None,
    iconUrl: str=None,
    style: ActionStyle=None,
    fallback: Union[IAction, FallbackOption]=None):
        super().__init__(title, iconUrl, style, fallback)

@adcard()
class IElement:
    pass

class Element(IElement):
    def __init__(self,
    fallback: Union[IElement, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None):
        self._fallback = fallback
        self._height = height
        self._separator = separator
        self._spacing = spacing
        self._id = id
        self._isVisible = isVisible

class ToggleableItem(Element):
    def __init__(self,
    fallback: Union[Element, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None):
        super().__init__(fallback, height, separator, spacing, id, isVisible)

class Input(ToggleableItem):
    def __init__(self,
    id: str,
    errorMessage: str=None,
    isRequired: bool=None,
    label: str=None,
    fallback: Union[Element, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    isVisible: bool=None,
    additionalProperties: Dict=None
    ):
        super().__init__(fallback, height, separator, spacing, id, isVisible)
        self._id = id
        self._errorMessage = errorMessage
        self._isRequired = isRequired
        self._label = label
        self._additionalProperties = additionalProperties

@adcard()
class Inline:
    pass

######################

class TargetElement(Item):
    _type = "TargetElement"
    def __init__(self,
    elementId: str,
    isVisible: bool=None):
        self._elementId = elementId
        self._isVisible = isVisible

class BackgroundImage(Item):
    _type = "BackgroundImage"

    def __init__(self,
    url: str,
    fillMode: ImageFillMode=None,
    horizontalAlignment: HorizontalAlignment=None,
    verticalAlignment: VerticalAlignment=None):
        self._url = url
        self._fillMode = fillMode
        self._horizontalAlignment = horizontalAlignment
        self._verticalAlignment = verticalAlignment

class Column(ToggleableItem):
    _type = "Column"

    def __init__(self,
    fallback: Union[Element, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None,
    items: List[Element]=[],
    backgroundImage: str=None,
    bleed: bool=None,
    minHeight: str=None,
    selectAction: SelectAction=None,
    style: ContainerStyle=None,
    verticalContentAlignment: VerticalContentAlignment=None,
    width: Union[str, int]=None,
    additionalProperties: Dict=None):
        super().__init__(fallback, height, separator, spacing, id, isVisible)
        self._items = items
        self._backgroundImage = backgroundImage
        self._bleed = bleed
        self._minHeight = minHeight
        self._selectAction = selectAction
        self._style = style
        self._verticalContentAlignment = verticalContentAlignment
        self._width = width
        self._additionalProperties = additionalProperties

class Fact(Item):
    _type = "Fact"

    def __init__(self,
    title: str,
    value: str
    ):
        self._title = title
        self._value = value

class Input_Choice(Item):
    _type = "Input.Choice"
    
    def __init__(self, title, value):
        self._title = title
        self._value = value

class MediaSource(Item):
    _type = "MediaSource"

    def __init__(self,
    mimeType:str,
    url:str
    ):
        self._mimeType = mimeType
        self.url = url

class TextRun(Inline):
    _type = "TextRun"

    def __init__(self,
    text: str,
    color: Colors=None,
    fontType: FontType=None,
    highlight: bool=None,
    isSubtle: bool=None,
    italic: bool=None,
    selectAction: SelectAction=None,
    size: FontSize=None,
    strikethrough: bool=None,
    underline: bool=None,
    weight: FontWeight=None
    ):
        self._text = text
        self._color = color
        self._fontType = fontType
        self._highlight = highlight
        self._isSubtle = isSubtle
        self._italic = italic
        self._selectAction = selectAction
        self._size = size
        self._strikethrough = strikethrough
        self._underline = underline
        self._weight = weight
