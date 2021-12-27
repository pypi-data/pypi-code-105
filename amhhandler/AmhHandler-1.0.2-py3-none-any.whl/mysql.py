#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@time   : 2020/9/21 16:39
@file   : mysql_conn.py
@author : 
@desc   : 
@exec   : 
"""

import pymysql


class Conn():
    """定义一个 MySQL 操作类"""

    def __init__(self, config):
        """初始化数据库信息并创建数据库连接"""
        self.config = config
        try:
            self.conn = pymysql.connect(**self.config)
            self.cur = self.conn.cursor()
        except Exception as e:
            exit(e)

    def SelectQuery(self, sql):
        """执行select, show 类查询，有返回值"""
        try:
            self.cur.execute(sql)
            resList = self.cur.fetchall()
            return resList
        except Exception as e:
            print(e)
            return b''
        finally:
            DatabaseHandle.Close()

    def ExecQuery(self, sql):
        """执行非查询类语句"""
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
        finally:
            DatabaseHandle.Close()

    def Close(self):
        self.cur.close()
        self.conn.close()
