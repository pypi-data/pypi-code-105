# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/16 18:56
# @Author : BruceLong
# @FileName: cd_sqlserver.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
import pymssql
import threading

from .config import SQLSERVER_HOST, SQLSERVER_USERNAME, SQLSERVER_PASSWORD, SQLSERVER_DB


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class SqlServerPipeline(metaclass=SingletonType):
    '''
    SqlServer存储管道
    '''

    def __init__(self):
        '''
        初始化操作
        '''
        self.host = SQLSERVER_HOST
        self.username = SQLSERVER_USERNAME
        self.password = SQLSERVER_PASSWORD
        self.db = SQLSERVER_DB

    def __get_connect(self):
        '''
        创建连接信息
        :return:
        '''
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.connect = pymssql.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.db,
            charset="utf8"
        )
        cursor = self.connect.cursor()
        if not cursor:
            raise (NameError, "连接数据库失败")
        else:
            return cursor

    def get_connect_test(self):
        return self.__get_connect()

    def __create_table(self, cur, item: dict, table: str):
        '''
        合建表相关的信息
        :param item: 数据
        :param table: 表名
        :return:
        '''
        # cur = self.__get_connect()
        # 判断是否存在该表
        sql = f'''SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID('{table}') AND type IN ('U')'''
        cur.execute(sql)
        if not cur.fetchone():
            # 生成创建字段信息
            # ------------目前只支持两种整型及字符串----------------------
            field_info = ',\n'.join(
                [
                    # f'{field} bigint' if isinstance(values, int) else f'{field} nvarchar(max)'
                    f'{field} nvarchar(max)'
                    for field, values in item.items()
                ]
            )

            sql_table = f'''create table {table}(
                    cd_id bigint identity(1,1) primary key,
                    cd_inserttime datetime default getdate(),
                    cd_updatetime datetime default getdate(),
                    {field_info}
                    )'''
            # --创建update触发器
            sql_trigger = f'''
                    create trigger trig_{table}_updatetime
                    on {table}
                    after update
                    as
                    begin
                        update {table} set cd_updatetime =getdate() WHERE cd_ID IN (SELECT DISTINCT cd_ID FROM inserted)
                    end'''
            try:
                # print(sql_table)
                cur.execute(sql_table)
                cur.execute(sql_trigger)
                self.connect.commit()
                print('Create Table Successful')
            except Exception as e:
                print('Create Table Failed', e)
        else:
            # 查询表字段
            select_fields_sql = f'''SELECT Name FROM SysColumns WHERE id=Object_Id('{table}')'''
            cur.execute(select_fields_sql)
            # 获取已经存在的表字段
            allready_exists_fields = {i[0].lower() for i in cur.fetchall()}
            # 目前新的字段名
            new_fields = {i.lower() for i in item.keys()}
            # 差集算出需要添加的字段名
            not_exists_fields = new_fields - allready_exists_fields
            if list(not_exists_fields):
                # 构造字段信息
                not_exists_fields_info = ','.join(
                    [
                        # f'{field} bigint' if isinstance(values, int) else f'{field} nvarchar(max)'
                        f'{field} nvarchar(max)'
                        for field, values in item.items() if field.lower() in not_exists_fields
                    ]
                )
                add_fields_sql = f'''alter table {table} add {not_exists_fields_info}'''
                try:
                    # print(add_fields_sql)
                    cur.execute(add_fields_sql)
                    self.connect.commit()
                    print('Create Field Successful')
                except Exception as e:
                    print('Create Field Failed', e)

    def insert_one(self, item: dict, table: str):
        '''
        插入一条数据
        :param item:
        :param table:
        :return:
        '''
        cur = self.__get_connect()
        self.__create_table(cur=cur, item=item, table=table)
        # 获取到一个以键且为逗号分隔的字符串，返回一个字符串
        keys = ', '.join(item.keys())
        values = ', '.join(['%s'] * len(item))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        # print(sql)
        try:
            # 这里的第二个参数传入的要是一个元组
            # data = [v if isinstance(v, int) else str(v) for v in item.values()]
            data = [str(v) for v in item.values()]
            # print(data)
            cur.execute(sql, tuple(data))
            print('Insert One Successful')
            self.connect.commit()
        except:
            print('Insert One Failed')
            self.connect.rollback()
        finally:
            cur.close()
            self.connect.close()
        pass

    def insert_many(self, items: list, table: str):
        '''
        批量插入数据
        :param items:
        :param table:
        :return:
        '''
        if not isinstance(items, list):
            raise (TypeError, 'please input items for list type')
        cur = self.__get_connect()
        k_temp = {k for ite in items for k in ite.keys()}
        v_temp = ['' for _ in range(len(k_temp))]
        data = dict(zip(k_temp, v_temp))
        self.__create_table(cur=cur, item=data, table=table)
        values = ', '.join(['%s'] * len(data))
        # [[item.update({k: str(v)}) for k, v in item.items() if not isinstance(v, (int, str))] for item in items]
        result_data = [{k: str(item.get(k)) if item.get(k) else '' for k in data.keys()} for item in items]
        # print(result_data)
        keys = ', '.join(result_data[0].keys())
        datas = [tuple(i.values()) for i in result_data]
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        try:
            cur.executemany(sql, datas)
            self.connect.commit()
            print('Insert Many Successful')
        except Exception as e:
            self.connect.rollback()
            print('Insert Many Failed:', e)
        finally:
            cur.close()
            self.connect.close()


cd_Ss = SqlServerPipeline()
if __name__ == '__main__':
    cur = cd_Ss.get_connect_test()
    # sql = '''SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID('test2') AND type IN ('U')'''
    # cur.execute(sql)
    # print(cur.fetchone())
    itemss = {'Spu_Name': '麦德龙法国原装波尔多银麓谷AOC干红葡萄酒2瓶赤霞珠美乐送礼红酒', 'Red_Title': "荣获2016'马贡金奖  2016/2018年份随机发货",
              'img_Url': 'http://img.alicdn.com/imgextra/i1/2630035235/O1CN01kvARr21oXg8CprjJD_!!2630035235.jpg;http://img.alicdn.com/imgextra/i2/2630035235/O1CN01DYD1Nv1oXg83aSySg_!!2630035235.jpg;http://img.alicdn.com/imgextra/i4/2630035235/O1CN01UBRtxV1oXg1UGW4gP_!!2630035235.jpg;http://img.alicdn.com/imgextra/i2/2630035235/O1CN01WI8tNq1oXg1LswGXp_!!2630035235.jpg;http://img.alicdn.com/imgextra/i3/2630035235/O1CN0186cf9s1oXg6aj3MHM_!!2630035235.jpg;',
              'Spu_ID': '536935869234', 'categoryId': '201334103', 'Project_ID': '',
              'Spu_Url': 'https://detail.tmall.com/item.htm?id=536935869234', 'Comment_Count': '3320',
              'Popularity': '12478', 'Store_Name': '麦德龙官方海外旗舰店', 'Store_ID': '129134153', 'Product_Details': '',
              'Month_Sales': '1000', 'Total_Sales': '',
              'Store_Url': 'https://market.m.taobao.com/app/tb-source-app/shop-auction/pages/auction?shopId=129134153&displayShopHeader=true',
              'Credits': '', 'Search_Keyword': '', 'Create_Time': '2021-12-17 13:52:30', 'Sku_ID': '3219510199080',
              'Sku_Name': 'Chateau Pied dArgent Bellevue 750mL ', 'Ori_Price': '388.00', 'Sales_Price': '198',
              'Quantity': '1634', 'Quantity_longfei': 123456}
    cd_Ss.insert_one(item=itemss, table='brucelong_test')
    # cur.execute('''SELECT Name FROM SysColumns WHERE id=Object_Id('brucelong_test')''')
    # allready_exists = {i[0] for i in cur.fetchall()}
    # new_fields = set(item.keys())
    # print(new_fields - allready_exists)
