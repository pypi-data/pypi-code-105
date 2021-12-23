from .string import (join, is_null_or_empty, format, substring)
from .reflection import class_type
from .util import (int32_to_string, clear)
from .types import to_string

def expr_8():
    return class_type("System.Text.StringBuilder", None, StringBuilder)


class StringBuilder:
    def __init__(self, value, capacity):
        self.buf = []
        if not is_null_or_empty(value):
            (self.buf.append(value))
        
    
    def __str__(self):
        __ = self
        return join("", __.buf)
    

StringBuilder_reflection = expr_8

def StringBuilder__ctor_Z18115A39(value, capacity):
    return StringBuilder(value, capacity)


def StringBuilder__ctor_Z524259A4(capacity):
    return StringBuilder__ctor_Z18115A39("", capacity)


def StringBuilder__ctor_Z721C83C5(value):
    return StringBuilder__ctor_Z18115A39(value, 16)


def StringBuilder__ctor():
    return StringBuilder__ctor_Z18115A39("", 16)


def StringBuilder__Append_Z721C83C5(x, s):
    (x.buf.append(s))
    return x


def StringBuilder__Append_244C7CD6(x, c):
    (x.buf.append(c))
    return x


def StringBuilder__Append_Z524259A4(x, o):
    (x.buf.append(int32_to_string(o)))
    return x


def StringBuilder__Append_5E38073B(x, o):
    (x.buf.append(to_string(o)))
    return x


def StringBuilder__Append_Z1FBCCD16(x, o):
    (x.buf.append(to_string(o)))
    return x


def StringBuilder__Append_4E60E31B(x, o):
    (x.buf.append(to_string(o)))
    return x


def StringBuilder__Append_695F1130(x, cs):
    (x.buf.append(''.join(cs)))
    return x


def StringBuilder__Append_43A65C09(x, s):
    (x.buf.append(to_string(s)))
    return x


def StringBuilder__AppendFormat_433E080(x, fmt, o):
    (x.buf.append(format(fmt, o)))
    return x


def StringBuilder__AppendLine(x):
    (x.buf.append("\n"))
    return x


def StringBuilder__AppendLine_Z721C83C5(x, s):
    (x.buf.append(s))
    (x.buf.append("\n"))
    return x


def StringBuilder__get_Length(x):
    len_1 = 0
    for i in range(len(x.buf) - 1, 0 - 1, -1):
        len_1 = (len_1 + len(x.buf[i])) or 0
    return len_1


def StringBuilder__ToString_Z37302880(x, first_index, length):
    return substring(to_string(x), first_index, length)


def StringBuilder__Clear(x):
    clear(x.buf)
    return x


