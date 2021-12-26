#!/usr/bin/env python
# coding: utf-8
'''BaseField Module'''

__all__ = [
    'BaseField',
    'RegularField',
    'EnumField', 
    'ReferenceField', 
    'DateTime', 
    'Text', 
    'SemicolonStrToList',
    'String', 
    'Choice',
    'Date',
    'Title',
    'Number', 
    'Integer',
    'Float',
    'Real', 
    'Key',
    'KeyData',
    'Array',
    'ArrayOfKeys',
    'DataField',
    'DataEnum'
    ]

import re
import datetime
from abc import ABC
from collections import ChainMap
from decimal import Decimal
from typing import Any
from markupsafe import Markup

from metadoctor import enumeration
from metadoctor import db
from metadoctor import element

BaseEnum = enumeration.BaseEnum
Variable = enumeration.Variable
is_defined = Variable.is_defined
exist = Variable.exist
process_undefined = lambda x: None if x in [None, Variable.UNDEFINED] else x

Fieldset = element.Fieldset
Input = element.Input
TextArea = element.TextArea
Select = element.Select
Li = element.Li
FormField = element.FormField
Div = element.Div
Option = element.Option
DataList = element.DataList

INPUT_STYLE = 'width: 100%; padding: 12px 20px; margin: 8px 0; display: inline-block; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
POSITIONAL_HTML_ELEMENT_ATTRIBUTES = 'required hidden disabled multiple readonly'.split()
KEYWORD_VALUE_HTML_ELEMENT_ATTRIBUTES = 'placeholder max min minlength maxlength step pattern'.split()
BASE_FIELD_CONFIG_KEYS = 'transform fsize fclass fstyle tag default factory exclude title description options'.split()

column_set = lambda x,y,z: f'col-sm-{x} col-md-{y} col-lg-{z}'


class BaseField(ABC):
    __positional__ = POSITIONAL_HTML_ELEMENT_ATTRIBUTES
    __keyvalue__ = KEYWORD_VALUE_HTML_ELEMENT_ATTRIBUTES
    __config__ = [*BASE_FIELD_CONFIG_KEYS, *POSITIONAL_HTML_ELEMENT_ATTRIBUTES, *KEYWORD_VALUE_HTML_ELEMENT_ATTRIBUTES]
    __config_defaults__ = dict(required=True, fsize=(12,6,3), tag='input', type='text')
    
    def __init__(self, 
                 *args, 
                 required=True,
                 hidden=Variable.UNDEFINED,
                 disabled=Variable.UNDEFINED,
                 multiple=Variable.UNDEFINED,
                 readonly=Variable.UNDEFINED,
                 placeholder=Variable.UNDEFINED,
                 max=Variable.UNDEFINED,
                 min=Variable.UNDEFINED,
                 minlength=Variable.UNDEFINED,
                 maxlength=Variable.UNDEFINED,
                 step=Variable.UNDEFINED,
                 pattern=Variable.UNDEFINED,
                 transform=Variable.UNDEFINED,
                 ftype='text',
                 fsize=(12,6,3),
                 fclass=Variable.UNDEFINED,
                 fstyle=INPUT_STYLE,
                 tag='input',
                 default=Variable.UNDEFINED,
                 factory=Variable.UNDEFINED,
                 exclude=Variable.UNDEFINED,
                 title=Variable.UNDEFINED,
                 description=Variable.UNDEFINED,
                 choices=Variable.UNDEFINED,
                 **kwargs) -> None:
        self.required=required
        self.hidden=hidden
        self.disabled=disabled
        self.multiple=multiple
        self.readonly=readonly
        self.placeholder=placeholder
        self.max=max
        self.min=min
        self.minlength=minlength
        self.maxlength=maxlength
        self.step=step
        self.pattern=pattern
        self.ftype=ftype
        self.fclass=fclass
        self.fsize=fsize
        self.fstyle=fstyle
        self.transform=transform
        self.tag=tag
        self.default=default
        self.factory=factory
        self.title=title
        self.exclude=exclude
        self.description=description
        self.choices=choices
        self.element=None
        
        if len(args) > 0:
            if type(args[0]) == str:
                self.owner = None
                self.owner_name = args[0]
            else:
                self.owner = args[0]
                self.owner_name = self.owner.__name__
        else:
            self.owner = Variable.UNDEFINED
            self.owner_name = Variable.UNDEFINED
                
    def initial_value(self):
        value = None
        if is_defined(self.factory):
            value = self.factory()
        elif is_defined(self.default):
            value = self.default
        if isinstance(value, BaseEnum):
            return value.name
        return value
    
    def submit_button(self):
        return str(Input(ftype='submit', style=SUBMIT_STYLE))

    def get_formfield_attrs(self, novalue=False) -> str:
        result = [f'id="{self.public_name}" name="{self.public_name}"']
        for k,v in vars(self).items():
            if is_defined(v):
                if k in self.__keyvalue__:
                    result.append(f'{k}="{v}"')
                elif k in self.__positional__ and v == True:
                    result.append(k)
        if is_defined(self.ftype):
            result.append(f'type="{self.ftype}"')
        if self.initial_value():
            if not novalue:
                result.append(f'value="{self.initial_value()}"')
        if is_defined(self.fstyle):
            result.append(f'style="{self.fstyle}"')
        if is_defined(self.fclass):
            result.append(f'class="{self.fclass} field"')
        else:
            result.append(f'class="field"')
        if is_defined(self.placeholder):
            result.append(f'placeholder="{self.placeholder}"')
        return ' '.join(result)
    
    
    def get_formfield(self, inner_text=None):
        label = lambda field: f'<label for="{self.public_name}" class="form-label">{self.title if is_defined(self.title) else self.description if is_defined(self.description) else self.public_name} {field}</label>'
        fd = ''
        if self.element == Input:
            fd = f'<input {self.get_formfield_attrs()}>'
        elif self.element == DataList:
            lt = f"{self.public_name}_list"
            fd = f'<input list="{lt}" {self.get_formfield_attrs(novalue=True)}><datalist id="{lt}">{inner_text or self.owner.choices(selected=self.initial_value())}</datalist>'
        elif self.element == Select:
            fd = f'<select {self.get_formfield_attrs(novalue=True)}>{inner_text or self.owner.choices(selected=self.initial_value())}</select>'
        elif self.element == TextArea:
            fd = f'<textarea {self.get_formfield_attrs()}>{inner_text or ""}</textarea>'
        return label(fd)
    
    
    def parse_in(self, obj):
        return getattr(obj, self.private_name)
    
    
    def parse_out(self, obj):
        return getattr(obj, self.public_name)

    
    def __set_name__(self, obj, name) -> None:
        self.public_name = name 
        self.private_name = f'_{name}'

    def pre_validation(self, obj, value) -> Any:
        if not exist(value):
            if is_defined(self.factory):
                value = self.factory()
            elif is_defined(self.default):
                value = self.default        
        return value
    
    def check_required(self, obj, value) -> None:
        if self.required == True:
            if not Variable.exist(value):
                raise ValueError(f'{type(obj).__name__}.{self.public_name} cannot be "{value}"')
            
    def post_validation(self, obj, value) -> Any:
        if exist(value):
            if is_defined(self.transform):
                if not issubclass(type(self), (EnumField, ReferenceField)):
                    return self.transform(value)
        return value
            
    def validate(self, obj, value) -> None:
        self.check_required(obj, value)
        if exist(value):
            if is_defined(self.min):
                if float(self.min) > value:    
                    raise ValueError(f'{self._name_} of {type(obj).__name__} is "{value}" and cannot be lesser then {self.min}')
            if is_defined(self.max):
                if float(self.max) < value:    
                    raise ValueError(f'{self._name_} of {type(obj).__name__} is "{value}" and cannot be greater then {self.max}')
            if is_defined(self.minlength):
                if float(self.minlength) > len(value):    
                    raise ValueError(f'{self._name_} of {type(obj).__name__} is "{value}" and cannot has length lesser then {self.minlength}')
            if is_defined(self.maxlength):
                if float(self.maxlength) < value:    
                    raise ValueError(f'{self._name_} of {type(obj).__name__} is "{value}" and cannot be greater then {self.maxlength}')
            if is_defined(self.pattern):
                if not re.match(self.pattern, value):
                    raise ValueError(f'{self._name_} of {type(obj).__name__} is "{value}" does not match {self.pattern}')
                    
                    
    def __set__(self, obj, value) -> None:
        pre = self.pre_validation(obj, value)
        self.validate(obj, pre)
        post = self.post_validation(obj, pre)
        setattr(obj, self.private_name, post)
        
    def parse(self, obj, value) -> Any:
        return value 
    
    def __get__(self, obj, owner=None) -> Any:
        value = getattr(obj, self.private_name)
        return self.parse(obj, value)
    

class  RegularField(BaseField):
    '''
    Used for direct access of database  
    '''
    pass 


class  EnumField(BaseField):
    '''
    Used for Enum classes lookup
    '''
    pass 

        
class ReferenceField(BaseField):
    '''
    Used to store the key and get access of database object
    '''
    pass 


class DateTime(RegularField):
    def __init__(self, **kwargs) -> None:
        super().__init__(datetime.datetime, **kwargs) 
        self.element = Input
        self.tag = 'input'
        self.ftype = 'datetime-local'
        
        
class Text(RegularField):
    def __init__(self, **kwargs) -> None:
        super().__init__(str, **kwargs) 
        self.element = TextArea
        self.tag = 'textarea'
        self.ftype = Variable.UNDEFINED

        
class SemicolonStrToList(RegularField):
    def __init__(self, **kwargs) -> None:
        super().__init__(str, **kwargs) 
        self.element = TextArea
        self.tag = 'textarea'
        self.ftype = Variable.UNDEFINED

    def parse(self, obj, value):
        trim = lambda x: x.strip()
        split = lambda x: x.split(";")
        process = lambda x: [i for i in sorted([trim(w) for w in split(x) if w not in ['', None]]) if i not in ['', None]]
        if value:
            return process(value)
        return value

    
class String(RegularField):
    
    def __init__(self,**kwargs) -> None:
        super().__init__(str, **kwargs) 
        self.element = Input

    def parse(self, obj, value):
        return value

        
class Choice(EnumField):
    '''
    Receive enumeration name to store in db. 
    The __get__ method return the enumeration member instance.
    '''
    
    def __init__(self,enum, **kwargs) -> None:
        super().__init__(enum, **kwargs) 
        self.element = Select
        self.tag = "select"
        self.ftype = Variable.UNDEFINED

        
    def  parse(self, obj, value):
        if value:
            return self.owner.get(value)
        return value 

    
class DataEnum(EnumField):
    def __init__(self,enum, **kwargs) -> None:
        super().__init__(enum, **kwargs) 
        self.element = DataList
        self.tag = "datalist"
        self.ftype = Variable.UNDEFINED
        self.options = ''.join([str(Option(value=key, content=option)) for key, option in self.owner.choices()])

    def  parse(self, obj, value):
        if value:
            return self.owner.get(value)
        return value 

    

class Date(RegularField):
    '''
    Receive date as a isoformat string to store in db. 
    The __get__ method return the datetime.date instance.
    '''
    
    def __init__(self, **kwargs) -> None:
        super().__init__(datetime.date, **kwargs) 
        self.tag = 'input'
        self.ftype = 'date'
        self.element = Input


    def  parse(self, obj, value):
        return datetime.date.fromisoformat(value) if isinstance(value, str) else value  



class Title(RegularField):
    '''
    Receive a string to store in db.
    The __get__ method return the db string formated to title().
    '''
    
    def __init__(self, **kwargs) -> None:
        super().__init__(str, **kwargs) 
        self.element = Input

    def parse(self, obj, value):
        if isinstance(value, str):
            return value.title()
        return value 

    
    
class Number(RegularField):
    '''
    Receive a string or number store in db.
    The __get__ method return as a float.
    '''
    def __init__(self, **kwargs) -> None:
        super().__init__(float, **kwargs) 
        self.element = Input
        self.tag = 'input'
        self.ftype = 'number'

    def parse(self, obj, value):
        return float(value) if isinstance(value, str) else value  

    
    
class Integer(RegularField):
    '''
    Receive a string or number store in db.
    The __get__ method return as a integer.
    '''
    def __init__(self,**kwargs) -> None:
        super().__init__(int, **kwargs) 
        self.element = Input
        self.tag = 'input'
        self.ftype = 'number'
        
    def parse(self, obj, value):
        return int(value) if isinstance(value, str) else value  

    
    
class Float(RegularField):
    '''
    Receive a string or number store in db.
    The __get__ method return as a float.
    '''
    def __init__(self, **kwargs) -> None:
        super().__init__(float, **kwargs) 
        self.element = Input
        self.tag = 'input'
        self.ftype = 'number'
        
    def parse(self, obj, value):
        return float(value) if isinstance(value, str) else value  

    
    
class Real(RegularField):
    '''
    Receive a string or number store in db.
    The __get__ method return as a Decimal.
    '''
    def __init__(self,**kwargs) -> None:
        super().__init__(Decimal, **kwargs) 
        self.element = Input
        self.tag = 'input'
        self.ftype = 'number'
                
    def parse(self, obj, value):
        if value:
            return Decimal(value)
        return value

    

class Array(RegularField):
    '''
    Receive a string to stored in db.
    The __get__ method parse the string to a list.
    '''
    def __init__(self,**kwargs) -> None:
        super().__init__(list, **kwargs) 
        self.element = Input
        self.tag = 'input'
                
    def parse(self, obj, value):
        if isinstance(value, str):
            value = [x.strip() for x in re.split('[;\n]', value)]
        elif isinstance(value, list):
            pass 
        else:
            value = [value]
        return value

    

class KeyData(ReferenceField):
    def __init__(self,table, db: db.AbstractDB, fields=None, **kwargs) -> None:
        super().__init__(table, **kwargs) 
        self.db = db
        self.element = Select
        self.tag = 'select'
        self.ftype = Variable.UNDEFINED
        self.table = self.owner_name
        self.fields = fields or list()
        
    def parse(self, obj, value):
        dbdata = self.db().sync_connect(self.table).get(str(value)) or dict()
        fields = self.fields if isinstance(self.fields, list) else [x.strip() for x in self.fields.split()]
        if fields:
            result = ChainMap({}, dbdata)
            result.update({"key": value, "table": self.table})
            for item in fields:
                result.update({item: result.get(item)})
            return result.maps[0]
        else:
            return dbdata
    
    
    
class DataField(ReferenceField):
    def __init__(self,table,  db: db.AbstractDB, fields=None, **kwargs) -> None:
        super().__init__(table, **kwargs) 
        self.db = db
        self.table = self.owner_name
        self.element = DataList
        self.tag = 'datalist'
        self.ftype = Variable.UNDEFINED
        self.fields = fields or list()
        
    def parse(self, obj, value):
        dbdata = self.db().sync_connect(self.table).get(str(value)) or dict()
        fields = self.fields if isinstance(self.fields, list) else [x.strip() for x in self.fields.split()]
        if fields:
            result = ChainMap({}, dbdata)
            result.update({"key": value, "table": self.table})
            for item in fields:
                result.update({item: result.get(item)})
            return result.maps[0]
        else:
            return dbdata
        
    
class Instance(ReferenceField):
    def __init__(self,table, db: db.AbstractDB, fields=None, **kwargs) -> None:
        super().__init__(table, **kwargs) 
        self.db = db
        self.element = Select
        self.tag = 'select'
        self.ftype = Variable.UNDEFINED
        self.table = self.owner_name
        self.fields = fields or list()
        
    def parse(self, obj, value):
        dbdata = self.db().sync_connect(self.table).get(str(value)) or dict()
        result = ChainMap({}, {k:v for k,v in dbdata.items() if not isinstance(v, dict)}, *[x for x in dbdata.values() if isinstance(x, dict)])
        fields = self.fields if isinstance(self.fields, list) else self.fields.split()
        result.update({"key": value, "table": self.table})
        for item in fields:
            result.update({item: result.get(item)})
        return result.maps[0]
    

class Key(ReferenceField):
    def __init__(self,table, project='Client', **kwargs) -> None:
        super().__init__(table, **kwargs) 
        self.project = project
        self.tag = 'select'
        self.ftype = Variable.UNDEFINED
        self.table = self.owner_name
        
        
class ArrayOfKeys(ReferenceField):
    def __init__(self,table, project='Client', **kwargs) -> None:
        super().__init__(table, **kwargs) 
        self.project = project
        self.tag = 'select'
        self.multiple = True
        self.ftype = Variable.UNDEFINED
        self.table = self.owner_name
        
    def parse(self, obj, value):
        if isinstance(value, str):
            value = [x.strip() for x in re.split('\s', value)]
        elif isinstance(value, list):
            pass 
        return value