#!/usr/bin/env python
# coding: utf-8
'''base_manager module'''

__all__ = ['BaseManager']

import asyncio
from abc import ABC
from functools import cache
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union, NamedTuple, List

from metadoctor.db import Connection
from metadoctor import enumeration
from metadoctor.model import BaseModel
from metadoctor import models
from metadoctor import element
    
# enumeration aliases
is_defined = enumeration.Variable.is_defined
exist = enumeration.Variable.exist
Project = enumeration.Project
BaseEnum = enumeration.BaseEnum
Form = element.Form
Fieldset = element.Fieldset
User = models.User


class BaseManager(ABC):
    
    def __init__(self, user: User = None, connection: Connection = None) -> None:
        self.user = user
        self.connection = connection or Connection()
        
    @cache
    async def list_all(self, model: BaseModel) -> list:
        async with self.db(model.project()).ListAll(model.table()) as result:
            return [model(**item) for item in result]
        
        
    async def get_one(self, model: BaseModel, key: str):
        print(model, key)
        db = self.db(model.project())
        print(db)
        async with db.Get(model.table(), key=key) as result:
            print(result)
            if result:
                return model(**result)
            return None

    @cache
    def sync_list_all(self, model: BaseModel):
        return asyncio.run(self.list_all(model))

    @cache
    async def check_repr(self, instance: BaseModel):
        return True if repr(instance) in [repr(x) for x in await self.list_all(type(instance))] else False

    async def search(self, instance: BaseModel):
        async with self.db(instance.project()).Search(instance.table(), instance.json()) as result:
            return [type(instance)(**item) for item in result]

    def sync_search(self, model: BaseModel, query: dict):
        return asyncio.run(self.search(model, query))
    
    async def save(self, instance: BaseModel):
        async with self.db(instance.project()).Put(instance.table(), instance.json()) as created:
            if created:
                return type(instance)(**created)
            return None
        
    def sync_save(self, instance: BaseModel):
        return asyncio.run(self.save(instance))
    
    
    async def get_or_create(self, instance: BaseModel):
        async with self.db(instance.project()).Search(instance.table(), instance.json()) as result:
            instances = [type(instance)(**item) for item in result]
            if len(instances) == 0:
                async with self.db(instance.project()).Put(instance.table(), instance.json()) as created:
                    return type(instance)(**created)
            else:
                return instances[0]


    def sync_get_or_create(self, instance: BaseModel):
        return asyncio.run(self.get_or_create(instance=instance))
    
    
    def get_form(self, model: BaseModel, method='get', action=".", extra_models=None):
        result= []
        for field in model.fields().values():
            result.append(field.get_formfield())
        if extra_models:
            for extra_model in extra_models:
                extra_result = []
                for extra_field in extra_model.fields().values():
                    extra_result.append(extra_field.get_formfield())
                result.append(str(Fieldset(legend=extra_model.__pt_singular__, content=''.join(extra_result))))
        return str(Form(pk=f'{model.__name__}Form', content=str(Fieldset(legend=model.__pt_singular__, content=result)), method=method, action=action, novalidate=True)) 
    
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
        return BaseEnum(f'{model}Enum', [(x.key, x) for x in await self.list_all(model)])
    
    @cache
    def sync_enum_from_db(self, model: BaseModel):
        return asyncio.run(self.enum_from_db(model))
    
    @cache
    def get_model(self, name: str):
        model_list =  [v for v in vars(models).values() if hasattr(v, 'is_basemodel') and v.__name__ == name]
        return None if len(model_list) == 0 else model_list[0]
