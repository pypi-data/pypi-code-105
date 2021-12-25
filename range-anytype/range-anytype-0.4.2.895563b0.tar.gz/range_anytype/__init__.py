#!/usr/bin/env python
# coding=UTF-8

"""
range-anytype

Not an accurate Range for float. For best experience, you can use
decimal.Decimal or fractions.Fraction instead of float.
"""

try :
    raw_input
except NameError :
    ispy3 = 1
else :
    ispy3 = 0

class Range(object) :
    """Range(stop) or Range(start, stop[, step])"""
    
    if ispy3 :
        def __init__(self, *args) :
            """Initialize self.  See help(type(self)) for accurate signature."""
            
            if len(args) == 0 :
                raise TypeError("Range expected 1 argument, got 0")
            elif len(args) == 1 : # Range(stop)
                self.__start = 0
                self.__stop = args[0]
                self.__step = 1
                return None
            elif len(args) == 2 : # Range(start, stop)
                self.__start = args[0]
                self.__stop = args[1]
                self.__step = 1
                return None
            elif len(args) == 3 : # Range(start, stop, step)
                self.__start = args[0]
                self.__stop = args[1]
                self.__step = args[2]
                return None
            raise TypeError("Range expected at most 3 arguments, got %d"%\
                            len(args))
    else :
        def __init__(self, *args) :
            """x.__init__(...) initializes x; see help(type(x)) for signature"""
            
            if len(args) == 0 :
                raise TypeError("Range expected 1 argument, got 0")
            elif len(args) == 1 : # Range(stop)
                self.__start = 0
                self.__stop = args[0]
                self.__step = 1
                return None
            elif len(args) == 2 : # Range(start, stop)
                self.__start = args[0]
                self.__stop = args[1]
                self.__step = 1
                return None
            elif len(args) == 3 : # Range(start, stop, step)
                self.__start = args[0]
                self.__stop = args[1]
                self.__step = args[2]
                return None
            raise TypeError("Range expected at most 3 arguments, got %d"%\
                            len(args))
    
    start = property(lambda self: self.__start)
    
    stop = property(lambda self: self.__stop)
    
    step = property(lambda self: self.__step)
    
    if ispy3 :
        def __repr__(self) :
            """Return repr(self)."""
            
            if self.step == 1 :
                return "Range(%s, %s)" % (repr(self.start), repr(self.stop))
            return "Range(%s, %s, %s)" % (repr(self.start), repr(self.stop),
                                          repr(self.step))
        
        def __iter__(self) :
            """Implement iter(self)."""
            
            self.__a = self.start
            return self
        
        def __next__(self) :
            """Implement next(self)."""
            
            try :
                if self.__a + self.step > self.__a :
                    if self.__a >= self.stop :
                        del self.__a
                        raise StopIteration
                elif self.__a + self.step < self.__a :
                    if self.__a <= self.stop :
                        del self.__a
                        raise StopIteration
                else :
                	raise ValueError("Range() arg 3 must not be zero")
            except AttributeError :
                raise StopIteration
            res = self.__a
            self.__a += self.step
            return res
        
        def __bool__(self) :
            """self != 0"""
            
            return tuple(self) != ()
        
        def __len__(self) :
            """Return len(self)."""
            
            res = 0
            for i in type(self)(self.start, self.stop, self.step) :
                res += 1
            return res
        
        def __contains__(self, key) :
            """Return key in self."""
            
            return key in tuple(self)
        
        def __getitem__(self, key) :
            """Return self[key]."""
            
            try :
                if isinstance(key, slice) :
                    if key.step != None :
                        if key.step + key.step == key.step :
                            raise ValueError("slice step cannot be zero")
                    k = (key.step, 1)[key.step==None]
                    labb = tuple(self)[key]
                    return type(self)(labb[0],labb[-1]+self.step*k, self.step*k)
            except NameError :
                pass
            try :
                return tuple(self)[key]
            except IndexError :
                raise IndexError("Range object index out of range")
        
        def __eq__(self, value) :
            """Return self==value."""
            
            try :
                if self.start == value.start and self.stop == value.stop and \
                   self.step == value.step :
                    return True
                return tuple(self) == tuple(value)
            except (AttributeError, TypeError) :
                return False
        
        def __ne__(self, value) :
           """Return self!=value."""
           
           return not self == value
        
        def __hash__(self) :
            """Return hash(self)."""
            
            return hash(tuple(self))
    else :
        def __repr__(self) :
            """x.__repr__() <==> repr(x)"""
            
            if self.step == 1 :
                return "Range(%s, %s)" % (repr(self.start), repr(self.stop))
            return "Range(%s, %s, %s)" % (repr(self.start), repr(self.stop),
                                          repr(self.step))
        
        def __iter__(self) :
            """x.__iter__() <==> iter(x)"""
            
            self.__a = self.start
            return self
        
        def next(self) :
            """x.next() -> the next value, or raise StopIteration"""
            
            try :
                if self.__a + self.step > self.__a :
                    if self.__a >= self.stop :
                        del self.__a
                        raise StopIteration
                elif self.__a + self.step < self.__a :
                    if self.__a <= self.stop :
                        del self.__a
                        raise StopIteration
                else :
                	raise ValueError("Range() arg 3 must not be zero")
            except AttributeError :
                raise StopIteration
            res = self.__a
            self.__a += self.step
            return res
        
        def __bool__(self) :
            """self != 0"""
            
            return tuple(self) != ()
        
        def __len__(self) :
            """x.__len__() <==> len(x)"""
            
            res = 0
            for i in type(self)(self.start, self.stop, self.step) :
                res += 1
            return res
        
        def __contains__(self, key) :
            """x.__contains__(y) <==> y in x"""
            
            return key in tuple(self)
        
        def __getitem__(self, key) :
            """x.__getitem__(y) <==> x[y]"""
            
            try :
                if isinstance(key, slice) :
                    if key.step != None :
                        if key.step + key.step == key.step :
                            raise ValueError("slice step cannot be zero")
                    k = (key.step, 1)[key.step==None]
                    labb = tuple(self)[key]
                    return type(self)(labb[0],labb[-1]+self.step*k, self.step*k)
            except NameError :
                pass
            try :
                return tuple(self)[key]
            except IndexError :
                raise IndexError("Range object index out of range")
        
        def __eq__(self, value) :
            """x.__eq__(y) <==> x==y"""
            
            try :
                if self.start == value.start and self.stop == value.stop and \
                   self.step == value.step :
                    return True
                return tuple(self) == tuple(value)
            except (AttributeError, TypeError) :
                return False
        
        def __ne__(self, value) :
           """x.__ne__(y) <==> x!=y"""
           
           return not self == value
        
        def __hash__(self) :
            """x.__hash__() <==> hash(x)"""
            
            return hash(tuple(self))
    
    def count(self, value) :
        return tuple(self).count(value)
    
    def index(self, value) :
        """Raise ValueError if the value is not present."""
        
        try :
            return tuple(self).index(value)
        except ValueError :
            raise ValueError("%s is not in Range"%repr(value))
    
class ProtectedRange(Range) :
    """ProtectedRange(stop) or peotected_Range(start, stop[, step])"""
    
    if ispy3 :
        def __init__(self, *args) :
            """Initialize self.  See help(type(self)) for accurate signature."""
            
            if len(args) == 0 :
                raise TypeError("ProtectedRange expected 1 argument, got 0")
            elif len(args) == 1 :
                self.__start = 0
                self.__stop = args[0]
                self.__step = 1
                return None
            elif len(args) == 2 :
                self.__start = args[0]
                self.__stop = args[1]
                self.__step = 1
                return None
            elif len(args) == 3 :
                self.__start = args[0]
                self.__stop = args[1]
                self.__step = args[2]
                return None
            raise TypeError("ProtectedRange expected at most 3 arguments, got %\
d"%len(args))
    else :
        def __init__(self, *args) :
            """Initialize self.  See help(type(self)) for accurate signature."""
            
            if len(args) == 0 :
                raise TypeError("ProtectedRange expected 1 argument, got 0")
            elif len(args) == 1 :
                self.__start = 0
                self.__stop = args[0]
                self.__step = 1
                return None
            elif len(args) == 2 :
                self.__start = args[0]
                self.__stop = args[1]
                self.__step = 1
                return None
            elif len(args) == 3 :
                self.__start = args[0]
                self.__stop = args[1]
                self.__step = args[2]
                return None
            raise TypeError("ProtectedRange expected at most 3 arguments, got %\
d"%len(args))
    
    start = property(lambda self: self.__start)
    
    stop = property(lambda self: self.__stop)
    
    step = property(lambda self: self.__step)
    
    if ispy3 :
        def __repr__(self) :
            """Return repr(self)."""
            
            if self.step == 1 :
                return "ProtectedRange(%s, %s)" % (repr(self.start),
                                                   repr(self.stop))
            return "ProtectedRange(%s, %s, %s)" % (repr(self.start),
                                                   repr(self.stop),
                                                   repr(self.step))
        
        def __iter__(self) :
            """Implement iter(self)."""
            
            try :
                self.start + self.start - self.start # protect
            except (TypeError, ValueError, MemoryError) :
                raise ValueError("protected range")
            self.__a = self.start
            return self
        
        def __next__(self) :
            """Implement next(self)."""
            
            try :
                if self.__a + self.step > self.__a :
                    if self.__a >= self.stop :
                        del self.__a
                        raise StopIteration
                elif self.__a + self.step < self.__a :
                    if self.__a <= self.stop :
                        del self.__a
                        raise StopIteration
                else :
                	raise ValueError("ProtectedRange() arg 3 must not be zero")
            except AttributeError :
                raise StopIteration
            res = self.__a
            self.__a += self.step
            return res
        
        def __getitem__(self, key) :
            """Return self[key]."""
            
            try :
                if isinstance(key, slice) :
                    if key.step != None :
                        if key.step + key.step == key.step :
                            raise ValueError("slice step cannot be zero")
                    k = (key.step, 1)[key.step==None]
                    labb = tuple(self)[key]
                    return type(self)(labb[0],labb[-1]+self.step*k, self.step*k)
            except NameError :
                pass
            try :
                return tuple(self)[key]
            except IndexError :
                raise IndexError("ProtectedRange object index out of range")
    else :
        def __repr__(self) :
            """x.__repr__() <==> repr(x)"""
            
            if self.step == 1 :
                return "ProtectedRange(%s, %s)" % (repr(self.start),
                                                   repr(self.stop))
            return "ProtectedRange(%s, %s, %s)" % (repr(self.start),
                                                   repr(self.stop),
                                                   repr(self.step))
        
        def __iter__(self) :
            """x.__iter__() <==> iter(x)"""
            
            try :
                self.start + self.start - self.start # protect
            except (TypeError, ValueError, MemoryError) :
                raise ValueError("protected range")
            self.__a = self.start
            return self
        
        def next(self) :
            """x.next() -> the next value, or raise StopIteration"""
            
            try :
                if self.__a + self.step > self.__a :
                    if self.__a >= self.stop :
                        del self.__a
                        raise StopIteration
                elif self.__a + self.step < self.__a :
                    if self.__a <= self.stop :
                        del self.__a
                        raise StopIteration
                else :
                	raise ValueError("ProtectedRange() arg 3 must not be zero")
            except AttributeError :
                raise StopIteration
            res = self.__a
            self.__a += self.step
            return res
        
        def __getitem__(self, key) :
            """x.__getitem__(y) <==> x[y]"""
            
            try :
                if isinstance(key, slice) :
                    if key.step != None :
                        if key.step + key.step == key.step :
                            raise ValueError("slice step cannot be zero")
                    k = (key.step, 1)[key.step==None]
                    labb = tuple(self)[key]
                    return type(self)(labb[0],labb[-1]+self.step*k, self.step*k)
            except NameError :
                pass
            try :
                return tuple(self)[key]
            except IndexError :
                raise IndexError("ProtectedRange object index out of range")
    
    def index(self, value) :
        try :
            return tuple(self).index(value)
        except ValueError :
            raise ValueError("%s is not in ProtectedRange"%repr(value))

del ispy3
