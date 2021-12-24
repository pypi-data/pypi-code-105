from dotnetz.runtime import *

from dotnetz.System.IDisposable import *

class Disposable(ABC):
  """IDisposable as an abstract base class. See dotnetz.System.IDisposable.IDisposable."""

  disposed: bool

  @abstractmethod
  def dispose(self):
    self.disposed = True

  def _do_dispose(self):
    self.dispose()
    if not self.disposed:
      raise RuntimeError("self.disposed is False. (Did you forget to call super().dispose() in your def dispose(self) method?")

  def __init__(self):
    super().__init__()
    self.disposed = False
    assert isinstance(self, IDisposable)

  def __del__(self):
    self._do_dispose()

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self._do_dispose()
