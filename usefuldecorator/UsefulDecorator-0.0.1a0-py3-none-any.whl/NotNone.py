import inspect

class NotNone(object):
    def __init__(self, *arg:str):
        self.NotNone = arg

    def __call__(self, func):
        args_ = inspect.getfullargspec(func)

        if args_.varargs != None:
            raise Exception('arglist is not allowed in NotNone function!')

        def wrappe(*args, **kwargs):
            for i in range(len(args)):
                if (args[i] == None) and (self.NotNone.__contains__(args_.args[i])):
                    raise Exception(f'None is not allowed in {args_.args[i]} argument.')
            return func(*args, **kwargs)
        return wrappe