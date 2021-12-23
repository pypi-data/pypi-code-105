from .util import compare
from .seq import (delay, unfold)
from .big_int import (from_zero, op_addition)
from .decimal import (from_parts, op_addition as op_addition_1)
from .long import (from_bits, op_addition as op_addition_2)

def make_range_step_function(step, stop, zero, add):
    step_compared_with_zero = compare(step, zero) or 0
    if step_compared_with_zero == 0:
        raise Exception("The step of a range cannot be zero")
    
    step_greater_than_zero = step_compared_with_zero > 0
    def arrow_5(x=None, step=step, stop=stop, zero=zero, add=add):
        compared_with_last = compare(x, stop) or 0
        return (x, add(x, step)) if (True if (compared_with_last <= 0 if (step_greater_than_zero) else (False)) else (compared_with_last >= 0 if (not step_greater_than_zero) else (False))) else (None)
    
    return arrow_5


def integral_range_step(start, step, stop, zero, add):
    step_fn = make_range_step_function(step, stop, zero, add)
    return delay(lambda start=start, step=step, stop=stop, zero=zero, add=add: unfold(step_fn, start))


def range_big_int(start, step, stop):
    return integral_range_step(start, step, stop, from_zero(), lambda x, y, start=start, step=step, stop=stop: op_addition(x, y))


def range_decimal(start, step, stop):
    return integral_range_step(start, step, stop, from_parts(0, 0, 0, False, 0), lambda x, y, start=start, step=step, stop=stop: op_addition_1(x, y))


def range_double(start, step, stop):
    return integral_range_step(start, step, stop, 0, lambda x, y, start=start, step=step, stop=stop: x + y)


def range_int64(start, step, stop):
    return integral_range_step(start, step, stop, from_bits(0, 0, False), lambda x, y, start=start, step=step, stop=stop: op_addition_2(x, y))


def range_uint64(start, step, stop):
    return integral_range_step(start, step, stop, from_bits(0, 0, True), lambda x, y, start=start, step=step, stop=stop: op_addition_2(x, y))


def range_char(start, stop):
    int_stop = ord(stop) or 0
    def arrow_6(start=start, stop=stop):
        def step_fn(c):
            if c <= int_stop:
                return (chr(c), c + 1)
            
            else: 
                return None
            
        
        return unfold(step_fn, ord(start))
    
    return delay(arrow_6)


