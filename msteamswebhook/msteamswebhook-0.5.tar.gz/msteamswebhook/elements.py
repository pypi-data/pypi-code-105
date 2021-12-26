from msteamswebhook.base import *
from typing import Union, List, Dict

class ActionSet(ToggleableItem):
    _type = "ActionSet"

    def __init__(self,
    actions: List[ Action ],
    #Element
    fallback:  Union[Element, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None):
        super().__init__(fallback, height, separator, spacing, id, isVisible)
        self._actions = actions

class ColumnSet(ToggleableItem):
    _type = "ColumnSet"

    def __init__(self,
    columns: List[Column]=[],
    selectAction: SelectAction=None,
    style: ContainerStyle=None,
    bleed: bool=None,
    minHeight: str=None,
    horizontalAlignment: HorizontalAlignment=None,
    #Element
    fallback:  Union[Element, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None,
    additionalProperties: Dict=None):
        super().__init__(fallback, height, separator, spacing, id, isVisible)
        self._columns = columns
        self._selectAction = selectAction
        self._style = style
        self._bleed = bleed
        self._minHeight = minHeight
        self._horizontalAlignment = horizontalAlignment
        self._columns = columns
        self._selectAction = selectAction
        self._style = style
        self._bleed = bleed
        self._minHeight = minHeight
        self._horizontalAlignment = horizontalAlignment
        self._additionalProperties = additionalProperties

class Container(ToggleableItem):
    _type = "Container"

    def __init__(self,
    items: List[Element],
    selectAction: SelectAction=None,
    style: ContainerStyle=None,
    verticalContentAlignment: VerticalContentAlignment=None,
    bleed: bool=None,
    backgroundImage: Union[str, BackgroundImage]=None,
    minHeight: str=None,
    horizontalAlignment: HorizontalAlignment=None,
    #Element
    fallback:  Union[Element, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None,
    additionalProperties: Dict=None):
        super().__init__(fallback, height, separator, spacing, id, isVisible)
        self._items = items
        self._selectAction = selectAction
        self._style = style
        self._verticalContentAlignment = verticalContentAlignment
        self._bleed = bleed
        self._backgroundImage = backgroundImage
        self._minHeight = minHeight
        self._horizontalAlignment = horizontalAlignment
        self._additionalProperties = additionalProperties

class FactSet(ToggleableItem):
    _type = "FactSet"

    def __init__(self,
    facts: List[Fact],
    #Element
    fallback:  Union[Element, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None):
        super().__init__(fallback, height, separator, spacing, id, isVisible)
        self._facts = facts

class Image(ToggleableItem):
    _type = "Image"

    def __init__(self,
    url: str,
    altText: str=None,
    backgroundColor: str=None,    
    horizontalAlignment: HorizontalAlignment=None,
    selectAction: SelectAction=None,
    size: ImageSize=None,
    style: ImageStyle=None,
    width: str=None,
    fallback: Union[Element, FallbackOption] = None,
    height: Union[str, BlockElementHeight]=None,
    separator: bool=None,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None,
    additionalProperties: Dict=None
    ):
        super().__init__(fallback, height, separator, spacing, id, isVisible)
        self._url = url
        self._altText = altText
        self._backgroundColor = backgroundColor
        self._horizontalAlignment = horizontalAlignment
        self._selectAction = selectAction
        self._size = size
        self._style = style
        self._width = width
        self._additionalProperties = additionalProperties

class ImageSet(ToggleableItem):
    _type = "ImageSet"

    def __init__(self,
    images: List[Image],
    imageSize: ImageSize=None,
    #Element
    fallback:  Union[Element, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None):
        super().__init__(fallback, height, separator, spacing, id, isVisible)
        self._images = images
        self._imageSize = imageSize

class Media(ToggleableItem):
    _type = "Media"

    def __init__(self,
    sources: List[MediaSource],
    poster: str=None,
    altText: str=None,
    #Element
    fallback:  Union[Element, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None):
        super().__init__(fallback, height, separator, spacing, id, isVisible)
        self._sources = sources
        self._poster = poster
        self._altText = altText

class RichTextBlock(ToggleableItem):
    _type = "RichTextBlock"

    def __init__(self,
    inlines: List[ Union[str, Inline] ],
    horizontalAlignment: HorizontalAlignment=None,
    #Element
    fallback:  Union[Element, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=False,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None):
        super().__init__(fallback, height, separator, spacing, id, isVisible)
        self._inlines = inlines
        self._horizontalAlignment = horizontalAlignment

class TextBlock(ToggleableItem):
    _type = "TextBlock"

    def __init__(self,
    text: str,
    color: Colors=None,
    fontType: FontType=None,
    horizontalAlignment: HorizontalAlignment=None,
    isSubtle: bool=None,
    maxLines: int=None,
    size: FontSize=None,
    weight: FontWeight=None,
    wrap: bool=None,
    #Element
    fallback:  Union[Element, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    id: str=None,
    isVisible: bool=None):
        super().__init__(fallback, height, separator, spacing, id, isVisible)
        self._text = text
        self._color = color
        self._fontType = fontType
        self._horizontalAlignment = horizontalAlignment
        self._isSubtle = isSubtle
        self._maxLines = maxLines
        self._size = size
        self._weight = weight
        self._wrap = wrap

