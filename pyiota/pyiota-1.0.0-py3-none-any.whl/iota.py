"""Simple Go lang iota pattern implementation"""

# This file is a part of pyiota package
# Licensed under Do-What-The-Fuck-You-Want license
# Initially made by @jedi2light (aka Stoian Minaiev)

class iota:
  _counter = 0
  def __new__(cls):
    cls._counter += 1
    return cls._counter

class new:
  _iota_class = iota
  def __enter__(self):
    self._iota_class._counter = 0
    return self
  def __exit__(self, _, __, ___):
    self._iota_class._counter = 0

iota.new = new  # thanks to first-class classes