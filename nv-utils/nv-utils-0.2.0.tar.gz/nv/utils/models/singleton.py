# Singleton implementation


class SingletonType(type):
    """
    Python Cookbook, 3rd edition, by David Beazley and Brian K. Jones (O’Reilly).
    Copyright 2013 David Beazley and Brian Jones, 978-1-449-34037-7.
    """
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
        return self.__instance
