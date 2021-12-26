#!/usr/bin/env python
# coding: utf-8
from __future__ import annotations

'''metadoctor.base module'''

__all__ = [
    'BaseModel',
    'BaseField',
    'BaseManager',
    'Manager',
    'RegularField',
    'EnumField', 
    'ReferenceField', 
    'DateTime', 
    'Text', 
    'SemicolonStrToList',
    'String', 
    'Choice',
    'SelectEnum',
    'Date',
    'Title',
    'Number', 
    'Integer',
    'Float',
    'Real', 
    'Boolean',
    'Key',
    'KeyData',
    'Array',
    'ArrayOfKeys',
    'DataField',
    'Instance'
]

import asyncio 
from abc import ABC
from collections import ChainMap, namedtuple
from markupsafe import Markup
import re
import datetime
from abc import ABC
from collections import ChainMap
from decimal import Decimal
from typing import Any
from markupsafe import Markup
import asyncio
from abc import ABC
from functools import cache
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union, NamedTuple, List

from metadoctor import enumeration
from metadoctor import element
from metadoctor import utils
from metadoctor import database as db

# aliases and lambdas
Connection = db.Connection
is_defined = enumeration.Variable.is_defined
exist = enumeration.Variable.exist
Project = enumeration.Project
BaseEnum = enumeration.BaseEnum
Form = element.Form
Fieldset = element.Fieldset
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
column_set = lambda x,y,z: f'col-sm-{x} col-md-{y} col-lg-{z}'
only_digits = utils.only_digits

INPUT_STYLE = element.INPUT_STYLE
POSITIONAL_HTML_ELEMENT_ATTRIBUTES = element.POSITIONAL_HTML_ELEMENT_ATTRIBUTES
KEYWORD_VALUE_HTML_ELEMENT_ATTRIBUTES = element.KEYWORD_VALUE_HTML_ELEMENT_ATTRIBUTES
BASE_FIELD_CONFIG_KEYS = 'transform fsize fclass fstyle tag default factory exclude title description options'.split()



class BaseModel(ABC):
    __project = None
    __table = None
    __objname = None
    __singular = None
    __plural = None

    def __init__(self, *args, **kwargs) -> None:
        self._extra_data = dict()
        for base in [*type(self).__bases__, type(self)]:
            if issubclass(base, BaseModel):
                for k, field in base.fields().items():
                    setattr(type(self), k, field) 
        for k in self.fields().keys():
            if k in kwargs.keys():
                setattr(self, k, kwargs[k])
            else:
                setattr(self, k, None)
        
        for k,v in kwargs.items():
            if not k in self.fields().keys():
                self._extra_data[k] = v
                
        self._key = kwargs.get('key') or self._autokey()

        self.__post_init__()
        
        
    def __post_init__(self):
        pass 
    
    def _autokey(self):
        return None
    
    
    def __str__(self) -> str:
        return ', '.join([str(v) for v in self.main_data().values() if exist(v)])

    def __repr__(self) -> str:
        return f'{type(self).__name__}({", ".join([f"{k}={str(v)}" for k, v in self.main_data().items() if exist(v)])})' 
    
    def __hash__(self):
        return hash(tuple(self.main_json().values()))
    
    def __eq__(self, other):
        return repr(self) == repr(other)


    def __repr_html__(self) -> str:
        return Markup(f'<h3>{str(self)}</h3>')

    def __html__(self) -> str:
        return self.__repr_html__()
    
    @classmethod
    @cache
    async def list_all(cls):
        async with getattr(Connection(), cls.project()).ListAll(cls.table()) as data:
            return [cls(**item) for item in data]
        
    @classmethod
    @cache
    async def options(cls, selected=None):
        data = await cls.list_all()
        result = list(sorted(data, key=lambda x: str(x)))
        options = [Option(value=x.key, content=str(x)) for x in result]
        for item in options:
            if item == selected:
                item.selected = True 
        return ''.join([str(x) for x in options])
        
        
    @cache
    async def _exist(self):
        data = await self.list_all()
        result = list(filter(lambda x: x == self, data))
        return None if len(result) == 0 else result[0]
    
    

        
        
    @classmethod
    @cache
    async def by_key(cls, key: str):
        async with getattr(Connection(), cls.project()).Get(cls.table(), key) as result:
            if result:
                return cls(**result)
            return None
        
    @cache
    async def from_db(self):
        async with getattr(Connection, self.project()).Get(self.table(), self.key) as result:
            if result:
                return type(self)(**result)
            return None
        

    async def update(self, **kwargs):
        data = self.json().update(**kwargs)
        async with getattr(Connection(), self.project()).Put(self.table(), data) as result:
            if result:
                return type(self)(**result)
            return None
        
    @cache
    async def get_or_create(self):
        exist, created = await self._exist(), None
        if not exist:
            async with getattr(Connection(), self.project()).Put(self.table(), self.json()) as result:
                if result:
                    created = type(self)(**result)
        return exist, created
    
    
    @classmethod
    @cache
    async def list_all_enum(cls):
        return BaseEnum(f'{cls.__name__}Enum', [(x.key, x) for x in await cls.list_all()])
    
    
    @classmethod
    def ismodel(cls):
        return True 
    
    @classmethod
    def table_project(cls):
        return cls.table(), cls.project()
    
    @staticmethod
    def json_encode(v):
        return utils.json_encode(v)
                
    @classmethod
    def fields(cls):
        return {k:v for (k,v) in vars(cls).items() if isinstance(v, BaseField)}         
    
    @classmethod
    def namedtuple(cls):
        ntuple = namedtuple(f'{cls.table()}NamedTuple', ' '.join(cls.fields().keys()) + ' key')
        ntuple.__model__ = cls
        ntuple.model_instance = lambda x: cls(**x._asdict())
        return ntuple
    
    def astuple(self):
        return self.namedtuple()(**self.data())
    
    def data(self) -> dict:
        result = {k:v.__get__(self) for (k,v) in self.fields().items()}
        if exist(self.key):
            result['key'] = self.key
        return result 
    
    def json(self) -> dict:
        result = {k: self.json_encode(v.unparsed(self)) for k,v in self.fields().items()}
        if exist(self.key):
            result['key'] = self.key
        return result 
    
    def main_data(self) -> str:
        return {k: v.__get__(self) for k, v in self.fields().items() if not is_defined(v.exclude)}
    
    
    def main_json(self) -> str:
        return {k: self.json_encode(v.unparsed(self)) for k, v in self.fields().items() if not is_defined(v.exclude) if v.unparsed(self)}
    
    def extra_data(self):
        return self._extra_data
    
    @classmethod
    def table(cls):
        name = f'_{cls.__name__}__table'
        return cls.__name__ if not hasattr(cls, name) else getattr(cls, name)
            
    @classmethod
    def project(cls):
        name = f'_{cls.__name__}__project'
        return Project.BASE if not hasattr(cls, name) else getattr(cls, name)
    
    
    @classmethod
    def objname(cls):
        name = f'_{cls.__name__}__objname'
        return cls.__name__.lower() if not hasattr(cls, name) else getattr(cls, name)
    
    @classmethod
    def singular(cls):
        name = f'_{cls.__name__}__singular'
        return cls.__name__ if not hasattr(cls, name) else getattr(cls, name)
    
    @classmethod
    def plural(cls):
        name = f'_{cls.__name__}__plural'
        return f'{cls.__name__}s' if not hasattr(cls, name) else getattr(cls, name)
    
    
    @property
    def key(self):
        return getattr(self, '_key')
    
    @property
    def defaults(self) -> dict:
        defaults = {}
        for k,v in self.fields().items():
            if is_defined(v.factory):
                defaults.update({k: v.factory()})  
            elif is_defined(v.default):
                defaults.update({k: v.default})
        return defaults
    

class BaseField(ABC):
    POSITIONAL = POSITIONAL_HTML_ELEMENT_ATTRIBUTES
    KEYVALUE = KEYWORD_VALUE_HTML_ELEMENT_ATTRIBUTES
    CONFIG = [*BASE_FIELD_CONFIG_KEYS, *POSITIONAL_HTML_ELEMENT_ATTRIBUTES, *KEYWORD_VALUE_HTML_ELEMENT_ATTRIBUTES]
    
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
        self._instance_ = None
        self._dbdata_ = None
        
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
                
    def default_value(self):
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
                if k in self.KEYVALUE:
                    result.append(f'{k}="{v}"')
                elif k in self.POSITIONAL and v == True:
                    result.append(k)
        if is_defined(self.ftype):
            result.append(f'type="{self.ftype}"')
        if self.default_value():
            if not novalue:
                result.append(f'value="{str(self.default_value())}"')
        if is_defined(self.fstyle):
            result.append(f'style="{self.fstyle}"')
        if is_defined(self.fclass):
            result.append(f'class="{self.fclass} field"')
        else:
            result.append(f'class="field"')
        if is_defined(self.placeholder):
            result.append(f'placeholder="{self.placeholder}"')
        return ' '.join(result)
    
    async def get_formfield(self, inner_text=None):
        label = lambda field: f'<label for="{self.public_name}" class="form-label">{self.title if is_defined(self.title) else self.description if is_defined(self.description) else self.public_name} {field}</label>'
        fd = ''
        if self.element == Input:
            fd = f'<input {self.get_formfield_attrs()}>'
        elif self.element == DataList:
            lt = f"{self.public_name}_list"
            fd = f'<input list="{lt}" {self.get_formfield_attrs(novalue=True)}><datalist id="{lt}">{inner_text or await self.owner.options(selected=self.default_value())}</datalist>'
        elif self.element == Select:
            fd = f'<select {self.get_formfield_attrs(novalue=True)}>{inner_text or await self.owner.options(selected=self.default_value())}</select>'
        elif self.element == TextArea:
            fd = f'<textarea {self.get_formfield_attrs()}>{inner_text or ""}</textarea>'
        return label(fd)

    def pre_validate(self, obj, value) -> Any:
        if not exist(value):
            if is_defined(self.factory):
                value = self.factory()
            elif is_defined(self.default):
                value = self.default        
        return value
    
    def check_required(self, obj, value) -> None:
        if self.required == True:
            if not exist(value):
                raise ValueError(f'{type(obj).__name__}.{self.public_name} cannot be "{value}"')
            
    def post_validate(self, obj, value) -> Any:
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
        pre = self.pre_validate(obj, value)
        self.validate(obj, pre)
        post = self.post_validate(obj, pre)
        setattr(obj, self.private_name, post)
        
    def parse(self, obj, value) -> Any:
        return value 
    
    def unparsed(self, obj):
        '''Return attribute of object saved as private name. This is the value passed in to the __init__ method of the model.'''
        return getattr(obj, self.private_name)

    def __set_name__(self, obj, name) -> None:
        self.public_name = name 
        self.private_name = f'_{name}'
    
    def __get__(self, obj, owner=None) -> Any:
        return self.parse(obj, getattr(obj, self.private_name))
    

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
        
    def pre_validate(self, obj, value):
        value = super().pre_validate(obj, value)
        if isinstance(value, datetime.datetime):
            value = value.isoformat()
        return value
    
    def  parse(self, obj, value):
        if value:
            if isinstance(value, str):
                try:
                    value = datetime.datetime.fromisoformat(value)
                except BaseException as e:
                    print(e)
        return value 
        
class Text(RegularField):
    def __init__(self, **kwargs) -> None:
        super().__init__(str, **kwargs) 
        self.element = TextArea
        self.tag = 'textarea'
        self.ftype = Variable.UNDEFINED
        
    def post_validate(self, obj, value):
        value = super().post_validate(obj, value)
        return value 
    
    def parse(self, obj, value):
        if not isinstance(value, str):
            value = str(value)
        return value 

        
class SemicolonStrToList(RegularField):
    def __init__(self, **kwargs) -> None:
        super().__init__(str, **kwargs) 
        self.element = TextArea
        self.tag = 'textarea'
        self.ftype = Variable.UNDEFINED
        
    def post_validate(self, obj, value):
        value = super().post_validate(obj, value)
        if isinstance(value, (list, tuple)):
            value = '; '.join([str(x) for x in value])
        return value 
    
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
    
    def post_validate(self, obj, value):
        value = super().post_validate(obj, value)
        return value 
    
    def parse(self, obj, value):
        if not isinstance(value, str):
            value = str(value)
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
    
class SelectEnum(EnumField):
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
            try:
                value = self.owner[value]
            except KeyError:
                try:
                    value = self.owner(value)
                except:
                    try:
                        value = self.owner.get(value)
                    except:
                        pass 
        return value 

    
class InputListEnum(EnumField):
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

class Boolean(RegularField):
    '''
    Receive a int, string or bool and store as bool in db.
    '''
    def __init__(self,**kwargs) -> None:
        super().__init__(bool, **kwargs) 
        self.element = Input
        self.tag = 'input'
        self.ftype = 'checkbox'
        self.fstyle = 'display:inline-block'
        
    def pre_validate(self, obj, value):
        value = super().pre_validate(obj, value)
        return True if value in [1, 'true', True] else False
                
    def parse(self, obj, value):
        return True if value in [1, 'true', 'True', 'TRUE', True] else False

    

class Array(RegularField):
    '''
    Receive a string to stored in db.
    The __get__ method parse the string to a list.
    '''
    def __init__(self,**kwargs) -> None:
        super().__init__(list, **kwargs) 
        self.element = Input
        self.tag = 'input'
                
    def post_validate(self, obj, value):
        value = super().post_validate(obj, value)
        if isinstance(value, (list, tuple)):
            value = '; '.join([str(x) for x in value])
        return value 
    
    def parse(self, obj, value):
        if value:
            if isinstance(value, str):
                value = [x.strip() for x in re.split('[;\n]', value)]
        return value

    

class KeyData(ReferenceField):
    def __init__(self,table, project: Project = Project.CLIENT, fields=None, **kwargs) -> None:
        super().__init__(table, **kwargs) 
        self.project = project
        self.element = Select
        self.tag = 'select'
        self.ftype = Variable.UNDEFINED
        self.table = self.owner_name
        self.fields = fields or list()
        self.db = getattr(Connection(), str(project))
        
    def parse(self, obj, value):
        dbdata = self.db.sync_connect(self.table).get(str(value)) or dict()
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
    def __init__(self,table,  project: Project = Project.CLIENT, fields=None, **kwargs) -> None:
        super().__init__(table, **kwargs) 
        self.db = getattr(Connection(), str(project))
        self.table = self.owner_name
        self.element = DataList
        self.tag = 'datalist'
        self.ftype = Variable.UNDEFINED
        self.fields = fields or list()
        
    def parse(self, obj, value):
        dbdata = self.db.sync_connect(self.table).get(str(value)) or dict()
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
    '''Instance Field Class accept only the key of the object'''
    def __init__(self,owner, fields=None, **kwargs) -> None:
        super().__init__(owner, **kwargs)
        self.fields = fields if isinstance(fields, list) else [x.strip() for x in fields.split()] if isinstance(fields, str) else ''
#         if self.fields:
#             fields = 
#             self.ntuple = namedtuple(self.table, ' '.join(fields.keys()))
#         else:
#             self.ntuple = None
        self.project = self.owner.project()
        self.db = getattr(Connection(), str(self.project))
        self.element = Select
        self.tag = 'select'
        self.ftype = Variable.UNDEFINED
        self.table = self.owner_name
        self.fields = fields
        self._instance_ = None
        self._dbdata_ = None
        
    def parse(self, obj, value):
        def lazy_dbdata() -> dict:
            if self._instance_ and self._dbdata_:
                assert self._instance_.key == self._dbdata_['key']
            elif self._dbdata_ and value:
                assert value == self._dbdata_['key']
            elif exist(value):
                self._dbdata_ = self.db.sync_connect(self.table).get(str(value)) or dict()
        
        def lazy_instance():
            if not self._instance_:
                self._instance_ = self.owner(**self._dbdata_)
            return self._instance_
        
        lazy_dbdata()
        return lazy_instance() 
        

    

class Key(ReferenceField):
    def __init__(self,table,  project: Project = Project.CLIENT, **kwargs) -> None:
        super().__init__(table, **kwargs) 
        self.project = project
        self.element = Select
        self.tag = 'select'
        self.ftype = Variable.UNDEFINED
        self.table = self.owner_name
        
        
class ArrayOfKeys(ReferenceField):
    def __init__(self,table,  project: Project = Project.CLIENT, **kwargs) -> None:
        super().__init__(table, **kwargs) 
        self.project = project
        self.element = Select
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
    

class BaseManager(ABC):
    
    def __init__(self, user: User = None, connection: Connection = None) -> None:
        self.user = user
        self.connection = connection or Connection()
    
    
    async def get_form(self, model: BaseModel, method='get', action=".", extra_models=None):
        result= []
        for field in model.fields().values():
            result.append(await field.get_formfield())
            result.append('<br>')
        if extra_models:
            for extra_model in extra_models:
                extra_result = []
                for extra_field in extra_model.fields().values():
                    extra_result.append(await extra_field.get_formfield())
                    extra_result.append('<br>')
                result.append(str(Fieldset(legend=extra_model.singular(), content=''.join(extra_result))))
        return str(Form(pk=f'{model.__name__}Form', content=str(Fieldset(legend=model.singular(), content=result)), method=method, action=action, novalidate=True)) 
    
    @cache
    async def model_instances(self, model):
        async with self.db(Project(model.project())).ListAll(model.table()) as result:
            return [model(**item) for item in result]
    
    @cache
    async def namedtuple_instances(self, model):
        ntuple = model.namedtuple()
        async with self.db(Project(model.project())).ListAll(model.table()) as result:
            return [ntuple(**item) for item in result]
        
    @property
    def clientdb(self):
        return self.connection.client
        
    @property
    def logdb(self):
        return self.connection.log
    
    @property
    def basedb(self):
        return self.connection.base
    
    @property
    def userdb(self):
        return self.connection.user
    
    def db(self, project: Project = Project.BASE):
        return {
            'base': self.basedb,
            'client': self.clientdb,
            'log': self.logdb,
            'user': self.userdb,
        }.get(str(project), self.basedb)

    @staticmethod 
    def table(instance: BaseModel):
        return instance.table() or type(instance).__name__
    
    @staticmethod 
    def json(instance: BaseModel):
        return instance.json()
    
    @staticmethod 
    def project(instance: BaseModel):
        return instance.project() or 'base'
    
    @cache
    async def enum_from_db(self, model: BaseModel):
        return BaseEnum(f'{model}Enum', [(x.key, x) for x in await model.list_all()])
    
    @cache
    def sync_enum_from_db(self, model: BaseModel):
        return asyncio.run(self.enum_from_db(model))

    
    
class Manager(BaseManager):
    '''Subclass of BaseManager'''