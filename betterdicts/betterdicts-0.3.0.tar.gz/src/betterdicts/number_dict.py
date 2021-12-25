from betterdicts.codeio import CodeIO
from betterdicts import betterdict
from collections import abc, Counter


def mk_dict_bin_arith(name, expr, immediate=False, elidefalse=False, with_broadcast=True):
  src = CodeIO()
  src.print(f'def {name}(self, other):')
  src.indent += 2
  res = 'self' if immediate else 'res'
  if with_broadcast:
    src.print(f'if isinstance(other, self.__class__):')
    src.indent += 2
    if not immediate:
      src.print(f'res = self.copy()')
    src.print(f'for k in other.keys():')
    src.print(f'  if r := {expr("self[k]", "other[k]")}: {res}[k] = r' if elidefalse else
              f'  {res}[k] = {expr("self[k]", "other[k]")}')
    src.indent -= 2
    src.print(f'else:')
    src.indent += 2
  if not immediate:
    src.print(f'res = self.__class__()')
  src.print(f'for k,v in self.items():')
  src.print(f'  if r := {expr("v", "other")}: {res}[k] = r' if elidefalse else
            f'  {res}[k] = {expr("v", "other")}')
  if with_broadcast:
    src.indent -= 2
  src.print(f'return {res}')
  locals, _ = src.exec()
  return locals[name]


def mk_dict_unary_arith(name, expr):
  src = CodeIO()
  src.print(f'def {name}(self, other):')
  src.print(f'  return self.__class__({{k: {expr("v")} for k,v in self.items()}})')
  locals, _ = src.exec()
  return locals[name]


def mk_dict_filter(name, expr, with_broadcast=True):
  src = CodeIO()
  src.print(f'def {name}(self, other):')
  src.indent += 2
  if with_broadcast:
    src.print(f'if isinstance(other, self.__class__):')
    src.print(f'  res = self.__class__({{k: v for k,v in self.items() if {expr("v", "other[k]")} }})')
    src.print(f'else:')
    src.indent += 2
  src.print(f'res = self.__class__({{k: v for k,v in self.items() if {expr("v", "other")} }})')
  if with_broadcast:
    src.indent -= 2
  src.print(f'return res')
  locals, _ = src.exec()
  return locals[name]


class number_dict(betterdict):
  """Acts like an `collections.Counter()` with additional arithmetic support.

  """
  __slots__ = ()

  def __init__(self, arg=None, **kwargs):
    if arg is None:
      super().__init__(**kwargs)
    elif isinstance(arg, dict):
      super().__init__(arg)
    elif isinstance(arg, abc.Sequence):
      if len(arg) and isinstance(arg[0], tuple) and len(arg[0]) == 2:
        super().__init__(arg)
      else:
        super().__init__(Counter(arg))
    elif isinstance(arg, abc.Iterable):
      arg = iter(arg)
      try:
        first = next(arg)
      except StopIteration:
        super().__init__()
      else:
        if isinstance(first, tuple) and len(first) == 2:
          super().__init__()
          self[first[0]] = first[1]
          self.update(arg)
        else:
          super().__init__(Counter(arg))
          self[first] += 1
    else:
      raise TypeError(f'not sure what to do about {type(arg)}')

  @classmethod
  def one(cls, v):
    return cls((v,))

  @classmethod
  def union(cls, it):
    ret = cls()
    for c in it:
      ret += c
    return ret

  def copy(self):
    return self.__class__(self)

  def __getitem__(self, key):
    return super().__getitem__(key) if key in self else 0

  __lt__ = mk_dict_filter(f'__lt__', lambda x, y: f'{x} < {y}')
  __gt__ = mk_dict_filter(f'__gt__', lambda x, y: f'{x} > {y}')
  __le__ = mk_dict_filter(f'__le__', lambda x, y: f'{x} <= {y}')
  __ge__ = mk_dict_filter(f'__ge__', lambda x, y: f'{x} >= {y}')

  __abs__ = mk_dict_unary_arith('__abs__', lambda x: f'abs({x})')
  __neg__ = mk_dict_unary_arith('__neg__', lambda x: f'-{x}')
  __pos__ = mk_dict_unary_arith('__pos__', lambda x: f'+{x}')

  __add__ = mk_dict_bin_arith(f'__add__', lambda x, y: f'{x} + {y}')
  __sub__ = mk_dict_bin_arith(f'__sub__', lambda x, y: f'{x} - {y}')
  __mul__ = mk_dict_bin_arith(f'__mul__', lambda x, y: f'{x} * {y}')
  __mod__ = mk_dict_bin_arith(f'__mod__', lambda x, y: f'{x} % {y}')
  __floordiv__ = mk_dict_bin_arith(f'__floordiv__', lambda x, y: f'{x} // {y}')
  __truediv__ = mk_dict_bin_arith(f'__truediv__', lambda x, y: f'{x} / {y}')
  __pow__ = mk_dict_bin_arith(f'__pow__', lambda x, y: f'{x} ** {y}')

  __iadd__ = mk_dict_bin_arith(f'__iadd__', lambda x, y: f'{x} + {y}', immediate=True)
  __isub__ = mk_dict_bin_arith(f'__isub__', lambda x, y: f'{x} - {y}', immediate=True)
  __imul__ = mk_dict_bin_arith(f'__imul__', lambda x, y: f'{x} * {y}', immediate=True)
  __imod__ = mk_dict_bin_arith(f'__imod__', lambda x, y: f'{x} % {y}', immediate=True)
  __ifloordiv__ = mk_dict_bin_arith(f'__ifloordiv__', lambda x, y: f'{x} // {y}', immediate=True)
  __itruediv__ = mk_dict_bin_arith(f'__itruediv__', lambda x, y: f'{x} / {y}', immediate=True)
  __ipow__ = mk_dict_bin_arith(f'__ipow__', lambda x, y: f'{x} ** {y}', immediate=True)

  __radd__ = mk_dict_bin_arith(f'__radd__', lambda x, y: f'{y} + {x}', with_broadcast=False)
  __rsub__ = mk_dict_bin_arith(f'__rsub__', lambda x, y: f'{y} - {x}', with_broadcast=False)
  __rmul__ = mk_dict_bin_arith(f'__rmul__', lambda x, y: f'{y} * {x}', with_broadcast=False)
  __rmod__ = mk_dict_bin_arith(f'__rmod__', lambda x, y: f'{y} % {x}', with_broadcast=False)
  __rfloordiv__ = mk_dict_bin_arith(f'__rfloordiv__', lambda x, y: f'{y} // {x}', with_broadcast=False)
  __rtruediv__ = mk_dict_bin_arith(f'__rtruediv__', lambda x, y: f'{y} / {x}', with_broadcast=False)
  __rpow__ = mk_dict_bin_arith(f'__rpow__', lambda x, y: f'{y} ** {x}', with_broadcast=False)

  @classmethod
  def sum(cls, it):
    res = cls()
    for x in it:
      res += x
    return res

  @classmethod
  def prod(cls, it):
    res = cls()
    for x in it:
      res *= x
    return res


__all__ = ('number_dict', )
