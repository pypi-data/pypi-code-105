from __future__ import annotations
from dotnetz.runtime import *

P = ParamSpec("P")
T = TypeVar("T")

def delegate(f: Callable[P, T]) -> Callable[P, T]:
  @wraps(f)
  def inner(*args: P.args, **kwargs: P.kwargs) -> T:
    # await log_to_database()
    return f(*args, **kwargs)
  return inner

class EventHandler(Generic[T, P]):
  handlers: List[Callable[P, T]]

  def __init__(self):
    self.handlers = []

  def clone(self) -> EventHandler[T]:
    other: EventHandler[T] = EventHandler()
    for handler in self.handlers:
      other.add(handler)
    return other

  def __eq__(self, other):
    if other is None:
      return len(self.handlers) == 0
    if isinstance(other, EventHandler):
      return self.handlers == other.handlers
    return False

  def __ne__(self, other):
    return not (self == other)

  def __bool__(self):
    return self != None

  def __len__(self):
    return len(self.handlers)

  def add(self, callback: Callable[P, T]):
    self.handlers.append(callback)

  def remove(self, callback: Callable[P, T]):
    try:
      self.handlers.remove(callback)
    except ValueError:
      pass

  def __iadd__(self, callback: Callable[P, T]):
    return self.add(callback)

  def __isub__(self, callback: Callable[P, T]):
    return self.remove(callback)

  def __contains__(self, callback: Callable[P, T]):
    return callback in self.handlers

  def __call__(self, sender, event: T):
    for handler in self.handlers:
      handler(sender, event)
