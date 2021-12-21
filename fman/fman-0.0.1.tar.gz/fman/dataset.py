class Array:
    '''Array is a custom datatype for global use case.'''

    def __init__(self, *args):
        '''Array takes different values to create arrays.'''
        if args is None:
            self.list = []
        else:
            self.list = list(args)

    def push(self, value: any):
        '''To add a new value in array to end.'''
        self.list.append(value)

    def insert(self, position: int = 0, value: any = None):
        '''To insert a value in array in anywhere. As default it add in front.'''
        self.list.insert(position, value)

    def pop(self):
        '''To remove last value of array.'''
        self.list = self.list[:-1:]
        # return self.list

    def peek(self, index: int):
        '''To get a value by its index number.'''
        return self.list[index]

    def remove(self, value: any):
        '''To remove a value from array.'''
        self.list.remove(value)

    def find(self, value: any):
        '''To find any value in array.'''
        num = 0
        for l in self.list:
            if l == value:
                return num
            num += 1
        return -1

    def count(self, value: any):
        '''To count any repeated value in array.'''
        # return self.list.count(value)
        num = 0
        for l in self.list:
            if l == value:
                num += 1
        return num

    def sort(self):
        '''To sort the array.'''
        self.__cast(self.list).sort()

    def reverse(self):
        '''To reverse array.'''
        self.list = self.list[::-1]

    def clear(self):
        '''To clear array.'''
        self.list = []

    def len(self):
        '''To get length of array.'''
        return len(self.list)

    def slice(self, start: int = None, end: int = None, jump: int = None):
        '''To slice array.'''
        return self.__return_value(self.list[start:end:jump])

    def q(self):
        '''To set a sequential task.'''
    pass

    def foreach(self, callback):
        '''Looping all values.'''
        num = 0
        for val in self.list:
            num += 1
            try:
                callback(val)
            except:
                try:
                    callback(val, num)
                except:
                    pass

    def typecast(self, value: any):
        '''To type cast anything to Array object.'''
        if type(value) == list or type(value) == set or type(value) == tuple:
            a = Array()
            for v in value:
                a.push(v)
            return a
        elif type(value) == dict:
            raise ValueError('can\'t typecast dict object.')
        else:
            raise TypeError('unknown value receive.')

    def __str__(self):
        '''To return array object.'''
        return f'<{str(self.list)[1:-1]}>'

    def __add__(self, *value):
        '''To add array instances.'''
        arr = Array()
        for x in self.list:
            arr.push(x)
        for x in value:
            for b in x:
                arr.push(b)
        return arr

    def __getitem__(self, position):
        '''To get array iterate able and sliceable.'''
        return self.list[position]

    def __len__(self):
        '''To get len of array.'''
        return len(self.list)

    def __reversed__(self):
        '''To reversed the array instance.'''
        return self.list[::-1]

    def __repr__(self):
        '''To get representative string.'''
        return f'<{str(self.list)[1:-1]}>'

    def __cast(self, value):
        '''To cast array object to list. (Internal use only)'''
        return str(value)[1:-1].replace('\'', '').split(',')

    @staticmethod
    def __return_value(value):
        '''To get array instance. (Internal use only)'''
        return f'<{str(value)[1:-1]}>'
