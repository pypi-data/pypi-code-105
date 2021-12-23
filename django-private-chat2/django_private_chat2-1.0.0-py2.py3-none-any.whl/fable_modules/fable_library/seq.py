from .types import to_string
from .util import (get_enumerator, to_iterator, IDisposable, is_disposable, dispose as dispose_2, is_array_like, equals, ignore, clear)
from .reflection import class_type
from .option import (value as value_1, some)
from .fsharp_core import Operators_NullArg
from .array import (singleton as singleton_1, try_find_back as try_find_back_1, try_find_index_back as try_find_index_back_1, fold_back as fold_back_1, fold_back2 as fold_back2_1, try_head as try_head_1, try_item as try_item_1, map_fold as map_fold_1, map_fold_back as map_fold_back_1, reduce_back as reduce_back_1, reverse as reverse_1, scan_back as scan_back_1, pairwise as pairwise_1, map as map_1, split_into as split_into_1, windowed as windowed_1, transpose as transpose_1, permute as permute_1, chunk_by_size as chunk_by_size_1)
from .list import (FSharpList, to_array as to_array_1, of_array as of_array_1, of_seq as of_seq_1, try_head as try_head_2, is_empty as is_empty_1, try_item as try_item_2, length as length_1)
from .global_ import SR_indexOutOfBounds

SR_enumerationAlreadyFinished = "Enumeration already finished."

SR_enumerationNotStarted = "Enumeration has not started. Call MoveNext."

SR_inputSequenceEmpty = "The input sequence was empty."

SR_inputSequenceTooLong = "The input sequence contains more than one element."

SR_keyNotFoundAlt = "An index satisfying the predicate was not found in the collection."

SR_notEnoughElements = "The input sequence has an insufficient number of elements."

SR_resetNotSupported = "Reset is not supported on this enumerator."

def Enumerator_noReset():
    raise Exception(SR_resetNotSupported)


def Enumerator_notStarted():
    raise Exception(SR_enumerationNotStarted)


def Enumerator_alreadyFinished():
    raise Exception(SR_enumerationAlreadyFinished)


def expr_40(gen0):
    return class_type("SeqModule.Enumerator.Seq", [gen0], Enumerator_Seq)


class Enumerator_Seq:
    def __init__(self, f=None):
        self.f = f
    
    def __str__(self):
        xs = self
        max_count = 4
        i = 0
        str_1 = "seq ["
        with get_enumerator(xs) as e:
            while e.System_Collections_IEnumerator_MoveNext() if (i < max_count) else (False):
                if i > 0:
                    str_1 = str_1 + "; "
                
                str_1 = str_1 + to_string(e.System_Collections_Generic_IEnumerator_00601_get_Current())
                i = (i + 1) or 0
            if i == max_count:
                str_1 = str_1 + "; ..."
            
            return str_1 + "]"
    
    def GetEnumerator(self):
        x = self
        return x.f()
    
    def __iter__(self):
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_IEnumerable_GetEnumerator(self):
        x = self
        return x.f()
    

Enumerator_Seq_reflection = expr_40

def Enumerator_Seq__ctor_673A07F2(f):
    return Enumerator_Seq(f)


def expr_41(gen0):
    return class_type("SeqModule.Enumerator.FromFunctions`1", [gen0], Enumerator_FromFunctions_1)


class Enumerator_FromFunctions_1(IDisposable):
    def __init__(self, current, next_1, dispose):
        self.current = current
        self.next = next_1
        self.dispose = dispose
    
    def System_Collections_Generic_IEnumerator_00601_get_Current(self):
        __ = self
        return __.current()
    
    def System_Collections_IEnumerator_get_Current(self):
        __ = self
        return __.current()
    
    def System_Collections_IEnumerator_MoveNext(self):
        __ = self
        return __.next()
    
    def System_Collections_IEnumerator_Reset(self):
        Enumerator_noReset()
    
    def Dispose(self):
        __ = self
        __.dispose()
    

Enumerator_FromFunctions_1_reflection = expr_41

def Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose):
    return Enumerator_FromFunctions_1(current, next_1, dispose)


def Enumerator_cast(e):
    def dispose(e=e):
        if is_disposable(e):
            dispose_2(e)
        
    
    return Enumerator_FromFunctions_1__ctor_58C54629(lambda e=e: e.System_Collections_IEnumerator_get_Current(), lambda e=e: e.System_Collections_IEnumerator_MoveNext(), dispose)


def Enumerator_concat(sources):
    outer_opt = None
    inner_opt = None
    started = False
    finished = False
    curr = None
    def finish(sources=sources):
        nonlocal finished, inner_opt, outer_opt
        finished = True
        if inner_opt is not None:
            inner = inner_opt
            try: 
                dispose_2(inner)
            
            finally: 
                inner_opt = None
            
        
        if outer_opt is not None:
            outer = outer_opt
            try: 
                dispose_2(outer)
            
            finally: 
                outer_opt = None
            
        
    
    def current(sources=sources):
        if not started:
            Enumerator_notStarted()
        
        elif finished:
            Enumerator_alreadyFinished()
        
        if curr is not None:
            return value_1(curr)
        
        else: 
            return Enumerator_alreadyFinished()
        
    
    def next_1(sources=sources):
        nonlocal started
        if not started:
            started = True
        
        if finished:
            return False
        
        else: 
            res = None
            while res is None:
                nonlocal curr, inner_opt, outer_opt
                match_value = (outer_opt, inner_opt)
                if (match_value[0]) is not None:
                    if (match_value[1]) is not None:
                        inner_1 = match_value[1]
                        if inner_1.System_Collections_IEnumerator_MoveNext():
                            curr = some(inner_1.System_Collections_Generic_IEnumerator_00601_get_Current())
                            res = True
                        
                        else: 
                            try: 
                                dispose_2(inner_1)
                            
                            finally: 
                                inner_opt = None
                            
                        
                    
                    else: 
                        outer_1 = match_value[0]
                        if outer_1.System_Collections_IEnumerator_MoveNext():
                            ie = outer_1.System_Collections_Generic_IEnumerator_00601_get_Current()
                            def arrow_42(_unit=None):
                                copy_of_struct = ie
                                return get_enumerator(copy_of_struct)
                            
                            inner_opt = arrow_42()
                        
                        else: 
                            finish()
                            res = False
                        
                    
                
                else: 
                    outer_opt = get_enumerator(sources)
                
            return value_1(res)
        
    
    def dispose(sources=sources):
        if not finished:
            finish()
        
    
    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_enumerateThenFinally(f, e):
    def dispose(f=f, e=e):
        try: 
            dispose_2(e)
        
        finally: 
            f()
        
    
    return Enumerator_FromFunctions_1__ctor_58C54629(lambda f=f, e=e: e.System_Collections_Generic_IEnumerator_00601_get_Current(), lambda f=f, e=e: e.System_Collections_IEnumerator_MoveNext(), dispose)


def Enumerator_generateWhileSome(openf, compute, closef):
    started = False
    curr = None
    state = some(openf())
    def dispose(openf=openf, compute=compute, closef=closef):
        nonlocal state
        if state is not None:
            x_1 = value_1(state)
            try: 
                closef(x_1)
            
            finally: 
                state = None
            
        
    
    def finish(openf=openf, compute=compute, closef=closef):
        nonlocal curr
        try: 
            dispose()
        
        finally: 
            curr = None
        
    
    def current(openf=openf, compute=compute, closef=closef):
        if not started:
            Enumerator_notStarted()
        
        if curr is not None:
            return value_1(curr)
        
        else: 
            return Enumerator_alreadyFinished()
        
    
    def next_1(openf=openf, compute=compute, closef=closef):
        nonlocal started, curr
        if not started:
            started = True
        
        if state is not None:
            s = value_1(state)
            match_value_1 = None
            try: 
                match_value_1 = compute(s)
            
            except Exception as match_value:
                finish()
                raise match_value
            
            if match_value_1 is not None:
                curr = match_value_1
                return True
            
            else: 
                finish()
                return False
            
        
        else: 
            return False
        
    
    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def Enumerator_unfold(f, state=None):
    curr = None
    acc = state
    def current(f=f, state=state):
        if curr is not None:
            x = curr[0]
            st = curr[1]
            return x
        
        else: 
            return Enumerator_notStarted()
        
    
    def next_1(f=f, state=state):
        nonlocal curr, acc
        curr = f(acc)
        if curr is not None:
            x_1 = curr[0]
            st_1 = curr[1]
            acc = st_1
            return True
        
        else: 
            return False
        
    
    def dispose(f=f, state=state):
        pass
    
    return Enumerator_FromFunctions_1__ctor_58C54629(current, next_1, dispose)


def index_not_found():
    raise Exception(SR_keyNotFoundAlt)


def check_non_null(arg_name, arg=None):
    if arg is None:
        Operators_NullArg(arg_name)
    


def mk_seq(f):
    return Enumerator_Seq__ctor_673A07F2(f)


def of_seq(xs):
    check_non_null("source", xs)
    return get_enumerator(xs)


def delay(generator):
    return mk_seq(lambda generator=generator: get_enumerator(generator()))


def concat(sources):
    return mk_seq(lambda sources=sources: Enumerator_concat(sources))


def unfold(generator, state=None):
    return mk_seq(lambda generator=generator, state=state: Enumerator_unfold(generator, state))


def empty():
    return delay(lambda _unit=None: [])


def singleton(x=None):
    return delay(lambda x=x: singleton_1(x, None))


def of_array(arr):
    return arr


def to_array(xs):
    if isinstance(xs, FSharpList):
        return to_array_1(xs)
    
    else: 
        return list(xs)
    


def of_list(xs):
    return xs


def to_list(xs):
    if is_array_like(xs):
        return of_array_1(xs)
    
    elif isinstance(xs, FSharpList):
        return xs
    
    else: 
        return of_seq_1(xs)
    


def generate(create, compute, dispose):
    return mk_seq(lambda create=create, compute=compute, dispose=dispose: Enumerator_generateWhileSome(create, compute, dispose))


def generate_indexed(create, compute, dispose):
    def arrow_44(create=create, compute=compute, dispose=dispose):
        i = -1
        def arrow_43(x=None):
            nonlocal i
            i = (i + 1) or 0
            return compute(i, x)
        
        return Enumerator_generateWhileSome(create, arrow_43, dispose)
    
    return mk_seq(arrow_44)


def append(xs, ys):
    return concat([xs, ys])


def cast(xs):
    def arrow_45(xs=xs):
        check_non_null("source", xs)
        return Enumerator_cast(get_enumerator(xs))
    
    return mk_seq(arrow_45)


def choose(chooser, xs):
    def arrow_46(e, chooser=chooser, xs=xs):
        curr = None
        while e.System_Collections_IEnumerator_MoveNext() if (curr is None) else (False):
            curr = chooser(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        return curr
    
    def arrow_47(e_1, chooser=chooser, xs=xs):
        dispose_2(e_1)
    
    return generate(lambda chooser=chooser, xs=xs: of_seq(xs), arrow_46, arrow_47)


def compare_with(comparer, xs, ys):
    with of_seq(xs) as e1:
        with of_seq(ys) as e2:
            c = 0
            b1 = e1.System_Collections_IEnumerator_MoveNext()
            b2 = e2.System_Collections_IEnumerator_MoveNext()
            while b2 if (b1 if (c == 0) else (False)) else (False):
                c = comparer(e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current()) or 0
                if c == 0:
                    b1 = e1.System_Collections_IEnumerator_MoveNext()
                    b2 = e2.System_Collections_IEnumerator_MoveNext()
                
            if c != 0:
                return c
            
            elif b1:
                return 1
            
            elif b2:
                return -1
            
            else: 
                return 0
            


def contains(value, xs, comparer):
    with of_seq(xs) as e:
        found = False
        while e.System_Collections_IEnumerator_MoveNext() if (not found) else (False):
            found = comparer.Equals(value, e.System_Collections_Generic_IEnumerator_00601_get_Current())
        return found


def enumerate_from_functions(create, move_next, current):
    def arrow_48(x_1=None, create=create, move_next=move_next, current=current):
        match_value = x_1
        if is_disposable(match_value):
            dispose_2(match_value)
        
    
    return generate(create, lambda x=None, create=create, move_next=move_next, current=current: some(current(x)) if (move_next(x)) else (None), arrow_48)


def enumerate_then_finally(source, compensation):
    compensation_1 = compensation
    def arrow_49(source=source, compensation=compensation):
        try: 
            return Enumerator_enumerateThenFinally(compensation_1, of_seq(source))
        
        except Exception as match_value:
            compensation_1()
            raise match_value
        
    
    return mk_seq(arrow_49)


def enumerate_using(resource, source):
    def compensation(resource=resource, source=source):
        if equals(resource, None):
            pass
        
        else: 
            copy_of_struct = resource
            dispose_2(copy_of_struct)
        
    
    def arrow_50(resource=resource, source=source):
        try: 
            return Enumerator_enumerateThenFinally(compensation, of_seq(source(resource)))
        
        except Exception as match_value_1:
            compensation()
            raise match_value_1
        
    
    return mk_seq(arrow_50)


def enumerate_while(guard, xs):
    return concat(unfold(lambda i, guard=guard, xs=xs: (xs, i + 1) if (guard()) else (None), 0))


def filter(f, xs):
    def chooser(x=None, f=f, xs=xs):
        if f(x):
            return some(x)
        
        else: 
            return None
        
    
    return choose(chooser, xs)


def exists(predicate, xs):
    with of_seq(xs) as e:
        found = False
        while e.System_Collections_IEnumerator_MoveNext() if (not found) else (False):
            found = predicate(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        return found


def exists2(predicate, xs, ys):
    with of_seq(xs) as e1:
        with of_seq(ys) as e2:
            found = False
            while e2.System_Collections_IEnumerator_MoveNext() if (e1.System_Collections_IEnumerator_MoveNext() if (not found) else (False)) else (False):
                found = predicate(e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current())
            return found


def exactly_one(xs):
    with of_seq(xs) as e:
        if e.System_Collections_IEnumerator_MoveNext():
            v = e.System_Collections_Generic_IEnumerator_00601_get_Current()
            if e.System_Collections_IEnumerator_MoveNext():
                raise Exception((SR_inputSequenceTooLong + "\\nParameter name: ") + "source")
            
            else: 
                return v
            
        
        else: 
            raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")
        


def try_exactly_one(xs):
    with of_seq(xs) as e:
        if e.System_Collections_IEnumerator_MoveNext():
            v = e.System_Collections_Generic_IEnumerator_00601_get_Current()
            if e.System_Collections_IEnumerator_MoveNext():
                return None
            
            else: 
                return some(v)
            
        
        else: 
            return None
        


def try_find(predicate, xs):
    with of_seq(xs) as e:
        res = None
        while e.System_Collections_IEnumerator_MoveNext() if (res is None) else (False):
            c = e.System_Collections_Generic_IEnumerator_00601_get_Current()
            if predicate(c):
                res = some(c)
            
        return res


def find(predicate, xs):
    match_value = try_find(predicate, xs)
    if match_value is None:
        return index_not_found()
    
    else: 
        return value_1(match_value)
    


def try_find_back(predicate, xs):
    return try_find_back_1(predicate, to_array(xs))


def find_back(predicate, xs):
    match_value = try_find_back(predicate, xs)
    if match_value is None:
        return index_not_found()
    
    else: 
        return value_1(match_value)
    


def try_find_index(predicate, xs):
    with of_seq(xs) as e:
        def loop(i_mut, predicate=predicate, xs=xs):
            while True:
                (i,) = (i_mut,)
                if e.System_Collections_IEnumerator_MoveNext():
                    if predicate(e.System_Collections_Generic_IEnumerator_00601_get_Current()):
                        return i
                    
                    else: 
                        i_mut = i + 1
                        continue
                    
                
                else: 
                    return None
                
                break
        
        loop = loop
        return loop(0)


def find_index(predicate, xs):
    match_value = try_find_index(predicate, xs)
    if match_value is None:
        return index_not_found()
    
    else: 
        return match_value
    


def try_find_index_back(predicate, xs):
    return try_find_index_back_1(predicate, to_array(xs))


def find_index_back(predicate, xs):
    match_value = try_find_index_back(predicate, xs)
    if match_value is None:
        return index_not_found()
    
    else: 
        return match_value
    


def fold(folder, state, xs):
    with of_seq(xs) as e:
        acc = state
        while e.System_Collections_IEnumerator_MoveNext():
            acc = folder(acc, e.System_Collections_Generic_IEnumerator_00601_get_Current())
        return acc


def fold_back(folder, xs, state=None):
    return fold_back_1(folder, to_array(xs), state)


def fold2(folder, state, xs, ys):
    with of_seq(xs) as e1:
        with of_seq(ys) as e2:
            acc = state
            while e2.System_Collections_IEnumerator_MoveNext() if (e1.System_Collections_IEnumerator_MoveNext()) else (False):
                acc = folder(acc, e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current())
            return acc


def fold_back2(folder, xs, ys, state=None):
    return fold_back2_1(folder, to_array(xs), to_array(ys), state)


def for_all(predicate, xs):
    return not exists(lambda x=None, predicate=predicate, xs=xs: not predicate(x), xs)


def for_all2(predicate, xs, ys):
    return not exists2(lambda x, y=None, predicate=predicate, xs=xs, ys=ys: not predicate(x, y), xs, ys)


def try_head(xs):
    if is_array_like(xs):
        return try_head_1(xs)
    
    elif isinstance(xs, FSharpList):
        return try_head_2(xs)
    
    else: 
        with of_seq(xs) as e:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
            
            else: 
                return None
            
    


def head(xs):
    match_value = try_head(xs)
    if match_value is None:
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")
    
    else: 
        return value_1(match_value)
    


def initialize(count, f):
    return unfold(lambda i, count=count, f=f: (f(i), i + 1) if (i < count) else (None), 0)


def initialize_infinite(f):
    return initialize(2147483647, f)


def is_empty(xs):
    if is_array_like(xs):
        return len(xs) == 0
    
    elif isinstance(xs, FSharpList):
        return is_empty_1(xs)
    
    else: 
        with of_seq(xs) as e:
            return not e.System_Collections_IEnumerator_MoveNext()
    


def try_item(index, xs):
    if is_array_like(xs):
        return try_item_1(index, xs)
    
    elif isinstance(xs, FSharpList):
        return try_item_2(index, xs)
    
    else: 
        with of_seq(xs) as e:
            def loop(index_1_mut, index=index, xs=xs):
                while True:
                    (index_1,) = (index_1_mut,)
                    if not e.System_Collections_IEnumerator_MoveNext():
                        return None
                    
                    elif index_1 == 0:
                        return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
                    
                    else: 
                        index_1_mut = index_1 - 1
                        continue
                    
                    break
            
            loop = loop
            return loop(index)
    


def item(index, xs):
    match_value = try_item(index, xs)
    if match_value is None:
        raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "index")
    
    else: 
        return value_1(match_value)
    


def iterate(action, xs):
    def arrow_51(unit_var0, x=None, action=action, xs=xs):
        action(x)
    
    fold(arrow_51, None, xs)


def iterate2(action, xs, ys):
    def arrow_52(unit_var0, x, y=None, action=action, xs=xs, ys=ys):
        action(x, y)
    
    fold2(arrow_52, None, xs, ys)


def iterate_indexed(action, xs):
    def arrow_53(i, x=None, action=action, xs=xs):
        action(i, x)
        return i + 1
    
    ignore(fold(arrow_53, 0, xs))


def iterate_indexed2(action, xs, ys):
    def arrow_54(i, x, y=None, action=action, xs=xs, ys=ys):
        action(i, x, y)
        return i + 1
    
    ignore(fold2(arrow_54, 0, xs, ys))


def try_last(xs):
    with of_seq(xs) as e:
        def loop(acc_mut=None, xs=xs):
            while True:
                (acc,) = (acc_mut,)
                if not e.System_Collections_IEnumerator_MoveNext():
                    return acc
                
                else: 
                    acc_mut = e.System_Collections_Generic_IEnumerator_00601_get_Current()
                    continue
                
                break
        
        loop = loop
        if e.System_Collections_IEnumerator_MoveNext():
            return some(loop(e.System_Collections_Generic_IEnumerator_00601_get_Current()))
        
        else: 
            return None
        


def last(xs):
    match_value = try_last(xs)
    if match_value is None:
        raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")
    
    else: 
        return value_1(match_value)
    


def length(xs):
    if is_array_like(xs):
        return len(xs)
    
    elif isinstance(xs, FSharpList):
        return length_1(xs)
    
    else: 
        with of_seq(xs) as e:
            count = 0
            while e.System_Collections_IEnumerator_MoveNext():
                count = (count + 1) or 0
            return count
    


def map(mapping, xs):
    def arrow_55(e_1, mapping=mapping, xs=xs):
        dispose_2(e_1)
    
    return generate(lambda mapping=mapping, xs=xs: of_seq(xs), lambda e, mapping=mapping, xs=xs: some(mapping(e.System_Collections_Generic_IEnumerator_00601_get_Current())) if (e.System_Collections_IEnumerator_MoveNext()) else (None), arrow_55)


def map_indexed(mapping, xs):
    def arrow_56(e_1, mapping=mapping, xs=xs):
        dispose_2(e_1)
    
    return generate_indexed(lambda mapping=mapping, xs=xs: of_seq(xs), lambda i, e, mapping=mapping, xs=xs: some(mapping(i, e.System_Collections_Generic_IEnumerator_00601_get_Current())) if (e.System_Collections_IEnumerator_MoveNext()) else (None), arrow_56)


def indexed(xs):
    return map_indexed(lambda i, x=None, xs=xs: (i, x), xs)


def map2(mapping, xs, ys):
    def arrow_57(tupled_arg, mapping=mapping, xs=xs, ys=ys):
        e1 = tupled_arg[0]
        e2 = tupled_arg[1]
        return some(mapping(e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current())) if (e2.System_Collections_IEnumerator_MoveNext() if (e1.System_Collections_IEnumerator_MoveNext()) else (False)) else (None)
    
    def arrow_58(tupled_arg_1, mapping=mapping, xs=xs, ys=ys):
        try: 
            dispose_2(tupled_arg_1[0])
        
        finally: 
            dispose_2(tupled_arg_1[1])
        
    
    return generate(lambda mapping=mapping, xs=xs, ys=ys: (of_seq(xs), of_seq(ys)), arrow_57, arrow_58)


def map_indexed2(mapping, xs, ys):
    def arrow_59(i, tupled_arg, mapping=mapping, xs=xs, ys=ys):
        e1 = tupled_arg[0]
        e2 = tupled_arg[1]
        return some(mapping(i, e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current())) if (e2.System_Collections_IEnumerator_MoveNext() if (e1.System_Collections_IEnumerator_MoveNext()) else (False)) else (None)
    
    def arrow_60(tupled_arg_1, mapping=mapping, xs=xs, ys=ys):
        try: 
            dispose_2(tupled_arg_1[0])
        
        finally: 
            dispose_2(tupled_arg_1[1])
        
    
    return generate_indexed(lambda mapping=mapping, xs=xs, ys=ys: (of_seq(xs), of_seq(ys)), arrow_59, arrow_60)


def map3(mapping, xs, ys, zs):
    def arrow_61(tupled_arg, mapping=mapping, xs=xs, ys=ys, zs=zs):
        e1 = tupled_arg[0]
        e2 = tupled_arg[1]
        e3 = tupled_arg[2]
        return some(mapping(e1.System_Collections_Generic_IEnumerator_00601_get_Current(), e2.System_Collections_Generic_IEnumerator_00601_get_Current(), e3.System_Collections_Generic_IEnumerator_00601_get_Current())) if (e3.System_Collections_IEnumerator_MoveNext() if (e2.System_Collections_IEnumerator_MoveNext() if (e1.System_Collections_IEnumerator_MoveNext()) else (False)) else (False)) else (None)
    
    def arrow_62(tupled_arg_1, mapping=mapping, xs=xs, ys=ys, zs=zs):
        try: 
            dispose_2(tupled_arg_1[0])
        
        finally: 
            try: 
                dispose_2(tupled_arg_1[1])
            
            finally: 
                dispose_2(tupled_arg_1[2])
            
        
    
    return generate(lambda mapping=mapping, xs=xs, ys=ys, zs=zs: (of_seq(xs), of_seq(ys), of_seq(zs)), arrow_61, arrow_62)


def read_only(xs):
    check_non_null("source", xs)
    return map(lambda x=None, xs=xs: x, xs)


def expr_63(gen0):
    return class_type("SeqModule.CachedSeq`1", [gen0], CachedSeq_1)


class CachedSeq_1(IDisposable):
    def __init__(self, cleanup, res):
        self.cleanup = cleanup
        self.res = res
    
    def Dispose(self):
        _ = self
        _.cleanup()
    
    def GetEnumerator(self):
        _ = self
        return get_enumerator(_.res)
    
    def __iter__(self):
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_IEnumerable_GetEnumerator(self):
        _ = self
        return get_enumerator(_.res)
    

CachedSeq_1_reflection = expr_63

def CachedSeq_1__ctor_Z7A8347D4(cleanup, res):
    return CachedSeq_1(cleanup, res)


def CachedSeq_1__Clear(_):
    _.cleanup()


def cache(source):
    check_non_null("source", source)
    prefix = []
    enumerator_r = None
    def cleanup(source=source):
        nonlocal enumerator_r
        clear(prefix)
        (pattern_matching_result, e) = (None, None)
        if enumerator_r is not None:
            if value_1(enumerator_r) is not None:
                pattern_matching_result = 0
                e = value_1(enumerator_r)
            
            else: 
                pattern_matching_result = 1
            
        
        else: 
            pattern_matching_result = 1
        
        if pattern_matching_result == 0:
            dispose_2(e)
        
        enumerator_r = None
    
    def arrow_65(i_1, source=source):
        nonlocal enumerator_r
        if i_1 < len(prefix):
            return (prefix[i_1], i_1 + 1)
        
        else: 
            if i_1 >= len(prefix):
                opt_enumerator_2 = None
                if enumerator_r is not None:
                    opt_enumerator_2 = value_1(enumerator_r)
                
                else: 
                    opt_enumerator = get_enumerator(source)
                    enumerator_r = some(opt_enumerator)
                    opt_enumerator_2 = opt_enumerator
                
                if opt_enumerator_2 is None:
                    pass
                
                else: 
                    enumerator = opt_enumerator_2
                    if enumerator.System_Collections_IEnumerator_MoveNext():
                        (prefix.append(enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()))
                    
                    else: 
                        dispose_2(enumerator)
                        enumerator_r = some(None)
                    
                
            
            return (prefix[i_1], i_1 + 1) if (i_1 < len(prefix)) else (None)
        
    
    return CachedSeq_1__ctor_Z7A8347D4(cleanup, unfold(arrow_65, 0))


def all_pairs(xs, ys):
    ys_cache = cache(ys)
    return delay(lambda xs=xs, ys=ys: concat(map(lambda x=None: map(lambda y=None, x=x: (x, y), ys_cache), xs)))


def map_fold(mapping, state, xs):
    pattern_input = map_fold_1(mapping, state, to_array(xs), None)
    return (read_only(pattern_input[0]), pattern_input[1])


def map_fold_back(mapping, xs, state=None):
    pattern_input = map_fold_back_1(mapping, to_array(xs), state, None)
    return (read_only(pattern_input[0]), pattern_input[1])


def try_pick(chooser, xs):
    with of_seq(xs) as e:
        res = None
        while e.System_Collections_IEnumerator_MoveNext() if (res is None) else (False):
            res = chooser(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        return res


def pick(chooser, xs):
    match_value = try_pick(chooser, xs)
    if match_value is None:
        return index_not_found()
    
    else: 
        return value_1(match_value)
    


def reduce(folder, xs):
    with of_seq(xs) as e:
        def loop(acc_mut=None, folder=folder, xs=xs):
            while True:
                (acc,) = (acc_mut,)
                if e.System_Collections_IEnumerator_MoveNext():
                    acc_mut = folder(acc, e.System_Collections_Generic_IEnumerator_00601_get_Current())
                    continue
                
                else: 
                    return acc
                
                break
        
        loop = loop
        if e.System_Collections_IEnumerator_MoveNext():
            return loop(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        
        else: 
            raise Exception(SR_inputSequenceEmpty)
        


def reduce_back(folder, xs):
    arr = to_array(xs)
    if len(arr) > 0:
        return reduce_back_1(folder, arr)
    
    else: 
        raise Exception(SR_inputSequenceEmpty)
    


def replicate(n, x=None):
    return initialize(n, lambda _arg1, n=n, x=x: x)


def reverse(xs):
    return delay(lambda xs=xs: of_array(reverse_1(to_array(xs))))


def scan(folder, state, xs):
    def arrow_66(folder=folder, state=state, xs=xs):
        acc = state
        def mapping(x=None):
            nonlocal acc
            acc = folder(acc, x)
            return acc
        
        return concat([singleton(state), map(mapping, xs)])
    
    return delay(arrow_66)


def scan_back(folder, xs, state=None):
    return delay(lambda folder=folder, xs=xs, state=state: of_array(scan_back_1(folder, to_array(xs), state, None)))


def skip(count, source):
    def arrow_68(count=count, source=source):
        e = of_seq(source)
        try: 
            for _ in range(1, count + 1, 1):
                if not e.System_Collections_IEnumerator_MoveNext():
                    raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")
                
            def compensation(_unit=None):
                pass
            
            return Enumerator_enumerateThenFinally(compensation, e)
        
        except Exception as match_value:
            dispose_2(e)
            raise match_value
        
    
    return mk_seq(arrow_68)


def skip_while(predicate, xs):
    def arrow_69(predicate=predicate, xs=xs):
        skipped = True
        def f(x=None):
            nonlocal skipped
            if skipped:
                skipped = predicate(x)
            
            return not skipped
        
        return filter(f, xs)
    
    return delay(arrow_69)


def tail(xs):
    return skip(1, xs)


def take(count, xs):
    def arrow_70(i, e, count=count, xs=xs):
        if i < count:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
            
            else: 
                raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "source")
            
        
        else: 
            return None
        
    
    def arrow_71(e_1, count=count, xs=xs):
        dispose_2(e_1)
    
    return generate_indexed(lambda count=count, xs=xs: of_seq(xs), arrow_70, arrow_71)


def take_while(predicate, xs):
    def arrow_72(e_1, predicate=predicate, xs=xs):
        dispose_2(e_1)
    
    return generate(lambda predicate=predicate, xs=xs: of_seq(xs), lambda e, predicate=predicate, xs=xs: some(e.System_Collections_Generic_IEnumerator_00601_get_Current()) if (predicate(e.System_Collections_Generic_IEnumerator_00601_get_Current()) if (e.System_Collections_IEnumerator_MoveNext()) else (False)) else (None), arrow_72)


def truncate(count, xs):
    def arrow_73(e_1, count=count, xs=xs):
        dispose_2(e_1)
    
    return generate_indexed(lambda count=count, xs=xs: of_seq(xs), lambda i, e, count=count, xs=xs: some(e.System_Collections_Generic_IEnumerator_00601_get_Current()) if (e.System_Collections_IEnumerator_MoveNext() if (i < count) else (False)) else (None), arrow_73)


def zip(xs, ys):
    return map2(lambda x, y=None, xs=xs, ys=ys: (x, y), xs, ys)


def zip3(xs, ys, zs):
    return map3(lambda x, y, z=None, xs=xs, ys=ys, zs=zs: (x, y, z), xs, ys, zs)


def collect(mapping, xs):
    return delay(lambda mapping=mapping, xs=xs: concat(map(mapping, xs)))


def where(predicate, xs):
    return filter(predicate, xs)


def pairwise(xs):
    return delay(lambda xs=xs: of_array(pairwise_1(to_array(xs))))


def split_into(chunks, xs):
    return delay(lambda chunks=chunks, xs=xs: of_array(map_1(lambda arr: of_array(arr), split_into_1(chunks, to_array(xs)), None)))


def windowed(window_size, xs):
    return delay(lambda window_size=window_size, xs=xs: of_array(map_1(lambda arr: of_array(arr), windowed_1(window_size, to_array(xs)), None)))


def transpose(xss):
    return delay(lambda xss=xss: of_array(map_1(lambda arr: of_array(arr), transpose_1(map_1(lambda xs_1=None: to_array(xs_1), to_array(xss), None), None), None)))


def sort_with(comparer, xs):
    def arrow_74(comparer=comparer, xs=xs):
        arr = to_array(xs)
        arr.sort()
        return of_array(arr)
    
    return delay(arrow_74)


def sort(xs, comparer):
    return sort_with(lambda x, y=None, xs=xs, comparer=comparer: comparer.Compare(x, y), xs)


def sort_by(projection, xs, comparer):
    return sort_with(lambda x, y=None, projection=projection, xs=xs, comparer=comparer: comparer.Compare(projection(x), projection(y)), xs)


def sort_descending(xs, comparer):
    return sort_with(lambda x, y=None, xs=xs, comparer=comparer: comparer.Compare(x, y) * -1, xs)


def sort_by_descending(projection, xs, comparer):
    return sort_with(lambda x, y=None, projection=projection, xs=xs, comparer=comparer: comparer.Compare(projection(x), projection(y)) * -1, xs)


def sum(xs, adder):
    return fold(lambda acc, x=None, xs=xs, adder=adder: adder.Add(acc, x), adder.GetZero(), xs)


def sum_by(f, xs, adder):
    return fold(lambda acc, x=None, f=f, xs=xs, adder=adder: adder.Add(acc, f(x)), adder.GetZero(), xs)


def max_by(projection, xs, comparer):
    return reduce(lambda x, y=None, projection=projection, xs=xs, comparer=comparer: y if (comparer.Compare(projection(y), projection(x)) > 0) else (x), xs)


def max(xs, comparer):
    return reduce(lambda x, y=None, xs=xs, comparer=comparer: y if (comparer.Compare(y, x) > 0) else (x), xs)


def min_by(projection, xs, comparer):
    return reduce(lambda x, y=None, projection=projection, xs=xs, comparer=comparer: x if (comparer.Compare(projection(y), projection(x)) > 0) else (y), xs)


def min(xs, comparer):
    return reduce(lambda x, y=None, xs=xs, comparer=comparer: x if (comparer.Compare(y, x) > 0) else (y), xs)


def average(xs, averager):
    count = 0
    def folder(acc, x=None, xs=xs, averager=averager):
        nonlocal count
        count = (count + 1) or 0
        return averager.Add(acc, x)
    
    total = fold(folder, averager.GetZero(), xs)
    if count == 0:
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")
    
    else: 
        return averager.DivideByInt(total, count)
    


def average_by(f, xs, averager):
    count = 0
    def arrow_82(acc, x=None, f=f, xs=xs, averager=averager):
        nonlocal count
        count = (count + 1) or 0
        return averager.Add(acc, f(x))
    
    total = fold(arrow_82, averager.GetZero(), xs)
    if count == 0:
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "source")
    
    else: 
        return averager.DivideByInt(total, count)
    


def permute(f, xs):
    return delay(lambda f=f, xs=xs: of_array(permute_1(f, to_array(xs))))


def chunk_by_size(chunk_size, xs):
    return delay(lambda chunk_size=chunk_size, xs=xs: of_array(map_1(lambda arr: of_array(arr), chunk_by_size_1(chunk_size, to_array(xs)), None)))


def insert_at(index, y, xs):
    is_done = False
    if index < 0:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    def arrow_83(i, e, index=index, y=y, xs=xs):
        nonlocal is_done
        if e.System_Collections_IEnumerator_MoveNext() if (True if (is_done) else (i < index)) else (False):
            return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        
        elif i == index:
            is_done = True
            return some(y)
        
        else: 
            if not is_done:
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
            
            return None
        
    
    def arrow_84(e_1, index=index, y=y, xs=xs):
        dispose_2(e_1)
    
    return generate_indexed(lambda index=index, y=y, xs=xs: of_seq(xs), arrow_83, arrow_84)


def insert_many_at(index, ys, xs):
    status = -1
    if index < 0:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    def arrow_85(i, tupled_arg, index=index, ys=ys, xs=xs):
        nonlocal status
        e1 = tupled_arg[0]
        e2 = tupled_arg[1]
        if i == index:
            status = 0
        
        inserted = None
        if status == 0:
            if e2.System_Collections_IEnumerator_MoveNext():
                inserted = some(e2.System_Collections_Generic_IEnumerator_00601_get_Current())
            
            else: 
                status = 1
                inserted = None
            
        
        else: 
            inserted = None
        
        if inserted is None:
            if e1.System_Collections_IEnumerator_MoveNext():
                return some(e1.System_Collections_Generic_IEnumerator_00601_get_Current())
            
            else: 
                if status < 1:
                    raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
                
                return None
            
        
        else: 
            return some(value_1(inserted))
        
    
    def arrow_86(tupled_arg_1, index=index, ys=ys, xs=xs):
        dispose_2(tupled_arg_1[0])
        dispose_2(tupled_arg_1[1])
    
    return generate_indexed(lambda index=index, ys=ys, xs=xs: (of_seq(xs), of_seq(ys)), arrow_85, arrow_86)


def remove_at(index, xs):
    is_done = False
    if index < 0:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    def arrow_87(i, e, index=index, xs=xs):
        nonlocal is_done
        if e.System_Collections_IEnumerator_MoveNext() if (True if (is_done) else (i < index)) else (False):
            return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        
        elif e.System_Collections_IEnumerator_MoveNext() if (i == index) else (False):
            is_done = True
            return some(e.System_Collections_Generic_IEnumerator_00601_get_Current()) if (e.System_Collections_IEnumerator_MoveNext()) else (None)
        
        else: 
            if not is_done:
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
            
            return None
        
    
    def arrow_88(e_1, index=index, xs=xs):
        dispose_2(e_1)
    
    return generate_indexed(lambda index=index, xs=xs: of_seq(xs), arrow_87, arrow_88)


def remove_many_at(index, count, xs):
    if index < 0:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    def arrow_89(i, e, index=index, count=count, xs=xs):
        if i < index:
            if e.System_Collections_IEnumerator_MoveNext():
                return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
            
            else: 
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
            
        
        else: 
            if i == index:
                for _ in range(1, count + 1, 1):
                    if not e.System_Collections_IEnumerator_MoveNext():
                        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "count")
                    
            
            return some(e.System_Collections_Generic_IEnumerator_00601_get_Current()) if (e.System_Collections_IEnumerator_MoveNext()) else (None)
        
    
    def arrow_90(e_1, index=index, count=count, xs=xs):
        dispose_2(e_1)
    
    return generate_indexed(lambda index=index, count=count, xs=xs: of_seq(xs), arrow_89, arrow_90)


def update_at(index, y, xs):
    is_done = False
    if index < 0:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    def arrow_91(i, e, index=index, y=y, xs=xs):
        nonlocal is_done
        if e.System_Collections_IEnumerator_MoveNext() if (True if (is_done) else (i < index)) else (False):
            return some(e.System_Collections_Generic_IEnumerator_00601_get_Current())
        
        elif e.System_Collections_IEnumerator_MoveNext() if (i == index) else (False):
            is_done = True
            return some(y)
        
        else: 
            if not is_done:
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
            
            return None
        
    
    def arrow_92(e_1, index=index, y=y, xs=xs):
        dispose_2(e_1)
    
    return generate_indexed(lambda index=index, y=y, xs=xs: of_seq(xs), arrow_91, arrow_92)


