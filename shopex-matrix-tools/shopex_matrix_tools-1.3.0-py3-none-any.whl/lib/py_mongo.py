#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymongo


def init_mongo(conf):
    """ 获取mongo连接实例 """
    kw = {
        'maxPoolSize': 10,  # 可选，设置mongo连接时的连接池
        'readPreference': 'primaryPreferred',
        'sale': False  # 连接不用ack，提升查询效率
    }
    addr_list = list(addr.strip() for addr in conf['addr'].split(','))
    if conf.get('mongodb_type') == 'repl':
        kw['replicaSet'] = conf['repl_name']
        conn = pymongo.MongoClient('mongodb://' + ','.join(map(lambda s: s.lstrip('mongodb://'), addr_list)), **kw)
    else:
        conn = pymongo.MongoClient(addr_list[0], **kw)
    # todo 钉钉通知 mongo 连接失败
    return conn
