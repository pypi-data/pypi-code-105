from .util import (get_enumerator, to_iterator, ignore, dispose)
from .seq import (concat, iterate_indexed, map, iterate)
from .types import FSharpRef
from .reflection import class_type
from .map_util import (try_get_value, get_item_from_dict)
from .array import find_index
from .option import some

def expr_23(gen0):
    return class_type("Fable.Collections.HashSet", [gen0], HashSet)


class HashSet:
    def __init__(self, items, comparer):
        this = FSharpRef(None)
        class ObjectExpr22:
            pass
        ObjectExpr22()
        self.comparer = comparer
        this.contents = self
        self.hash_map = dict([])
        self.init_00409_002d1 = 1
        with get_enumerator(items) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                ignore(HashSet__Add_2B595(this.contents, enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()))
    
    @property
    def Symbol_toStringTag(self):
        return "HashSet"
    
    def to_json(self, _key):
        this = self
        return list(this)
    
    def System_Collections_IEnumerable_GetEnumerator(self):
        this = self
        return get_enumerator(this)
    
    def GetEnumerator(self):
        this = self
        return get_enumerator(concat(this.hash_map.values()))
    
    def __iter__(self):
        return to_iterator(self.GetEnumerator())
    
    def System_Collections_Generic_ICollection_00601_Add2B595(self, item=None):
        this = self
        ignore(HashSet__Add_2B595(this, item))
    
    def System_Collections_Generic_ICollection_00601_Clear(self):
        this = self
        HashSet__Clear(this)
    
    def System_Collections_Generic_ICollection_00601_Contains2B595(self, item=None):
        this = self
        return HashSet__Contains_2B595(this, item)
    
    def System_Collections_Generic_ICollection_00601_CopyToZ2E171D71(self, array, array_index):
        this = self
        def action(i, e=None):
            array[array_index + i] = e
        
        iterate_indexed(action, this)
    
    def System_Collections_Generic_ICollection_00601_get_Count(self):
        this = self
        return HashSet__get_Count(this)
    
    def System_Collections_Generic_ICollection_00601_get_IsReadOnly(self):
        return False
    
    def System_Collections_Generic_ICollection_00601_Remove2B595(self, item=None):
        this = self
        return HashSet__Remove_2B595(this, item)
    
    @property
    def size(self):
        this = self
        return HashSet__get_Count(this)
    
    def add(self, k=None):
        this = self
        ignore(HashSet__Add_2B595(this, k))
        return this
    
    def clear(self):
        this = self
        HashSet__Clear(this)
    
    def delete(self, k=None):
        this = self
        return HashSet__Remove_2B595(this, k)
    
    def has(self, k=None):
        this = self
        return HashSet__Contains_2B595(this, k)
    
    def keys(self):
        this = self
        return map(lambda x=None: x, this)
    
    def values(self):
        this = self
        return map(lambda x=None: x, this)
    
    def entries(self):
        this = self
        return map(lambda v=None: (v, v), this)
    
    def for_each(self, f, this_arg=None):
        this = self
        def action(x=None):
            f(x, x, this)
        
        iterate(action, this)
    

HashSet_reflection = expr_23

def HashSet__ctor_Z6150332D(items, comparer):
    return HashSet(items, comparer)


def HashSet__TryFindIndex_2B595(this, k=None):
    h = this.comparer.GetHashCode(k) or 0
    match_value = None
    out_arg = None
    def arrow_24(v, this=this, k=k):
        nonlocal out_arg
        out_arg = v
    
    match_value = (try_get_value(this.hash_map, h, FSharpRef(lambda this=this, k=k: out_arg, arrow_24)), out_arg)
    if match_value[0]:
        return (True, h, find_index(lambda v_1=None, this=this, k=k: this.comparer.Equals(k, v_1), match_value[1]))
    
    else: 
        return (False, h, -1)
    


def HashSet__TryFind_2B595(this, k=None):
    match_value = HashSet__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[0]:
        if (match_value[2]) > -1:
            pattern_matching_result = 0
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return some(get_item_from_dict(this.hash_map, match_value[1])[match_value[2]])
    
    elif pattern_matching_result == 1:
        return None
    


def HashSet__get_Comparer(this):
    return this.comparer


def HashSet__Clear(this):
    this.hash_map.clear()


def HashSet__get_Count(this):
    count = 0
    enumerator = get_enumerator(this.hash_map.values())
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            items = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
            count = (count + len(items)) or 0
    
    finally: 
        dispose(enumerator)
    
    return count


def HashSet__Add_2B595(this, k=None):
    match_value = HashSet__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[0]:
        if (match_value[2]) > -1:
            pattern_matching_result = 0
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return False
    
    elif pattern_matching_result == 1:
        if match_value[0]:
            value = (get_item_from_dict(this.hash_map, match_value[1]).append(k))
            ignore()
            return True
        
        else: 
            this.hash_map[match_value[1]] = [k]
            return True
        
    


def HashSet__Contains_2B595(this, k=None):
    match_value = HashSet__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[0]:
        if (match_value[2]) > -1:
            pattern_matching_result = 0
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return True
    
    elif pattern_matching_result == 1:
        return False
    


def HashSet__Remove_2B595(this, k=None):
    match_value = HashSet__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[0]:
        if (match_value[2]) > -1:
            pattern_matching_result = 0
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        get_item_from_dict(this.hash_map, match_value[1]).pop(match_value[2], 1)
        return True
    
    elif pattern_matching_result == 1:
        return False
    


