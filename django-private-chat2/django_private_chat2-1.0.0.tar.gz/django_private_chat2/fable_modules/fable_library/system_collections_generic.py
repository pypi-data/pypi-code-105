from .util import (compare, equals, structural_hash, get_enumerator, to_iterator, max, compare_primitives)
from .reflection import class_type
from .seq import (delay, enumerate_while, append, singleton, empty, to_array)
from .array import (fill, copy_to, initialize)

def expr_25(gen0):
    return class_type("System.Collections.Generic.Comparer`1", [gen0], Comparer_1)


class Comparer_1:
    def __init__(self):
        pass
    
    def Compare(self, x, y=None):
        return compare(x, y)
    

Comparer_1_reflection = expr_25

def Comparer_1__ctor():
    return Comparer_1()


def Comparer_1_get_Default():
    class ObjectExpr26:
        def Compare(self, x, y=None):
            return compare(x, y)
        
    return ObjectExpr26()


def expr_27(gen0):
    return class_type("System.Collections.Generic.EqualityComparer`1", [gen0], EqualityComparer_1)


class EqualityComparer_1:
    def __init__(self):
        pass
    
    def __eq__(self, x, y=None):
        return equals(x, y)
    
    def GetHashCode(self, x=None):
        return structural_hash(x)
    

EqualityComparer_1_reflection = expr_27

def EqualityComparer_1__ctor():
    return EqualityComparer_1()


def EqualityComparer_1_get_Default():
    class ObjectExpr28:
        def Equals(self, x, y=None):
            return equals(x, y)
        
        def GetHashCode(self, x_1=None):
            return structural_hash(x_1)
        
    return ObjectExpr28()


def expr_32(gen0):
    return class_type("System.Collections.Generic.Stack`1", [gen0], Stack_1)


class Stack_1:
    def __init__(self, initial_contents, initial_count):
        self.contents = initial_contents
        self.count = initial_count or 0
    
    def GetEnumerator(self):
        this = self
        def arrow_31(_unit=None):
            index = (this.count - 1) or 0
            def arrow_30(_unit=None):
                def arrow_29(_unit=None):
                    nonlocal index
                    index = (index - 1) or 0
                    return empty()
                
                return append(singleton(this.contents[index]), delay(arrow_29))
            
            return enumerate_while(lambda _unit=None: index >= 0, delay(arrow_30))
        
        return get_enumerator(delay(arrow_31))
    
    def __iter__(self):
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_IEnumerable_GetEnumerator(self):
        this = self
        return get_enumerator(this)
    

Stack_1_reflection = expr_32

def Stack_1__ctor_Z2E171D71(initial_contents, initial_count):
    return Stack_1(initial_contents, initial_count)


def Stack_1__ctor_Z524259A4(initial_capacity):
    return Stack_1__ctor_Z2E171D71(fill([0] * initial_capacity, 0, initial_capacity, None), 0)


def Stack_1__ctor():
    return Stack_1__ctor_Z524259A4(4)


def Stack_1__ctor_BB573A(xs):
    arr = list(xs)
    return Stack_1__ctor_Z2E171D71(arr, len(arr))


def Stack_1__Ensure_Z524259A4(this, new_size):
    old_size = len(this.contents) or 0
    if new_size > old_size:
        old = this.contents
        this.contents = fill([0] * max(lambda x, y, this=this, new_size=new_size: compare_primitives(x, y), new_size, old_size * 2), 0, max(lambda x, y, this=this, new_size=new_size: compare_primitives(x, y), new_size, old_size * 2), None)
        copy_to(old, 0, this.contents, 0, this.count)
    


def Stack_1__get_Count(this):
    return this.count


def Stack_1__Pop(this):
    this.count = (this.count - 1) or 0
    return this.contents[this.count]


def Stack_1__Peek(this):
    return this.contents[this.count - 1]


def Stack_1__Contains_2B595(this, x=None):
    found = False
    i = 0
    while not found if (i < this.count) else (False):
        if equals(x, this.contents[i]):
            found = True
        
        else: 
            i = (i + 1) or 0
        
    return found


def Stack_1__TryPeek_1F3DB691(this, result):
    if this.count > 0:
        result.contents = Stack_1__Peek(this)
        return True
    
    else: 
        return False
    


def Stack_1__TryPop_1F3DB691(this, result):
    if this.count > 0:
        result.contents = Stack_1__Pop(this)
        return True
    
    else: 
        return False
    


def Stack_1__Push_2B595(this, x=None):
    Stack_1__Ensure_Z524259A4(this, this.count + 1)
    this.contents[this.count] = x
    this.count = (this.count + 1) or 0


def Stack_1__Clear(this):
    this.count = 0
    fill(this.contents, 0, len(this.contents), None)


def Stack_1__TrimExcess(this):
    if (this.count / len(this.contents)) > 0.9:
        Stack_1__Ensure_Z524259A4(this, this.count)
    


def Stack_1__ToArray(this):
    return initialize(this.count, lambda i, this=this: this.contents[(this.count - 1) - i], None)


def expr_33(gen0):
    return class_type("System.Collections.Generic.Queue`1", [gen0], Queue_1)


class Queue_1:
    def __init__(self, initial_contents, initial_count):
        self.contents = initial_contents
        self.count = initial_count or 0
        self.head = 0
        self.tail = initial_count or 0
    
    def GetEnumerator(self):
        this = self
        return get_enumerator(Queue_1__toSeq(this))
    
    def __iter__(self):
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_IEnumerable_GetEnumerator(self):
        this = self
        return get_enumerator(this)
    

Queue_1_reflection = expr_33

def Queue_1__ctor_Z2E171D71(initial_contents, initial_count):
    return Queue_1(initial_contents, initial_count)


def Queue_1__ctor_Z524259A4(initial_capacity):
    if initial_capacity < 0:
        raise Exception("capacity is less than 0")
    
    return Queue_1__ctor_Z2E171D71(fill([0] * initial_capacity, 0, initial_capacity, None), 0)


def Queue_1__ctor():
    return Queue_1__ctor_Z524259A4(4)


def Queue_1__ctor_BB573A(xs):
    arr = list(xs)
    return Queue_1__ctor_Z2E171D71(arr, len(arr))


def Queue_1__get_Count(_):
    return _.count


def Queue_1__Enqueue_2B595(_, value=None):
    if _.count == Queue_1__size(_):
        Queue_1__ensure_Z524259A4(_, _.count + 1)
    
    _.contents[_.tail] = value
    _.tail = ((_.tail + 1) % Queue_1__size(_)) or 0
    _.count = (_.count + 1) or 0


def Queue_1__Dequeue(_):
    if _.count == 0:
        raise Exception("Queue is empty")
    
    value = _.contents[_.head]
    _.head = ((_.head + 1) % Queue_1__size(_)) or 0
    _.count = (_.count - 1) or 0
    return value


def Queue_1__Peek(_):
    if _.count == 0:
        raise Exception("Queue is empty")
    
    return _.contents[_.head]


def Queue_1__TryDequeue_1F3DB691(this, result):
    if this.count == 0:
        return False
    
    else: 
        result.contents = Queue_1__Dequeue(this)
        return True
    


def Queue_1__TryPeek_1F3DB691(this, result):
    if this.count == 0:
        return False
    
    else: 
        result.contents = Queue_1__Peek(this)
        return True
    


def Queue_1__Contains_2B595(this, x=None):
    found = False
    i = 0
    while not found if (i < this.count) else (False):
        if equals(x, this.contents[Queue_1__toIndex_Z524259A4(this, i)]):
            found = True
        
        else: 
            i = (i + 1) or 0
        
    return found


def Queue_1__Clear(this):
    this.count = 0
    this.head = 0
    this.tail = 0
    fill(this.contents, 0, Queue_1__size(this), None)


def Queue_1__TrimExcess(this):
    if (this.count / len(this.contents)) > 0.9:
        Queue_1__ensure_Z524259A4(this, this.count)
    


def Queue_1__ToArray(this):
    return to_array(Queue_1__toSeq(this))


def Queue_1__CopyTo_Z2E171D71(this, target, start):
    i = start or 0
    with get_enumerator(Queue_1__toSeq(this)) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            item = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
            target[i] = item
            i = (i + 1) or 0


def Queue_1__size(this):
    return len(this.contents)


def Queue_1__toIndex_Z524259A4(this, i):
    return (this.head + i) % Queue_1__size(this)


def Queue_1__ensure_Z524259A4(this, required_size):
    new_buffer = fill([0] * required_size, 0, required_size, None)
    if this.head < this.tail:
        copy_to(this.contents, this.head, new_buffer, 0, this.count)
    
    else: 
        copy_to(this.contents, this.head, new_buffer, 0, Queue_1__size(this) - this.head)
        copy_to(this.contents, 0, new_buffer, Queue_1__size(this) - this.head, this.tail)
    
    this.head = 0
    this.tail = this.count or 0
    this.contents = new_buffer


def Queue_1__toSeq(this):
    def arrow_36(this=this):
        i = 0
        def arrow_35(_unit=None):
            def arrow_34(_unit=None):
                nonlocal i
                i = (i + 1) or 0
                return empty()
            
            return append(singleton(this.contents[Queue_1__toIndex_Z524259A4(this, i)]), delay(arrow_34))
        
        return enumerate_while(lambda _unit=None: i < this.count, delay(arrow_35))
    
    return delay(arrow_36)


