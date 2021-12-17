import os
import threading
import time
import uuid
from typing import Optional

import redis
from redis.client import Pipeline

from lightning_fast.tools.base_tools.ip_tools import IpTools

REDIS_LOCK_PREFIX = "REDIS_READ_WRITE_LOCK"


class RedisReadWriteLock:
    def __init__(self, conn, lock_name, acquire_timeout=10, lock_timeout=1000):
        self.conn = conn
        self.lock_name = lock_name
        self.acquire_timeout = acquire_timeout
        self.lock_timeout = lock_timeout
        self.identifier = None

    @property
    def acquire_success(self):
        return self.identifier is not None

    def __enter__(self):
        self.identifier = self.acquire_lock(
            self.conn, self.lock_name, self.acquire_timeout, self.lock_timeout
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.identifier is not None:
            self.release_lock(self.conn, self.lock_name, self.identifier)

    @classmethod
    def combine_lock_key(cls, lock_name):
        return f"{REDIS_LOCK_PREFIX}:" + lock_name

    @classmethod
    def acquire_lock(
        cls,
        conn: redis.StrictRedis,
        lock_name: str,
        acquire_timeout: int,
        lock_timeout: int,
    ) -> Optional[str]:
        """
        :param conn: redis连接
        :param lock_name: 锁名字
        :param acquire_timeout: 拿锁超时时间(秒)
        :param lock_timeout: 锁自然过期时间(秒)
        :return: 锁的唯一值
        """
        # 拿到本机网络ip
        ip = IpTools.get_ip()
        # 拿到本程序进程id
        pid = os.getpid()
        # 拿到线程id
        thread_name = threading.current_thread().name
        # 生成一个唯一用来删除时识别的值
        identifier = f"{ip}-{pid}-{thread_name}-{uuid.uuid4()}"
        # 生成一个key
        lock_key = cls.combine_lock_key(lock_name)
        # 根据获取超时时间设定结束获取时间
        end = time.time() + acquire_timeout
        while time.time() < end:
            # 使用 setnx 本操作如果已经有key会返回0, 否则返回1
            if conn.setnx(lock_key, identifier):
                # 设置过期时间
                conn.expire(lock_key, lock_timeout)
                return identifier
            # 如果发现没有设置过期时间(-1)或者没有key(-2)或者非严格模式(None)
            else:
                ttl_time = conn.ttl(lock_key)
                if ttl_time is None or (-1 <= ttl_time <= 0):
                    conn.expire(lock_key, lock_timeout)
            time.sleep(0.001)

        return None

    @classmethod
    def release_lock(
        cls, conn: redis.StrictRedis, lock_name: str, identifier: str
    ) -> bool:
        """
        :param conn: redis连接
        :param lock_name: 锁名字
        :param identifier: 拿锁的时候创建的唯一值, 用来识别是否可以删掉这个锁, 别删错了
        :return: 返回是否释放成功
        """
        # 创建redis pipeline
        pipe: Pipeline = conn.pipeline(True)
        # 生成一个key
        lock_key = cls.combine_lock_key(lock_name)
        while True:
            try:
                # break transaction once lock has been changed, use watch watch result in pipeline.
                pipe.watch(lock_key)
                # 如果获取到的key是需要识别的值
                lock_value = pipe.get(lock_key)
                if isinstance(lock_value, bytes):
                    lock_value = lock_value.decode()
                if lock_value == identifier:
                    # 增加命令
                    pipe.multi()
                    # 删除当前的key
                    pipe.delete(lock_key)
                    # 执行
                    pipe.execute()
                    # 返回释放成功
                    return True

                # execute when identifier not equal. 当没有拿到的时候把watch释放
                pipe.unwatch()
                # 直接结束
                break
            except redis.exceptions.WatchError as e:
                # 如果发现中间有人把lock给改了, 直接结束
                print(e)
                return False
        return False
