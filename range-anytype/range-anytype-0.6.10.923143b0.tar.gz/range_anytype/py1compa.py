#!/usr/bin/env python
# coding=UTF-8

try :
    StopIteration
except NameError :
    class StopIteration(Exception) :
        pass

class Range :
    def __init__(self, *args) :
        if len(args) == 0 :
            raise TypeError("Range expected 1 argument, got 0")
        elif len(args) == 1 : # Range(stop)
            self.start = 0
            self.stop = args[0]
            self.step = 1
            return None
        elif len(args) == 2 : # Range(start, stop)
            self.start = args[0]
            self.stop = args[1]
            self.step = 1
            return None
        elif len(args) == 3 : # Range(start, stop, step)
            self.start = args[0]
            self.stop = args[1]
            self.step = args[2]
            return None
        raise TypeError("Range expected at most 3 arguments, got %d"%len(args))
    
    def __repr__(self) :
        if self.step == 1 :
            return "Range(%s, %s)" % (repr(self.start), repr(self.stop))
        return "Range(%s, %s, %s)" % (repr(self.start), repr(self.stop),
                                      repr(self.step))
    
    def __iter__(self) :
        self.__a = self.start
        return self
    
    try :
        StopIteration
    except NameError :
        StopIteration = StopIteration
    
    def next(self) :
        try :
            if self.__a + self.step > self.__a :
                if self.__a >= self.stop :
                    del self.__a
                    try :
                        StopIteration
                    except NameError :
                        raise self.StopIteration
                    else :
                        raise StopIteration
            elif self.__a + self.step < self.__a :
                if self.__a <= self.stop :
                    del self.__a
                    try :
                        StopIteration
                    except NameError :
                        raise self.StopIteration
                    else :
                        raise StopIteration
            else :
            	raise ValueError("Range() arg 3 must not be zero")
        except AttributeError :
            try :
                StopIteration
            except NameError :
                raise self.StopIteration
            else :
                raise StopIteration
        res = self.__a
        self.__a = self.__a + self.step
        return res
    
    def to_tuple(self) :
        res = ()
        try :
            StopIteration
        except NameError :
            try :
                asatemp = Range(self.start, self.stop, self.step).__iter__()
                while 1 :
                    res = res + (asatemp.next(),)
            except self.StopIteration :
                pass
        else :
            try :
                asatemp = Range(self.start, self.stop, self.step).__iter__()
                while 1 :
                    res = res + (asatemp.next(),)
            except StopIteration :
                pass
        return res
    
    def __bool__(self) :
        return self.to_tuple() != ()
    
    def __len__(self) :
        return len(self.to_tuple())
    
    def __contains__(self, key) :
        return key in self.to_tuple()
    
    def __getitem__(self, key) :
        try :
            if type(key) == type(slice(None)) :
                if key.step != None :
                    if key.step + key.step == key.step :
                        raise ValueError("slice step cannot be zero")
                k = (key.step, 1)[key.step==None]
                labb = self.to_tuple()[key]
                return Range(labb[0], labb[-1]+self.step*k, self.step*k)
        except NameError :
            pass
        try :
            return self.to_tuple()[key]
        except IndexError :
            raise IndexError("Range object index out of range")
    
    def __getslice__(self, x, y) :
        labb = self.to_tuple()[x:y]
        return Range(labb[0], labb[-1]+self.step, self.step)
    
    def __eq__(self, value) :
        try :
            if self.start == value.start and self.stop == value.stop and \
               self.step == value.step :
                return 1
            return self.to_tuple() == tuple(value)
        except (AttributeError, TypeError) :
            return 0
    
    def __ne__(self, value) :
        return not self == value
    
    def __hash__(self) :
        return hash(self.to_tuple())
    
    def count(self, value) :
        return self.to_tuple().count(value)
    
    def index(self, value) :
        try :
            return self.to_tuple().index(value)
        except ValueError :
            raise ValueError("%s is not in Range"%repr(value))
    
class ProtectedRange(Range) :
    def __init__(self, *args) :
        if len(args) == 0 :
            raise TypeError("ProtectedRange expected 1 argument, got 0")
        elif len(args) == 1 :
            self.start = 0
            self.stop = args[0]
            self.step = 1
            return None
        elif len(args) == 2 :
            self.start = args[0]
            self.stop = args[1]
            self.step = 1
            return None
        elif len(args) == 3 :
            self.start = args[0]
            self.stop = args[1]
            self.step = args[2]
            return None
        raise TypeError("ProtectedRange expected at most 3 arguments, got %d"%\
                        len(args))
    
    def __repr__(self) :
        if self.step == 1 :
            return "ProtectedRange(%s, %s)" % (repr(self.start),
                                               repr(self.stop))
        return "ProtectedRange(%s, %s, %s)" % (repr(self.start),
                                               repr(self.stop), repr(self.step))
    
    def __iter__(self) :
        try :
            self.start + self.start - self.start # protect
        except (TypeError, ValueError) :
            raise ValueError("protected range")
        self.__a = self.start
        return self
    
    def next(self) :
        try :
            if self.__a + self.step > self.__a :
                if self.__a >= self.stop :
                    del self.__a
                    try :
                        StopIteration
                    except NameError :
                        raise self.StopIteration
                    else :
                        raise StopIteration
            elif self.__a + self.step < self.__a :
                if self.__a <= self.stop :
                    del self.__a
                    try :
                        StopIteration
                    except NameError :
                        raise self.StopIteration
                    else :
                        raise StopIteration
            else :
            	raise ValueError("ProtectedRange() arg 3 must not be zero")
        except AttributeError :
            try :
                StopIteration
            except NameError :
                raise self.StopIteration
            else :
                raise StopIteration
        res = self.__a
        self.__a = self.__a + self.step
        return res
    
    def to_tuple(self) :
        res = ()
        try :
            StopIteration
        except NameError :
            try :
                asatemp = ProtectedRange(self.start, self.stop,
                                         self.step).__iter__()
                while 1 :
                    res = res + (asatemp.next(),)
            except self.StopIteration :
                pass
        else :
            try :
                asatemp = ProtectedRange(self.start, self.stop,
                                         self.step).__iter__()
                while 1 :
                    res = res + (asatemp.next(),)
            except StopIteration :
                pass
        return res
    
    def __getitem__(self, key) :
        try :
            if type(key) == type(slice(None)) :
                if key.step != None :
                    if key.step + key.step == key.step :
                        raise ValueError("slice step cannot be zero")
                k = (key.step, 1)[key.step==None]
                labb = self.to_tuple()[key]
                return ProtectedRange(labb[0],labb[-1]+self.step*k, self.step*k)
        except NameError :
            pass
        try :
            return self.to_tuple()[key]
        except IndexError :
            raise IndexError("ProtectedRange object index out of range")
    
    def __getslice__(self, x, y) :
        labb = self.to_tuple()[x:y]
        return ProtectedRange(labb[0], labb[-1]+self.step, self.step)
    
    def index(self, value) :
        try :
            return self.to_tuple().index(value)
        except ValueError :
            raise ValueError("%s is not in ProtectedRange"%repr(value))
