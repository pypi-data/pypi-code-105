from .seq import (delay, filter, map, to_array, to_list)
from .mutable_set import HashSet
from .map_util import (add_to_set, try_get_value, get_item_from_dict, add_to_dict)
from .mutable_map import Dictionary
from .types import FSharpRef
from .util import get_enumerator

def distinct(xs, comparer):
    def arrow_9(xs=xs, comparer=comparer):
        hash_set = HashSet([], comparer)
        return filter(lambda x=None: add_to_set(x, hash_set), xs)
    
    return delay(arrow_9)


def distinct_by(projection, xs, comparer):
    def arrow_10(projection=projection, xs=xs, comparer=comparer):
        hash_set = HashSet([], comparer)
        return filter(lambda x=None: add_to_set(projection(x), hash_set), xs)
    
    return delay(arrow_10)


def except_(items_to_exclude, xs, comparer):
    def arrow_11(items_to_exclude=items_to_exclude, xs=xs, comparer=comparer):
        hash_set = HashSet(items_to_exclude, comparer)
        return filter(lambda x=None: add_to_set(x, hash_set), xs)
    
    return delay(arrow_11)


def count_by(projection, xs, comparer):
    def arrow_13(projection=projection, xs=xs, comparer=comparer):
        dict_1 = Dictionary([], comparer)
        keys = []
        with get_enumerator(xs) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                key = projection(enumerator.System_Collections_Generic_IEnumerator_00601_get_Current())
                match_value = None
                out_arg = 0
                def arrow_12(v):
                    nonlocal out_arg
                    out_arg = v or 0
                
                match_value = (try_get_value(dict_1, key, FSharpRef(lambda _unit=None: out_arg, arrow_12)), out_arg)
                if match_value[0]:
                    dict_1[key] = (match_value[1]) + 1
                
                else: 
                    dict_1[key] = 1
                    (keys.append(key))
                
        return map(lambda key_1=None: (key_1, get_item_from_dict(dict_1, key_1)), keys)
    
    return delay(arrow_13)


def group_by(projection, xs, comparer):
    def arrow_15(projection=projection, xs=xs, comparer=comparer):
        dict_1 = Dictionary([], comparer)
        keys = []
        with get_enumerator(xs) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                x = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
                key = projection(x)
                match_value = None
                out_arg = None
                def arrow_14(v):
                    nonlocal out_arg
                    out_arg = v
                
                match_value = (try_get_value(dict_1, key, FSharpRef(lambda _unit=None: out_arg, arrow_14)), out_arg)
                if match_value[0]:
                    (match_value[1].append(x))
                
                else: 
                    add_to_dict(dict_1, key, [x])
                    (keys.append(key))
                
        return map(lambda key_1=None: (key_1, get_item_from_dict(dict_1, key_1)), keys)
    
    return delay(arrow_15)


def Array_distinct(xs, comparer):
    return to_array(distinct(xs, comparer))


def Array_distinctBy(projection, xs, comparer):
    return to_array(distinct_by(projection, xs, comparer))


def Array_except(items_to_exclude, xs, comparer):
    return to_array(except_(items_to_exclude, xs, comparer))


def Array_countBy(projection, xs, comparer):
    return to_array(count_by(projection, xs, comparer))


def Array_groupBy(projection, xs, comparer):
    return to_array(map(lambda tupled_arg, projection=projection, xs=xs, comparer=comparer: (tupled_arg[0], to_array(tupled_arg[1])), group_by(projection, xs, comparer)))


def List_distinct(xs, comparer):
    return to_list(distinct(xs, comparer))


def List_distinctBy(projection, xs, comparer):
    return to_list(distinct_by(projection, xs, comparer))


def List_except(items_to_exclude, xs, comparer):
    return to_list(except_(items_to_exclude, xs, comparer))


def List_countBy(projection, xs, comparer):
    return to_list(count_by(projection, xs, comparer))


def List_groupBy(projection, xs, comparer):
    return to_list(map(lambda tupled_arg, projection=projection, xs=xs, comparer=comparer: (tupled_arg[0], to_list(tupled_arg[1])), group_by(projection, xs, comparer)))


