from .reflection import (class_type, option_type, list_type, bool_type, record_type)
from .option import (value as value_1, some)
from .types import (Record, to_string)
from .list import (is_empty as is_empty_1, head, tail, of_array_with_tail, empty as empty_1, singleton as singleton_1, cons, fold as fold_2, FSharpList)
from .util import (IDisposable, is_array_like, get_enumerator, ignore, to_iterator, structural_hash)
from .array import (fill, fold as fold_1)
from .string import join
from .seq import (map as map_1, iterate as iterate_1, reduce, fold as fold_3, for_all as for_all_1, cache, exists as exists_1)
import math
from .mutable_set import (HashSet, HashSet__ctor_Z6150332D, HashSet__get_Comparer)

def expr_152(gen0):
    return class_type("Set.SetTreeLeaf`1", [gen0], SetTreeLeaf_1)


class SetTreeLeaf_1:
    def __init__(self, k=None):
        self.k = k
    

SetTreeLeaf_1_reflection = expr_152

def SetTreeLeaf_1__ctor_2B595(k=None):
    return SetTreeLeaf_1(k)


def SetTreeLeaf_1__get_Key(_):
    return _.k


def expr_153(gen0):
    return class_type("Set.SetTreeNode`1", [gen0], SetTreeNode_1, SetTreeLeaf_1_reflection(gen0))


class SetTreeNode_1(SetTreeLeaf_1):
    def __init__(self, v, left, right, h):
        super().__init__(v)
        self.left = left
        self.right = right
        self.h = h or 0
    

SetTreeNode_1_reflection = expr_153

def SetTreeNode_1__ctor_5F465FC9(v, left, right, h):
    return SetTreeNode_1(v, left, right, h)


def SetTreeNode_1__get_Left(_):
    return _.left


def SetTreeNode_1__get_Right(_):
    return _.right


def SetTreeNode_1__get_Height(_):
    return _.h


def SetTreeModule_empty():
    return None


def SetTreeModule_countAux(t_mut, acc_mut):
    while True:
        (t, acc) = (t_mut, acc_mut)
        if t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                t_mut = SetTreeNode_1__get_Left(t2)
                acc_mut = SetTreeModule_countAux(SetTreeNode_1__get_Right(t2), acc + 1)
                continue
            
            else: 
                return acc + 1
            
        
        else: 
            return acc
        
        break


def SetTreeModule_count(s=None):
    return SetTreeModule_countAux(s, 0)


def SetTreeModule_mk(l, k, r=None):
    hl = None
    t = l
    def arrow_154(_unit=None):
        t2 = t
        return SetTreeNode_1__get_Height(t2) if (isinstance(t2, SetTreeNode_1)) else (1)
    
    hl = arrow_154() if (t is not None) else (0)
    hr = None
    t_1 = r
    def arrow_155(_unit=None):
        t2_1 = t_1
        return SetTreeNode_1__get_Height(t2_1) if (isinstance(t2_1, SetTreeNode_1)) else (1)
    
    hr = arrow_155() if (t_1 is not None) else (0)
    m = (hr if (hl < hr) else (hl)) or 0
    if m == 0:
        return SetTreeLeaf_1__ctor_2B595(k)
    
    else: 
        return SetTreeNode_1__ctor_5F465FC9(k, l, r, m + 1)
    


def SetTreeModule_rebalance(t1, v, t2=None):
    t1h = None
    t = t1
    def arrow_156(_unit=None):
        t2_1 = t
        return SetTreeNode_1__get_Height(t2_1) if (isinstance(t2_1, SetTreeNode_1)) else (1)
    
    t1h = arrow_156() if (t is not None) else (0)
    t2h = None
    t_1 = t2
    def arrow_157(_unit=None):
        t2_2 = t_1
        return SetTreeNode_1__get_Height(t2_2) if (isinstance(t2_2, SetTreeNode_1)) else (1)
    
    t2h = arrow_157() if (t_1 is not None) else (0)
    if t2h > (t1h + 2):
        match_value = value_1(t2)
        if isinstance(match_value, SetTreeNode_1):
            def arrow_159(_unit=None):
                t_2 = SetTreeNode_1__get_Left(match_value)
                def arrow_158(_unit=None):
                    t2_3 = t_2
                    return SetTreeNode_1__get_Height(t2_3) if (isinstance(t2_3, SetTreeNode_1)) else (1)
                
                return arrow_158() if (t_2 is not None) else (0)
            
            if arrow_159() > (t1h + 1):
                match_value_1 = value_1(SetTreeNode_1__get_Left(match_value))
                if isinstance(match_value_1, SetTreeNode_1):
                    return SetTreeModule_mk(SetTreeModule_mk(t1, v, SetTreeNode_1__get_Left(match_value_1)), SetTreeLeaf_1__get_Key(match_value_1), SetTreeModule_mk(SetTreeNode_1__get_Right(match_value_1), SetTreeLeaf_1__get_Key(match_value), SetTreeNode_1__get_Right(match_value)))
                
                else: 
                    raise Exception("internal error: Set.rebalance")
                
            
            else: 
                return SetTreeModule_mk(SetTreeModule_mk(t1, v, SetTreeNode_1__get_Left(match_value)), SetTreeLeaf_1__get_Key(match_value), SetTreeNode_1__get_Right(match_value))
            
        
        else: 
            raise Exception("internal error: Set.rebalance")
        
    
    elif t1h > (t2h + 2):
        match_value_2 = value_1(t1)
        if isinstance(match_value_2, SetTreeNode_1):
            def arrow_161(_unit=None):
                t_3 = SetTreeNode_1__get_Right(match_value_2)
                def arrow_160(_unit=None):
                    t2_4 = t_3
                    return SetTreeNode_1__get_Height(t2_4) if (isinstance(t2_4, SetTreeNode_1)) else (1)
                
                return arrow_160() if (t_3 is not None) else (0)
            
            if arrow_161() > (t2h + 1):
                match_value_3 = value_1(SetTreeNode_1__get_Right(match_value_2))
                if isinstance(match_value_3, SetTreeNode_1):
                    return SetTreeModule_mk(SetTreeModule_mk(SetTreeNode_1__get_Left(match_value_2), SetTreeLeaf_1__get_Key(match_value_2), SetTreeNode_1__get_Left(match_value_3)), SetTreeLeaf_1__get_Key(match_value_3), SetTreeModule_mk(SetTreeNode_1__get_Right(match_value_3), v, t2))
                
                else: 
                    raise Exception("internal error: Set.rebalance")
                
            
            else: 
                return SetTreeModule_mk(SetTreeNode_1__get_Left(match_value_2), SetTreeLeaf_1__get_Key(match_value_2), SetTreeModule_mk(SetTreeNode_1__get_Right(match_value_2), v, t2))
            
        
        else: 
            raise Exception("internal error: Set.rebalance")
        
    
    else: 
        return SetTreeModule_mk(t1, v, t2)
    


def SetTreeModule_add(comparer, k, t=None):
    if t is not None:
        t2 = t
        c = comparer.Compare(k, SetTreeLeaf_1__get_Key(t2)) or 0
        if isinstance(t2, SetTreeNode_1):
            if c < 0:
                return SetTreeModule_rebalance(SetTreeModule_add(comparer, k, SetTreeNode_1__get_Left(t2)), SetTreeLeaf_1__get_Key(t2), SetTreeNode_1__get_Right(t2))
            
            elif c == 0:
                return t
            
            else: 
                return SetTreeModule_rebalance(SetTreeNode_1__get_Left(t2), SetTreeLeaf_1__get_Key(t2), SetTreeModule_add(comparer, k, SetTreeNode_1__get_Right(t2)))
            
        
        else: 
            c_1 = comparer.Compare(k, SetTreeLeaf_1__get_Key(t2)) or 0
            if c_1 < 0:
                return SetTreeNode_1__ctor_5F465FC9(k, SetTreeModule_empty(), t, 2)
            
            elif c_1 == 0:
                return t
            
            else: 
                return SetTreeNode_1__ctor_5F465FC9(k, t, SetTreeModule_empty(), 2)
            
        
    
    else: 
        return SetTreeLeaf_1__ctor_2B595(k)
    


def SetTreeModule_balance(comparer, t1, k, t2=None):
    if t1 is not None:
        t1_0027 = t1
        if t2 is not None:
            t2_0027 = t2
            if isinstance(t1_0027, SetTreeNode_1):
                if isinstance(t2_0027, SetTreeNode_1):
                    if (SetTreeNode_1__get_Height(t1_0027) + 2) < SetTreeNode_1__get_Height(t2_0027):
                        return SetTreeModule_rebalance(SetTreeModule_balance(comparer, t1, k, SetTreeNode_1__get_Left(t2_0027)), SetTreeLeaf_1__get_Key(t2_0027), SetTreeNode_1__get_Right(t2_0027))
                    
                    elif (SetTreeNode_1__get_Height(t2_0027) + 2) < SetTreeNode_1__get_Height(t1_0027):
                        return SetTreeModule_rebalance(SetTreeNode_1__get_Left(t1_0027), SetTreeLeaf_1__get_Key(t1_0027), SetTreeModule_balance(comparer, SetTreeNode_1__get_Right(t1_0027), k, t2))
                    
                    else: 
                        return SetTreeModule_mk(t1, k, t2)
                    
                
                else: 
                    return SetTreeModule_add(comparer, k, SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t2_0027), t1))
                
            
            else: 
                return SetTreeModule_add(comparer, k, SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t1_0027), t2))
            
        
        else: 
            return SetTreeModule_add(comparer, k, t1)
        
    
    else: 
        return SetTreeModule_add(comparer, k, t2)
    


def SetTreeModule_split(comparer, pivot, t=None):
    if t is not None:
        t2 = t
        if isinstance(t2, SetTreeNode_1):
            c = comparer.Compare(pivot, SetTreeLeaf_1__get_Key(t2)) or 0
            if c < 0:
                pattern_input = SetTreeModule_split(comparer, pivot, SetTreeNode_1__get_Left(t2))
                return (pattern_input[0], pattern_input[1], SetTreeModule_balance(comparer, pattern_input[2], SetTreeLeaf_1__get_Key(t2), SetTreeNode_1__get_Right(t2)))
            
            elif c == 0:
                return (SetTreeNode_1__get_Left(t2), True, SetTreeNode_1__get_Right(t2))
            
            else: 
                pattern_input_1 = SetTreeModule_split(comparer, pivot, SetTreeNode_1__get_Right(t2))
                return (SetTreeModule_balance(comparer, SetTreeNode_1__get_Left(t2), SetTreeLeaf_1__get_Key(t2), pattern_input_1[0]), pattern_input_1[1], pattern_input_1[2])
            
        
        else: 
            c_1 = comparer.Compare(SetTreeLeaf_1__get_Key(t2), pivot) or 0
            if c_1 < 0:
                return (t, False, SetTreeModule_empty())
            
            elif c_1 == 0:
                return (SetTreeModule_empty(), True, SetTreeModule_empty())
            
            else: 
                return (SetTreeModule_empty(), False, t)
            
        
    
    else: 
        return (SetTreeModule_empty(), False, SetTreeModule_empty())
    


def SetTreeModule_spliceOutSuccessor(t=None):
    if t is not None:
        t2 = t
        if isinstance(t2, SetTreeNode_1):
            if SetTreeNode_1__get_Left(t2) is None:
                return (SetTreeLeaf_1__get_Key(t2), SetTreeNode_1__get_Right(t2))
            
            else: 
                pattern_input = SetTreeModule_spliceOutSuccessor(SetTreeNode_1__get_Left(t2))
                return (pattern_input[0], SetTreeModule_mk(pattern_input[1], SetTreeLeaf_1__get_Key(t2), SetTreeNode_1__get_Right(t2)))
            
        
        else: 
            return (SetTreeLeaf_1__get_Key(t2), SetTreeModule_empty())
        
    
    else: 
        raise Exception("internal error: Set.spliceOutSuccessor")
    


def SetTreeModule_remove(comparer, k, t=None):
    if t is not None:
        t2 = t
        c = comparer.Compare(k, SetTreeLeaf_1__get_Key(t2)) or 0
        if isinstance(t2, SetTreeNode_1):
            if c < 0:
                return SetTreeModule_rebalance(SetTreeModule_remove(comparer, k, SetTreeNode_1__get_Left(t2)), SetTreeLeaf_1__get_Key(t2), SetTreeNode_1__get_Right(t2))
            
            elif c == 0:
                if SetTreeNode_1__get_Left(t2) is None:
                    return SetTreeNode_1__get_Right(t2)
                
                elif SetTreeNode_1__get_Right(t2) is None:
                    return SetTreeNode_1__get_Left(t2)
                
                else: 
                    pattern_input = SetTreeModule_spliceOutSuccessor(SetTreeNode_1__get_Right(t2))
                    return SetTreeModule_mk(SetTreeNode_1__get_Left(t2), pattern_input[0], pattern_input[1])
                
            
            else: 
                return SetTreeModule_rebalance(SetTreeNode_1__get_Left(t2), SetTreeLeaf_1__get_Key(t2), SetTreeModule_remove(comparer, k, SetTreeNode_1__get_Right(t2)))
            
        
        elif c == 0:
            return SetTreeModule_empty()
        
        else: 
            return t
        
    
    else: 
        return t
    


def SetTreeModule_mem(comparer_mut, k_mut, t_mut):
    while True:
        (comparer, k, t) = (comparer_mut, k_mut, t_mut)
        if t is not None:
            t2 = t
            c = comparer.Compare(k, SetTreeLeaf_1__get_Key(t2)) or 0
            if isinstance(t2, SetTreeNode_1):
                if c < 0:
                    comparer_mut = comparer
                    k_mut = k
                    t_mut = SetTreeNode_1__get_Left(t2)
                    continue
                
                elif c == 0:
                    return True
                
                else: 
                    comparer_mut = comparer
                    k_mut = k
                    t_mut = SetTreeNode_1__get_Right(t2)
                    continue
                
            
            else: 
                return c == 0
            
        
        else: 
            return False
        
        break


def SetTreeModule_iter(f_mut, t_mut):
    while True:
        (f, t) = (f_mut, t_mut)
        if t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                SetTreeModule_iter(f, SetTreeNode_1__get_Left(t2))
                f(SetTreeLeaf_1__get_Key(t2))
                f_mut = f
                t_mut = SetTreeNode_1__get_Right(t2)
                continue
            
            else: 
                f(SetTreeLeaf_1__get_Key(t2))
            
        
        break


def SetTreeModule_foldBackOpt(f_mut, t_mut, x_mut=None):
    while True:
        (f, t, x) = (f_mut, t_mut, x_mut)
        if t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                f_mut = f
                t_mut = SetTreeNode_1__get_Left(t2)
                x_mut = f(SetTreeLeaf_1__get_Key(t2), SetTreeModule_foldBackOpt(f, SetTreeNode_1__get_Right(t2), x))
                continue
            
            else: 
                return f(SetTreeLeaf_1__get_Key(t2), x)
            
        
        else: 
            return x
        
        break


def SetTreeModule_foldBack(f, m, x=None):
    return SetTreeModule_foldBackOpt(f, m, x)


def SetTreeModule_foldOpt(f_mut, x_mut, t_mut):
    while True:
        (f, x, t) = (f_mut, x_mut, t_mut)
        if t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                f_mut = f
                x_mut = f(SetTreeModule_foldOpt(f, x, SetTreeNode_1__get_Left(t2)), SetTreeLeaf_1__get_Key(t2))
                t_mut = SetTreeNode_1__get_Right(t2)
                continue
            
            else: 
                return f(x, SetTreeLeaf_1__get_Key(t2))
            
        
        else: 
            return x
        
        break


def SetTreeModule_fold(f, x, m=None):
    return SetTreeModule_foldOpt(f, x, m)


def SetTreeModule_forall(f_mut, t_mut):
    while True:
        (f, t) = (f_mut, t_mut)
        if t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                if SetTreeModule_forall(f, SetTreeNode_1__get_Left(t2)) if (f(SetTreeLeaf_1__get_Key(t2))) else (False):
                    f_mut = f
                    t_mut = SetTreeNode_1__get_Right(t2)
                    continue
                
                else: 
                    return False
                
            
            else: 
                return f(SetTreeLeaf_1__get_Key(t2))
            
        
        else: 
            return True
        
        break


def SetTreeModule_exists(f_mut, t_mut):
    while True:
        (f, t) = (f_mut, t_mut)
        if t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                if True if (f(SetTreeLeaf_1__get_Key(t2))) else (SetTreeModule_exists(f, SetTreeNode_1__get_Left(t2))):
                    return True
                
                else: 
                    f_mut = f
                    t_mut = SetTreeNode_1__get_Right(t2)
                    continue
                
            
            else: 
                return f(SetTreeLeaf_1__get_Key(t2))
            
        
        else: 
            return False
        
        break


def SetTreeModule_subset(comparer, a=None, b=None):
    return SetTreeModule_forall(lambda x=None, comparer=comparer, a=a, b=b: SetTreeModule_mem(comparer, x, b), a)


def SetTreeModule_properSubset(comparer, a=None, b=None):
    if SetTreeModule_forall(lambda x=None, comparer=comparer, a=a, b=b: SetTreeModule_mem(comparer, x, b), a):
        return SetTreeModule_exists(lambda x_1=None, comparer=comparer, a=a, b=b: not SetTreeModule_mem(comparer, x_1, a), b)
    
    else: 
        return False
    


def SetTreeModule_filterAux(comparer_mut, f_mut, t_mut, acc_mut):
    while True:
        (comparer, f, t, acc) = (comparer_mut, f_mut, t_mut, acc_mut)
        if t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                acc_1 = SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t2), acc) if (f(SetTreeLeaf_1__get_Key(t2))) else (acc)
                comparer_mut = comparer
                f_mut = f
                t_mut = SetTreeNode_1__get_Left(t2)
                acc_mut = SetTreeModule_filterAux(comparer, f, SetTreeNode_1__get_Right(t2), acc_1)
                continue
            
            elif f(SetTreeLeaf_1__get_Key(t2)):
                return SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t2), acc)
            
            else: 
                return acc
            
        
        else: 
            return acc
        
        break


def SetTreeModule_filter(comparer, f, s=None):
    return SetTreeModule_filterAux(comparer, f, s, SetTreeModule_empty())


def SetTreeModule_diffAux(comparer_mut, t_mut, acc_mut):
    while True:
        (comparer, t, acc) = (comparer_mut, t_mut, acc_mut)
        if acc is None:
            return acc
        
        elif t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                comparer_mut = comparer
                t_mut = SetTreeNode_1__get_Left(t2)
                acc_mut = SetTreeModule_diffAux(comparer, SetTreeNode_1__get_Right(t2), SetTreeModule_remove(comparer, SetTreeLeaf_1__get_Key(t2), acc))
                continue
            
            else: 
                return SetTreeModule_remove(comparer, SetTreeLeaf_1__get_Key(t2), acc)
            
        
        else: 
            return acc
        
        break


def SetTreeModule_diff(comparer, a=None, b=None):
    return SetTreeModule_diffAux(comparer, b, a)


def SetTreeModule_union(comparer, t1=None, t2=None):
    if t1 is not None:
        t1_0027 = t1
        if t2 is not None:
            t2_0027 = t2
            if isinstance(t1_0027, SetTreeNode_1):
                if isinstance(t2_0027, SetTreeNode_1):
                    if SetTreeNode_1__get_Height(t1_0027) > SetTreeNode_1__get_Height(t2_0027):
                        pattern_input = SetTreeModule_split(comparer, SetTreeLeaf_1__get_Key(t1_0027), t2)
                        return SetTreeModule_balance(comparer, SetTreeModule_union(comparer, SetTreeNode_1__get_Left(t1_0027), pattern_input[0]), SetTreeLeaf_1__get_Key(t1_0027), SetTreeModule_union(comparer, SetTreeNode_1__get_Right(t1_0027), pattern_input[2]))
                    
                    else: 
                        pattern_input_1 = SetTreeModule_split(comparer, SetTreeLeaf_1__get_Key(t2_0027), t1)
                        return SetTreeModule_balance(comparer, SetTreeModule_union(comparer, SetTreeNode_1__get_Left(t2_0027), pattern_input_1[0]), SetTreeLeaf_1__get_Key(t2_0027), SetTreeModule_union(comparer, SetTreeNode_1__get_Right(t2_0027), pattern_input_1[2]))
                    
                
                else: 
                    return SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t2_0027), t1)
                
            
            else: 
                return SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t1_0027), t2)
            
        
        else: 
            return t1
        
    
    else: 
        return t2
    


def SetTreeModule_intersectionAux(comparer_mut, b_mut, t_mut, acc_mut):
    while True:
        (comparer, b, t, acc) = (comparer_mut, b_mut, t_mut, acc_mut)
        if t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                acc_1 = SetTreeModule_intersectionAux(comparer, b, SetTreeNode_1__get_Right(t2), acc)
                acc_2 = SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t2), acc_1) if (SetTreeModule_mem(comparer, SetTreeLeaf_1__get_Key(t2), b)) else (acc_1)
                comparer_mut = comparer
                b_mut = b
                t_mut = SetTreeNode_1__get_Left(t2)
                acc_mut = acc_2
                continue
            
            elif SetTreeModule_mem(comparer, SetTreeLeaf_1__get_Key(t2), b):
                return SetTreeModule_add(comparer, SetTreeLeaf_1__get_Key(t2), acc)
            
            else: 
                return acc
            
        
        else: 
            return acc
        
        break


def SetTreeModule_intersection(comparer, a=None, b=None):
    return SetTreeModule_intersectionAux(comparer, b, a, SetTreeModule_empty())


def SetTreeModule_partition1(comparer, f, k, acc1=None, acc2=None):
    if f(k):
        return (SetTreeModule_add(comparer, k, acc1), acc2)
    
    else: 
        return (acc1, SetTreeModule_add(comparer, k, acc2))
    


def SetTreeModule_partitionAux(comparer_mut, f_mut, t_mut, acc_0_mut, acc_1_mut):
    while True:
        (comparer, f, t, acc_0, acc_1) = (comparer_mut, f_mut, t_mut, acc_0_mut, acc_1_mut)
        acc = (acc_0, acc_1)
        if t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                acc_2 = SetTreeModule_partitionAux(comparer, f, SetTreeNode_1__get_Right(t2), acc[0], acc[1])
                acc_3 = SetTreeModule_partition1(comparer, f, SetTreeLeaf_1__get_Key(t2), acc_2[0], acc_2[1])
                comparer_mut = comparer
                f_mut = f
                t_mut = SetTreeNode_1__get_Left(t2)
                acc_0_mut = acc_3[0]
                acc_1_mut = acc_3[1]
                continue
            
            else: 
                return SetTreeModule_partition1(comparer, f, SetTreeLeaf_1__get_Key(t2), acc[0], acc[1])
            
        
        else: 
            return acc
        
        break


def SetTreeModule_partition(comparer, f, s=None):
    return SetTreeModule_partitionAux(comparer, f, s, SetTreeModule_empty(), SetTreeModule_empty())


def SetTreeModule_minimumElementAux(t_mut, n_mut=None):
    while True:
        (t, n) = (t_mut, n_mut)
        if t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                t_mut = SetTreeNode_1__get_Left(t2)
                n_mut = SetTreeLeaf_1__get_Key(t2)
                continue
            
            else: 
                return SetTreeLeaf_1__get_Key(t2)
            
        
        else: 
            return n
        
        break


def SetTreeModule_minimumElementOpt(t=None):
    if t is not None:
        t2 = t
        if isinstance(t2, SetTreeNode_1):
            return some(SetTreeModule_minimumElementAux(SetTreeNode_1__get_Left(t2), SetTreeLeaf_1__get_Key(t2)))
        
        else: 
            return some(SetTreeLeaf_1__get_Key(t2))
        
    
    else: 
        return None
    


def SetTreeModule_maximumElementAux(t_mut, n_mut=None):
    while True:
        (t, n) = (t_mut, n_mut)
        if t is not None:
            t2 = t
            if isinstance(t2, SetTreeNode_1):
                t_mut = SetTreeNode_1__get_Right(t2)
                n_mut = SetTreeLeaf_1__get_Key(t2)
                continue
            
            else: 
                return SetTreeLeaf_1__get_Key(t2)
            
        
        else: 
            return n
        
        break


def SetTreeModule_maximumElementOpt(t=None):
    if t is not None:
        t2 = t
        if isinstance(t2, SetTreeNode_1):
            return some(SetTreeModule_maximumElementAux(SetTreeNode_1__get_Right(t2), SetTreeLeaf_1__get_Key(t2)))
        
        else: 
            return some(SetTreeLeaf_1__get_Key(t2))
        
    
    else: 
        return None
    


def SetTreeModule_minimumElement(s=None):
    match_value = SetTreeModule_minimumElementOpt(s)
    if match_value is None:
        raise Exception("Set contains no elements")
    
    else: 
        return value_1(match_value)
    


def SetTreeModule_maximumElement(s=None):
    match_value = SetTreeModule_maximumElementOpt(s)
    if match_value is None:
        raise Exception("Set contains no elements")
    
    else: 
        return value_1(match_value)
    


def expr_162(gen0):
    return record_type("Set.SetTreeModule.SetIterator`1", [gen0], SetTreeModule_SetIterator_1, lambda: [["stack", list_type(option_type(SetTreeLeaf_1_reflection(gen0)))], ["started", bool_type]])


class SetTreeModule_SetIterator_1(Record):
    def __init__(self, stack, started):
        super().__init__()
        self.stack = stack
        self.started = started
    

SetTreeModule_SetIterator_1_reflection = expr_162

def SetTreeModule_collapseLHS(stack_mut):
    while True:
        (stack,) = (stack_mut,)
        if not is_empty_1(stack):
            x = head(stack)
            rest = tail(stack)
            if x is not None:
                x2 = x
                if isinstance(x2, SetTreeNode_1):
                    stack_mut = of_array_with_tail([SetTreeNode_1__get_Left(x2), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x2)), SetTreeNode_1__get_Right(x2)], rest)
                    continue
                
                else: 
                    return stack
                
            
            else: 
                stack_mut = rest
                continue
            
        
        else: 
            return empty_1()
        
        break


def SetTreeModule_mkIterator(s=None):
    return SetTreeModule_SetIterator_1(SetTreeModule_collapseLHS(singleton_1(s)), False)


def SetTreeModule_notStarted():
    raise Exception("Enumeration not started")


def SetTreeModule_alreadyFinished():
    raise Exception("Enumeration already started")


def SetTreeModule_current(i):
    if i.started:
        match_value = i.stack
        if is_empty_1(match_value):
            return SetTreeModule_alreadyFinished()
        
        elif head(match_value) is not None:
            t = head(match_value)
            return SetTreeLeaf_1__get_Key(t)
        
        else: 
            raise Exception("Please report error: Set iterator, unexpected stack for current")
        
    
    else: 
        return SetTreeModule_notStarted()
    


def SetTreeModule_moveNext(i):
    if i.started:
        match_value = i.stack
        if not is_empty_1(match_value):
            if head(match_value) is not None:
                t = head(match_value)
                if isinstance(t, SetTreeNode_1):
                    raise Exception("Please report error: Set iterator, unexpected stack for moveNext")
                
                else: 
                    i.stack = SetTreeModule_collapseLHS(tail(match_value))
                    return not is_empty_1(i.stack)
                
            
            else: 
                raise Exception("Please report error: Set iterator, unexpected stack for moveNext")
            
        
        else: 
            return False
        
    
    else: 
        i.started = True
        return not is_empty_1(i.stack)
    


def SetTreeModule_mkIEnumerator(s=None):
    i = SetTreeModule_mkIterator(s)
    class ObjectExpr163(IDisposable):
        def System_Collections_Generic_IEnumerator_00601_get_Current(self, s=s):
            return SetTreeModule_current(i)
        
        def System_Collections_IEnumerator_get_Current(self, s=s):
            return SetTreeModule_current(i)
        
        def System_Collections_IEnumerator_MoveNext(self, s=s):
            return SetTreeModule_moveNext(i)
        
        def System_Collections_IEnumerator_Reset(self, s=s):
            nonlocal i
            i = SetTreeModule_mkIterator(s)
        
        def Dispose(self, s=s):
            pass
        
    return ObjectExpr163()


def SetTreeModule_compareStacks(comparer_mut, l1_mut, l2_mut):
    while True:
        (comparer, l1, l2) = (comparer_mut, l1_mut, l2_mut)
        match_value = (l1, l2)
        if not is_empty_1(match_value[0]):
            if not is_empty_1(match_value[1]):
                if head(match_value[1]) is not None:
                    if head(match_value[0]) is not None:
                        x1_3 = head(match_value[0])
                        x2_3 = head(match_value[1])
                        if isinstance(x1_3, SetTreeNode_1):
                            if SetTreeNode_1__get_Left(x1_3) is None:
                                if isinstance(x2_3, SetTreeNode_1):
                                    if SetTreeNode_1__get_Left(x2_3) is None:
                                        c = comparer.Compare(SetTreeLeaf_1__get_Key(x1_3), SetTreeLeaf_1__get_Key(x2_3)) or 0
                                        if c != 0:
                                            return c
                                        
                                        else: 
                                            comparer_mut = comparer
                                            l1_mut = cons(SetTreeNode_1__get_Right(x1_3), tail(match_value[0]))
                                            l2_mut = cons(SetTreeNode_1__get_Right(x2_3), tail(match_value[1]))
                                            continue
                                        
                                    
                                    else: 
                                        match_value_3 = (l1, l2)
                                        (pattern_matching_result, t1_6, x1_4, t2_6, x2_4) = (None, None, None, None, None)
                                        if not is_empty_1(match_value_3[0]):
                                            if head(match_value_3[0]) is not None:
                                                pattern_matching_result = 0
                                                t1_6 = tail(match_value_3[0])
                                                x1_4 = head(match_value_3[0])
                                            
                                            elif not is_empty_1(match_value_3[1]):
                                                if head(match_value_3[1]) is not None:
                                                    pattern_matching_result = 1
                                                    t2_6 = tail(match_value_3[1])
                                                    x2_4 = head(match_value_3[1])
                                                
                                                else: 
                                                    pattern_matching_result = 2
                                                
                                            
                                            else: 
                                                pattern_matching_result = 2
                                            
                                        
                                        elif not is_empty_1(match_value_3[1]):
                                            if head(match_value_3[1]) is not None:
                                                pattern_matching_result = 1
                                                t2_6 = tail(match_value_3[1])
                                                x2_4 = head(match_value_3[1])
                                            
                                            else: 
                                                pattern_matching_result = 2
                                            
                                        
                                        else: 
                                            pattern_matching_result = 2
                                        
                                        if pattern_matching_result == 0:
                                            if isinstance(x1_4, SetTreeNode_1):
                                                comparer_mut = comparer
                                                l1_mut = of_array_with_tail([SetTreeNode_1__get_Left(x1_4), SetTreeNode_1__ctor_5F465FC9(SetTreeLeaf_1__get_Key(x1_4), SetTreeModule_empty(), SetTreeNode_1__get_Right(x1_4), 0)], t1_6)
                                                l2_mut = l2
                                                continue
                                            
                                            else: 
                                                comparer_mut = comparer
                                                l1_mut = of_array_with_tail([SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x1_4))], t1_6)
                                                l2_mut = l2
                                                continue
                                            
                                        
                                        elif pattern_matching_result == 1:
                                            if isinstance(x2_4, SetTreeNode_1):
                                                comparer_mut = comparer
                                                l1_mut = l1
                                                l2_mut = of_array_with_tail([SetTreeNode_1__get_Left(x2_4), SetTreeNode_1__ctor_5F465FC9(SetTreeLeaf_1__get_Key(x2_4), SetTreeModule_empty(), SetTreeNode_1__get_Right(x2_4), 0)], t2_6)
                                                continue
                                            
                                            else: 
                                                comparer_mut = comparer
                                                l1_mut = l1
                                                l2_mut = of_array_with_tail([SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x2_4))], t2_6)
                                                continue
                                            
                                        
                                        elif pattern_matching_result == 2:
                                            raise Exception("unexpected state in SetTree.compareStacks")
                                        
                                    
                                
                                else: 
                                    c_1 = comparer.Compare(SetTreeLeaf_1__get_Key(x1_3), SetTreeLeaf_1__get_Key(x2_3)) or 0
                                    if c_1 != 0:
                                        return c_1
                                    
                                    else: 
                                        comparer_mut = comparer
                                        l1_mut = cons(SetTreeNode_1__get_Right(x1_3), tail(match_value[0]))
                                        l2_mut = cons(SetTreeModule_empty(), tail(match_value[1]))
                                        continue
                                    
                                
                            
                            else: 
                                match_value_4 = (l1, l2)
                                (pattern_matching_result_1, t1_7, x1_5, t2_7, x2_5) = (None, None, None, None, None)
                                if not is_empty_1(match_value_4[0]):
                                    if head(match_value_4[0]) is not None:
                                        pattern_matching_result_1 = 0
                                        t1_7 = tail(match_value_4[0])
                                        x1_5 = head(match_value_4[0])
                                    
                                    elif not is_empty_1(match_value_4[1]):
                                        if head(match_value_4[1]) is not None:
                                            pattern_matching_result_1 = 1
                                            t2_7 = tail(match_value_4[1])
                                            x2_5 = head(match_value_4[1])
                                        
                                        else: 
                                            pattern_matching_result_1 = 2
                                        
                                    
                                    else: 
                                        pattern_matching_result_1 = 2
                                    
                                
                                elif not is_empty_1(match_value_4[1]):
                                    if head(match_value_4[1]) is not None:
                                        pattern_matching_result_1 = 1
                                        t2_7 = tail(match_value_4[1])
                                        x2_5 = head(match_value_4[1])
                                    
                                    else: 
                                        pattern_matching_result_1 = 2
                                    
                                
                                else: 
                                    pattern_matching_result_1 = 2
                                
                                if pattern_matching_result_1 == 0:
                                    if isinstance(x1_5, SetTreeNode_1):
                                        comparer_mut = comparer
                                        l1_mut = of_array_with_tail([SetTreeNode_1__get_Left(x1_5), SetTreeNode_1__ctor_5F465FC9(SetTreeLeaf_1__get_Key(x1_5), SetTreeModule_empty(), SetTreeNode_1__get_Right(x1_5), 0)], t1_7)
                                        l2_mut = l2
                                        continue
                                    
                                    else: 
                                        comparer_mut = comparer
                                        l1_mut = of_array_with_tail([SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x1_5))], t1_7)
                                        l2_mut = l2
                                        continue
                                    
                                
                                elif pattern_matching_result_1 == 1:
                                    if isinstance(x2_5, SetTreeNode_1):
                                        comparer_mut = comparer
                                        l1_mut = l1
                                        l2_mut = of_array_with_tail([SetTreeNode_1__get_Left(x2_5), SetTreeNode_1__ctor_5F465FC9(SetTreeLeaf_1__get_Key(x2_5), SetTreeModule_empty(), SetTreeNode_1__get_Right(x2_5), 0)], t2_7)
                                        continue
                                    
                                    else: 
                                        comparer_mut = comparer
                                        l1_mut = l1
                                        l2_mut = of_array_with_tail([SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x2_5))], t2_7)
                                        continue
                                    
                                
                                elif pattern_matching_result_1 == 2:
                                    raise Exception("unexpected state in SetTree.compareStacks")
                                
                            
                        
                        elif isinstance(x2_3, SetTreeNode_1):
                            if SetTreeNode_1__get_Left(x2_3) is None:
                                c_2 = comparer.Compare(SetTreeLeaf_1__get_Key(x1_3), SetTreeLeaf_1__get_Key(x2_3)) or 0
                                if c_2 != 0:
                                    return c_2
                                
                                else: 
                                    comparer_mut = comparer
                                    l1_mut = cons(SetTreeModule_empty(), tail(match_value[0]))
                                    l2_mut = cons(SetTreeNode_1__get_Right(x2_3), tail(match_value[1]))
                                    continue
                                
                            
                            else: 
                                match_value_5 = (l1, l2)
                                (pattern_matching_result_2, t1_8, x1_6, t2_8, x2_6) = (None, None, None, None, None)
                                if not is_empty_1(match_value_5[0]):
                                    if head(match_value_5[0]) is not None:
                                        pattern_matching_result_2 = 0
                                        t1_8 = tail(match_value_5[0])
                                        x1_6 = head(match_value_5[0])
                                    
                                    elif not is_empty_1(match_value_5[1]):
                                        if head(match_value_5[1]) is not None:
                                            pattern_matching_result_2 = 1
                                            t2_8 = tail(match_value_5[1])
                                            x2_6 = head(match_value_5[1])
                                        
                                        else: 
                                            pattern_matching_result_2 = 2
                                        
                                    
                                    else: 
                                        pattern_matching_result_2 = 2
                                    
                                
                                elif not is_empty_1(match_value_5[1]):
                                    if head(match_value_5[1]) is not None:
                                        pattern_matching_result_2 = 1
                                        t2_8 = tail(match_value_5[1])
                                        x2_6 = head(match_value_5[1])
                                    
                                    else: 
                                        pattern_matching_result_2 = 2
                                    
                                
                                else: 
                                    pattern_matching_result_2 = 2
                                
                                if pattern_matching_result_2 == 0:
                                    if isinstance(x1_6, SetTreeNode_1):
                                        comparer_mut = comparer
                                        l1_mut = of_array_with_tail([SetTreeNode_1__get_Left(x1_6), SetTreeNode_1__ctor_5F465FC9(SetTreeLeaf_1__get_Key(x1_6), SetTreeModule_empty(), SetTreeNode_1__get_Right(x1_6), 0)], t1_8)
                                        l2_mut = l2
                                        continue
                                    
                                    else: 
                                        comparer_mut = comparer
                                        l1_mut = of_array_with_tail([SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x1_6))], t1_8)
                                        l2_mut = l2
                                        continue
                                    
                                
                                elif pattern_matching_result_2 == 1:
                                    if isinstance(x2_6, SetTreeNode_1):
                                        comparer_mut = comparer
                                        l1_mut = l1
                                        l2_mut = of_array_with_tail([SetTreeNode_1__get_Left(x2_6), SetTreeNode_1__ctor_5F465FC9(SetTreeLeaf_1__get_Key(x2_6), SetTreeModule_empty(), SetTreeNode_1__get_Right(x2_6), 0)], t2_8)
                                        continue
                                    
                                    else: 
                                        comparer_mut = comparer
                                        l1_mut = l1
                                        l2_mut = of_array_with_tail([SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x2_6))], t2_8)
                                        continue
                                    
                                
                                elif pattern_matching_result_2 == 2:
                                    raise Exception("unexpected state in SetTree.compareStacks")
                                
                            
                        
                        else: 
                            c_3 = comparer.Compare(SetTreeLeaf_1__get_Key(x1_3), SetTreeLeaf_1__get_Key(x2_3)) or 0
                            if c_3 != 0:
                                return c_3
                            
                            else: 
                                comparer_mut = comparer
                                l1_mut = tail(match_value[0])
                                l2_mut = tail(match_value[1])
                                continue
                            
                        
                    
                    else: 
                        x2 = head(match_value[1])
                        match_value_1 = (l1, l2)
                        (pattern_matching_result_3, t1_2, x1, t2_2, x2_1) = (None, None, None, None, None)
                        if not is_empty_1(match_value_1[0]):
                            if head(match_value_1[0]) is not None:
                                pattern_matching_result_3 = 0
                                t1_2 = tail(match_value_1[0])
                                x1 = head(match_value_1[0])
                            
                            elif not is_empty_1(match_value_1[1]):
                                if head(match_value_1[1]) is not None:
                                    pattern_matching_result_3 = 1
                                    t2_2 = tail(match_value_1[1])
                                    x2_1 = head(match_value_1[1])
                                
                                else: 
                                    pattern_matching_result_3 = 2
                                
                            
                            else: 
                                pattern_matching_result_3 = 2
                            
                        
                        elif not is_empty_1(match_value_1[1]):
                            if head(match_value_1[1]) is not None:
                                pattern_matching_result_3 = 1
                                t2_2 = tail(match_value_1[1])
                                x2_1 = head(match_value_1[1])
                            
                            else: 
                                pattern_matching_result_3 = 2
                            
                        
                        else: 
                            pattern_matching_result_3 = 2
                        
                        if pattern_matching_result_3 == 0:
                            if isinstance(x1, SetTreeNode_1):
                                comparer_mut = comparer
                                l1_mut = of_array_with_tail([SetTreeNode_1__get_Left(x1), SetTreeNode_1__ctor_5F465FC9(SetTreeLeaf_1__get_Key(x1), SetTreeModule_empty(), SetTreeNode_1__get_Right(x1), 0)], t1_2)
                                l2_mut = l2
                                continue
                            
                            else: 
                                comparer_mut = comparer
                                l1_mut = of_array_with_tail([SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x1))], t1_2)
                                l2_mut = l2
                                continue
                            
                        
                        elif pattern_matching_result_3 == 1:
                            if isinstance(x2_1, SetTreeNode_1):
                                comparer_mut = comparer
                                l1_mut = l1
                                l2_mut = of_array_with_tail([SetTreeNode_1__get_Left(x2_1), SetTreeNode_1__ctor_5F465FC9(SetTreeLeaf_1__get_Key(x2_1), SetTreeModule_empty(), SetTreeNode_1__get_Right(x2_1), 0)], t2_2)
                                continue
                            
                            else: 
                                comparer_mut = comparer
                                l1_mut = l1
                                l2_mut = of_array_with_tail([SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x2_1))], t2_2)
                                continue
                            
                        
                        elif pattern_matching_result_3 == 2:
                            raise Exception("unexpected state in SetTree.compareStacks")
                        
                    
                
                elif head(match_value[0]) is not None:
                    x1_1 = head(match_value[0])
                    match_value_2 = (l1, l2)
                    (pattern_matching_result_4, t1_4, x1_2, t2_4, x2_2) = (None, None, None, None, None)
                    if not is_empty_1(match_value_2[0]):
                        if head(match_value_2[0]) is not None:
                            pattern_matching_result_4 = 0
                            t1_4 = tail(match_value_2[0])
                            x1_2 = head(match_value_2[0])
                        
                        elif not is_empty_1(match_value_2[1]):
                            if head(match_value_2[1]) is not None:
                                pattern_matching_result_4 = 1
                                t2_4 = tail(match_value_2[1])
                                x2_2 = head(match_value_2[1])
                            
                            else: 
                                pattern_matching_result_4 = 2
                            
                        
                        else: 
                            pattern_matching_result_4 = 2
                        
                    
                    elif not is_empty_1(match_value_2[1]):
                        if head(match_value_2[1]) is not None:
                            pattern_matching_result_4 = 1
                            t2_4 = tail(match_value_2[1])
                            x2_2 = head(match_value_2[1])
                        
                        else: 
                            pattern_matching_result_4 = 2
                        
                    
                    else: 
                        pattern_matching_result_4 = 2
                    
                    if pattern_matching_result_4 == 0:
                        if isinstance(x1_2, SetTreeNode_1):
                            comparer_mut = comparer
                            l1_mut = of_array_with_tail([SetTreeNode_1__get_Left(x1_2), SetTreeNode_1__ctor_5F465FC9(SetTreeLeaf_1__get_Key(x1_2), SetTreeModule_empty(), SetTreeNode_1__get_Right(x1_2), 0)], t1_4)
                            l2_mut = l2
                            continue
                        
                        else: 
                            comparer_mut = comparer
                            l1_mut = of_array_with_tail([SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x1_2))], t1_4)
                            l2_mut = l2
                            continue
                        
                    
                    elif pattern_matching_result_4 == 1:
                        if isinstance(x2_2, SetTreeNode_1):
                            comparer_mut = comparer
                            l1_mut = l1
                            l2_mut = of_array_with_tail([SetTreeNode_1__get_Left(x2_2), SetTreeNode_1__ctor_5F465FC9(SetTreeLeaf_1__get_Key(x2_2), SetTreeModule_empty(), SetTreeNode_1__get_Right(x2_2), 0)], t2_4)
                            continue
                        
                        else: 
                            comparer_mut = comparer
                            l1_mut = l1
                            l2_mut = of_array_with_tail([SetTreeModule_empty(), SetTreeLeaf_1__ctor_2B595(SetTreeLeaf_1__get_Key(x2_2))], t2_4)
                            continue
                        
                    
                    elif pattern_matching_result_4 == 2:
                        raise Exception("unexpected state in SetTree.compareStacks")
                    
                
                else: 
                    comparer_mut = comparer
                    l1_mut = tail(match_value[0])
                    l2_mut = tail(match_value[1])
                    continue
                
            
            else: 
                return 1
            
        
        elif is_empty_1(match_value[1]):
            return 0
        
        else: 
            return -1
        
        break


def SetTreeModule_compare(comparer, t1=None, t2=None):
    if t1 is None:
        if t2 is None:
            return 0
        
        else: 
            return -1
        
    
    elif t2 is None:
        return 1
    
    else: 
        return SetTreeModule_compareStacks(comparer, singleton_1(t1), singleton_1(t2))
    


def SetTreeModule_choose(s=None):
    return SetTreeModule_minimumElement(s)


def SetTreeModule_toList(t=None):
    def loop(t_0027_mut, acc_mut, t=t):
        while True:
            (t_0027, acc) = (t_0027_mut, acc_mut)
            if t_0027 is not None:
                t2 = t_0027
                if isinstance(t2, SetTreeNode_1):
                    t_0027_mut = SetTreeNode_1__get_Left(t2)
                    acc_mut = cons(SetTreeLeaf_1__get_Key(t2), loop(SetTreeNode_1__get_Right(t2), acc))
                    continue
                
                else: 
                    return cons(SetTreeLeaf_1__get_Key(t2), acc)
                
            
            else: 
                return acc
            
            break
    
    return loop(t, empty_1())


def SetTreeModule_copyToArray(s, arr, i):
    j = i or 0
    def arrow_164(x=None, s=s, arr=arr, i=i):
        nonlocal j
        arr[j] = x
        j = (j + 1) or 0
    
    SetTreeModule_iter(arrow_164, s)


def SetTreeModule_toArray(s=None):
    n = SetTreeModule_count(s) or 0
    res = fill([0] * n, 0, n, None)
    SetTreeModule_copyToArray(s, res, 0)
    return res


def SetTreeModule_mkFromEnumerator(comparer_mut, acc_mut, e_mut):
    while True:
        (comparer, acc, e) = (comparer_mut, acc_mut, e_mut)
        if e.System_Collections_IEnumerator_MoveNext():
            comparer_mut = comparer
            acc_mut = SetTreeModule_add(comparer, e.System_Collections_Generic_IEnumerator_00601_get_Current(), acc)
            e_mut = e
            continue
        
        else: 
            return acc
        
        break


def SetTreeModule_ofArray(comparer, l):
    return fold_1(lambda acc, k=None, comparer=comparer, l=l: SetTreeModule_add(comparer, k, acc), SetTreeModule_empty(), l)


def SetTreeModule_ofList(comparer, l):
    return fold_2(lambda acc, k=None, comparer=comparer, l=l: SetTreeModule_add(comparer, k, acc), SetTreeModule_empty(), l)


def SetTreeModule_ofSeq(comparer, c):
    if is_array_like(c):
        return SetTreeModule_ofArray(comparer, c)
    
    elif isinstance(c, FSharpList):
        return SetTreeModule_ofList(comparer, c)
    
    else: 
        with get_enumerator(c) as ie:
            return SetTreeModule_mkFromEnumerator(comparer, SetTreeModule_empty(), ie)
    


def expr_166(gen0):
    return class_type("Set.FSharpSet", [gen0], FSharpSet)


class FSharpSet:
    def __init__(self, comparer, tree=None):
        self.comparer = comparer
        self.tree = tree
    
    def GetHashCode(self):
        this = self
        return FSharpSet__ComputeHashCode(this)
    
    def __eq__(self, that):
        this = self
        return SetTreeModule_compare(FSharpSet__get_Comparer(this), FSharpSet__get_Tree(this), FSharpSet__get_Tree(that)) == 0 if (isinstance(that, FSharpSet)) else (False)
    
    def __str__(self):
        this = self
        def arrow_165(x=None):
            copy_of_struct = x
            return to_string(copy_of_struct)
        
        return ("set [" + join("; ", map_1(arrow_165, this))) + "]"
    
    @property
    def Symbol_toStringTag(self):
        return "FSharpSet"
    
    def to_json(self, _key):
        this = self
        return list(this)
    
    def CompareTo(self, that):
        s = self
        return SetTreeModule_compare(FSharpSet__get_Comparer(s), FSharpSet__get_Tree(s), FSharpSet__get_Tree(that))
    
    def System_Collections_Generic_ICollection_00601_Add2B595(self, x=None):
        ignore(x)
        raise Exception("ReadOnlyCollection")
    
    def System_Collections_Generic_ICollection_00601_Clear(self):
        raise Exception("ReadOnlyCollection")
    
    def System_Collections_Generic_ICollection_00601_Remove2B595(self, x=None):
        ignore(x)
        raise Exception("ReadOnlyCollection")
    
    def System_Collections_Generic_ICollection_00601_Contains2B595(self, x=None):
        s = self
        return SetTreeModule_mem(FSharpSet__get_Comparer(s), x, FSharpSet__get_Tree(s))
    
    def System_Collections_Generic_ICollection_00601_CopyToZ2E171D71(self, arr, i):
        s = self
        SetTreeModule_copyToArray(FSharpSet__get_Tree(s), arr, i)
    
    def System_Collections_Generic_ICollection_00601_get_IsReadOnly(self):
        return True
    
    def System_Collections_Generic_ICollection_00601_get_Count(self):
        s = self
        return FSharpSet__get_Count(s)
    
    def System_Collections_Generic_IReadOnlyCollection_00601_get_Count(self):
        s = self
        return FSharpSet__get_Count(s)
    
    def GetEnumerator(self):
        s = self
        return SetTreeModule_mkIEnumerator(FSharpSet__get_Tree(s))
    
    def __iter__(self):
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_IEnumerable_GetEnumerator(self):
        s = self
        return SetTreeModule_mkIEnumerator(FSharpSet__get_Tree(s))
    
    @property
    def size(self):
        s = self
        return FSharpSet__get_Count(s)
    
    def add(self, k=None):
        s = self
        raise Exception("Set cannot be mutated")
        return s
    
    def clear(self):
        raise Exception("Set cannot be mutated")
    
    def delete(self, k=None):
        raise Exception("Set cannot be mutated")
        return False
    
    def has(self, k=None):
        s = self
        return FSharpSet__Contains(s, k)
    
    def keys(self):
        s = self
        return map_1(lambda x=None: x, s)
    
    def values(self):
        s = self
        return map_1(lambda x=None: x, s)
    
    def entries(self):
        s = self
        return map_1(lambda v=None: (v, v), s)
    
    def for_each(self, f, this_arg=None):
        s = self
        def action(x=None):
            f(x, x, s)
        
        iterate_1(action, s)
    

FSharpSet_reflection = expr_166

def FSharpSet__ctor(comparer, tree=None):
    return FSharpSet(comparer, tree)


def FSharpSet__get_Comparer(set_1):
    return set_1.comparer


def FSharpSet__get_Tree(set_1):
    return set_1.tree


def FSharpSet_Empty(comparer):
    return FSharpSet__ctor(comparer, SetTreeModule_empty())


def FSharpSet__Add(s, value=None):
    return FSharpSet__ctor(FSharpSet__get_Comparer(s), SetTreeModule_add(FSharpSet__get_Comparer(s), value, FSharpSet__get_Tree(s)))


def FSharpSet__Remove(s, value=None):
    return FSharpSet__ctor(FSharpSet__get_Comparer(s), SetTreeModule_remove(FSharpSet__get_Comparer(s), value, FSharpSet__get_Tree(s)))


def FSharpSet__get_Count(s):
    return SetTreeModule_count(FSharpSet__get_Tree(s))


def FSharpSet__Contains(s, value=None):
    return SetTreeModule_mem(FSharpSet__get_Comparer(s), value, FSharpSet__get_Tree(s))


def FSharpSet__Iterate(s, x):
    SetTreeModule_iter(x, FSharpSet__get_Tree(s))


def FSharpSet__Fold(s, f, z=None):
    f_1 = f
    return SetTreeModule_fold(lambda x, z_1=None, s=s, f=f, z=z: f_1(z_1, x), z, FSharpSet__get_Tree(s))


def FSharpSet__get_IsEmpty(s):
    return FSharpSet__get_Tree(s) is None


def FSharpSet__Partition(s, f):
    if FSharpSet__get_Tree(s) is None:
        return (s, s)
    
    else: 
        pattern_input = SetTreeModule_partition(FSharpSet__get_Comparer(s), f, FSharpSet__get_Tree(s))
        return (FSharpSet__ctor(FSharpSet__get_Comparer(s), pattern_input[0]), FSharpSet__ctor(FSharpSet__get_Comparer(s), pattern_input[1]))
    


def FSharpSet__Filter(s, f):
    if FSharpSet__get_Tree(s) is None:
        return s
    
    else: 
        return FSharpSet__ctor(FSharpSet__get_Comparer(s), SetTreeModule_filter(FSharpSet__get_Comparer(s), f, FSharpSet__get_Tree(s)))
    


def FSharpSet__Map(s, f, comparer):
    return FSharpSet__ctor(comparer, SetTreeModule_fold(lambda acc, k=None, s=s, f=f, comparer=comparer: SetTreeModule_add(comparer, f(k), acc), SetTreeModule_empty(), FSharpSet__get_Tree(s)))


def FSharpSet__Exists(s, f):
    return SetTreeModule_exists(f, FSharpSet__get_Tree(s))


def FSharpSet__ForAll(s, f):
    return SetTreeModule_forall(f, FSharpSet__get_Tree(s))


def FSharpSet_op_Subtraction(set1, set2):
    if FSharpSet__get_Tree(set1) is None:
        return set1
    
    elif FSharpSet__get_Tree(set2) is None:
        return set1
    
    else: 
        return FSharpSet__ctor(FSharpSet__get_Comparer(set1), SetTreeModule_diff(FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set1), FSharpSet__get_Tree(set2)))
    


def FSharpSet_op_Addition(set1, set2):
    if FSharpSet__get_Tree(set2) is None:
        return set1
    
    elif FSharpSet__get_Tree(set1) is None:
        return set2
    
    else: 
        return FSharpSet__ctor(FSharpSet__get_Comparer(set1), SetTreeModule_union(FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set1), FSharpSet__get_Tree(set2)))
    


def FSharpSet_Intersection(a, b):
    if FSharpSet__get_Tree(b) is None:
        return b
    
    elif FSharpSet__get_Tree(a) is None:
        return a
    
    else: 
        return FSharpSet__ctor(FSharpSet__get_Comparer(a), SetTreeModule_intersection(FSharpSet__get_Comparer(a), FSharpSet__get_Tree(a), FSharpSet__get_Tree(b)))
    


def FSharpSet_IntersectionMany(sets):
    return reduce(lambda s1, s2, sets=sets: FSharpSet_Intersection(s1, s2), sets)


def FSharpSet_Equality(a, b):
    return SetTreeModule_compare(FSharpSet__get_Comparer(a), FSharpSet__get_Tree(a), FSharpSet__get_Tree(b)) == 0


def FSharpSet_Compare(a, b):
    return SetTreeModule_compare(FSharpSet__get_Comparer(a), FSharpSet__get_Tree(a), FSharpSet__get_Tree(b))


def FSharpSet__get_Choose(x):
    return SetTreeModule_choose(FSharpSet__get_Tree(x))


def FSharpSet__get_MinimumElement(x):
    return SetTreeModule_minimumElement(FSharpSet__get_Tree(x))


def FSharpSet__get_MaximumElement(x):
    return SetTreeModule_maximumElement(FSharpSet__get_Tree(x))


def FSharpSet__IsSubsetOf(x, other_set):
    return SetTreeModule_subset(FSharpSet__get_Comparer(x), FSharpSet__get_Tree(x), FSharpSet__get_Tree(other_set))


def FSharpSet__IsSupersetOf(x, other_set):
    return SetTreeModule_subset(FSharpSet__get_Comparer(x), FSharpSet__get_Tree(other_set), FSharpSet__get_Tree(x))


def FSharpSet__IsProperSubsetOf(x, other_set):
    return SetTreeModule_properSubset(FSharpSet__get_Comparer(x), FSharpSet__get_Tree(x), FSharpSet__get_Tree(other_set))


def FSharpSet__IsProperSupersetOf(x, other_set):
    return SetTreeModule_properSubset(FSharpSet__get_Comparer(x), FSharpSet__get_Tree(other_set), FSharpSet__get_Tree(x))


def FSharpSet__ToList(x):
    return SetTreeModule_toList(FSharpSet__get_Tree(x))


def FSharpSet__ToArray(x):
    return SetTreeModule_toArray(FSharpSet__get_Tree(x))


def FSharpSet__ComputeHashCode(this):
    res = 0
    with get_enumerator(this) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            x_1 = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
            def arrow_167(_unit=None):
                y = structural_hash(x_1) or 0
                return ((res << 1) + y) + 631
            
            res = arrow_167() or 0
    return math.abs(res)


def is_empty(set_1):
    return FSharpSet__get_IsEmpty(set_1)


def contains(element, set_1):
    return FSharpSet__Contains(set_1, element)


def add(value, set_1):
    return FSharpSet__Add(set_1, value)


def singleton(value, comparer):
    return FSharpSet__Add(FSharpSet_Empty(comparer), value)


def remove(value, set_1):
    return FSharpSet__Remove(set_1, value)


def union(set1, set2):
    return FSharpSet_op_Addition(set1, set2)


def union_many(sets, comparer):
    return fold_3(lambda s1, s2, sets=sets, comparer=comparer: FSharpSet_op_Addition(s1, s2), FSharpSet_Empty(comparer), sets)


def intersect(set1, set2):
    return FSharpSet_Intersection(set1, set2)


def intersect_many(sets):
    return FSharpSet_IntersectionMany(sets)


def iterate(action, set_1):
    FSharpSet__Iterate(set_1, action)


def empty(comparer):
    return FSharpSet_Empty(comparer)


def for_all(predicate, set_1):
    return FSharpSet__ForAll(set_1, predicate)


def exists(predicate, set_1):
    return FSharpSet__Exists(set_1, predicate)


def filter(predicate, set_1):
    return FSharpSet__Filter(set_1, predicate)


def partition(predicate, set_1):
    return FSharpSet__Partition(set_1, predicate)


def fold(folder, state, set_1):
    return SetTreeModule_fold(folder, state, FSharpSet__get_Tree(set_1))


def fold_back(folder, set_1, state=None):
    return SetTreeModule_foldBack(folder, FSharpSet__get_Tree(set_1), state)


def map(mapping, set_1, comparer):
    return FSharpSet__Map(set_1, mapping, comparer)


def count(set_1):
    return FSharpSet__get_Count(set_1)


def of_list(elements, comparer):
    return FSharpSet__ctor(comparer, SetTreeModule_ofSeq(comparer, elements))


def of_array(array, comparer):
    return FSharpSet__ctor(comparer, SetTreeModule_ofArray(comparer, array))


def to_list(set_1):
    return FSharpSet__ToList(set_1)


def to_array(set_1):
    return FSharpSet__ToArray(set_1)


def to_seq(set_1):
    return map_1(lambda x=None, set_1=set_1: x, set_1)


def of_seq(elements, comparer):
    return FSharpSet__ctor(comparer, SetTreeModule_ofSeq(comparer, elements))


def difference(set1, set2):
    return FSharpSet_op_Subtraction(set1, set2)


def is_subset(set1, set2):
    return SetTreeModule_subset(FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set1), FSharpSet__get_Tree(set2))


def is_superset(set1, set2):
    return SetTreeModule_subset(FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set2), FSharpSet__get_Tree(set1))


def is_proper_subset(set1, set2):
    return SetTreeModule_properSubset(FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set1), FSharpSet__get_Tree(set2))


def is_proper_superset(set1, set2):
    return SetTreeModule_properSubset(FSharpSet__get_Comparer(set1), FSharpSet__get_Tree(set2), FSharpSet__get_Tree(set1))


def min_element(set_1):
    return FSharpSet__get_MinimumElement(set_1)


def max_element(set_1):
    return FSharpSet__get_MaximumElement(set_1)


def union_with(s1, s2):
    return fold_3(lambda acc, x=None, s1=s1, s2=s2: acc.add(x), s1, s2)


def new_mutable_set_with(s1, s2):
    if isinstance(s1, HashSet):
        return HashSet__ctor_Z6150332D(s2, HashSet__get_Comparer(s1))
    
    else: 
        return Set(s2)
    


def intersect_with(s1, s2):
    s2_1 = new_mutable_set_with(s1, s2)
    def action(x=None, s1=s1, s2=s2):
        if not (s2_1 in x):
            ignore(s1.delete(x))
        
    
    iterate_1(action, s1.values())


def except_with(s1, s2):
    def action(x=None, s1=s1, s2=s2):
        ignore(s1.delete(x))
    
    iterate_1(action, s2)


def is_subset_of(s1, s2):
    s2_1 = new_mutable_set_with(s1, s2)
    return for_all_1(lambda arg00=None, s1=s1, s2=s2: s2_1 in arg00, s1.values())


def is_superset_of(s1, s2):
    return for_all_1(lambda arg00=None, s1=s1, s2=s2: s1 in arg00, s2)


def is_proper_subset_of(s1, s2):
    s2_1 = new_mutable_set_with(s1, s2)
    if s2_1.size > s1.size:
        return for_all_1(lambda arg00=None, s1=s1, s2=s2: s2_1 in arg00, s1.values())
    
    else: 
        return False
    


def is_proper_superset_of(s1, s2):
    s2_1 = cache(s2)
    if exists_1(lambda arg=None, s1=s1, s2=s2: not (s1 in arg), s2_1):
        return for_all_1(lambda arg00_1=None, s1=s1, s2=s2: s1 in arg00_1, s2_1)
    
    else: 
        return False
    


