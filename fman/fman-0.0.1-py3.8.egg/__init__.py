import os
import string

'''
fman - File Manager
A Python 3 based module that can deal with non-binary files.

Written by : Md. Almas Ali

Website : almasali.net
E-mail : almas@almasali.net
Github: https://github.com/Almas-Ali/fman.git
'''

__version__ = '0.0.1'


class FileIO:
    '''FileIO is a file managing system'''

    def __init__(self, string: str = None, file=None):
        self.string = string
        self.file = file

    def read(self):
        '''Read a full file to end not for string object'''
        if self.file:
            with open(self.file, 'r') as __file:
                __f = __file.read()
                __f = ''.join(__f)

            return __f
        elif self.string:
            return self.string
        else:
            raise TypeError('Expected file object but got string')


    def get(self):
        '''To get all file attributes not for string object'''

        if self.file:
            name, ext = os.path.splitext(self.file)
            return (name, ext)
        elif self.string:
            return None
        else:
            raise TypeError('Expected file object but got string')


    def __file_operator(self):  # Hidden workers
        if self.file:
            with open(self.file, 'r') as f:
                __counter = 0
                for _ in f.readlines():
                    __counter += 1
                return __counter
        elif self.string:
            line = self.string.count('\n')
            if line == 0:
                return 1
            else:
                return line + 1
        else:
            raise TypeError('Expected file object but got string')

    def name(self):
        '''Return file name'''
        if self.file:
            return self.file
        elif self.string:
            return None
        else:
            raise TypeError('Expected file object but got string')


    def fullpath(self):
        '''Return file name'''
        if self.file:
            return os.path.abspath(self.file)
        elif self.string:
            return None
        else:
            raise TypeError('Expected file object but got string')


    def charlen(self):
        '''Counts Character length of a file'''
        if self.file:
            return len(self.read())
        elif self.string:
            return len(self.string)
        else:
            raise TypeError('Expected file object but got string')

    def linelen(self):
        '''Counts total lines of a file'''
        if self.file:
            return self.__file_operator()
        elif self.string:
            return self.__file_operator()
        else:
            raise TypeError('Expected file object but got string')

    def wordlen(self):
        '''Counts total words of a file'''
        if self.file:
            __wcount = self.read().replace('\n', ' ').split(' ')
            __wcount = [__x for __x in __wcount if __x]
            return len(__wcount)
        elif self.string:
            __wcount = self.string.replace('\n', ' ').split(' ')
            __wcount = [__x for __x in __wcount if __x]
            return len(__wcount)
        else:
            raise TypeError('Expected file object but got string')


class Filter:
    '''Filter is for text filtering.'''
    def __init__(self, text:str):
        self.text = text

    def filter(self, list:list):
        '''filter for text filtering'''
        char = string.punctuation
        number, words = 0, []
        post = self.text.lower()
        for j in char:
            post = post.replace(j, ' ')
        post = post.split(' ')
        for word in post:
            if word in list:
                number += 1
                words.append(word)
        return (number, words)


    def is_clean(self, list:list):
        val = self.filter(list)[0]
        if val == 0:
            return True
        return False
