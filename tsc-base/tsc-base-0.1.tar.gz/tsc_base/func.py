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
        defaults = [None] * (len(fullargspec.args) - len(fullargspec.defaults)) + list(fullargspec.defaults)
        paras.update({k: v for k, v in zip(fullargspec.args, defaults) if k not in del_para})
    paras.update(add_para)
    return paras


if __name__ == '__main__':
    def f(a, b=2, c=3, **kw):
        pass
    pprint(get_func_para(f))
