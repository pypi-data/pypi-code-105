import numpy as np
from functools import lru_cache
from types import MethodType, FunctionType
import warnings
import sys
import multiprocessing


def func_transformer(func):
    # getattr() 函数用于返回一个对象属性值。
    # func不包含’mode‘ = ’other'
    mode = getattr(func, 'mode', 'others')
    # 当func包含mode，mode的值只能执行这些类型的模型，
    valid_mode = ('common', 'multithreading', 'multiprocessing', 'vectorization', 'cached', 'others')
    assert mode in valid_mode, 'valid mode should be in ' + str(valid_mode)
    if mode == 'vectorization':
        return func
    elif mode == 'cached':
        # @lru_cache装饰器可以提供缓存的功能,在下次函数接收到相同参数调用时直接返回上一次的结果,用以节约高开销或I/O函数的调用时间
        # maxsize :  None，LRU 特性将被禁用且缓存可无限增长
        # type : True不同类型被分开存放
        @lru_cache(maxsize=None)
        def func_cached(x):
            return func(x)

        def func_warped(X):
            return np.array([func_cached(tuple(x)) for x in X])

        return func_warped
    elif mode == 'multithreading':
        # 是否使用线程池
        from multiprocessing.dummy import Pool as ThreadPool

        pool = ThreadPool()

        def func_transformed(X):
            return np.array(pool.map(func, X))

        return func_transformed
    elif mode == 'multiprocessing':
        # 是否使用多进程
        from multiprocessing import Pool
        pool = Pool()

        def func_transformed(X):
            return np.array(pool.map(func, X))

        return func_transformed
    else:
        # 普遍的方法
        def func_transformed(X):
            return np.array([func(x) for x in X])

        return func_transformed
