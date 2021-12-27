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
    """Range(stop) or Range(start, stop[, step])
Like built-in type 'range' or 'xrange', Range is not immutable."""
    
    if ispy3 :
        def __init__(self, *args) :
            """Initialize self.  See help(type(self)) for accurate signature."""
            
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
            raise TypeError("Range expected at most 3 arguments, got %d"%\
                            len(args))
    else :
        def __init__(self, *args) :
            """x.__init__(...) initializes x; see help(type(x)) for signature"""
            
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
            raise TypeError("Range expected at most 3 arguments, got %d"%\
                            len(args))
    
    if ispy3 :
        def __delattr__(self, name) :
            """Execute delattr(self, name)."""
            
            raise AttributeError("%s cannot be deleted" % name)
        
        def __setattr__(self, name, value) :
            """Execute setattr(self, name, value)."""
            
            if name in ("start", "stop", "step") :
                if not hasattr(self, name) :
                    self.__dict__[name] = value
                else :
                    raise AttributeError("can't set attribute")
            else :
                raise AttributeError("can't set attribute")
        
        def __repr__(self) :
            """Return repr(self)."""
            
            if self.step == 1 :
                return "Range(%s, %s)" % (repr(self.start), repr(self.stop))
            return "Range(%s, %s, %s)" % (repr(self.start), repr(self.stop),
                                          repr(self.step))
        
        class Range_iterator(object) :
            def __init__(self, start, stop, step) :
                self.__start = start
                self.__stop = stop
                self.__step = step
            
            def __iter__(self) :
                """Implement iter(self)."""
                
                return self
            
            def __next__(self) :
                """Implement next(self)."""
                
                if hasattr(self, "_Range_iterator__a") :
                    try :
                        if self.__a + self.__step > self.__a :
                            if self.__a >= self.__stop :
                                del self.__a
                                raise StopIteration
                        elif self.__a + self.__step < self.__a :
                            if self.__a <= self.__stop :
                                del self.__a
                                raise StopIteration
                        else :
                            raise ValueError("Range() arg 3 must not be zero")
                    except AttributeError :
                        raise StopIteration
                    res = self.__a
                    self.__a += self.__step
                    return res
                else :
                    self.__a = self.__start
                    self.__next__()
                    return self.__start
            
            def __setattr__(self, name, value) :
                if name in ("_Range_iterator__start", "_Range_iterator__stop",
                            "_Range_iterator__step", "_Range_iterator__a") :
                    if not hasattr(self, name) :
                        self.__dict__[name] = value
                    else :
                        if name != "_Range_iterator__a" :
                            raise AttributeError("can't set attribute")
                        else :
                            self.__dict__[name] = value
                else :
                    raise AttributeError("can't set attribute")
            
            def __delattr__(self, name) :
                if name in ("_Range_iterator__start", "_Range_iterator__stop",
                            "_Range_iterator__step", "_Range_iterator__a") :
                    if name != "_Range_iterator__a" :
                        raise AttributeError("can't delete attribute")
                    else :
                        del self.__dict__[name]
                else :
                    raise AttributeError("can't delete attribute")
        
        def __iter__(self) :
            """Implement iter(self)."""
            
            return type(self).Range_iterator(self.start, self.stop, self.step)
        
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
        def __delattr__(self, name) :
            """Execute delattr(self, name)."""
            
            raise AttributeError("%s cannot be deleted" % name)
        
        def __setattr__(self, name, value) :
            """Execute setattr(self, name, value)."""
            
            if name in ("start", "stop", "step") :
                if not hasattr(self, name) :
                    self.__dict__[name] = value
                else :
                    raise AttributeError("can't set attribute")
            else :
                raise AttributeError("can't set attribute")
        
        def __repr__(self) :
            """x.__repr__() <==> repr(x)"""
            
            if self.step == 1 :
                return "Range(%s, %s)" % (repr(self.start), repr(self.stop))
            return "Range(%s, %s, %s)" % (repr(self.start), repr(self.stop),
                                          repr(self.step))
        
        class Range_iterator(object) :
            def __init__(self, start, stop, step) :
                self.__start = start
                self.__stop = stop
                self.__step = step
            
            def __iter__(self) :
                """x.__iter__() <==> iter(x)"""
                
                return self
            
            def next(self) :
                """x.next() -> the next value, or raise StopIteration"""
                
                if hasattr(self, "_Range_iterator__a") :
                    try :
                        if self.__a + self.__step > self.__a :
                            if self.__a >= self.__stop :
                                del self.__a
                                raise StopIteration
                        elif self.__a + self.__step < self.__a :
                            if self.__a <= self.__stop :
                                del self.__a
                                raise StopIteration
                        else :
                            raise ValueError("Range() arg 3 must not be zero")
                    except AttributeError :
                        raise StopIteration
                    res = self.__a
                    self.__a += self.__step
                    return res
                else :
                    self.__a = self.__start
                    self.next()
                    return self.__start
            
            def __setattr__(self, name, value) :
                if name in ("_Range_iterator__start", "_Range_iterator__stop",
                            "_Range_iterator__step", "_Range_iterator__a") :
                    if not hasattr(self, name) :
                        self.__dict__[name] = value
                    else :
                        if name != "_Range_iterator__a" :
                            raise AttributeError("can't set attribute")
                        else :
                            self.__dict__[name] = value
                else :
                    raise AttributeError("can't set attribute")
            
            def __delattr__(self, name) :
                if name in ("_Range_iterator__start", "_Range_iterator__stop",
                            "_Range_iterator__step", "_Range_iterator__a") :
                    if name != "_Range_iterator__a" :
                        raise AttributeError("can't delete attribute")
                    else :
                        del self.__dict__[name]
                else :
                    raise AttributeError("can't delete attribute")
        
        def __iter__(self) :
            """x.__iter__() <==> iter(x)"""
            
            return type(self).Range_iterator(self.start, self.stop, self.step)
        
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
    """ProtectedRange(stop) or peotected_Range(start, stop[, step])
Like built-in type 'range' or 'xrange', ProtectedRange is not immutable."""
    
    if ispy3 :
        def __init__(self, *args) :
            """Initialize self.  See help(type(self)) for accurate signature."""
            
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
            raise TypeError("ProtectedRange expected at most 3 arguments, got %\
d"%len(args))
    else :
        def __init__(self, *args) :
            """x.__init__(...) initializes x; see help(type(x)) for signature"""
            
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
            raise TypeError("ProtectedRange expected at most 3 arguments, got %\
d"%len(args))
    
    if ispy3 :
        def __delattr__(self, name) :
            """Execute delattr(self, name)."""
            
            raise AttributeError("%s cannot be deleted" % name)
        
        def __setattr__(self, name, value) :
            """Execute setattr(self, name, value)."""
            
            if name in ("start", "stop", "step") :
                if not hasattr(self, name) :
                    self.__dict__[name] = value
                else :
                    raise AttributeError("can't set attribute")
            else :
                raise AttributeError("can't set attribute")
        
        def __repr__(self) :
            """Return repr(self)."""
            
            if self.step == 1 :
                return "ProtectedRange(%s, %s)" % (repr(self.start),
                                                   repr(self.stop))
            return "ProtectedRange(%s, %s, %s)" % (repr(self.start),
                                                   repr(self.stop),
                                                   repr(self.step))
        
        class ProtectedRange_iterator(object) :
            def __init__(self, start, stop, step) :
                self.__start = start
                self.__stop = stop
                self.__step = step
            
            def __iter__(self) :
                """Implement iter(self)."""
                
                return self
            
            def __next__(self) :
                """Implement next(self)."""
                
                if hasattr(self, "_ProtectedRange_iterator__a") :
                    try :
                        if self.__a + self.__step > self.__a :
                            if self.__a >= self.__stop :
                                del self.__a
                                raise StopIteration
                        elif self.__a + self.__step < self.__a :
                            if self.__a <= self.__stop :
                                del self.__a
                                raise StopIteration
                        else :
                            raise ValueError("ProtectedRange() arg 3 must not b\
e zero")
                    except AttributeError :
                        raise StopIteration
                    res = self.__a
                    self.__a += self.__step
                    return res
                else :
                    self.__a = self.__start
                    self.__next__()
                    return self.__start
            
            def __setattr__(self, name, value) :
                if name in ("_ProtectedRange_iterator__start", "_ProtectedRange\
_iterator__stop", "_ProtectedRange_iterator__step", "_ProtectedRange_iterator__\
a") :
                    if not hasattr(self, name) :
                        self.__dict__[name] = value
                    else :
                        if name != "_ProtectedRange_iterator__a" :
                            raise AttributeError("can't set attribute")
                        else :
                            self.__dict__[name] = value
                else :
                    raise AttributeError("can't set attribute")
            
            def __delattr__(self, name) :
                if name in ("_ProtectedRange_iterator__start", "_ProtectedRange\
_iterator__stop", "_ProtectedRange_iterator__step", "_ProtectedRange_iterator__\
a") :
                    if name != "_ProtectedRange_iterator__a" :
                        raise AttributeError("can't delete attribute")
                    else :
                        del self.__dict__[name]
                else :
                    raise AttributeError("can't delete attribute")
        
        def __iter__(self) :
            """Implement iter(self)."""
            
            try :
                self.start + self.start - self.start # protect
            except (TypeError, ValueError, MemoryError) :
                raise ValueError("protected range")
            return type(self).ProtectedRange_iterator(self.start, self.stop,
                                                      self.step)
        
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
        def __delattr__(self, name) :
            """Execute delattr(self, name)."""
            
            raise AttributeError("%s cannot be deleted" % name)
        
        def __setattr__(self, name, value) :
            """Execute setattr(self, name, value)."""
            
            if name in ("start", "stop", "step") :
                if not hasattr(self, name) :
                    self.__dict__[name] = value
                else :
                    raise AttributeError("can't set attribute")
            else :
                raise AttributeError("can't set attribute")
        
        class ProtectedRange_iterator(object) :
            def __init__(self, start, stop, step) :
                self.__start = start
                self.__stop = stop
                self.__step = step
            
            def __iter__(self) :
                """x.__iter__() <==> iter(x)"""
                
                return self
            
            def next(self) :
                """x.next() -> the next value, or raise StopIteration"""
                
                if hasattr(self, "_ProtectedRange_iterator__a") :
                    try :
                        if self.__a + self.__step > self.__a :
                            if self.__a >= self.__stop :
                                del self.__a
                                raise StopIteration
                        elif self.__a + self.__step < self.__a :
                            if self.__a <= self.__stop :
                                del self.__a
                                raise StopIteration
                        else :
                            raise ValueError("ProtectedRange() arg 3 must not b\
e zero")
                    except AttributeError :
                        raise StopIteration
                    res = self.__a
                    self.__a += self.__step
                    return res
                else :
                    self.__a = self.__start
                    self.next()
                    return self.__start
        
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
            return type(self).ProtectedRange_iterator(self.start, self.stop,
                                                      self.step)
        
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
