import inspect

class NotNone(object):
    def __init__(self, *arg:str):
        self.NotNoneAll = False
        if len(arg) == 1 and arg[0] == '*':
            self.NotNoneAll = True
            return

        self.NotNone = arg

    def __call__(self, func):
        args_ = inspect.getfullargspec(func)

        if not self.NotNoneAll:
            if args_.varargs != None:
                raise Exception('arg list is not allowed in this function!')
            if args_.varkw != None:
                raise Exception('keyword arg list is not allowed in this function!')


        def wrappe(*args, **kwargs):

            if len(args) > 0:
                if self.NotNoneAll == True:

                    for arg in args:
                        if arg == None:
                            raise Exception(f'None is not allowed in this function!')

                    if list(kwargs.values()).__contains__(None):
                        raise Exception(f'None is not allowed in this function!')



                else:
                    for i in range(len(args)):
                        if (args[i] == None) and (self.NotNone.__contains__(args_.args[i])):
                            raise Exception(f'None is not allowed in {args_.args[i]} argument.')

                return func(*args, **kwargs)
        return wrappe