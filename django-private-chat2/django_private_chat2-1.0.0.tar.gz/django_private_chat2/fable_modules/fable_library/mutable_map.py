from .util import (get_enumerator, to_iterator, equals, ignore, dispose)
from .seq import (concat, iterate_indexed, to_array, delay, map, iterate)
from .types import FSharpRef
from .reflection import class_type
from .map_util import (try_get_value, get_item_from_dict)
from .array import find_index
from .string import format

def expr_38(gen0, gen1):
    return class_type("Fable.Collections.Dictionary", [gen0, gen1], Dictionary)


class Dictionary:
    def __init__(self, pairs, comparer):
        this = FSharpRef(None)
        class ObjectExpr37:
            pass
        ObjectExpr37()
        self.comparer = comparer
        this.contents = self
        self.hash_map = dict([])
        self.init_00409 = 1
        with get_enumerator(pairs) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                pair = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
                Dictionary__Add_5BDDA1(this.contents, pair[0], pair[1])
    
    @property
    def Symbol_toStringTag(self):
        return "Dictionary"
    
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
    
    def System_Collections_Generic_ICollection_00601_Add2B595(self, item):
        this = self
        Dictionary__Add_5BDDA1(this, item[0], item[1])
    
    def System_Collections_Generic_ICollection_00601_Clear(self):
        this = self
        Dictionary__Clear(this)
    
    def System_Collections_Generic_ICollection_00601_Contains2B595(self, item):
        this = self
        match_value = Dictionary__TryFind_2B595(this, item[0])
        (pattern_matching_result,) = (None,)
        if match_value is not None:
            if equals(match_value[1], item[1]):
                pattern_matching_result = 0
            
            else: 
                pattern_matching_result = 1
            
        
        else: 
            pattern_matching_result = 1
        
        if pattern_matching_result == 0:
            return True
        
        elif pattern_matching_result == 1:
            return False
        
    
    def System_Collections_Generic_ICollection_00601_CopyToZ2E171D71(self, array, array_index):
        this = self
        def action(i, e):
            array[array_index + i] = e
        
        iterate_indexed(action, this)
    
    def System_Collections_Generic_ICollection_00601_get_Count(self):
        this = self
        return Dictionary__get_Count(this)
    
    def System_Collections_Generic_ICollection_00601_get_IsReadOnly(self):
        return False
    
    def System_Collections_Generic_ICollection_00601_Remove2B595(self, item):
        this = self
        match_value = Dictionary__TryFind_2B595(this, item[0])
        if match_value is not None:
            if equals(match_value[1], item[1]):
                ignore(Dictionary__Remove_2B595(this, item[0]))
            
            return True
        
        else: 
            return False
        
    
    def System_Collections_Generic_IDictionary_00602_Add5BDDA1(self, key, value=None):
        this = self
        Dictionary__Add_5BDDA1(this, key, value)
    
    def System_Collections_Generic_IDictionary_00602_ContainsKey2B595(self, key=None):
        this = self
        return Dictionary__ContainsKey_2B595(this, key)
    
    def System_Collections_Generic_IDictionary_00602_get_Item2B595(self, key=None):
        this = self
        return Dictionary__get_Item_2B595(this, key)
    
    def System_Collections_Generic_IDictionary_00602_set_Item5BDDA1(self, key, v=None):
        this = self
        Dictionary__set_Item_5BDDA1(this, key, v)
    
    def System_Collections_Generic_IDictionary_00602_get_Keys(self):
        this = self
        return to_array(delay(lambda _unit=None: map(lambda pair: pair[0], this)))
    
    def System_Collections_Generic_IDictionary_00602_Remove2B595(self, key=None):
        this = self
        return Dictionary__Remove_2B595(this, key)
    
    def System_Collections_Generic_IDictionary_00602_TryGetValue6DC89625(self, key, value):
        this = self
        match_value = Dictionary__TryFind_2B595(this, key)
        if match_value is not None:
            pair = match_value
            value.contents = pair[1]
            return True
        
        else: 
            return False
        
    
    def System_Collections_Generic_IDictionary_00602_get_Values(self):
        this = self
        return to_array(delay(lambda _unit=None: map(lambda pair: pair[1], this)))
    
    @property
    def size(self):
        this = self
        return Dictionary__get_Count(this)
    
    def clear(self):
        this = self
        Dictionary__Clear(this)
    
    def delete(self, k=None):
        this = self
        return Dictionary__Remove_2B595(this, k)
    
    def entries(self):
        this = self
        return map(lambda p: (p[0], p[1]), this)
    
    def __getitem__(self, k=None):
        this = self
        return Dictionary__get_Item_2B595(this, k)
    
    def has(self, k=None):
        this = self
        return Dictionary__ContainsKey_2B595(this, k)
    
    def keys(self):
        this = self
        return map(lambda p: p[0], this)
    
    def __setitem__(self, k, v=None):
        this = self
        Dictionary__set_Item_5BDDA1(this, k, v)
        return this
    
    def values(self):
        this = self
        return map(lambda p: p[1], this)
    
    def for_each(self, f, this_arg=None):
        this = self
        def action(p):
            f(p[1], p[0], this)
        
        iterate(action, this)
    

Dictionary_reflection = expr_38

def Dictionary__ctor_6623D9B3(pairs, comparer):
    return Dictionary(pairs, comparer)


def Dictionary__TryFindIndex_2B595(this, k=None):
    h = this.comparer.GetHashCode(k) or 0
    match_value = None
    out_arg = None
    def arrow_39(v, this=this, k=k):
        nonlocal out_arg
        out_arg = v
    
    match_value = (try_get_value(this.hash_map, h, FSharpRef(lambda this=this, k=k: out_arg, arrow_39)), out_arg)
    if match_value[0]:
        return (True, h, find_index(lambda pair, this=this, k=k: this.comparer.Equals(k, pair[0]), match_value[1]))
    
    else: 
        return (False, h, -1)
    


def Dictionary__TryFind_2B595(this, k=None):
    match_value = Dictionary__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[0]:
        if (match_value[2]) > -1:
            pattern_matching_result = 0
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return get_item_from_dict(this.hash_map, match_value[1])[match_value[2]]
    
    elif pattern_matching_result == 1:
        return None
    


def Dictionary__get_Comparer(this):
    return this.comparer


def Dictionary__Clear(this):
    this.hash_map.clear()


def Dictionary__get_Count(this):
    count = 0
    enumerator = get_enumerator(this.hash_map.values())
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            pairs = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
            count = (count + len(pairs)) or 0
    
    finally: 
        dispose(enumerator)
    
    return count


def Dictionary__get_Item_2B595(this, k=None):
    match_value = Dictionary__TryFind_2B595(this, k)
    if match_value is not None:
        return match_value[1]
    
    else: 
        raise Exception("The item was not found in collection")
    


def Dictionary__set_Item_5BDDA1(this, k, v=None):
    match_value = Dictionary__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[0]:
        if (match_value[2]) > -1:
            pattern_matching_result = 0
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        get_item_from_dict(this.hash_map, match_value[1])[match_value[2]] = (k, v)
    
    elif pattern_matching_result == 1:
        if match_value[0]:
            value = (get_item_from_dict(this.hash_map, match_value[1]).append((k, v)))
            ignore()
        
        else: 
            this.hash_map[match_value[1]] = [(k, v)]
        
    


def Dictionary__Add_5BDDA1(this, k, v=None):
    match_value = Dictionary__TryFindIndex_2B595(this, k)
    (pattern_matching_result,) = (None,)
    if match_value[0]:
        if (match_value[2]) > -1:
            pattern_matching_result = 0
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        raise Exception(format("An item with the same key has already been added. Key: {0}", k))
    
    elif pattern_matching_result == 1:
        if match_value[0]:
            value = (get_item_from_dict(this.hash_map, match_value[1]).append((k, v)))
            ignore()
        
        else: 
            this.hash_map[match_value[1]] = [(k, v)]
        
    


def Dictionary__ContainsKey_2B595(this, k=None):
    match_value = Dictionary__TryFindIndex_2B595(this, k)
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
    


def Dictionary__Remove_2B595(this, k=None):
    match_value = Dictionary__TryFindIndex_2B595(this, k)
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
    


