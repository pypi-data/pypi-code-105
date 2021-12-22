import cProfile
import os

import wrapt
from line_profiler import LineProfiler

lp = LineProfiler()


def lp_wrapper():
    """
    显示函数调用时间
    """
    @wrapt.decorator
    def wrapper(func, instance, args, kwargs):
        global lp
        lp_wrapper = lp(func)
        res = lp_wrapper(*args, **kwargs)
        lp.print_stats()
        return res
    return wrapper


def cp_wrapper(filename="cp", png=False):
    """
    火焰图
    """
    @wrapt.decorator
    def wrapper(func, instance, args, kwargs):
        pr = cProfile.Profile()
        pr.enable()
        res = func(*args, **kwargs)
        pr.disable()
        pr.dump_stats(f"{filename}.prof")
        if png:
            export_png(filename)
        return res
    return wrapper


def export_png(filename):
    checks = {
        "dot": "dot not found\nplease install graphviz, e.g.:yum install -y graphviz\n",
        "gprof2dot": "not found gprof2dot\nplease install gprof2dot, e.g.:pip3 install gprof2dot",
    }
    for k in checks:
        rep = os.system(f"which {k}")
        if rep:
            print(checks[k])
            return
    cmd = f"gprof2dot -f pstats {filename}.prof |dot -Tpng -o {filename}.png"
    rep = os.system(cmd)
    if rep:
        print(f"convert {filename}.prof error")


def break_point():
    import pdb
    pdb.set_trace()

