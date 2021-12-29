from abc import ABCMeta, abstractmethod
import types
import warnings
from Statech.spssbase import SpssPro


class proBase(SpssPro, metaclass=ABCMeta):
    def register(self, operator_name, operator, *args, **kwargs):
        def operator_wapper(*wrapper_args):
            return operator(*(wrapper_args + args), **kwargs)

        # setattr() 函数对应函数 getattr()，用于设置属性值，该属性不一定是存在的。
        setattr(self, operator_name, types.MethodType(operator_wapper, self))
        return self

    def fit(self, *args, **kwargs):
        warnings.warn('.fit() will be deprecated in the future. use .run() instead.'
                      , DeprecationWarning)
        return self.run(*args, **kwargs)
