from pprint import pprint
import inspect


def get_func_para(func, del_para=None, add_para: dict = None):
    """提取函数的参数和默认值, 没有默认值设为 None
    比如可以用于设定 TaskDB.result 的例子

    Args:
        func (list, function): 单/多个函数组成的列表, 后面函数出现一样的参数会覆盖前面的默认值
        del_para (set, list, optional): 删除不想看到返回的参数
        add_para (dict, optional): 增加想补充的参数和值, 会覆盖原始值, 不会被 del_para 删除

    Returns:
        dict: 所有函数修剪后的参数和默认值
    """
    paras = {}
    func = func if isinstance(func, list) else [func]
    del_para = set(del_para) if del_para else set()
    add_para = add_para if add_para else {}
    for f in func:
        fullargspec = inspect.getfullargspec(f)
        defaults = fullargspec.defaults if fullargspec.defaults else []
        defaults = [None] * (len(fullargspec.args) - len(defaults)) + list(defaults)
        paras.update({k: v for k, v in zip(fullargspec.args, defaults) if k not in del_para})
    paras.update(add_para)
    return paras


def cover_dict(new_para: dict, default_para: dict):
    """使用 new_para 中的健值对递归覆盖 default_para 中的值, 遇到非 dict 就不再递归而直接覆盖, 出现类型不一样也会直接覆盖
    比如可以用于新参数覆盖旧参数 (注意因为失误导致的参数覆盖)

    Args:
        new_para (dict): 不能出现 default_para 中没有的 key
        default_para (dict): 被覆盖的

    Returns:
        dict: default_para
    """
    for k, v in new_para.items():
        assert k in default_para, f'构建了默认参数中没有的参数: {k} not in {set(default_para)}'
        if isinstance(v, dict) and isinstance(default_para[k], dict):
            cover_dict(v, default_para[k])
        else:
            default_para[k] = v
    return default_para


if __name__ == '__main__':
    class c:
        def __init__(self) -> None:
            pass

        @staticmethod
        def f(a, b=2, c=3, **kw):
            pass
    # get_func_para
    print('=' * 10, 'get_func_para')
    print(get_func_para(c), get_func_para(c.f))

    # cover_dict
    print('=' * 10, 'cover_dict')
    new_para = {'a': [1, 2, {'bb': 2}], 'b': {'c': (1, 2), 'd': 2}}
    default_para = {'a': [4, 2, {'b': 21}], 'b': {'c': (1, 1), 'd': 22, 'e': None}}
    pprint(cover_dict(new_para, default_para))
