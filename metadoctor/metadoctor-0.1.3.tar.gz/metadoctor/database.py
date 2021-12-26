#!/usr/bin/env python
# coding: utf-8
'''db module'''

__all__ = [
    'AbstractDB', 
    'Database', 
    'Connection',
]

import contextlib
from abc import ABC
from deta import Deta
from typing import Dict, Any
from starlette.datastructures import Secret

from metadoctor import utils
from metadoctor import settings
from metadoctor import enumeration

Project = enumeration.Project


class AbstractDB(ABC):
    
    def __init__(self, key, project=Project.BASE):
        self.key = key
        self.project = project

    def sync_connect(self, table: str):
        return Deta(str(self.key)).Base(table)

    async def connect(self, table: str):
        return Deta(str(self.key)).Base(table)

    @contextlib.asynccontextmanager
    async def Count(self, table):
        db = await self.connect(table)
        count = 0
        try:
            count = len(db.fetch().items)
        finally:
            yield count
            db.client.close()

    @contextlib.asynccontextmanager
    async def ListAll(self, table):
        db, result = await self.connect(table), []
        try:
            result = db.fetch().items
        except BaseException as e:
            print(e.__dict__)
        finally:
            yield result
            db.client.close()

    @contextlib.asynccontextmanager
    async def Get(self, table, key=None, keys=None):
        db, result = await self.connect(table), None
        try:
            if key:
                result = db.get(key=key)
            elif keys:
                result = []
                for key in keys:
                    result.append(db.get(key=key))
        finally:
            yield result
            db.client.close()

    @contextlib.asynccontextmanager
    async def Search(self, table, query=None):
        query = query or {}
        db = await self.connect(table)
        result = []
        try:
            result = db.fetch(query).items
        finally:
            yield result
            db.client.close()

    @contextlib.asynccontextmanager
    async def First(self, table, query=None):
        query = query or {}
        db = await self.connect(table)
        result = None
        try:
            result = db.fetch(query).items
        finally:
            yield result
            db.client.close()

    @contextlib.asynccontextmanager
    async def Last(self, table, query={}):
        db = await self.connect(table)
        result = None
        try:
            result =  db.fetch(query).last
        finally:
            yield result
            db.client.close()
            
    @contextlib.asynccontextmanager
    async def Put(self, table, data):
        db = await self.connect(table)
        result = None
        try:
            result = db.put(data)
        finally:
            yield result
            db.client.close()
            
    @contextlib.asynccontextmanager
    async def Insert(self, table, data):
        key = data.get("key")
        if not key:
            raise AttributeError("a key is necessary")
        db = await self.connect(table)
        result = None
        try:
            result = db.insert(data)
        finally:
            yield result
            db.client.close()

    @contextlib.asynccontextmanager
    async def Delete(self, table, key):
        db = await self.connect(table)
        result = None
        try:
            yield db.delete(key=key)
            result = True
        finally:
            yield result
            db.client.close()

    @contextlib.asynccontextmanager
    async def GetOrCreate(self, table: str, data: Dict[ str, Any ]):
        code = data.get('meta', {}).get('code', None) 
        assert code != None, 'CODE could not be found'
        exist, created = None, None
        base = await self.connect(table)
        result = base.fetch({'meta.code': code}).items
        if len(result) >= 1:
            exist = result[0]
        else:
            exist = None
            result = base.put(utils.json_encode(data))
            if result:
                created = result
        try:
            yield exist, created
        finally:
            base.client.close()
            
    @contextlib.asynccontextmanager
    async def CheckCode(self, table, code):
        db = await self.connect(table)
        result = None
        try:
            result = db.fetch({'meta.code': code}).items[0]
        finally:
            yield result
            db.client.close()
            
    @contextlib.asynccontextmanager
    async def SearchPersonByName(self, table, name):
        db = await self.connect(table)
        result = []
        try:
            result = db.fetch({'fullname?contains': name}).items
        finally:
            yield result
            db.client.close()
    
    @contextlib.asynccontextmanager
    async def Update(self, table: str, updates: dict, key: str):
        db = await self.connect(table)
        update_dict = {}
        for k, v in updates.items():
            if k == 'set':
                for k1, v1 in v.items():
                    update_dict[k1] = v1
            elif k == 'increment':
                for k1, v1 in v.items():
                    update_dict[k1] = db.util.increment(v1)
            elif k == 'append':
                for k1, v1 in v.items():
                    update_dict[k1] = db.util.append(v1)
            elif k == 'prepend':
                for k1, v1 in v.items():
                    update_dict[k1] = db.util.prepend(v1)
            elif k == 'trim':
                for k1 in v:
                    update_dict[k1] = db.util.trim()
        result = None
        try:
            result = db.update(updates, key)
            yield result
        except BaseException as e:
            print(e.__dict__)
            yield e
        finally:
            db.client.close()

            
class Database(AbstractDB):
    
    def __init__(self, key, project=Project.BASE):
        super().__init__(key=key, project=project)

        
class Connection(ABC):
    def __init__(self, 
                 base = Database(settings.config.get('BASE_PROJECT', cast=Secret), project=Project.BASE), 
                 log = Database(settings.config.get('LOG_PROJECT', cast=Secret), project=Project.LOG),
                 client = Database(settings.config.get('CLIENT_PROJECT', cast=Secret), project=Project.CLIENT),
                 user = Database(settings.config.get('USER_PROJECT', cast=Secret), project=Project.USER), 
                 ) -> None:
        self.base = base
        self.client = client
        self.log = log
        self.user = user
        