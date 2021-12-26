#coding: utf-8
if __name__ == "__main__":
    from gitee import GiteeRepo
    from urlparse import URL
    from crypto import CryptoHandler
    from exceptions import ColumnDataDoesNotFit, ColumnNotFoundError
else:
    from .crypto import CryptoHandler
    from .gitee import GiteeRepo
    from .urlparse import URL
    from .exceptions import ColumnDataDoesNotFit, ColumnNotFoundError

import json, warnings

def model_to_data(model=None):
    return tuple([i.data if hasattr(i, "data") else i for i in model])

class table_objects:
    def __init__(self, obj=None):
        self.obj = obj

    def all(self):
        return self.obj.columns
    
    def get(self, *args, **kwargs):
        """ Usage: get(**namespace) """
        if len(kwargs) == 1 and hasattr(kwargs, self.obj.index):
            return SqleeColumn(
                    url = self.obj.url / column,
                    repo = self.obj.repo,
                    index = self.obj.index,
                    table = self.obj,
                    namespace = self.obj.namespace,
                    )
        need = len(kwargs)
        result = []
        for column in self.obj.columns:
            transit = 0
            for kwarg in kwargs:
                if kwargs[kwarg] in column.data:
                    transit += 1
            if transit == need:
                result.append(column)
        if len(result) != 1:
            raise ValueError("找到了 %d 个匹配的数据，如果你试图筛选多数据，请参考‘filter’." % len(result))
        return result[0]

    def create(self, *args, **kwargs):
        """ Usage: create(**namespace) """
        column = self._get_cloumn(kwargs)
        all_columns = self.obj.repo.list_file(self.obj.name)

        if str(column) in all_columns:
            raise ValueError("目标索引已存在.")

        datas = []
        for namespace in self.obj.namespace:
            if namespace == self.obj.index:
                continue
            datas.append(kwargs[namespace])

        self.obj.repo.upload_file(
            path = URL(self.obj.name) / column,
            content = self.obj.crypto.encrypt_to_str(json.dumps(datas))
            )
        
        self.obj.sync()
        return self.obj.columns

    def delete(self):
        return self.obj.delete()
    
    @property
    def length(self):
        return len(self.obj.columns)

    def count(self):
        return len(self.obj.columns)
    
    def filter(self, *args, **kwargs):
        if len(kwargs) == 1 and self.obj.index in kwargs:
            return [SqleeColumn(
                    path = URL(self.obj.name) / kwargs[self.obj.index],
                    repo = self.obj.repo,
                    index = self.obj.index,
                    table = self.obj,
                    index_data = kwargs[self.obj.index],
                    namespace = self.obj.namespace,
                    )]
        need = len(kwargs)
        result = []
        for column in self.obj.columns:
            transit = 0
            for kwarg in kwargs:
                if kwargs[kwarg] in column.data:
                    transit += 1
            if transit == need:
                result.append(column)
        return result

    def _get_cloumn(self, kwargs):
        if self.obj.index == "id":
            column = self.obj.repo.list_file_int(path=self.obj.name)
            if len(column) == 0:
                column = 0
            else:
                column = max(column) + 1
            return column
        else:
            if self.obj.index in kwargs:
                return kwargs[self.obj.index]
            else:
                raise ValueError("未传入索引数据 %s." % self.obj.index)

    def sync(self):
        return self.obj.sync()

class SqleeColumn:
    datas = []
    def __init__(self, path=None, repo=None, index=None, index_data=None, 
                 table=None, namespace=[], *args, **kwargs):
        if not isinstance(repo, GiteeRepo):
            raise ValueError("参数'repo'必须是GiteeRepo.")

        self.index = index
        self.index_data = index_data
        self.repo = repo
        self.table = table
        self.path = path
        self.namespace = namespace
        self.sync()

    @property
    def data(self):
        return tuple(model_to_data(self.datas))

    @property
    def length(self):
        return len(self.data)

    def count(self):
        return len(self.data)

    def sync(self):
        self.datas = [self.index_data, ]

        datas = json.loads(self.table.crypto.decrypt_by_str(
            self.repo.get_file(path=self.path)
            ))

        for data in datas:
            setattr(self, self.namespace[datas.index(data)], data)
        self.datas += datas

        if len(self.datas) != len(self.namespace):
            print(ColumnDataDoesNotFit(namespace=self.namespace, datas=self.datas))
        return self.datas

    def update(self, *args, **kwargs):
        for kwarg in kwargs:
            self.datas[self.namespace.index(kwarg)] = kwargs[kwarg]
        self.repo.update_file(
            path = self.path,
            content = self.table.crypto.encrypt_to_str(json.dumps(self.datas))
            )
        return self.sync()

    def delete(self):
        del self
        return True

class SqleeTable:
    columns = []
    def __init__(self, name=None, repo=None, directly_load=True, encrypt=True):
        if not isinstance(name, str) and not isinstance(name, URL):
            raise ValueError("参数 'name' 必须是字符串或URL.")
        if not isinstance(repo, GiteeRepo):
            raise ValueError("参数 'repo' 必须是GiteeRepo.")

        self.crypto = CryptoHandler(crypto=encrypt)
        self.name = name
        self.repo = repo
        self.namespace = json.loads(self.repo.get_file(path=URL(self.name)/".namespace"))
        self.index = self.namespace[0]
        self.url = URL()/self.repo.user/self.repo.repo/self.name
        self.objects = table_objects(obj=self)
        if directly_load:
            self.sync()
    
    def get_column(self, id=None):
        for column in self.columns:
            if column.id == id:
                return column
        else:
            raise ColumnNotFoundError(id)

    def insert(self, *args, **kwargs):
        return self.objects.create(*args, **kwargs)

    def sync(self):
        self.columns = []
        for column in self.repo.list_file_int(path=self.name):
            self.columns.append(
                SqleeColumn(
                    path = URL(self.name) / column,
                    repo = self.repo,
                    index = self.namespace[0],
                    index_data = column,
                    table = self,
                    namespace = self.namespace,
                    )
                )
        self.columns = tuple(self.columns)
        return self.columns

    def delete(self):
        answer = self.repo.drop_folder(path=self.name)
        del self
        return answer

if __name__ == "__main__":
    repo = GiteeRepo(token="1895956f770eb0e4d08013ee4b753203", user="fu050409", repo="TEST_API")
    table = SqleeTable(
        name="Table",
        repo = repo
        )
    print(table.columns[0].datas[0].data)
    
