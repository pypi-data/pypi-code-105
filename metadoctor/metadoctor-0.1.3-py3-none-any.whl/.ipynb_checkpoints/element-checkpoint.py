#!/usr/bin/env python
# coding: utf-8

__all__ = [
    'BaseElement',
    'Element',
    'Anchor',
    'Header',
    'Div',
    'OL',
    'Ul',
    'FormField',
    'Fieldset',
    'Input',
    'Select',
    'TextArea',
    'Form',
    'Li',
    'Option',
    'DataList'
    ]

from abc import ABC 
from enum import Enum
from dataclasses import dataclass, field, MISSING
from typing import Optional, Union, Any, List, Dict, Tuple, TypeVar
from markupsafe import Markup

from metadoctor.enumeration import Variable 


is_defined = Variable.is_defined
exist = Variable.exist


HTML5 = '<!doctype html>'
HTML_LANG = '<html lang="pt">'
META_CHARSET = '<meta charset="utf-8">'
META_VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">'
BOOTSTRAP5_CSS = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">'
BOOTSTRAP5_JS = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>'
INPUT_STYLE = 'width: 100%; padding: 12px 20px; margin: 8px 0; display: inline-block; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
POSITIONAL_HTML_ELEMENT_ATTRIBUTES = 'required hidden disabled multiple readonly'.split()
KEYWORD_VALUE_HTML_ELEMENT_ATTRIBUTES = 'placeholder max min minlength maxlength step pattern'.split()



class BaseEnum(Enum):
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f'{type(self).__name__}.{self.name}'
    
    @classmethod
    def members(cls):
        return [m for m in cls.__members__.values()]
    
    
@dataclass 
class BaseElement(ABC):
    class TOF(BaseEnum):
        TRUE = 'true'
        FALSE = 'false'
    class YON(BaseEnum):
        YES = 'yes'
        NO = 'no'
    tag: str 
    pk: Optional[str] = None
    klass: Optional[str] = None
    style: Optional[str] = None
    title: Optional[str] = None
    accesskey: Optional[str] = None
    lang: Optional[str] = None
    hidden: Optional[bool] = None
    tabindex: Optional[int] = None
    contenteditable: Optional[TOF] = None
    spellcheck: Optional[TOF] = None
    draggable: Optional[TOF] = None
    translate: Optional[YON] = None
    data_attr: Optional[Tuple[str, str]] = None
    content: List[Union[str, 'BaseElement', None]] = field(default_factory=list)
    is_empty: bool = False 
    has_items: bool = False 
    has_options: bool = False 
    # Clipboard Events  
    oncopy: Optional[str] = None # Fires when the user copies the content of an element
    oncut: Optional[str] = None # Fires when the user cuts the content of an element
    onpaste: Optional[str] = None # Fires when the user pastes some content in an element
    # Drag Events
    ondrag: Optional[str] = None # Script to be run when an element is dragged
    ondragend: Optional[str] = None # Script to be run at the end of a drag operation
    ondragenter: Optional[str] = None # Script to be run when an element has been dragged to a valid drop target
    ondragleave: Optional[str] = None # Script to be run when an element leaves a valid drop target
    ondragover: Optional[str] = None # Script to be run when an element is being dragged over a valid drop target
    ondragstart: Optional[str] = None # Script to be run at the start of a drag operation
    ondrop: Optional[str] = None # Script to be run when dragged element is being dropped
    onscroll: Optional[str] = None # Script to be run when an element's scrollbar is being scrolled
        
    
        
    def __add__(self, other):
        assert isinstance(other, (str, BaseElement, Markup)), f'{type(self).__name__} can be added to str, BaseElemente or Markup instances only'
        other = other if isinstance(other, (str, Markup)) else str(other)
        return self.__html__() + other
    
    @property
    def _tag(self):
        return self.tag.lower()
    
    @property
    def _pk(self):
        return f'id="{self.pk}"' if self.pk else None 
    
    @property
    def _data_attr(self):
        return f'data-{self.data_attr[0]}="{self.data_attr[1]}"' if self.data_attr else None
                         
    @property        
    def _klass(self):
        return f'class="{self.klass}"' if self.klass else None 
            
    @property        
    def _style(self):
        return f'style="{self.style}"' if self.style else None 
                         
    @property        
    def _title(self):
        return f'title="{self.title}"' if self.title else None  
                         
    @property        
    def _accesskey(self):
        return f'accesskey="{self.accesskey}"' if self.accesskey else None 

    @property        
    def _tabindex(self):
        return f'tabindex="{self.tabindex}"' if self.tabindex else None 
                         
    @property        
    def _lang(self):
        if type(self) == HTML:
            return f'lang="{self.lang}"' if self.lang else f'lang="pt"' 
        return f'lang="{self.lang}"' if self.lang else None 
                         
    @property        
    def _hidden(self):
        return 'hidden' if self.hidden in [True, self.YON.YES, 'yes', self.TOF.TRUE, 'true'] else None  
                       
    @property        
    def _spellcheck(self):
        return 'spellcheck="true"' if self.spellcheck in [True, self.YON.YES, 'yes', self.TOF.TRUE, 'true'] else None  
    
    
    @property        
    def _draggable(self):
        return 'draggable="true"' if self.draggable in [True, self.YON.YES, 'yes', self.TOF.TRUE, 'true'] else None  

    @property        
    def _translate(self):
        return 'translate="yes"' if self.translate in [True, self.YON.YES, 'yes', self.TOF.TRUE, 'true'] else None  
    
    
    @property        
    def _contenteditable(self):
        return f'contenteditable="true"' if self.contenteditable in [True, self.YON.YES, 'yes', self.TOF.TRUE, 'true'] else None 
    
    def _global_attributes_str(self) -> str:
        return ' '.join(filter(lambda x: x != None, [
            self._pk, 
            self._klass, 
            self._style, 
            self._title, 
            self._accesskey, 
            self._tabindex, 
            self._lang, 
            self._hidden, 
            self._contenteditable,
            self._translate,
            self._spellcheck,
            self._draggable
        ]))
    
#     @classmethod
#     def parse_item(cls, item):
#         return str(Li(item))
        

    def compile_items(self):
        def parse_item(item):
            return Li(str(item))
        result = []
        if isinstance(self.content, (tuple, list)):
            for item in self.content:
                result.append(parse_item(item))
        elif isinstance(self.content, str):
            result.append(parse_item(item))
        return result
    
    
    def compile_options(self):
        def parse_option(value, option, selected=None, label=None):
            return Option(value=value, content=option, selected=None, label=label) 
        result = []
        if isinstance(self.content, (tuple, list)):
            for item in self.content:
                if isinstance(item, BaseEnum):
                    result.append(parse_option(item.name, item.value))
                elif isinstance(item, (tuple, list)):
                    result.append(parse_option(item[0], item[1]))
                elif isinstance(item, str):
                    result.append(parse_option(item, item))
        return result 
    
    
    def compile_text(self):
        if isinstance(self.content, str):
            return self.content 
        elif isinstance(self.content, (tuple, list)):
            return ''.join([str(x) for x in self.content])
            
    
    @property        
    def _content(self) -> str:
        if self.has_options:
            return ''.join([str(x) for x in self.compile_options()])
        elif self.has_items:
            return ''.join([str(x) for x in self.compile_items()])
        else:
            return self.compile_text()
#         result = []
#         if self.has_items:
#             for item in self.content:
#                 result.append(self.parse_item(str(item)))
#         elif self.has_options:
#             if isinstance(self.content, str):
#                 result.append(self.content)
#             elif isinstance(self.content, list):
#                 for item in self.content:
#                     result.append(
#                         self.parse_option(
#                             *item if isinstance(item, (tuple, list)) 
#                             else (item, item) if isinstance(item, str) 
#                             else (item.name, item.value) if isinstance(item, Enum) 
#                             else (str(item), str(item))))
#         elif self.is_empty:
#             return ''
#         else:
#             if isinstance(self.content, str):
#                 result.append(self.content)
#             elif isinstance(self.content, (tuple, list)):
#                 for item in self.content:
#                     result.append(str(item))   
#         return ''.join(result)
    
                         
    def _local_attributes_str(self) -> str:
        return '' 

    def _attributes(self) -> str:
        return ' '.join([x for x in [self._global_attributes_str(), self._local_attributes_str()] if len(x) > 0])
        
    def _repr_html_(self):
        if self.is_empty:
            return f'<{" ".join([self._tag, self._attributes()])}>'
        return f'<{" ".join([self._tag, self._attributes()])}>{self._content}</{self._tag}>'
    
    def __str__(self):
        return self._repr_html_()  
    
    def __html__(self):
        return Markup(self._repr_html_())  
    

@dataclass 
class HTML(BaseElement):
    tag: str = 'HTML' 
    
        
    def __repr_html__(self):
        text = HTML5
        text += f'<html lang="{self.lang or "pt"}">'


@dataclass
class Body(BaseElement):
    onafterprint: Optional[str] = None # Script to be run after the document is printed
    onbeforeprint: Optional[str] = None # Script to be run before the document is printed
    onbeforeunload: Optional[str] = None # Script to be run when the document is about to be unloaded
    onerror: Optional[str] = None # Script to be run when an error occurs
    onhashchange: Optional[str] = None # Script to be run when there has been changes to the anchor part of the a URL
    onload: Optional[str] = None # Fires after the page is finished loading
    onmessage: Optional[str] = None # Script to be run when the message is triggered
    onoffline: Optional[str] = None # Script to be run when the browser starts to work offline
    ononline: Optional[str] = None # Script to be run when the browser starts to work online
    onepagehide: Optional[str] = None # Script to be run when a user navigates away from a page
    onpageshow: Optional[str] = None # Script to be run when a user navigates to a page
    onpopstate: Optional[str] = None # Script to be run when the window's history changes
    onresize: Optional[str] = None # Fires when the browser window is resized
    onstorage: Optional[str] = None # Script to be run when a Web Storage area is updated
    onunload: Optional[str] = None # Fires once a page has unloaded (or the browser window has been closed)
        
    def _local_attributes_str(self) -> str:
        result = []
        if self.onafterprint: result.append(f'onafterprint="{self.onafterprint}"')
        if self.onbeforeprint: result.append(f'onbeforeprint="{self.onbeforeprint}"')
        if self.onbeforeunload: result.append(f'onbeforeunload="{self.onbeforeunload}"')
        if self.onerror: result.append(f'onerror="{self.onerror}"')
        if self.onload: result.append(f'onload="{self.onload}"')
        if self.onmessage: result.append(f'onmessage="{self.onmessage}"')
        if self.onoffline: result.append(f'onoffline="{self.onoffline}"')
        if self.ononline: result.append(f'ononline="{self.ononline}"')
        if self.onepagehide: result.append(f'onepagehide="{self.onepagehide}"')
        if self.onpageshow: result.append(f'onpageshow="{self.onpageshow}"')
        if self.onpopstate: result.append(f'onpopstate="{self.onpopstate}"')
        if self.onresize: result.append(f'onresize="{self.onresize}"')
        if self.onstorage: result.append(f'onstorage="{self.onstorage}"')
        if self.onunload: result.append(f'onunload="{self.onunload}"')            
        return ' '.join(result)
    

@dataclass 
class Element(BaseElement):
    pass 


@dataclass 
class Form(BaseElement):
    tag: str = 'FORM'
    action: str = '.'
    # events 
    onblur: Optional[str] = None # Fires the moment that the element loses focus
    onchange: Optional[str] = None # Fires the moment when the value of the element is changed
    oncontextmenu: Optional[str] = None # Script to be run when a context menu is triggered
    onfocus: Optional[str] = None # Fires the moment when the element gets focus
    oninput: Optional[str] = None # Script to be run when an element gets user input
    oninvalid: Optional[str] = None # Script to be run when an element is invalid
    onreset: Optional[str] = None # Fires when the Reset button in a form is clicked
    onsearch: Optional[str] = None # Fires when the user writes something in a search field (for <input="search">)
    onselect: Optional[str] = None # Fires after some text has been selected in an element
    onsubmit: Optional[str] = None # Fires when a form is submitted
    onblur: Optional[str] = None # 
        
    class Target(BaseEnum):
        BLANK = '_blank' # The response is displayed in a new window or tab
        TOP = '_top' # The response is displayed in the full body of the window
        SELF = '_self' # The response is displayed in the current window
        PARENT = '_parent' # The response is displayed in the parent frame
        FRAMENAME = 'framaneme' # The response is displayed in a named iframe
        
    target: Optional[Target] = None
        
    class Method(BaseEnum):
        GET = 'get'
        POST = 'post'
        
    method: Method = Method.GET
        
    class Autocomplete(BaseEnum):
        ON = 'on'
        OFF = 'off'
        
    autocomplete: Optional[Autocomplete] = None
    novalidate: bool = False
        
    class Rel(BaseEnum):
        EXTERNAL = 'external' # Specifies that the referenced document is not a part of the current site
        HELP = 'help' # Links to a help document
        LICENCE = 'licence' # Indicates that the main content of the current document is covered by the copyright license described by the referenced document.
        NEXT = 'next' # Indicates that the current document is a part of a series and that the next document in the series is the referenced document.
        NOFOLLOW = 'nofollow' # Links to an unendorsed document, like a paid link. Indicates that the current document's original author or publisher does not endorse the referenced document.
        NOOPENER = 'noopener' # Creates a top-level browsing context that is not an auxiliary browsing context if the hyperlink would create either of those, 
                              # to begin with (i.e., has an appropriatetargetattribute value).
        NOREFERRER = 'noreferrer' # Specifies that the browser should not send a HTTP referrer header if the user follows the hyperlink. No Referer header will be included. 
                                  # Additionally, has the same effect as noopener.
        OPENER = 'opener' # Creates an auxiliary browsing context if the hyperlink would otherwise create a top-level browsing context that 
                          # is not an auxiliary browsing context (i.e., has "_blank" as target attribute value).
        PREV = 'prev' # Indicates that the current document is a part of a series and that the previous document in the series is the referenced document.
        SEARCH = 'search' # Gives a link to a resource that can be used to search through the current document and its related pages.
    
    rel: Optional[Rel] = None
    
    def _local_attributes_str(self):
        data = [
            f'action="{self.action}" method="{self.method}"',
            f'autocomplete="{self.autocomplete}"' if self.autocomplete else None,
            f'rel="{self.rel}"' if self.rel else None,
            f'target="{self.target}"' if self.target else None,
            f'novalidate' if self.novalidate else None,
            ]
        return ' '.join(filter(lambda x: x != None, data))
    
    @property
    def _content(self):
        text = super()._content 
        text += str(Input(input_type=Input.Type('submit')))
        return text


@dataclass 
class Anchor(Element):
    tag: str = 'A' 
    href: str =  field(default=...)

    def _local_attributes_str(self):
        return f'href="{self.href}"'
    
    @property
    def _content(self):
        return self.content if isinstance(self.content, str) else ''.join(self.content)
    

@dataclass 
class Header(Element):
    tag: int
    
    @property
    def _tag(self):
        assert isinstance(self.tag, int)
        assert self.tag > 0
        assert self.tag < 7
        return 'h' + str(self.tag)
    

@dataclass 
class Fieldset(Element):
    tag: str = 'FIELDSET'
    legend: Optional[str] = None
        
    @property
    def _klass(self):
        klass = super()._klass
        return f'class="{klass} row"' if klass else 'class="row"'
    
    @property
    def _content(self):
        if isinstance(self.content, str):
            return self.content
        elif isinstance(self.content, (tuple, list)):
            return ''.join([str(x) for x in self.content])
        return super()._content
    
    def _repr_html_(self):
        legend = None
        if self.legend:
            legend = f'<legend >{self.legend} </legend>'
        if legend:
            fieldset = f'<{" ".join([self._tag, self._attributes()])}>{legend}{self._content}</{self._tag}>'
        else:
            fieldset = f'<{" ".join([self._tag, self._attributes()])}>{self._content}</{self._tag}>'
        return fieldset
    

@dataclass 
class Li(Element):
    tag: str = 'LI'

    
@dataclass 
class Option(Element):
    tag: str = 'OPTION'
    value: Optional[str] = None
    label: Optional[str] = None
    selected: bool = False
    optgroup: Optional[str] = None
        
    @property 
    def _content(self):
        return self.content.value if isinstance(self.content, BaseEnum) else str(self.content)
        
        
    def _attributes(self):
        value = self.value or self._content
        value = f'value="{value}"'
        if self.selected: value += ' selected'
        return value 


@dataclass 
class Ol(Element):
    tag: str = 'OL'
    has_items: bool = True


@dataclass 
class Ul(Element):
    tag: str = 'UL'
    has_items: bool = True
    
    
@dataclass 
class Div(Element):
    tag: str = 'DIV'
        


@dataclass
class FormField(Element):
    label: Optional[str] = None
    required: Optional[bool] = None
    readonly: Optional[bool] = None
    disabled: Optional[bool] = None
    hidden: Optional[bool] = None
    max: Optional[bool] = None
    min: Optional[bool] = None
    minlength: Optional[bool] = None
    maxlength: Optional[bool] = None
    step: Optional[bool] = None
    pattern: Optional[bool] = None
    placeholder: Optional[str] = None
    name: Optional[str] = None
    value: Optional[str] = None


    class Type(BaseEnum):
        TEXT='text'
        DATETIME_LOCAL='datetime-local'
        DATE='date'
        SUBMIT='submit'
        NUMBER='number'
        WEEK='week'
        COLOR='color'
        IMAGE='image'
        MONTH='month'
        RANGE='range'
        BUTTON="button"
        CHECKBOX="checkbox"
        EMAIL="email"
        FILE="file"
        HIDDEN="hidden"
        PASSWORD="password"
        RADIO="radio"
        RESET="reset"
        SEARCH="search"
        TEL="tel"
        TIME="time"
        URL="url"

        def __str__(self):
            return f'type="{self.value}"'
        
    input_type: Optional[Type] = None
    
    @property        
    def _klass(self):
        return f'class="{self.klass} form-control form-field"' if self.klass else 'class="form-control form-field"' 
    
    
    def _local_attributes_str(self):
        result = []
        if self.input_type:
            result.append(f'type="{self.input_type}"')
        if self.required:
            result.append('required')
        if self.readonly:
            result.append('readonly')
        if self.disabled:
            result.append('disabled')
        if self.hidden:
            result.append('hidden')
        if self.max:
            result.append(f'max="{self.max}"')
        if self.min:
            result.append(f'min="{self.min}"')
        if self.minlength:
            result.append(f'minlength="{self.minlength}"')
        if self.maxlength:
            result.append(f'maxlength="{self.maxlength}"')
        if self.step:
            result.append(f'step="{self.step}"')
        if self.pattern:
            result.append(f'pattern="{self.pattern}"')
        if self.value and not type(self) == Select:
            result.append(f'value="{self.value}"')
        return ' '.join(result) 
            
    
    @property
    def _pk(self):
        if self.pk:
            return f'id="{self.pk}" name="{self.name or self.pk}"'
        return
    
    def _repr_html_(self):
        field_wraper = lambda: f'<{" ".join([self._tag, self._attributes()])}>{self._content}</{self._tag}>'
        html = lambda: f'<label for="{self.pk}" class="form-label">{self.label or self.pk} {field_wraper()}</label>'.replace('</input>','')
        return html()
        
#         label = None
#         if self.label:
#             if self.pk:
#                 label = f'<label for="{self.pk}" class="form-label">{self.label} </label>'
#             else:
#                 label = f'<label class="form-label">{self.label} </label>'
#         if self.is_empty:
#             if label:
#                 htmlfield = f'{label}<{" ".join([self._tag, self._attributes()])}>'
#             else:
#                 htmlfield = f'<{" ".join([self._tag, self._attributes()])}>'
#         else:
#             if label:
#                 htmlfield = f'{label}<{" ".join([self._tag, self._attributes()])}>{self._content}</{self._tag}>'
#             else:
#                 htmlfield = f'<{" ".join([self._tag, self._attributes()])}>{self._content}</{self._tag}>'
#         return htmlfield
    

@dataclass 
class Select(FormField):
    tag: str = 'SELECT'
    has_options: bool = True
    input_type: Optional[str] = None
    form: Optional[str] = None # the form id
    multiple: Optional[str] = None
    size: Optional[int] = None
        
    def _attributes(self):
        result = [super()._attributes()]
        if self.form:
            result.append(f'form="{self.form}"')
        if self.multiple:
            result.append(self.multiple)
        if self.size:
            result.append(f'size="{self.size}"')
        
        return ' '.join(result)
    
    
@dataclass 
class TextArea(FormField):
    tag: str = 'TEXTAREA'
    
    
@dataclass 
class Input(FormField):
    tag: str = 'INPUT'
    is_empty: str = True
    list: Optional[str] = None
    
    def __post_init__(self):
        if self.input_type:
            self.input_type = self.Type(self.input_type)
    
    def _local_attributes_str(self):
        return ' '.join(filter(
            lambda x: x != None,
            [
                str(self.Type('text')) if not self.input_type else str(self.input_type),
                f'list="{self.list}"' if self.list else None
            ]
        ))
    

    
    
@dataclass 
class DataList(FormField):
    tag: str = 'INPUT'
    has_options: bool = True
    input_type: Optional[str] = None
    
    @property
    def list_name(self):
        return f'{self.pk}List'
    
    def _local_attributes_str(self):
        text = super()._local_attributes_str()
        text += f' list="{self.list_name}"'
        return text 

    
    @property        
    def _content(self) -> str:
        datalist = lambda options: f'<datalist id="{self.list_name}">{options}</datalist>'
        return datalist(super()._content)
    

    
        
@dataclass
class Media(Element):
    # events 
    onabort: Optional[str] = None # 
    oncanplay: Optional[str] = None # Script to be run when a file is ready to start playing (when it has buffered enough to begin)
    oncanplaythrough: Optional[str] = None # Script to be run when a file can be played all the way to the end without pausing for buffering
    oncuechange: Optional[str] = None # Script to be run when the cue changes in a <track> element
    ondurationchange: Optional[str] = None # Script to be run when the length of the media changes
    onemptied: Optional[str] = None # Script to be run when something bad happens and the file is suddenly unavailable (like unexpectedly disconnects)
    onended: Optional[str] = None # Script to be run when the media has reach the end (a useful event for messages like "thanks for listening")
    onerror: Optional[str] = None # Script to be run when an error occurs when the file is being loaded
    onloadeddata: Optional[str] = None # Script to be run when media data is loaded
    onloadedmetadata: Optional[str] = None # Script to be run when meta data (like dimensions and duration) are loaded
    onloadstart: Optional[str] = None # Script to be run just as the file begins to load before anything is actually loaded
    onpause: Optional[str] = None # Script to be run when the media is paused either by the user or programmatically
    onplay: Optional[str] = None # Script to be run when the media is ready to start playing
    onplaying: Optional[str] = None # Script to be run when the media actually has started playing
    onprogress: Optional[str] = None # Script to be run when the browser is in the process of getting the media data
    onratechange: Optional[str] = None # Script to be run each time the playback rate changes (like when a user switches to a slow motion or fast forward mode)
    onseeked: Optional[str] = None # Script to be run when the seeking attribute is set to false indicating that seeking has ended
    onseeking: Optional[str] = None # Script to be run when the seeking attribute is set to true indicating that seeking is active
    onstalled: Optional[str] = None # Script to be run when the browser is unable to fetch the media data for whatever reason
    onsuspend: Optional[str] = None # Script to be run when fetching the media data is stopped before it is completely loaded for whatever reason
    ontimeupdate: Optional[str] = None # Script to be run when the playing position has changed (like when the user fast forwards to a different point in the media)
    onvolumechange: Optional[str] = None # Script to be run each time the volume is changed which (includes setting the volume to "mute")
    onwaiting: Optional[str] = None # Script to be run when the media has paused but is expected to resume (like when the media pauses to buffer more data)
        
        
    def _attributes(self):
        result = [super()._attributes()]
        if self.onabort: 
            result.append(f'onabort="{self.onboard}"')
        if self.oncanplay: 
            result.append(f'oncanplay="{self.oncanplay}"')
        if self.oncanplaythrough: 
            result.append(f'oncanplaythrough="{self.oncanplaythrough}"')
        if self.ondurationchange: 
            result.append(f'ondurationchange="{self.ondurationchange}"')
        if self.onerror: 
            result.append(f'onerror="{self.onerror}"')
        if self.onloadeddata: 
            result.append(f'onloadeddata="{self.onloadeddata}"')
        if self.onloadedmetadata: 
            result.append(f'onloadedmetadata="{self.onloadedmetadata}"')
        if self.onloadstart: 
            result.append(f'onloadstart="{self.onloadstart}"')
        if self.onpause: 
            result.append(f'onpause="{self.onpause}"')
        if self.onplay: 
            result.append(f'onplay="{self.onplay}"')
        if self.onplaying: 
            result.append(f'onplaying="{self.onplaying}"')
        if self.onprogress: 
            result.append(f'onprogress="{self.onprogress}"')
        if self.onratechange: 
            result.append(f'onratechange="{self.onratechange}"')
        if self.onseeked: 
            result.append(f'onseeked="{self.onseeked}"')
        if self.onseeking: 
            result.append(f'onseeking="{self.onseeking}"')
        if self.onstalled: 
            result.append(f'onstalled="{self.onstalled}"')
        if self.onsuspend: 
            result.append(f'onsuspend="{self.onsuspend}"')
        if self.ontimeupdate: 
            result.append(f'ontimeupdate="{self.ontimeupdate}"')
        if self.onvolumechange: 
            result.append(f'onvolumechange="{self.onvolumechange}"')
        if self.onwaiting: 
            result.append(f'onwaiting="{self.onwaiting}"')
        return ' '.join(result)
            

@dataclass
class Img(Media):
    tag: str = 'IMG'
        

@dataclass
class Audio(Media):
    tag: str = 'AUDIO'


@dataclass
class Embed(Media):
    tag: str = 'IMG'
        
        
@dataclass
class Object(Media):
    tag: str = 'OBJECT'

        
@dataclass
class Video(Media):
    tag: str = 'VIDEO'
