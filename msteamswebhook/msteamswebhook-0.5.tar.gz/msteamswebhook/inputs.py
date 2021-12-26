from msteamswebhook.base import *
from typing import Union, List, Dict

class Input_ChoiceSet(Input):
    _type = "Input.ChoiceSet"

    def __init__(self,
        id: str,
        choices: List[Input_Choice],
        isMultiSelect: bool=None,
        style: ChoiceInputStyle=None,
        value: str=None,
        placeholder: str=None,
        wrap: bool=None,
        #Input 
        errorMessage: str=None,
        isRequired: bool=None,
        label: str=None,
        fallback: Union[IElement, FallbackOption]=None,
        height: BlockElementHeight=None,
        separator: bool=None,
        spacing: Spacing=None,
        isVisible: bool=None,
        additionalProperties: Dict=None
    ):
        super().__init__(id, errorMessage, isRequired, label, fallback, height, separator, spacing, isVisible, additionalProperties)
        self._choices = choices
        self._isMultiSelect = isMultiSelect
        self._style = style
        self._value = value
        self._placeholder = placeholder
        self._wrap = wrap

class Input_Date(Input):
    _type = "Input.Date"
    
    def __init__(self,
    id: str,
    max: str=None,
    min: str=None,
    placeholder: str=None,
    value: str=None,
    #Input 
    errorMessage: str=None,
    isRequired: bool=None,
    label: str=None,
    fallback: Union[IElement, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    isVisible: bool=None,
    additionalProperties: Dict=None
    ):
        super().__init__(id, errorMessage, isRequired, label, fallback, height, separator, spacing, isVisible, additionalProperties)
        self._max = max
        self._min = min
        self._placeholder = placeholder
        self._value = value

class Input_Number(Input):
    _type = "Input.Number"
    
    def __init__(self, 
    id: str,
    max: int=None,
    min: int=None,
    placeholder: str=None,
    value: int=None,
    #Input 
    errorMessage: str=None,
    isRequired: bool=None,
    label: str=None,
    fallback: Union[IElement, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    isVisible: bool=None,
    additionalProperties: Dict=None
    ):
        super().__init__(id, errorMessage, isRequired, label, fallback, height, separator, spacing, isVisible, additionalProperties)
        self._max = max
        self._min = min
        self._placeholder = placeholder
        self._value = value

class Input_Text(Input):
    _type = "Input.Text"

    def __init__(self,
    id: str,
    isMultiline: bool=None,
    maxLength: int=None,
    placeholder: str=None,
    regex: str=None,
    style: TextInputStyle=None,
    inlineAction: SelectAction=None,
    value: str=None,
    #Input 
    errorMessage: str=None,
    isRequired: bool=None,
    label: str=None,
    fallback: Union[IElement, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    isVisible: bool=None,
    additionalProperties: Dict=None
    ):
        super().__init__(id, errorMessage, isRequired, label, fallback, height, separator, spacing, isVisible, additionalProperties)
        self._isMultiline = isMultiline
        self._maxLength = maxLength
        self._placeholder = placeholder
        self._regex = regex
        self._style = style
        self._inlineAction = inlineAction
        self._value = value

class Input_Time(Input):
    _type = "Input.Time"

    def __init__(self,
    id: str,
    max: str=None,
    min: str=None,
    placeholder: str=None,
    value: str=None,
    #Input 
    errorMessage: str=None,
    isRequired: bool=None,
    label: str=None,
    fallback: Union[IElement, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    isVisible: bool=None,
    additionalProperties: Dict=None
    ):
        super().__init__(id, errorMessage, isRequired, label, fallback, height, separator, spacing, isVisible, additionalProperties)
        self._max = max
        self._min = min
        self._placeholder = placeholder
        self._value = value

class Input_Toggle(Input):
    _type = "Input.Toggle"

    def __init__(self,
    id: str,
    title: str,
    value: str=None,
    valueOff: str=None,
    valueOn: str=None,
    wrap: bool=None,
    #Input 
    errorMessage: str=None,
    isRequired: bool=None,
    label: str=None,
    fallback: Union[IElement, FallbackOption]=None,
    height: BlockElementHeight=None,
    separator: bool=None,
    spacing: Spacing=None,
    isVisible: bool=None,
    additionalProperties: Dict=None
    ):
        super().__init__(id, errorMessage, isRequired, label, fallback, height, separator, spacing, isVisible, additionalProperties)
        self._title = title
        self._value = value
        self._valueOff = valueOff
        self._valueOn = valueOn
        self._wrap = wrap
