from .reflection import (class_type, option_type, list_type, bool_type, record_type)
from .option import (value as value_1, some)
from .list import (cons, empty as empty_1, fold as fold_1, FSharpList, is_empty as is_empty_1, tail, head, of_array_with_tail, singleton)
from .array import fill
from .util import (is_array_like, get_enumerator, IDisposable, equals, to_iterator, compare, ignore, structural_hash)
from .types import Record
from .seq import (unfold, map as map_1, compare_with, iterate as iterate_1, pick as pick_1, try_pick as try_pick_1)
from .string import (join, format)

def expr_137(gen0, gen1):
    return class_type("Map.MapTreeLeaf`2", [gen0, gen1], MapTreeLeaf_2)


class MapTreeLeaf_2:
    def __init__(self, k, v=None):
        self.k = k
        self.v = v
    

MapTreeLeaf_2_reflection = expr_137

def MapTreeLeaf_2__ctor_5BDDA1(k, v=None):
    return MapTreeLeaf_2(k, v)


def MapTreeLeaf_2__get_Key(_):
    return _.k


def MapTreeLeaf_2__get_Value(_):
    return _.v


def expr_138(gen0, gen1):
    return class_type("Map.MapTreeNode`2", [gen0, gen1], MapTreeNode_2, MapTreeLeaf_2_reflection(gen0, gen1))


class MapTreeNode_2(MapTreeLeaf_2):
    def __init__(self, k, v, left, right, h):
        super().__init__(k, v)
        self.left = left
        self.right = right
        self.h = h or 0
    

MapTreeNode_2_reflection = expr_138

def MapTreeNode_2__ctor_Z39DE9543(k, v, left, right, h):
    return MapTreeNode_2(k, v, left, right, h)


def MapTreeNode_2__get_Left(_):
    return _.left


def MapTreeNode_2__get_Right(_):
    return _.right


def MapTreeNode_2__get_Height(_):
    return _.h


def MapTreeModule_empty():
    return None


def MapTreeModule_sizeAux(acc_mut, m_mut):
    while True:
        (acc, m) = (acc_mut, m_mut)
        if m is not None:
            m2 = m
            if isinstance(m2, MapTreeNode_2):
                acc_mut = MapTreeModule_sizeAux(acc + 1, MapTreeNode_2__get_Left(m2))
                m_mut = MapTreeNode_2__get_Right(m2)
                continue
            
            else: 
                return acc + 1
            
        
        else: 
            return acc
        
        break


def MapTreeModule_size(x=None):
    return MapTreeModule_sizeAux(0, x)


def MapTreeModule_mk(l, k, v, r=None):
    hl = None
    m = l
    def arrow_139(_unit=None):
        m2 = m
        return MapTreeNode_2__get_Height(m2) if (isinstance(m2, MapTreeNode_2)) else (1)
    
    hl = arrow_139() if (m is not None) else (0)
    hr = None
    m_1 = r
    def arrow_140(_unit=None):
        m2_1 = m_1
        return MapTreeNode_2__get_Height(m2_1) if (isinstance(m2_1, MapTreeNode_2)) else (1)
    
    hr = arrow_140() if (m_1 is not None) else (0)
    m_2 = (hr if (hl < hr) else (hl)) or 0
    if m_2 == 0:
        return MapTreeLeaf_2__ctor_5BDDA1(k, v)
    
    else: 
        return MapTreeNode_2__ctor_Z39DE9543(k, v, l, r, m_2 + 1)
    


def MapTreeModule_rebalance(t1, k, v, t2=None):
    t1h = None
    m = t1
    def arrow_141(_unit=None):
        m2 = m
        return MapTreeNode_2__get_Height(m2) if (isinstance(m2, MapTreeNode_2)) else (1)
    
    t1h = arrow_141() if (m is not None) else (0)
    t2h = None
    m_1 = t2
    def arrow_142(_unit=None):
        m2_1 = m_1
        return MapTreeNode_2__get_Height(m2_1) if (isinstance(m2_1, MapTreeNode_2)) else (1)
    
    t2h = arrow_142() if (m_1 is not None) else (0)
    if t2h > (t1h + 2):
        match_value = value_1(t2)
        if isinstance(match_value, MapTreeNode_2):
            def arrow_144(_unit=None):
                m_2 = MapTreeNode_2__get_Left(match_value)
                def arrow_143(_unit=None):
                    m2_2 = m_2
                    return MapTreeNode_2__get_Height(m2_2) if (isinstance(m2_2, MapTreeNode_2)) else (1)
                
                return arrow_143() if (m_2 is not None) else (0)
            
            if arrow_144() > (t1h + 1):
                match_value_1 = value_1(MapTreeNode_2__get_Left(match_value))
                if isinstance(match_value_1, MapTreeNode_2):
                    return MapTreeModule_mk(MapTreeModule_mk(t1, k, v, MapTreeNode_2__get_Left(match_value_1)), MapTreeLeaf_2__get_Key(match_value_1), MapTreeLeaf_2__get_Value(match_value_1), MapTreeModule_mk(MapTreeNode_2__get_Right(match_value_1), MapTreeLeaf_2__get_Key(match_value), MapTreeLeaf_2__get_Value(match_value), MapTreeNode_2__get_Right(match_value)))
                
                else: 
                    raise Exception("internal error: Map.rebalance")
                
            
            else: 
                return MapTreeModule_mk(MapTreeModule_mk(t1, k, v, MapTreeNode_2__get_Left(match_value)), MapTreeLeaf_2__get_Key(match_value), MapTreeLeaf_2__get_Value(match_value), MapTreeNode_2__get_Right(match_value))
            
        
        else: 
            raise Exception("internal error: Map.rebalance")
        
    
    elif t1h > (t2h + 2):
        match_value_2 = value_1(t1)
        if isinstance(match_value_2, MapTreeNode_2):
            def arrow_146(_unit=None):
                m_3 = MapTreeNode_2__get_Right(match_value_2)
                def arrow_145(_unit=None):
                    m2_3 = m_3
                    return MapTreeNode_2__get_Height(m2_3) if (isinstance(m2_3, MapTreeNode_2)) else (1)
                
                return arrow_145() if (m_3 is not None) else (0)
            
            if arrow_146() > (t2h + 1):
                match_value_3 = value_1(MapTreeNode_2__get_Right(match_value_2))
                if isinstance(match_value_3, MapTreeNode_2):
                    return MapTreeModule_mk(MapTreeModule_mk(MapTreeNode_2__get_Left(match_value_2), MapTreeLeaf_2__get_Key(match_value_2), MapTreeLeaf_2__get_Value(match_value_2), MapTreeNode_2__get_Left(match_value_3)), MapTreeLeaf_2__get_Key(match_value_3), MapTreeLeaf_2__get_Value(match_value_3), MapTreeModule_mk(MapTreeNode_2__get_Right(match_value_3), k, v, t2))
                
                else: 
                    raise Exception("internal error: Map.rebalance")
                
            
            else: 
                return MapTreeModule_mk(MapTreeNode_2__get_Left(match_value_2), MapTreeLeaf_2__get_Key(match_value_2), MapTreeLeaf_2__get_Value(match_value_2), MapTreeModule_mk(MapTreeNode_2__get_Right(match_value_2), k, v, t2))
            
        
        else: 
            raise Exception("internal error: Map.rebalance")
        
    
    else: 
        return MapTreeModule_mk(t1, k, v, t2)
    


def MapTreeModule_add(comparer, k, v, m=None):
    if m is not None:
        m2 = m
        c = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2)) or 0
        if isinstance(m2, MapTreeNode_2):
            if c < 0:
                return MapTreeModule_rebalance(MapTreeModule_add(comparer, k, v, MapTreeNode_2__get_Left(m2)), MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), MapTreeNode_2__get_Right(m2))
            
            elif c == 0:
                return MapTreeNode_2__ctor_Z39DE9543(k, v, MapTreeNode_2__get_Left(m2), MapTreeNode_2__get_Right(m2), MapTreeNode_2__get_Height(m2))
            
            else: 
                return MapTreeModule_rebalance(MapTreeNode_2__get_Left(m2), MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), MapTreeModule_add(comparer, k, v, MapTreeNode_2__get_Right(m2)))
            
        
        elif c < 0:
            return MapTreeNode_2__ctor_Z39DE9543(k, v, MapTreeModule_empty(), m, 2)
        
        elif c == 0:
            return MapTreeLeaf_2__ctor_5BDDA1(k, v)
        
        else: 
            return MapTreeNode_2__ctor_Z39DE9543(k, v, m, MapTreeModule_empty(), 2)
        
    
    else: 
        return MapTreeLeaf_2__ctor_5BDDA1(k, v)
    


def MapTreeModule_tryFind(comparer_mut, k_mut, m_mut):
    while True:
        (comparer, k, m) = (comparer_mut, k_mut, m_mut)
        if m is not None:
            m2 = m
            c = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2)) or 0
            if c == 0:
                return some(MapTreeLeaf_2__get_Value(m2))
            
            elif isinstance(m2, MapTreeNode_2):
                comparer_mut = comparer
                k_mut = k
                m_mut = MapTreeNode_2__get_Left(m2) if (c < 0) else (MapTreeNode_2__get_Right(m2))
                continue
            
            else: 
                return None
            
        
        else: 
            return None
        
        break


def MapTreeModule_find(comparer, k, m=None):
    match_value = MapTreeModule_tryFind(comparer, k, m)
    if match_value is None:
        raise Exception()
    
    else: 
        return value_1(match_value)
    


def MapTreeModule_partition1(comparer, f, k, v, acc1=None, acc2=None):
    if f(k, v):
        return (MapTreeModule_add(comparer, k, v, acc1), acc2)
    
    else: 
        return (acc1, MapTreeModule_add(comparer, k, v, acc2))
    


def MapTreeModule_partitionAux(comparer_mut, f_mut, m_mut, acc_0_mut, acc_1_mut):
    while True:
        (comparer, f, m, acc_0, acc_1) = (comparer_mut, f_mut, m_mut, acc_0_mut, acc_1_mut)
        acc = (acc_0, acc_1)
        if m is not None:
            m2 = m
            if isinstance(m2, MapTreeNode_2):
                acc_2 = MapTreeModule_partitionAux(comparer, f, MapTreeNode_2__get_Right(m2), acc[0], acc[1])
                acc_3 = MapTreeModule_partition1(comparer, f, MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), acc_2[0], acc_2[1])
                comparer_mut = comparer
                f_mut = f
                m_mut = MapTreeNode_2__get_Left(m2)
                acc_0_mut = acc_3[0]
                acc_1_mut = acc_3[1]
                continue
            
            else: 
                return MapTreeModule_partition1(comparer, f, MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), acc[0], acc[1])
            
        
        else: 
            return acc
        
        break


def MapTreeModule_partition(comparer, f, m=None):
    return MapTreeModule_partitionAux(comparer, f, m, MapTreeModule_empty(), MapTreeModule_empty())


def MapTreeModule_filter1(comparer, f, k, v, acc=None):
    if f(k, v):
        return MapTreeModule_add(comparer, k, v, acc)
    
    else: 
        return acc
    


def MapTreeModule_filterAux(comparer_mut, f_mut, m_mut, acc_mut):
    while True:
        (comparer, f, m, acc) = (comparer_mut, f_mut, m_mut, acc_mut)
        if m is not None:
            m2 = m
            if isinstance(m2, MapTreeNode_2):
                acc_1 = MapTreeModule_filterAux(comparer, f, MapTreeNode_2__get_Left(m2), acc)
                acc_2 = MapTreeModule_filter1(comparer, f, MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), acc_1)
                comparer_mut = comparer
                f_mut = f
                m_mut = MapTreeNode_2__get_Right(m2)
                acc_mut = acc_2
                continue
            
            else: 
                return MapTreeModule_filter1(comparer, f, MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), acc)
            
        
        else: 
            return acc
        
        break


def MapTreeModule_filter(comparer, f, m=None):
    return MapTreeModule_filterAux(comparer, f, m, MapTreeModule_empty())


def MapTreeModule_spliceOutSuccessor(m=None):
    if m is not None:
        m2 = m
        if isinstance(m2, MapTreeNode_2):
            if MapTreeNode_2__get_Left(m2) is None:
                return (MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), MapTreeNode_2__get_Right(m2))
            
            else: 
                pattern_input = MapTreeModule_spliceOutSuccessor(MapTreeNode_2__get_Left(m2))
                return (pattern_input[0], pattern_input[1], MapTreeModule_mk(pattern_input[2], MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), MapTreeNode_2__get_Right(m2)))
            
        
        else: 
            return (MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), MapTreeModule_empty())
        
    
    else: 
        raise Exception("internal error: Map.spliceOutSuccessor")
    


def MapTreeModule_remove(comparer, k, m=None):
    if m is not None:
        m2 = m
        c = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2)) or 0
        if isinstance(m2, MapTreeNode_2):
            if c < 0:
                return MapTreeModule_rebalance(MapTreeModule_remove(comparer, k, MapTreeNode_2__get_Left(m2)), MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), MapTreeNode_2__get_Right(m2))
            
            elif c == 0:
                if MapTreeNode_2__get_Left(m2) is None:
                    return MapTreeNode_2__get_Right(m2)
                
                elif MapTreeNode_2__get_Right(m2) is None:
                    return MapTreeNode_2__get_Left(m2)
                
                else: 
                    pattern_input = MapTreeModule_spliceOutSuccessor(MapTreeNode_2__get_Right(m2))
                    return MapTreeModule_mk(MapTreeNode_2__get_Left(m2), pattern_input[0], pattern_input[1], pattern_input[2])
                
            
            else: 
                return MapTreeModule_rebalance(MapTreeNode_2__get_Left(m2), MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), MapTreeModule_remove(comparer, k, MapTreeNode_2__get_Right(m2)))
            
        
        elif c == 0:
            return MapTreeModule_empty()
        
        else: 
            return m
        
    
    else: 
        return MapTreeModule_empty()
    


def MapTreeModule_change(comparer, k, u, m=None):
    if m is not None:
        m2 = m
        if isinstance(m2, MapTreeNode_2):
            c = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2)) or 0
            if c < 0:
                return MapTreeModule_rebalance(MapTreeModule_change(comparer, k, u, MapTreeNode_2__get_Left(m2)), MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), MapTreeNode_2__get_Right(m2))
            
            elif c == 0:
                match_value_1 = u(some(MapTreeLeaf_2__get_Value(m2)))
                if match_value_1 is not None:
                    return MapTreeNode_2__ctor_Z39DE9543(k, value_1(match_value_1), MapTreeNode_2__get_Left(m2), MapTreeNode_2__get_Right(m2), MapTreeNode_2__get_Height(m2))
                
                elif MapTreeNode_2__get_Left(m2) is None:
                    return MapTreeNode_2__get_Right(m2)
                
                elif MapTreeNode_2__get_Right(m2) is None:
                    return MapTreeNode_2__get_Left(m2)
                
                else: 
                    pattern_input = MapTreeModule_spliceOutSuccessor(MapTreeNode_2__get_Right(m2))
                    return MapTreeModule_mk(MapTreeNode_2__get_Left(m2), pattern_input[0], pattern_input[1], pattern_input[2])
                
            
            else: 
                return MapTreeModule_rebalance(MapTreeNode_2__get_Left(m2), MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), MapTreeModule_change(comparer, k, u, MapTreeNode_2__get_Right(m2)))
            
        
        else: 
            c_1 = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2)) or 0
            if c_1 < 0:
                match_value_2 = u(None)
                if match_value_2 is not None:
                    return MapTreeNode_2__ctor_Z39DE9543(k, value_1(match_value_2), MapTreeModule_empty(), m, 2)
                
                else: 
                    return m
                
            
            elif c_1 == 0:
                match_value_3 = u(some(MapTreeLeaf_2__get_Value(m2)))
                if match_value_3 is not None:
                    return MapTreeLeaf_2__ctor_5BDDA1(k, value_1(match_value_3))
                
                else: 
                    return MapTreeModule_empty()
                
            
            else: 
                match_value_4 = u(None)
                if match_value_4 is not None:
                    return MapTreeNode_2__ctor_Z39DE9543(k, value_1(match_value_4), m, MapTreeModule_empty(), 2)
                
                else: 
                    return m
                
            
        
    
    else: 
        match_value = u(None)
        if match_value is not None:
            return MapTreeLeaf_2__ctor_5BDDA1(k, value_1(match_value))
        
        else: 
            return m
        
    


def MapTreeModule_mem(comparer_mut, k_mut, m_mut):
    while True:
        (comparer, k, m) = (comparer_mut, k_mut, m_mut)
        if m is not None:
            m2 = m
            c = comparer.Compare(k, MapTreeLeaf_2__get_Key(m2)) or 0
            if isinstance(m2, MapTreeNode_2):
                if c < 0:
                    comparer_mut = comparer
                    k_mut = k
                    m_mut = MapTreeNode_2__get_Left(m2)
                    continue
                
                elif c == 0:
                    return True
                
                else: 
                    comparer_mut = comparer
                    k_mut = k
                    m_mut = MapTreeNode_2__get_Right(m2)
                    continue
                
            
            else: 
                return c == 0
            
        
        else: 
            return False
        
        break


def MapTreeModule_iterOpt(f_mut, m_mut):
    while True:
        (f, m) = (f_mut, m_mut)
        if m is not None:
            m2 = m
            if isinstance(m2, MapTreeNode_2):
                MapTreeModule_iterOpt(f, MapTreeNode_2__get_Left(m2))
                f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
                f_mut = f
                m_mut = MapTreeNode_2__get_Right(m2)
                continue
            
            else: 
                f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
            
        
        break


def MapTreeModule_iter(f, m=None):
    MapTreeModule_iterOpt(f, m)


def MapTreeModule_tryPickOpt(f_mut, m_mut):
    while True:
        (f, m) = (f_mut, m_mut)
        if m is not None:
            m2 = m
            if isinstance(m2, MapTreeNode_2):
                match_value = MapTreeModule_tryPickOpt(f, MapTreeNode_2__get_Left(m2))
                if match_value is None:
                    match_value_1 = f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
                    if match_value_1 is None:
                        f_mut = f
                        m_mut = MapTreeNode_2__get_Right(m2)
                        continue
                    
                    else: 
                        return match_value_1
                    
                
                else: 
                    return match_value
                
            
            else: 
                return f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
            
        
        else: 
            return None
        
        break


def MapTreeModule_tryPick(f, m=None):
    return MapTreeModule_tryPickOpt(f, m)


def MapTreeModule_existsOpt(f_mut, m_mut):
    while True:
        (f, m) = (f_mut, m_mut)
        if m is not None:
            m2 = m
            if isinstance(m2, MapTreeNode_2):
                if True if (MapTreeModule_existsOpt(f, MapTreeNode_2__get_Left(m2))) else (f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))):
                    return True
                
                else: 
                    f_mut = f
                    m_mut = MapTreeNode_2__get_Right(m2)
                    continue
                
            
            else: 
                return f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
            
        
        else: 
            return False
        
        break


def MapTreeModule_exists(f, m=None):
    return MapTreeModule_existsOpt(f, m)


def MapTreeModule_forallOpt(f_mut, m_mut):
    while True:
        (f, m) = (f_mut, m_mut)
        if m is not None:
            m2 = m
            if isinstance(m2, MapTreeNode_2):
                if f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2)) if (MapTreeModule_forallOpt(f, MapTreeNode_2__get_Left(m2))) else (False):
                    f_mut = f
                    m_mut = MapTreeNode_2__get_Right(m2)
                    continue
                
                else: 
                    return False
                
            
            else: 
                return f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
            
        
        else: 
            return True
        
        break


def MapTreeModule_forall(f, m=None):
    return MapTreeModule_forallOpt(f, m)


def MapTreeModule_map(f, m=None):
    if m is not None:
        m2 = m
        if isinstance(m2, MapTreeNode_2):
            l2 = MapTreeModule_map(f, MapTreeNode_2__get_Left(m2))
            v2 = f(MapTreeLeaf_2__get_Value(m2))
            r2 = MapTreeModule_map(f, MapTreeNode_2__get_Right(m2))
            return MapTreeNode_2__ctor_Z39DE9543(MapTreeLeaf_2__get_Key(m2), v2, l2, r2, MapTreeNode_2__get_Height(m2))
        
        else: 
            return MapTreeLeaf_2__ctor_5BDDA1(MapTreeLeaf_2__get_Key(m2), f(MapTreeLeaf_2__get_Value(m2)))
        
    
    else: 
        return MapTreeModule_empty()
    


def MapTreeModule_mapiOpt(f, m=None):
    if m is not None:
        m2 = m
        if isinstance(m2, MapTreeNode_2):
            l2 = MapTreeModule_mapiOpt(f, MapTreeNode_2__get_Left(m2))
            v2 = f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
            r2 = MapTreeModule_mapiOpt(f, MapTreeNode_2__get_Right(m2))
            return MapTreeNode_2__ctor_Z39DE9543(MapTreeLeaf_2__get_Key(m2), v2, l2, r2, MapTreeNode_2__get_Height(m2))
        
        else: 
            return MapTreeLeaf_2__ctor_5BDDA1(MapTreeLeaf_2__get_Key(m2), f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2)))
        
    
    else: 
        return MapTreeModule_empty()
    


def MapTreeModule_mapi(f, m=None):
    return MapTreeModule_mapiOpt(f, m)


def MapTreeModule_foldBackOpt(f_mut, m_mut, x_mut=None):
    while True:
        (f, m, x) = (f_mut, m_mut, x_mut)
        if m is not None:
            m2 = m
            if isinstance(m2, MapTreeNode_2):
                x_1 = MapTreeModule_foldBackOpt(f, MapTreeNode_2__get_Right(m2), x)
                x_2 = f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), x_1)
                f_mut = f
                m_mut = MapTreeNode_2__get_Left(m2)
                x_mut = x_2
                continue
            
            else: 
                return f(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), x)
            
        
        else: 
            return x
        
        break


def MapTreeModule_foldBack(f, m, x=None):
    return MapTreeModule_foldBackOpt(f, m, x)


def MapTreeModule_foldOpt(f_mut, x_mut, m_mut):
    while True:
        (f, x, m) = (f_mut, x_mut, m_mut)
        if m is not None:
            m2 = m
            if isinstance(m2, MapTreeNode_2):
                f_mut = f
                x_mut = f(MapTreeModule_foldOpt(f, x, MapTreeNode_2__get_Left(m2)), MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
                m_mut = MapTreeNode_2__get_Right(m2)
                continue
            
            else: 
                return f(x, MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2))
            
        
        else: 
            return x
        
        break


def MapTreeModule_fold(f, x, m=None):
    return MapTreeModule_foldOpt(f, x, m)


def MapTreeModule_foldSectionOpt(comparer, lo, hi, f, m, x=None):
    def fold_from_to(f_1_mut, m_1_mut, x_1_mut=None, comparer=comparer, lo=lo, hi=hi, f=f, m=m, x=x):
        while True:
            (f_1, m_1, x_1) = (f_1_mut, m_1_mut, x_1_mut)
            if m_1 is not None:
                m2 = m_1
                if isinstance(m2, MapTreeNode_2):
                    c_lo_key = comparer.Compare(lo, MapTreeLeaf_2__get_Key(m2)) or 0
                    c_key_hi = comparer.Compare(MapTreeLeaf_2__get_Key(m2), hi) or 0
                    x_2 = fold_from_to(f_1, MapTreeNode_2__get_Left(m2), x_1) if (c_lo_key < 0) else (x_1)
                    x_3 = f_1(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), x_2) if (c_key_hi <= 0 if (c_lo_key <= 0) else (False)) else (x_2)
                    if c_key_hi < 0:
                        f_1_mut = f_1
                        m_1_mut = MapTreeNode_2__get_Right(m2)
                        x_1_mut = x_3
                        continue
                    
                    else: 
                        return x_3
                    
                
                elif comparer.Compare(MapTreeLeaf_2__get_Key(m2), hi) <= 0 if (comparer.Compare(lo, MapTreeLeaf_2__get_Key(m2)) <= 0) else (False):
                    return f_1(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2), x_1)
                
                else: 
                    return x_1
                
            
            else: 
                return x_1
            
            break
    
    if comparer.Compare(lo, hi) == 1:
        return x
    
    else: 
        return fold_from_to(f, m, x)
    


def MapTreeModule_foldSection(comparer, lo, hi, f, m, x=None):
    return MapTreeModule_foldSectionOpt(comparer, lo, hi, f, m, x)


def MapTreeModule_toList(m=None):
    def loop(m_1_mut, acc_mut, m=m):
        while True:
            (m_1, acc) = (m_1_mut, acc_mut)
            if m_1 is not None:
                m2 = m_1
                if isinstance(m2, MapTreeNode_2):
                    m_1_mut = MapTreeNode_2__get_Left(m2)
                    acc_mut = cons((MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2)), loop(MapTreeNode_2__get_Right(m2), acc))
                    continue
                
                else: 
                    return cons((MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2)), acc)
                
            
            else: 
                return acc
            
            break
    
    return loop(m, empty_1())


def MapTreeModule_copyToArray(m, arr, i):
    j = i or 0
    def arrow_147(x, y=None, m=m, arr=arr, i=i):
        nonlocal j
        arr[j] = (x, y)
        j = (j + 1) or 0
    
    MapTreeModule_iter(arrow_147, m)


def MapTreeModule_toArray(m=None):
    n = MapTreeModule_size(m) or 0
    res = fill([0] * n, 0, n, (None, None))
    MapTreeModule_copyToArray(m, res, 0)
    return res


def MapTreeModule_ofList(comparer, l):
    return fold_1(lambda acc, tupled_arg, comparer=comparer, l=l: MapTreeModule_add(comparer, tupled_arg[0], tupled_arg[1], acc), MapTreeModule_empty(), l)


def MapTreeModule_mkFromEnumerator(comparer_mut, acc_mut, e_mut):
    while True:
        (comparer, acc, e) = (comparer_mut, acc_mut, e_mut)
        if e.System_Collections_IEnumerator_MoveNext():
            pattern_input = e.System_Collections_Generic_IEnumerator_00601_get_Current()
            comparer_mut = comparer
            acc_mut = MapTreeModule_add(comparer, pattern_input[0], pattern_input[1], acc)
            e_mut = e
            continue
        
        else: 
            return acc
        
        break


def MapTreeModule_ofArray(comparer, arr):
    res = MapTreeModule_empty()
    for idx in range(0, (len(arr) - 1) + 1, 1):
        for_loop_var = arr[idx]
        res = MapTreeModule_add(comparer, for_loop_var[0], for_loop_var[1], res)
    return res


def MapTreeModule_ofSeq(comparer, c):
    if is_array_like(c):
        return MapTreeModule_ofArray(comparer, c)
    
    elif isinstance(c, FSharpList):
        return MapTreeModule_ofList(comparer, c)
    
    else: 
        with get_enumerator(c) as ie:
            return MapTreeModule_mkFromEnumerator(comparer, MapTreeModule_empty(), ie)
    


def expr_148(gen0, gen1):
    return record_type("Map.MapTreeModule.MapIterator`2", [gen0, gen1], MapTreeModule_MapIterator_2, lambda: [["stack", list_type(option_type(MapTreeLeaf_2_reflection(gen0, gen1)))], ["started", bool_type]])


class MapTreeModule_MapIterator_2(Record):
    def __init__(self, stack, started):
        super().__init__()
        self.stack = stack
        self.started = started
    

MapTreeModule_MapIterator_2_reflection = expr_148

def MapTreeModule_collapseLHS(stack_mut):
    while True:
        (stack,) = (stack_mut,)
        if not is_empty_1(stack):
            rest = tail(stack)
            m = head(stack)
            if m is not None:
                m2 = m
                if isinstance(m2, MapTreeNode_2):
                    stack_mut = of_array_with_tail([MapTreeNode_2__get_Left(m2), MapTreeLeaf_2__ctor_5BDDA1(MapTreeLeaf_2__get_Key(m2), MapTreeLeaf_2__get_Value(m2)), MapTreeNode_2__get_Right(m2)], rest)
                    continue
                
                else: 
                    return stack
                
            
            else: 
                stack_mut = rest
                continue
            
        
        else: 
            return empty_1()
        
        break


def MapTreeModule_mkIterator(m=None):
    return MapTreeModule_MapIterator_2(MapTreeModule_collapseLHS(singleton(m)), False)


def MapTreeModule_notStarted():
    raise Exception("enumeration not started")


def MapTreeModule_alreadyFinished():
    raise Exception("enumeration already finished")


def MapTreeModule_current(i):
    if i.started:
        match_value = i.stack
        if not is_empty_1(match_value):
            if head(match_value) is not None:
                m = head(match_value)
                if isinstance(m, MapTreeNode_2):
                    raise Exception("Please report error: Map iterator, unexpected stack for current")
                
                else: 
                    return (MapTreeLeaf_2__get_Key(m), MapTreeLeaf_2__get_Value(m))
                
            
            else: 
                raise Exception("Please report error: Map iterator, unexpected stack for current")
            
        
        else: 
            return MapTreeModule_alreadyFinished()
        
    
    else: 
        return MapTreeModule_notStarted()
    


def MapTreeModule_moveNext(i):
    if i.started:
        match_value = i.stack
        if not is_empty_1(match_value):
            if head(match_value) is not None:
                m = head(match_value)
                if isinstance(m, MapTreeNode_2):
                    raise Exception("Please report error: Map iterator, unexpected stack for moveNext")
                
                else: 
                    i.stack = MapTreeModule_collapseLHS(tail(match_value))
                    return not is_empty_1(i.stack)
                
            
            else: 
                raise Exception("Please report error: Map iterator, unexpected stack for moveNext")
            
        
        else: 
            return False
        
    
    else: 
        i.started = True
        return not is_empty_1(i.stack)
    


def MapTreeModule_mkIEnumerator(m=None):
    i = MapTreeModule_mkIterator(m)
    class ObjectExpr149(IDisposable):
        def System_Collections_Generic_IEnumerator_00601_get_Current(self, m=m):
            return MapTreeModule_current(i)
        
        def System_Collections_IEnumerator_get_Current(self, m=m):
            return MapTreeModule_current(i)
        
        def System_Collections_IEnumerator_MoveNext(self, m=m):
            return MapTreeModule_moveNext(i)
        
        def System_Collections_IEnumerator_Reset(self, m=m):
            nonlocal i
            i = MapTreeModule_mkIterator(m)
        
        def Dispose(self, m=m):
            pass
        
    return ObjectExpr149()


def MapTreeModule_toSeq(s=None):
    def generator(en_1, s=s):
        if en_1.System_Collections_IEnumerator_MoveNext():
            return (en_1.System_Collections_Generic_IEnumerator_00601_get_Current(), en_1)
        
        else: 
            return None
        
    
    return unfold(generator, MapTreeModule_mkIEnumerator(s))


def expr_151(gen0, gen1):
    return class_type("Map.FSharpMap", [gen0, gen1], FSharpMap)


class FSharpMap:
    def __init__(self, comparer, tree=None):
        self.comparer = comparer
        self.tree = tree
    
    def GetHashCode(self):
        this = self
        return FSharpMap__ComputeHashCode(this)
    
    def __eq__(self, that):
        this = self
        if isinstance(that, FSharpMap):
            with get_enumerator(this) as e1:
                with get_enumerator(that) as e2:
                    def loop(_unit=None):
                        m1 = e1.System_Collections_IEnumerator_MoveNext()
                        if m1 == e2.System_Collections_IEnumerator_MoveNext():
                            if not m1:
                                return True
                            
                            else: 
                                e1c = e1.System_Collections_Generic_IEnumerator_00601_get_Current()
                                e2c = e2.System_Collections_Generic_IEnumerator_00601_get_Current()
                                if equals(e1c[1], e2c[1]) if (equals(e1c[0], e2c[0])) else (False):
                                    return loop()
                                
                                else: 
                                    return False
                                
                            
                        
                        else: 
                            return False
                        
                    
                    loop = loop
                    return loop()
        
        else: 
            return False
        
    
    def __str__(self):
        this = self
        return ("map [" + join("; ", map_1(lambda kv: format("({0}, {1})", kv[0], kv[1]), this))) + "]"
    
    @property
    def Symbol_toStringTag(self):
        return "FSharpMap"
    
    def to_json(self, _key):
        this = self
        return Array.from_(this)
    
    def GetEnumerator(self):
        _ = self
        return MapTreeModule_mkIEnumerator(_.tree)
    
    def __iter__(self):
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_IEnumerable_GetEnumerator(self):
        _ = self
        return MapTreeModule_mkIEnumerator(_.tree)
    
    def CompareTo(self, obj):
        m = self
        if isinstance(obj, FSharpMap):
            def arrow_150(kvp1, kvp2):
                c = m.comparer.Compare(kvp1[0], kvp2[0]) or 0
                return c if (c != 0) else (compare(kvp1[1], kvp2[1]))
            
            return compare_with(arrow_150, m, obj)
        
        else: 
            raise Exception("not comparable\\nParameter name: obj")
        
    
    def System_Collections_Generic_ICollection_00601_Add2B595(self, x):
        ignore(x)
        raise Exception("Map cannot be mutated")
    
    def System_Collections_Generic_ICollection_00601_Clear(self):
        raise Exception("Map cannot be mutated")
    
    def System_Collections_Generic_ICollection_00601_Remove2B595(self, x):
        ignore(x)
        raise Exception("Map cannot be mutated")
    
    def System_Collections_Generic_ICollection_00601_Contains2B595(self, x):
        m = self
        return equals(FSharpMap__get_Item(m, x[0]), x[1]) if (FSharpMap__ContainsKey(m, x[0])) else (False)
    
    def System_Collections_Generic_ICollection_00601_CopyToZ2E171D71(self, arr, i):
        m = self
        MapTreeModule_copyToArray(m.tree, arr, i)
    
    def System_Collections_Generic_ICollection_00601_get_IsReadOnly(self):
        return True
    
    def System_Collections_Generic_ICollection_00601_get_Count(self):
        m = self
        return FSharpMap__get_Count(m)
    
    def System_Collections_Generic_IReadOnlyCollection_00601_get_Count(self):
        m = self
        return FSharpMap__get_Count(m)
    
    @property
    def size(self):
        m = self
        return FSharpMap__get_Count(m)
    
    def clear(self):
        raise Exception("Map cannot be mutated")
    
    def delete(self, _arg1=None):
        raise Exception("Map cannot be mutated")
        return False
    
    def entries(self):
        m = self
        return map_1(lambda p: (p[0], p[1]), m)
    
    def __getitem__(self, k=None):
        m = self
        return FSharpMap__get_Item(m, k)
    
    def has(self, k=None):
        m = self
        return FSharpMap__ContainsKey(m, k)
    
    def keys(self):
        m = self
        return map_1(lambda p: p[0], m)
    
    def __setitem__(self, k, v=None):
        m = self
        raise Exception("Map cannot be mutated")
        return m
    
    def values(self):
        m = self
        return map_1(lambda p: p[1], m)
    
    def for_each(self, f, this_arg=None):
        m = self
        def action(p):
            f(p[1], p[0], m)
        
        iterate_1(action, m)
    

FSharpMap_reflection = expr_151

def FSharpMap__ctor(comparer, tree=None):
    return FSharpMap(comparer, tree)


def FSharpMap_Empty(comparer):
    return FSharpMap__ctor(comparer, MapTreeModule_empty())


def FSharpMap__get_Comparer(m):
    return m.comparer


def FSharpMap__get_Tree(m):
    return m.tree


def FSharpMap__Add(m, key, value=None):
    return FSharpMap__ctor(m.comparer, MapTreeModule_add(m.comparer, key, value, m.tree))


def FSharpMap__Change(m, key, f):
    return FSharpMap__ctor(m.comparer, MapTreeModule_change(m.comparer, key, f, m.tree))


def FSharpMap__get_IsEmpty(m):
    return m.tree is None


def FSharpMap__get_Item(m, key=None):
    return MapTreeModule_find(m.comparer, key, m.tree)


def FSharpMap__TryPick(m, f):
    return MapTreeModule_tryPick(f, m.tree)


def FSharpMap__Exists(m, predicate):
    return MapTreeModule_exists(predicate, m.tree)


def FSharpMap__Filter(m, predicate):
    return FSharpMap__ctor(m.comparer, MapTreeModule_filter(m.comparer, predicate, m.tree))


def FSharpMap__ForAll(m, predicate):
    return MapTreeModule_forall(predicate, m.tree)


def FSharpMap__Fold(m, f, acc=None):
    return MapTreeModule_foldBack(f, m.tree, acc)


def FSharpMap__FoldSection(m, lo, hi, f, acc=None):
    return MapTreeModule_foldSection(m.comparer, lo, hi, f, m.tree, acc)


def FSharpMap__Iterate(m, f):
    MapTreeModule_iter(f, m.tree)


def FSharpMap__MapRange(m, f):
    return FSharpMap__ctor(m.comparer, MapTreeModule_map(f, m.tree))


def FSharpMap__Map(m, f):
    return FSharpMap__ctor(m.comparer, MapTreeModule_mapi(f, m.tree))


def FSharpMap__Partition(m, predicate):
    pattern_input = MapTreeModule_partition(m.comparer, predicate, m.tree)
    return (FSharpMap__ctor(m.comparer, pattern_input[0]), FSharpMap__ctor(m.comparer, pattern_input[1]))


def FSharpMap__get_Count(m):
    return MapTreeModule_size(m.tree)


def FSharpMap__ContainsKey(m, key=None):
    return MapTreeModule_mem(m.comparer, key, m.tree)


def FSharpMap__Remove(m, key=None):
    return FSharpMap__ctor(m.comparer, MapTreeModule_remove(m.comparer, key, m.tree))


def FSharpMap__TryGetValue(_, key, value):
    match_value = MapTreeModule_tryFind(_.comparer, key, _.tree)
    if match_value is None:
        return False
    
    else: 
        v = value_1(match_value)
        value.contents = v
        return True
    


def FSharpMap__get_Keys(__):
    return list(map_1(lambda kvp, __=__: kvp[0], MapTreeModule_toSeq(__.tree)))


def FSharpMap__get_Values(__):
    return list(map_1(lambda kvp, __=__: kvp[1], MapTreeModule_toSeq(__.tree)))


def FSharpMap__TryFind(m, key=None):
    return MapTreeModule_tryFind(m.comparer, key, m.tree)


def FSharpMap__ToList(m):
    return MapTreeModule_toList(m.tree)


def FSharpMap__ToArray(m):
    return MapTreeModule_toArray(m.tree)


def FSharpMap__ComputeHashCode(this):
    combine_hash = lambda x, y, this=this: ((x << 1) + y) + 631
    res = 0
    with get_enumerator(this) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            active_pattern_result5184 = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
            res = combine_hash(res, structural_hash(active_pattern_result5184[0])) or 0
            res = combine_hash(res, structural_hash(active_pattern_result5184[1])) or 0
    return res


def is_empty(table):
    return FSharpMap__get_IsEmpty(table)


def add(key, value, table):
    return FSharpMap__Add(table, key, value)


def change(key, f, table):
    return FSharpMap__Change(table, key, f)


def find(key, table):
    return FSharpMap__get_Item(table, key)


def try_find(key, table):
    return FSharpMap__TryFind(table, key)


def remove(key, table):
    return FSharpMap__Remove(table, key)


def contains_key(key, table):
    return FSharpMap__ContainsKey(table, key)


def iterate(action, table):
    FSharpMap__Iterate(table, action)


def try_pick(chooser, table):
    return FSharpMap__TryPick(table, chooser)


def pick(chooser, table):
    match_value = try_pick(chooser, table)
    if match_value is not None:
        return value_1(match_value)
    
    else: 
        raise Exception()
    


def exists(predicate, table):
    return FSharpMap__Exists(table, predicate)


def filter(predicate, table):
    return FSharpMap__Filter(table, predicate)


def partition(predicate, table):
    return FSharpMap__Partition(table, predicate)


def for_all(predicate, table):
    return FSharpMap__ForAll(table, predicate)


def map(mapping, table):
    return FSharpMap__Map(table, mapping)


def fold(folder, state, table):
    return MapTreeModule_fold(folder, state, FSharpMap__get_Tree(table))


def fold_back(folder, table, state=None):
    return MapTreeModule_foldBack(folder, FSharpMap__get_Tree(table), state)


def to_seq(table):
    return map_1(lambda kvp, table=table: (kvp[0], kvp[1]), table)


def find_key(predicate, table):
    def chooser(kvp, predicate=predicate, table=table):
        k = kvp[0]
        if predicate(k, kvp[1]):
            return some(k)
        
        else: 
            return None
        
    
    return pick_1(chooser, table)


def try_find_key(predicate, table):
    def chooser(kvp, predicate=predicate, table=table):
        k = kvp[0]
        if predicate(k, kvp[1]):
            return some(k)
        
        else: 
            return None
        
    
    return try_pick_1(chooser, table)


def of_list(elements, comparer):
    return FSharpMap__ctor(comparer, MapTreeModule_ofSeq(comparer, elements))


def of_seq(elements, comparer):
    return FSharpMap__ctor(comparer, MapTreeModule_ofSeq(comparer, elements))


def of_array(elements, comparer):
    return FSharpMap__ctor(comparer, MapTreeModule_ofSeq(comparer, elements))


def to_list(table):
    return FSharpMap__ToList(table)


def to_array(table):
    return FSharpMap__ToArray(table)


def keys(table):
    return FSharpMap__get_Keys(table)


def values(table):
    return FSharpMap__get_Values(table)


def empty(comparer):
    return FSharpMap_Empty(comparer)


def count(table):
    return FSharpMap__get_Count(table)


