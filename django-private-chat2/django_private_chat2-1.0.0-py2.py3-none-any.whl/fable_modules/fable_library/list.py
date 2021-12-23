from .string import join
from .util import (equals, structural_hash, compare, to_iterator, get_enumerator, IDisposable, ignore, is_array_like, uncurry)
from .types import Record
from .reflection import (option_type, record_type, class_type)
from .global_ import (SR_inputWasEmpty, SR_indexOutOfBounds, SR_keyNotFoundAlt, SR_differentLengths, SR_notEnoughElements, SR_inputMustBeNonNegative, SR_inputSequenceEmpty, SR_inputSequenceTooLong)
from .option import (some, value as value_1, default_arg)
from .array import (fill, fold_back as fold_back_1, fold_back2 as fold_back2_1, iterate as iterate_1, scan_back as scan_back_1, try_find_back as try_find_back_1, try_find_index_back as try_find_index_back_1, permute as permute_1, map as map_1, chunk_by_size as chunk_by_size_1, pairwise as pairwise_1, windowed as windowed_1, split_into as split_into_1, transpose as transpose_1)

def expr_93(gen0):
    return record_type("ListModule.FSharpList", [gen0], FSharpList, lambda: [["head", gen0], ["tail", option_type(FSharpList_reflection(gen0))]])


class FSharpList(Record):
    def __init__(self, head, tail):
        super().__init__()
        self.head = head
        self.tail = tail
    
    def __str__(self):
        xs = self
        return ("[" + join("; ", xs)) + "]"
    
    def __eq__(self, other):
        xs = self
        if xs is other:
            return True
        
        else: 
            def loop(xs_1_mut, ys_1_mut):
                while True:
                    (xs_1, ys_1) = (xs_1_mut, ys_1_mut)
                    match_value = (xs_1.tail, ys_1.tail)
                    if (match_value[0]) is not None:
                        if (match_value[1]) is not None:
                            xt = match_value[0]
                            yt = match_value[1]
                            if equals(xs_1.head, ys_1.head):
                                xs_1_mut = xt
                                ys_1_mut = yt
                                continue
                            
                            else: 
                                return False
                            
                        
                        else: 
                            return False
                        
                    
                    elif (match_value[1]) is not None:
                        return False
                    
                    else: 
                        return True
                    
                    break
            
            loop = loop
            return loop(xs, other)
        
    
    def GetHashCode(self):
        xs = self
        def loop(i_mut, h_mut, xs_1_mut):
            while True:
                (i, h, xs_1) = (i_mut, h_mut, xs_1_mut)
                match_value = xs_1.tail
                if match_value is not None:
                    t = match_value
                    if i > 18:
                        return h
                    
                    else: 
                        i_mut = i + 1
                        h_mut = ((h << 1) + structural_hash(xs_1.head)) + (631 * i)
                        xs_1_mut = t
                        continue
                    
                
                else: 
                    return h
                
                break
        
        return loop(0, 0, xs)
    
    def to_json(self, _key):
        this = self
        return list(this)
    
    def CompareTo(self, other):
        xs = self
        def loop(xs_1_mut, ys_1_mut):
            while True:
                (xs_1, ys_1) = (xs_1_mut, ys_1_mut)
                match_value = (xs_1.tail, ys_1.tail)
                if (match_value[0]) is not None:
                    if (match_value[1]) is not None:
                        xt = match_value[0]
                        yt = match_value[1]
                        c = compare(xs_1.head, ys_1.head) or 0
                        if c == 0:
                            xs_1_mut = xt
                            ys_1_mut = yt
                            continue
                        
                        else: 
                            return c
                        
                    
                    else: 
                        return 1
                    
                
                elif (match_value[1]) is not None:
                    return -1
                
                else: 
                    return 0
                
                break
        
        return loop(xs, other)
    
    def GetEnumerator(self):
        xs = self
        return ListEnumerator_1__ctor_3002E699(xs)
    
    def __iter__(self):
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_IEnumerable_GetEnumerator(self):
        xs = self
        return get_enumerator(xs)
    

FSharpList_reflection = expr_93

def expr_94(gen0):
    return class_type("ListModule.ListEnumerator`1", [gen0], ListEnumerator_1)


class ListEnumerator_1(IDisposable):
    def __init__(self, xs=None):
        self.xs = xs
        self.it = self.xs
        self.current = None
    
    def System_Collections_Generic_IEnumerator_00601_get_Current(self):
        __ = self
        return __.current
    
    def System_Collections_IEnumerator_get_Current(self):
        __ = self
        return __.current
    
    def System_Collections_IEnumerator_MoveNext(self):
        __ = self
        match_value = __.it.tail
        if match_value is not None:
            t = match_value
            __.current = __.it.head
            __.it = t
            return True
        
        else: 
            return False
        
    
    def System_Collections_IEnumerator_Reset(self):
        __ = self
        __.it = __.xs
        __.current = None
    
    def Dispose(self):
        pass
    

ListEnumerator_1_reflection = expr_94

def ListEnumerator_1__ctor_3002E699(xs):
    return ListEnumerator_1(xs)


def FSharpList_get_Empty():
    return FSharpList(None, None)


def FSharpList_Cons_305B8EAC(x, xs):
    return FSharpList(x, xs)


def FSharpList__get_IsEmpty(xs):
    return xs.tail is None


def FSharpList__get_Length(xs):
    def loop(i_mut, xs_1_mut, xs=xs):
        while True:
            (i, xs_1) = (i_mut, xs_1_mut)
            match_value = xs_1.tail
            if match_value is not None:
                i_mut = i + 1
                xs_1_mut = match_value
                continue
            
            else: 
                return i
            
            break
    
    return loop(0, xs)


def FSharpList__get_Head(xs):
    match_value = xs.tail
    if match_value is not None:
        return xs.head
    
    else: 
        raise Exception((SR_inputWasEmpty + "\\nParameter name: ") + "list")
    


def FSharpList__get_Tail(xs):
    match_value = xs.tail
    if match_value is not None:
        return match_value
    
    else: 
        raise Exception((SR_inputWasEmpty + "\\nParameter name: ") + "list")
    


def FSharpList__get_Item_Z524259A4(xs, index):
    def loop(i_mut, xs_1_mut, xs=xs, index=index):
        while True:
            (i, xs_1) = (i_mut, xs_1_mut)
            match_value = xs_1.tail
            if match_value is not None:
                if i == index:
                    return xs_1.head
                
                else: 
                    i_mut = i + 1
                    xs_1_mut = match_value
                    continue
                
            
            else: 
                raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
            
            break
    
    return loop(0, xs)


def empty():
    return FSharpList_get_Empty()


def cons(x, xs):
    return FSharpList_Cons_305B8EAC(x, xs)


def singleton(x=None):
    return FSharpList_Cons_305B8EAC(x, FSharpList_get_Empty())


def is_empty(xs):
    return FSharpList__get_IsEmpty(xs)


def length(xs):
    return FSharpList__get_Length(xs)


def head(xs):
    return FSharpList__get_Head(xs)


def try_head(xs):
    if FSharpList__get_IsEmpty(xs):
        return None
    
    else: 
        return some(FSharpList__get_Head(xs))
    


def tail(xs):
    return FSharpList__get_Tail(xs)


def try_last(xs_mut):
    while True:
        (xs,) = (xs_mut,)
        if FSharpList__get_IsEmpty(xs):
            return None
        
        else: 
            t = FSharpList__get_Tail(xs)
            if FSharpList__get_IsEmpty(t):
                return some(FSharpList__get_Head(xs))
            
            else: 
                xs_mut = t
                continue
            
        
        break


def last(xs):
    match_value = try_last(xs)
    if match_value is None:
        raise Exception(SR_inputWasEmpty)
    
    else: 
        return value_1(match_value)
    


def compare_with(comparer, xs, ys):
    def loop(xs_1_mut, ys_1_mut, comparer=comparer, xs=xs, ys=ys):
        while True:
            (xs_1, ys_1) = (xs_1_mut, ys_1_mut)
            match_value = (FSharpList__get_IsEmpty(xs_1), FSharpList__get_IsEmpty(ys_1))
            if match_value[0]:
                if match_value[1]:
                    return 0
                
                else: 
                    return -1
                
            
            elif match_value[1]:
                return 1
            
            else: 
                c = comparer(FSharpList__get_Head(xs_1), FSharpList__get_Head(ys_1)) or 0
                if c == 0:
                    xs_1_mut = FSharpList__get_Tail(xs_1)
                    ys_1_mut = FSharpList__get_Tail(ys_1)
                    continue
                
                else: 
                    return c
                
            
            break
    
    return loop(xs, ys)


def to_array(xs):
    len_1 = FSharpList__get_Length(xs) or 0
    res = fill([0] * len_1, 0, len_1, None)
    def loop(i_mut, xs_1_mut, xs=xs):
        while True:
            (i, xs_1) = (i_mut, xs_1_mut)
            if not FSharpList__get_IsEmpty(xs_1):
                res[i] = FSharpList__get_Head(xs_1)
                i_mut = i + 1
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue
            
            break
    
    loop(0, xs)
    return res


def fold(folder, state, xs):
    acc = state
    xs_1 = xs
    while not FSharpList__get_IsEmpty(xs_1):
        acc = folder(acc, FSharpList__get_Head(xs_1))
        xs_1 = FSharpList__get_Tail(xs_1)
    return acc


def reverse(xs):
    return fold(lambda acc, x=None, xs=xs: FSharpList_Cons_305B8EAC(x, acc), FSharpList_get_Empty(), xs)


def fold_back(folder, xs, state=None):
    return fold_back_1(folder, to_array(xs), state)


def fold_indexed(folder, state, xs):
    def loop(i_mut, acc_mut, xs_1_mut, folder=folder, state=state, xs=xs):
        while True:
            (i, acc, xs_1) = (i_mut, acc_mut, xs_1_mut)
            if FSharpList__get_IsEmpty(xs_1):
                return acc
            
            else: 
                i_mut = i + 1
                acc_mut = folder(i, acc, FSharpList__get_Head(xs_1))
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue
            
            break
    
    return loop(0, state, xs)


def fold2(folder, state, xs, ys):
    acc = state
    xs_1 = xs
    ys_1 = ys
    while not FSharpList__get_IsEmpty(ys_1) if (not FSharpList__get_IsEmpty(xs_1)) else (False):
        acc = folder(acc, FSharpList__get_Head(xs_1), FSharpList__get_Head(ys_1))
        xs_1 = FSharpList__get_Tail(xs_1)
        ys_1 = FSharpList__get_Tail(ys_1)
    return acc


def fold_back2(folder, xs, ys, state=None):
    return fold_back2_1(folder, to_array(xs), to_array(ys), state)


def unfold(gen, state=None):
    def loop(acc_mut, node_mut, gen=gen, state=state):
        while True:
            (acc, node) = (acc_mut, node_mut)
            match_value = gen(acc)
            if match_value is not None:
                acc_mut = match_value[1]
                def arrow_95(_unit=None):
                    t = FSharpList(match_value[0], None)
                    node.tail = t
                    return t
                
                node_mut = arrow_95()
                continue
            
            else: 
                return node
            
            break
    
    root = FSharpList_get_Empty()
    node_1 = loop(state, root)
    t_2 = FSharpList_get_Empty()
    node_1.tail = t_2
    return FSharpList__get_Tail(root)


def iterate(action, xs):
    def arrow_96(unit_var0, x=None, action=action, xs=xs):
        action(x)
    
    fold(arrow_96, None, xs)


def iterate2(action, xs, ys):
    def arrow_97(unit_var0, x, y=None, action=action, xs=xs, ys=ys):
        action(x, y)
    
    fold2(arrow_97, None, xs, ys)


def iterate_indexed(action, xs):
    def arrow_98(i, x=None, action=action, xs=xs):
        action(i, x)
        return i + 1
    
    ignore(fold(arrow_98, 0, xs))


def iterate_indexed2(action, xs, ys):
    def arrow_99(i, x, y=None, action=action, xs=xs, ys=ys):
        action(i, x, y)
        return i + 1
    
    ignore(fold2(arrow_99, 0, xs, ys))


def to_seq(xs):
    return xs


def of_array_with_tail(xs, tail_1):
    res = tail_1
    for i in range(len(xs) - 1, 0 - 1, -1):
        res = FSharpList_Cons_305B8EAC(xs[i], res)
    return res


def of_array(xs):
    return of_array_with_tail(xs, FSharpList_get_Empty())


def of_seq(xs):
    if is_array_like(xs):
        return of_array(xs)
    
    elif isinstance(xs, FSharpList):
        return xs
    
    else: 
        root = FSharpList_get_Empty()
        node = root
        with get_enumerator(xs) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                x = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
                def arrow_101(_unit=None):
                    xs_3 = node
                    def arrow_100(_unit=None):
                        t = FSharpList(x, None)
                        xs_3.tail = t
                        return t
                    
                    return arrow_100()
                
                node = arrow_101()
        xs_5 = node
        t_2 = FSharpList_get_Empty()
        xs_5.tail = t_2
        return FSharpList__get_Tail(root)
    


def concat(lists):
    root = FSharpList_get_Empty()
    node = root
    def action(xs, lists=lists):
        nonlocal node
        def arrow_103(acc, x=None, xs=xs):
            def arrow_102(_unit=None):
                t = FSharpList(x, None)
                acc.tail = t
                return t
            
            return arrow_102()
        
        node = fold(arrow_103, node, xs)
    
    if is_array_like(lists):
        iterate_1(action, lists)
    
    elif isinstance(lists, FSharpList):
        iterate(action, lists)
    
    else: 
        with get_enumerator(lists) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                action(enumerator.System_Collections_Generic_IEnumerator_00601_get_Current())
    
    xs_6 = node
    t_2 = FSharpList_get_Empty()
    xs_6.tail = t_2
    return FSharpList__get_Tail(root)


def scan(folder, state, xs):
    root = FSharpList_get_Empty()
    def arrow_104(_unit=None):
        t = FSharpList(state, None)
        root.tail = t
        return t
    
    node = arrow_104()
    acc = state
    xs_3 = xs
    while not FSharpList__get_IsEmpty(xs_3):
        acc = folder(acc, FSharpList__get_Head(xs_3))
        def arrow_106(_unit=None):
            xs_4 = node
            def arrow_105(_unit=None):
                t_2 = FSharpList(acc, None)
                xs_4.tail = t_2
                return t_2
            
            return arrow_105()
        
        node = arrow_106()
        xs_3 = FSharpList__get_Tail(xs_3)
    xs_6 = node
    t_4 = FSharpList_get_Empty()
    xs_6.tail = t_4
    return FSharpList__get_Tail(root)


def scan_back(folder, xs, state=None):
    return of_array(scan_back_1(folder, to_array(xs), state, None))


def append(xs, ys):
    return fold(lambda acc, x=None, xs=xs, ys=ys: FSharpList_Cons_305B8EAC(x, acc), ys, reverse(xs))


def collect(mapping, xs):
    root = FSharpList_get_Empty()
    node = root
    ys = xs
    while not FSharpList__get_IsEmpty(ys):
        zs = mapping(FSharpList__get_Head(ys))
        while not FSharpList__get_IsEmpty(zs):
            def arrow_108(_unit=None):
                xs_1 = node
                def arrow_107(_unit=None):
                    t = FSharpList(FSharpList__get_Head(zs), None)
                    xs_1.tail = t
                    return t
                
                return arrow_107()
            
            node = arrow_108()
            zs = FSharpList__get_Tail(zs)
        ys = FSharpList__get_Tail(ys)
    xs_3 = node
    t_2 = FSharpList_get_Empty()
    xs_3.tail = t_2
    return FSharpList__get_Tail(root)


def map_indexed(mapping, xs):
    root = FSharpList_get_Empty()
    def folder(i, acc, x=None, mapping=mapping, xs=xs):
        def arrow_109(_unit=None):
            t = FSharpList(mapping(i, x), None)
            acc.tail = t
            return t
        
        return arrow_109()
    
    node = fold_indexed(folder, root, xs)
    t_2 = FSharpList_get_Empty()
    node.tail = t_2
    return FSharpList__get_Tail(root)


def map(mapping, xs):
    root = FSharpList_get_Empty()
    def folder(acc, x=None, mapping=mapping, xs=xs):
        def arrow_110(_unit=None):
            t = FSharpList(mapping(x), None)
            acc.tail = t
            return t
        
        return arrow_110()
    
    node = fold(folder, root, xs)
    t_2 = FSharpList_get_Empty()
    node.tail = t_2
    return FSharpList__get_Tail(root)


def indexed(xs):
    return map_indexed(lambda i, x=None, xs=xs: (i, x), xs)


def map2(mapping, xs, ys):
    root = FSharpList_get_Empty()
    def folder(acc, x, y=None, mapping=mapping, xs=xs, ys=ys):
        def arrow_111(_unit=None):
            t = FSharpList(mapping(x, y), None)
            acc.tail = t
            return t
        
        return arrow_111()
    
    node = fold2(folder, root, xs, ys)
    t_2 = FSharpList_get_Empty()
    node.tail = t_2
    return FSharpList__get_Tail(root)


def map_indexed2(mapping, xs, ys):
    def loop(i_mut, acc_mut, xs_1_mut, ys_1_mut, mapping=mapping, xs=xs, ys=ys):
        while True:
            (i, acc, xs_1, ys_1) = (i_mut, acc_mut, xs_1_mut, ys_1_mut)
            if True if (FSharpList__get_IsEmpty(xs_1)) else (FSharpList__get_IsEmpty(ys_1)):
                return acc
            
            else: 
                i_mut = i + 1
                def arrow_112(_unit=None):
                    t = FSharpList(mapping(i, FSharpList__get_Head(xs_1), FSharpList__get_Head(ys_1)), None)
                    acc.tail = t
                    return t
                
                acc_mut = arrow_112()
                xs_1_mut = FSharpList__get_Tail(xs_1)
                ys_1_mut = FSharpList__get_Tail(ys_1)
                continue
            
            break
    
    root = FSharpList_get_Empty()
    node_1 = loop(0, root, xs, ys)
    t_2 = FSharpList_get_Empty()
    node_1.tail = t_2
    return FSharpList__get_Tail(root)


def map3(mapping, xs, ys, zs):
    def loop(acc_mut, xs_1_mut, ys_1_mut, zs_1_mut, mapping=mapping, xs=xs, ys=ys, zs=zs):
        while True:
            (acc, xs_1, ys_1, zs_1) = (acc_mut, xs_1_mut, ys_1_mut, zs_1_mut)
            if True if (True if (FSharpList__get_IsEmpty(xs_1)) else (FSharpList__get_IsEmpty(ys_1))) else (FSharpList__get_IsEmpty(zs_1)):
                return acc
            
            else: 
                def arrow_113(_unit=None):
                    t = FSharpList(mapping(FSharpList__get_Head(xs_1), FSharpList__get_Head(ys_1), FSharpList__get_Head(zs_1)), None)
                    acc.tail = t
                    return t
                
                acc_mut = arrow_113()
                xs_1_mut = FSharpList__get_Tail(xs_1)
                ys_1_mut = FSharpList__get_Tail(ys_1)
                zs_1_mut = FSharpList__get_Tail(zs_1)
                continue
            
            break
    
    root = FSharpList_get_Empty()
    node_1 = loop(root, xs, ys, zs)
    t_2 = FSharpList_get_Empty()
    node_1.tail = t_2
    return FSharpList__get_Tail(root)


def map_fold(mapping, state, xs):
    root = FSharpList_get_Empty()
    def folder(tupled_arg, x=None, mapping=mapping, state=state, xs=xs):
        pattern_input = mapping(tupled_arg[1], x)
        def arrow_114(_unit=None):
            t = FSharpList(pattern_input[0], None)
            tupled_arg[0].tail = t
            return t
        
        return (arrow_114(), pattern_input[1])
    
    pattern_input_1 = fold(folder, (root, state), xs)
    t_2 = FSharpList_get_Empty()
    pattern_input_1[0].tail = t_2
    return (FSharpList__get_Tail(root), pattern_input_1[1])


def map_fold_back(mapping, xs, state=None):
    return map_fold(lambda acc, x=None, mapping=mapping, xs=xs, state=state: mapping(x, acc), state, reverse(xs))


def try_pick(f, xs):
    def loop(xs_1_mut, f=f, xs=xs):
        while True:
            (xs_1,) = (xs_1_mut,)
            if FSharpList__get_IsEmpty(xs_1):
                return None
            
            else: 
                match_value = f(FSharpList__get_Head(xs_1))
                if match_value is None:
                    xs_1_mut = FSharpList__get_Tail(xs_1)
                    continue
                
                else: 
                    return match_value
                
            
            break
    
    return loop(xs)


def pick(f, xs):
    match_value = try_pick(f, xs)
    if match_value is None:
        def arrow_115(_unit=None):
            raise Exception(SR_keyNotFoundAlt)
        
        return arrow_115()
    
    else: 
        return value_1(match_value)
    


def try_find(f, xs):
    return try_pick(lambda x=None, f=f, xs=xs: some(x) if (f(x)) else (None), xs)


def find(f, xs):
    match_value = try_find(f, xs)
    if match_value is None:
        def arrow_116(_unit=None):
            raise Exception(SR_keyNotFoundAlt)
        
        return arrow_116()
    
    else: 
        return value_1(match_value)
    


def try_find_back(f, xs):
    return try_find_back_1(f, to_array(xs))


def find_back(f, xs):
    match_value = try_find_back(f, xs)
    if match_value is None:
        def arrow_117(_unit=None):
            raise Exception(SR_keyNotFoundAlt)
        
        return arrow_117()
    
    else: 
        return value_1(match_value)
    


def try_find_index(f, xs):
    def loop(i_mut, xs_1_mut, f=f, xs=xs):
        while True:
            (i, xs_1) = (i_mut, xs_1_mut)
            if FSharpList__get_IsEmpty(xs_1):
                return None
            
            elif f(FSharpList__get_Head(xs_1)):
                return i
            
            else: 
                i_mut = i + 1
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue
            
            break
    
    return loop(0, xs)


def find_index(f, xs):
    match_value = try_find_index(f, xs)
    if match_value is None:
        def arrow_118(_unit=None):
            raise Exception(SR_keyNotFoundAlt)
        
        return arrow_118()
    
    else: 
        return match_value
    


def try_find_index_back(f, xs):
    return try_find_index_back_1(f, to_array(xs))


def find_index_back(f, xs):
    match_value = try_find_index_back(f, xs)
    if match_value is None:
        def arrow_119(_unit=None):
            raise Exception(SR_keyNotFoundAlt)
        
        return arrow_119()
    
    else: 
        return match_value
    


def try_item(n, xs):
    def loop(i_mut, xs_1_mut, n=n, xs=xs):
        while True:
            (i, xs_1) = (i_mut, xs_1_mut)
            if FSharpList__get_IsEmpty(xs_1):
                return None
            
            elif i == n:
                return some(FSharpList__get_Head(xs_1))
            
            else: 
                i_mut = i + 1
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue
            
            break
    
    return loop(0, xs)


def item(n, xs):
    return FSharpList__get_Item_Z524259A4(xs, n)


def filter(f, xs):
    root = FSharpList_get_Empty()
    def folder(acc, x=None, f=f, xs=xs):
        if f(x):
            def arrow_120(_unit=None):
                t = FSharpList(x, None)
                acc.tail = t
                return t
            
            return arrow_120()
        
        else: 
            return acc
        
    
    node = fold(folder, root, xs)
    t_2 = FSharpList_get_Empty()
    node.tail = t_2
    return FSharpList__get_Tail(root)


def partition(f, xs):
    pattern_input = (FSharpList_get_Empty(), FSharpList_get_Empty())
    root2 = pattern_input[1]
    root1 = pattern_input[0]
    def folder(tupled_arg, f=f, xs=xs):
        lacc = tupled_arg[0]
        racc = tupled_arg[1]
        def arrow_123(x=None, tupled_arg=tupled_arg):
            def arrow_121(_unit=None):
                t = FSharpList(x, None)
                lacc.tail = t
                return t
            
            def arrow_122(_unit=None):
                t_2 = FSharpList(x, None)
                racc.tail = t_2
                return t_2
            
            return (arrow_121(), racc) if (f(x)) else ((lacc, arrow_122()))
        
        return arrow_123
    
    pattern_input_1 = fold(uncurry(2, folder), (root1, root2), xs)
    t_4 = FSharpList_get_Empty()
    pattern_input_1[0].tail = t_4
    t_5 = FSharpList_get_Empty()
    pattern_input_1[1].tail = t_5
    return (FSharpList__get_Tail(root1), FSharpList__get_Tail(root2))


def choose(f, xs):
    root = FSharpList_get_Empty()
    def folder(acc, x=None, f=f, xs=xs):
        match_value = f(x)
        if match_value is None:
            return acc
        
        else: 
            def arrow_124(_unit=None):
                t = FSharpList(value_1(match_value), None)
                acc.tail = t
                return t
            
            return arrow_124()
        
    
    node = fold(folder, root, xs)
    t_2 = FSharpList_get_Empty()
    node.tail = t_2
    return FSharpList__get_Tail(root)


def contains(value, xs, eq):
    return try_find_index(lambda v=None, value=value, xs=xs, eq=eq: eq.Equals(value, v), xs) is not None


def initialize(n, f):
    root = FSharpList_get_Empty()
    node = root
    for i in range(0, (n - 1) + 1, 1):
        def arrow_126(_unit=None):
            xs = node
            def arrow_125(_unit=None):
                t = FSharpList(f(i), None)
                xs.tail = t
                return t
            
            return arrow_125()
        
        node = arrow_126()
    xs_2 = node
    t_2 = FSharpList_get_Empty()
    xs_2.tail = t_2
    return FSharpList__get_Tail(root)


def replicate(n, x=None):
    return initialize(n, lambda _arg1, n=n, x=x: x)


def reduce(f, xs):
    if FSharpList__get_IsEmpty(xs):
        raise Exception(SR_inputWasEmpty)
    
    else: 
        return fold(f, head(xs), tail(xs))
    


def reduce_back(f, xs):
    if FSharpList__get_IsEmpty(xs):
        raise Exception(SR_inputWasEmpty)
    
    else: 
        return fold_back(f, tail(xs), head(xs))
    


def for_all(f, xs):
    return fold(lambda acc, x=None, f=f, xs=xs: f(x) if (acc) else (False), True, xs)


def for_all2(f, xs, ys):
    return fold2(lambda acc, x, y=None, f=f, xs=xs, ys=ys: f(x, y) if (acc) else (False), True, xs, ys)


def exists(f, xs):
    return try_find_index(f, xs) is not None


def exists2(f_mut, xs_mut, ys_mut):
    while True:
        (f, xs, ys) = (f_mut, xs_mut, ys_mut)
        match_value = (FSharpList__get_IsEmpty(xs), FSharpList__get_IsEmpty(ys))
        (pattern_matching_result,) = (None,)
        if match_value[0]:
            if match_value[1]:
                pattern_matching_result = 0
            
            else: 
                pattern_matching_result = 2
            
        
        elif match_value[1]:
            pattern_matching_result = 2
        
        else: 
            pattern_matching_result = 1
        
        if pattern_matching_result == 0:
            return False
        
        elif pattern_matching_result == 1:
            if f(FSharpList__get_Head(xs), FSharpList__get_Head(ys)):
                return True
            
            else: 
                f_mut = f
                xs_mut = FSharpList__get_Tail(xs)
                ys_mut = FSharpList__get_Tail(ys)
                continue
            
        
        elif pattern_matching_result == 2:
            raise Exception((SR_differentLengths + "\\nParameter name: ") + "list2")
        
        break


def unzip(xs):
    return fold_back(lambda tupled_arg, tupled_arg_1, xs=xs: (FSharpList_Cons_305B8EAC(tupled_arg[0], tupled_arg_1[0]), FSharpList_Cons_305B8EAC(tupled_arg[1], tupled_arg_1[1])), xs, (FSharpList_get_Empty(), FSharpList_get_Empty()))


def unzip3(xs):
    return fold_back(lambda tupled_arg, tupled_arg_1, xs=xs: (FSharpList_Cons_305B8EAC(tupled_arg[0], tupled_arg_1[0]), FSharpList_Cons_305B8EAC(tupled_arg[1], tupled_arg_1[1]), FSharpList_Cons_305B8EAC(tupled_arg[2], tupled_arg_1[2])), xs, (FSharpList_get_Empty(), FSharpList_get_Empty(), FSharpList_get_Empty()))


def zip(xs, ys):
    return map2(lambda x, y=None, xs=xs, ys=ys: (x, y), xs, ys)


def zip3(xs, ys, zs):
    return map3(lambda x, y, z=None, xs=xs, ys=ys, zs=zs: (x, y, z), xs, ys, zs)


def sort_with(comparer, xs):
    arr = to_array(xs)
    arr.sort()
    return of_array(arr)


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
    
    return averager.DivideByInt(fold(folder, averager.GetZero(), xs), count)


def average_by(f, xs, averager):
    count = 0
    def arrow_127(acc, x=None, f=f, xs=xs, averager=averager):
        nonlocal count
        count = (count + 1) or 0
        return averager.Add(acc, f(x))
    
    return averager.DivideByInt(fold(arrow_127, averager.GetZero(), xs), count)


def permute(f, xs):
    return of_array(permute_1(f, to_array(xs)))


def chunk_by_size(chunk_size, xs):
    return of_array(map_1(lambda xs_1, chunk_size=chunk_size, xs=xs: of_array(xs_1), chunk_by_size_1(chunk_size, to_array(xs)), None))


def all_pairs(xs, ys):
    root = FSharpList_get_Empty()
    node = root
    def arrow_131(x=None, xs=xs, ys=ys):
        def arrow_130(y=None):
            nonlocal node
            def arrow_129(_unit=None):
                xs_1 = node
                def arrow_128(_unit=None):
                    t = FSharpList((x, y), None)
                    xs_1.tail = t
                    return t
                
                return arrow_128()
            
            node = arrow_129()
        
        iterate(arrow_130, ys)
    
    iterate(arrow_131, xs)
    xs_3 = node
    t_2 = FSharpList_get_Empty()
    xs_3.tail = t_2
    return FSharpList__get_Tail(root)


def skip(count_mut, xs_mut):
    while True:
        (count, xs) = (count_mut, xs_mut)
        if count <= 0:
            return xs
        
        elif FSharpList__get_IsEmpty(xs):
            raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "list")
        
        else: 
            count_mut = count - 1
            xs_mut = FSharpList__get_Tail(xs)
            continue
        
        break


def skip_while(predicate_mut, xs_mut):
    while True:
        (predicate, xs) = (predicate_mut, xs_mut)
        if FSharpList__get_IsEmpty(xs):
            return xs
        
        elif not predicate(FSharpList__get_Head(xs)):
            return xs
        
        else: 
            predicate_mut = predicate
            xs_mut = FSharpList__get_Tail(xs)
            continue
        
        break


def take(count, xs):
    if count < 0:
        raise Exception((SR_inputMustBeNonNegative + "\\nParameter name: ") + "count")
    
    def loop(i_mut, acc_mut, xs_1_mut, count=count, xs=xs):
        while True:
            (i, acc, xs_1) = (i_mut, acc_mut, xs_1_mut)
            if i <= 0:
                return acc
            
            elif FSharpList__get_IsEmpty(xs_1):
                raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "list")
            
            else: 
                i_mut = i - 1
                def arrow_132(_unit=None):
                    t = FSharpList(FSharpList__get_Head(xs_1), None)
                    acc.tail = t
                    return t
                
                acc_mut = arrow_132()
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue
            
            break
    
    root = FSharpList_get_Empty()
    node = loop(count, root, xs)
    t_2 = FSharpList_get_Empty()
    node.tail = t_2
    return FSharpList__get_Tail(root)


def take_while(predicate, xs):
    def loop(acc_mut, xs_1_mut, predicate=predicate, xs=xs):
        while True:
            (acc, xs_1) = (acc_mut, xs_1_mut)
            if FSharpList__get_IsEmpty(xs_1):
                return acc
            
            elif not predicate(FSharpList__get_Head(xs_1)):
                return acc
            
            else: 
                def arrow_133(_unit=None):
                    t = FSharpList(FSharpList__get_Head(xs_1), None)
                    acc.tail = t
                    return t
                
                acc_mut = arrow_133()
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue
            
            break
    
    root = FSharpList_get_Empty()
    node = loop(root, xs)
    t_2 = FSharpList_get_Empty()
    node.tail = t_2
    return FSharpList__get_Tail(root)


def truncate(count, xs):
    def loop(i_mut, acc_mut, xs_1_mut, count=count, xs=xs):
        while True:
            (i, acc, xs_1) = (i_mut, acc_mut, xs_1_mut)
            if i <= 0:
                return acc
            
            elif FSharpList__get_IsEmpty(xs_1):
                return acc
            
            else: 
                i_mut = i - 1
                def arrow_134(_unit=None):
                    t = FSharpList(FSharpList__get_Head(xs_1), None)
                    acc.tail = t
                    return t
                
                acc_mut = arrow_134()
                xs_1_mut = FSharpList__get_Tail(xs_1)
                continue
            
            break
    
    root = FSharpList_get_Empty()
    node = loop(count, root, xs)
    t_2 = FSharpList_get_Empty()
    node.tail = t_2
    return FSharpList__get_Tail(root)


def get_slice(start_index, end_index, xs):
    len_1 = length(xs) or 0
    start_index_1 = default_arg(start_index, 0) or 0
    end_index_1 = default_arg(end_index, len_1 - 1) or 0
    if start_index_1 < 0:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "startIndex")
    
    elif end_index_1 >= len_1:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "endIndex")
    
    elif end_index_1 < start_index_1:
        return FSharpList_get_Empty()
    
    else: 
        return take((end_index_1 - start_index_1) + 1, skip(start_index_1, xs))
    


def split_at(index, xs):
    if index < 0:
        raise Exception((SR_inputMustBeNonNegative + "\\nParameter name: ") + "index")
    
    if index > FSharpList__get_Length(xs):
        raise Exception((SR_notEnoughElements + "\\nParameter name: ") + "index")
    
    return (take(index, xs), skip(index, xs))


def exactly_one(xs):
    if FSharpList__get_IsEmpty(xs):
        raise Exception((SR_inputSequenceEmpty + "\\nParameter name: ") + "list")
    
    elif FSharpList__get_IsEmpty(FSharpList__get_Tail(xs)):
        return FSharpList__get_Head(xs)
    
    else: 
        raise Exception((SR_inputSequenceTooLong + "\\nParameter name: ") + "list")
    


def try_exactly_one(xs):
    if FSharpList__get_IsEmpty(FSharpList__get_Tail(xs)) if (not FSharpList__get_IsEmpty(xs)) else (False):
        return some(FSharpList__get_Head(xs))
    
    else: 
        return None
    


def where(predicate, xs):
    return filter(predicate, xs)


def pairwise(xs):
    return of_array(pairwise_1(to_array(xs)))


def windowed(window_size, xs):
    return of_array(map_1(lambda xs_1, window_size=window_size, xs=xs: of_array(xs_1), windowed_1(window_size, to_array(xs)), None))


def split_into(chunks, xs):
    return of_array(map_1(lambda xs_1, chunks=chunks, xs=xs: of_array(xs_1), split_into_1(chunks, to_array(xs)), None))


def transpose(lists):
    return of_array(map_1(lambda xs_1, lists=lists: of_array(xs_1), transpose_1(map_1(lambda xs, lists=lists: to_array(xs), list(lists), None), None), None))


def insert_at(index, y, xs):
    i = -1
    is_done = False
    def folder(acc, x=None, index=index, y=y, xs=xs):
        nonlocal i, is_done
        i = (i + 1) or 0
        if i == index:
            is_done = True
            return FSharpList_Cons_305B8EAC(x, FSharpList_Cons_305B8EAC(y, acc))
        
        else: 
            return FSharpList_Cons_305B8EAC(x, acc)
        
    
    result = fold(folder, FSharpList_get_Empty(), xs)
    def arrow_135(_unit=None):
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    return reverse(result if (is_done) else (FSharpList_Cons_305B8EAC(y, result) if ((i + 1) == index) else (arrow_135())))


def insert_many_at(index, ys, xs):
    i = -1
    is_done = False
    ys_1 = of_seq(ys)
    def folder(acc, x=None, index=index, ys=ys, xs=xs):
        nonlocal i, is_done
        i = (i + 1) or 0
        if i == index:
            is_done = True
            return FSharpList_Cons_305B8EAC(x, append(ys_1, acc))
        
        else: 
            return FSharpList_Cons_305B8EAC(x, acc)
        
    
    result = fold(folder, FSharpList_get_Empty(), xs)
    def arrow_136(_unit=None):
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    return reverse(result if (is_done) else (append(ys_1, result) if ((i + 1) == index) else (arrow_136())))


def remove_at(index, xs):
    i = -1
    is_done = False
    def f(_arg1=None, index=index, xs=xs):
        nonlocal i, is_done
        i = (i + 1) or 0
        if i == index:
            is_done = True
            return False
        
        else: 
            return True
        
    
    ys = filter(f, xs)
    if not is_done:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    return ys


def remove_many_at(index, count, xs):
    i = -1
    status = -1
    def f(_arg1=None, index=index, count=count, xs=xs):
        nonlocal i, status
        i = (i + 1) or 0
        if i == index:
            status = 0
            return False
        
        elif i > index:
            if i < (index + count):
                return False
            
            else: 
                status = 1
                return True
            
        
        else: 
            return True
        
    
    ys = filter(f, xs)
    status_1 = (1 if ((i + 1) == (index + count) if (status == 0) else (False)) else (status)) or 0
    if status_1 < 1:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + ("index" if (status_1 < 0) else ("count")))
    
    return ys


def update_at(index, y, xs):
    is_done = False
    def mapping(i, x=None, index=index, y=y, xs=xs):
        nonlocal is_done
        if i == index:
            is_done = True
            return y
        
        else: 
            return x
        
    
    ys = map_indexed(mapping, xs)
    if not is_done:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    return ys


