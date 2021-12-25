import pickle
import copyreg
from pathlib import Path
from functools import wraps

from betterdicts import betterdict

def make_wrapper(name, meth):
  def _override(self, /, *args, **kwargs):
    ret = meth(self, *args, **kwargs)
    with self._path.open('wb') as fil:
      pickle.dump(self, fil)
    return ret
  return wraps(meth)(_override)


class PDMeta(type):
  def __new__(cls, name, bases, ns):
    for meth_name in '__setitem__ __delitem__ clear update pop popitem setdefault'.split():
      ns[meth_name] = make_wrapper(meth_name, getattr(dict, meth_name))
    return type(name, bases, ns)


class persistent_dict(betterdict, metaclass=PDMeta):
  """A dict that auto-saves itself to disk _whenever it is modified_.

  Simply creating the instance `persistent_dict()` will auto-load the previous
  content from the default file `cache.pickle` in the current directory. To
  specify another file use `persistent_dict(cache_file="otherfile")`.

  Any modifications to the dictionary will be synced to this file. Note that
  "deep" changes are not detected -- i.e. modifications to a list stored in the
  dictionary -- thus it works best for simple, flat values.

  If a a lot modifications need to be done in one go (e.g. a tight loop), you
  can use a regular `dict()` and then periodically invoke `obj.update(work)` to
  update and save.

  Warning:: Use separate files for separate objects. Two separate
  `persistent_dict()` objects bound to the same file will *not* stay in sync.
  Whichever object was modified (and thus saved) last will be what is reflected
  in the saved file.

  """
  __slots__ = ('_path',)
  DEFAULT_CACHE_FILE = Path.cwd() / 'cache.pickle'

  def __new__(cls, *args, cache_file=None, skip_load=False, **kwargs):
    # Allows the default to be changed, as opposed to a keyword argument.
    pth = cls.DEFAULT_CACHE_FILE if not cache_file else Path(cache_file)
    if not skip_load and pth.is_file():
      with pth.open('rb') as fil:
        obj = pickle.load(fil)
    else:
      obj = dict.__new__(cls)
      if args or kwargs:
        obj.__init__(*args, **kwargs)
    obj._path = pth
    return obj

  def __init__(self, *args, cache_file=None, skip_load=True, **kwargs):
    super().__init__(*args, **kwargs)

  # Needed to prevent dict() from giving its own reduce tuple.
  def __reduce_ex__(self, pv):
    return (copyreg.__newobj_ex__, (persistent_dict, (dict(self), ), {'skip_load': True}))

  # The meta class has injecting save-logic in the regular dict() method
  # overrides.

  def reload(self):
    super().clear()
    if pth._path.is_file():
      with pth.open('rb') as fil:
        super().extend(pickle.load(fil))
    return self

  def save(self):
    with self._path.open('wb') as fil:
      pickle.dump(self, fil)
    return self

  def get_or(self, k, f):
    """Better than `dict.setdefault()` when it's expensive to construct the default.

    """
    if k not in self:
      self[k] = f()
    return self[k]


__all__ = ('persistent_dict',)
