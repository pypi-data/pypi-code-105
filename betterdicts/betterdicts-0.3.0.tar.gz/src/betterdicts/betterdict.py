

class betterdict(dict):
  """`betterdict` is a `dict` with a few extra utility methods.

  Extra methods: `invert()`, `collate(it, type=t)`, `filter(keys=None, values=None)`

  """

  def copy(self):
    return self.__class__(super().copy())

  def invert(self):
    """Invert keys and values, returning a dictionary that maps values to keys.

    >>> betterdict((i, i**2) for i in range(10)).invert()
    {0: 0, 1: 1, 4: 2, 9: 3, 16: 4, 25: 5, 36: 6, 49: 7, 64: 8, 81: 9}

    """
    return self.__class__({v:k for k,v in self.items()})

  def collate(self, it, type=list):
    """Collate a sequence of `(k,v)` tuples or a dictionary into this dictionary.

    For each `(k,v)` in the iterator (or alternatively each pair in `items()` if
    a dict is given), if `k` already exists, then `self[k].add(v)` or
    `self[k].append(v)` is called. Otherwise `self[k]` is initialized to an
    empty collection.

    The optional keyword parameter `type` specifies the collection type. It
    currently accepts subclasses of `list` or `set`.

    Returns `self`.

    >>> betterdict().collate((i%5, i**2) for i in range(20))
    {0: [0, 25, 100, 225], 1: [1, 36, 121, 256], 2: [4, 49, 144, 289], 3: [9, 64, 169, 324], 4: [16, 81, 196, 361]}

    """
    if isinstance(it, dict):
      it = it.items()
    if issubclass(type, list):
      f = type.append
    elif issubclass(type, set):
      f = type.add
    else:
      raise ValueError(f"unknown type {type.__name__}")
    for k,v in it:
      if k in self:
        f(self[k], v)
      else:
        self[k] = type((v,))
    return self

  def filter(self, keys=None, values=None):
    """Filter keys or values, returning a new dictionary.

    - filter()

      filters k=>v pairs where bool(v) is true.

    - filter(keys=f) or filter(f)

      filters k=>v pairs where f(k) evaluates to true.

    - filter(values=f) or filter(None, f)

      filters k=>v pairs where f(v) evaluates to true.

    - filter(f,g) or filter(keys=f, values=g)

      filters k=>v pairs where f(k) *and* g(v) evaluates to true.

    """
    if keys is None and values is None:
      values = bool
    return self.__class__({
      k:v for k,v in self.items()
      if (keys is None or keys(k)) and (values is None or values(v))
    })
