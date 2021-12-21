# Datatype classes

class Docs:
    '''To set docs string.'''

    def __init__(self, string: str = None):
        self.string = string

    def __str__(self):
        return self.string


class Version:
    '''To set version string.'''

    def __init__(self, string: str = None):
        self.string = string

    def __str__(self):
        return self.string

    def major(self):
        '''To get the major version code.'''
        return int(self.string.split('.')[0])

    def minor(self):
        '''To get the minor version code.'''
        return int(self.string.split('.')[1])

    def bugfix(self):
        '''To get the bugfix version code.'''
        return int(self.string.split('.')[2])


class Author:
    '''To set author string.'''

    def __init__(self, string: str = None):
        self.string = string

    def __str__(self):
        return self.string


class Dev_Status:
    '''To set development status string.'''

    def __init__(self, string: str = None):
        self.string = string

    def __str__(self):
        return self.string


class Copyright:
    '''To set copyright string.'''

    def __init__(self, string: str = None):
        self.string = string

    def __str__(self):
        return self.string


class License:
    '''To set license string.'''

    def __init__(self, string: str = None):
        self.string = string

    def __str__(self):
        return self.string


class ClassExplore:
    '''Learn more about Python class and you can create new magic method here.'''

    def __init__(self, cls: any):
        self.cls = cls

    def __version__(self):
        '''Version string.'''
        return '1.0.0'

    def __author__(self):
        '''Author string.'''
        return 'Md. Almas Ali'

    def __dev_status__(self):
        return f'{self.version()} alpha'

    def __copyright__(self):
        return 'copyright 2021'

    def __license__(self):
        return '''\
This is the Licence of this class.
This class is made by Md. Almas Ali and certified by MIT.

©2021
'''

    def docs(self):
        '''To get docs string.'''
        try:
            return Docs(self.cls.__doc__)
        except AttributeError:
            raise AttributeError('docs string not found !')

    def version(self):
        '''To get version string.'''
        try:
            return Version(self.cls.__version__(self))
        except AttributeError:
            raise AttributeError('version string not found !')

    def author(self):
        '''To get author name string.'''
        try:
            return Author(self.cls.__author__(self))
        except AttributeError:
            raise AttributeError('author name string not found !')

    def dev_status(self):
        '''To get development status string.'''
        try:
            return Dev_Status(self.cls.__dev_status__(self))
        except AttributeError:
            raise AttributeError('development status string not found !')

    def copyright(self):
        '''To get copyright string.'''
        try:
            return Copyright(self.cls.__copyright__(self))
        except AttributeError:
            raise AttributeError('copyright string not found !')

    def license(self):
        '''To get license string.'''
        try:
            return License(self.cls.__license__(self))
        except AttributeError:
            raise AttributeError('license string not found !')
