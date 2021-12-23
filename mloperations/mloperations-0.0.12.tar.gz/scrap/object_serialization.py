import dill as pickle
class A:
    def foo(self):
        return 'original'

a = A()
obj_type = type(a)
obj_module = obj_type.__module__
try:
    obj_type.__module__ = '__main__'
    serialized = pickle.dumps(a)
finally:
    obj_type.__module__ = obj_module

class A:
    def foo(self):
        return 'new'

print(pickle.loads(serialized, ignore=True).foo())


if __name__ == '__main__':
    pass
