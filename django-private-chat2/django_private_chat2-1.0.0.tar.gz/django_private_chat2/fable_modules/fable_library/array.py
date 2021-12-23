from .native import (Helpers_allocateArrayFromCons, Helpers_fillImpl, Helpers_indexOfImpl, Helpers_spliceImpl)
import builtins
import functools
import math
from .option import (some, default_arg, value as value_1)
from .util import (max as max_1, compare_primitives, ignore, get_enumerator, equals as equals_1, min as min_1)
from .global_ import SR_indexOutOfBounds

def index_not_found():
    raise Exception("An index satisfying the predicate was not found in the collection.")


def different_lengths():
    raise Exception("Arrays had different lengths")


def append(array1, array2, cons):
    len1 = len(array1) or 0
    len2 = len(array2) or 0
    new_array = Helpers_allocateArrayFromCons(cons, len1 + len2)
    for i in range(0, (len1 - 1) + 1, 1):
        new_array[i] = array1[i]
    for i_1 in range(0, (len2 - 1) + 1, 1):
        new_array[i_1 + len1] = array2[i_1]
    return new_array


def filter(predicate, array):
    return list(builtins.filter(predicate, array))


def fill(target, target_index, count, value=None):
    return Helpers_fillImpl(target, value, target_index, count)


def get_sub_array(array, start, count):
    return array[start:start+count]


def last(array):
    if len(array) == 0:
        raise Exception("The input array was empty\\nParameter name: array")
    
    return array[len(array) - 1]


def try_last(array):
    if len(array) == 0:
        return None
    
    else: 
        return some(array[len(array) - 1])
    


def map_indexed(f, source, cons):
    len_1 = len(source) or 0
    target = Helpers_allocateArrayFromCons(cons, len_1)
    for i in range(0, (len_1 - 1) + 1, 1):
        target[i] = f(i, source[i])
    return target


def map(f, source, cons):
    len_1 = len(source) or 0
    target = Helpers_allocateArrayFromCons(cons, len_1)
    for i in range(0, (len_1 - 1) + 1, 1):
        target[i] = f(source[i])
    return target


def map_indexed2(f, source1, source2, cons):
    if len(source1) != len(source2):
        raise Exception("Arrays had different lengths")
    
    result = Helpers_allocateArrayFromCons(cons, len(source1))
    for i in range(0, (len(source1) - 1) + 1, 1):
        result[i] = f(i, source1[i], source2[i])
    return result


def map2(f, source1, source2, cons):
    if len(source1) != len(source2):
        raise Exception("Arrays had different lengths")
    
    result = Helpers_allocateArrayFromCons(cons, len(source1))
    for i in range(0, (len(source1) - 1) + 1, 1):
        result[i] = f(source1[i], source2[i])
    return result


def map_indexed3(f, source1, source2, source3, cons):
    if True if (len(source1) != len(source2)) else (len(source2) != len(source3)):
        raise Exception("Arrays had different lengths")
    
    result = Helpers_allocateArrayFromCons(cons, len(source1))
    for i in range(0, (len(source1) - 1) + 1, 1):
        result[i] = f(i, source1[i], source2[i], source3[i])
    return result


def map3(f, source1, source2, source3, cons):
    if True if (len(source1) != len(source2)) else (len(source2) != len(source3)):
        raise Exception("Arrays had different lengths")
    
    result = Helpers_allocateArrayFromCons(cons, len(source1))
    for i in range(0, (len(source1) - 1) + 1, 1):
        result[i] = f(source1[i], source2[i], source3[i])
    return result


def map_fold(mapping, state, array, cons):
    match_value = len(array) or 0
    if match_value == 0:
        return ([], state)
    
    else: 
        acc = state
        res = Helpers_allocateArrayFromCons(cons, match_value)
        for i in range(0, (len(array) - 1) + 1, 1):
            pattern_input = mapping(acc, array[i])
            res[i] = pattern_input[0]
            acc = pattern_input[1]
        return (res, acc)
    


def map_fold_back(mapping, array, state, cons):
    match_value = len(array) or 0
    if match_value == 0:
        return ([], state)
    
    else: 
        acc = state
        res = Helpers_allocateArrayFromCons(cons, match_value)
        for i in range(len(array) - 1, 0 - 1, -1):
            pattern_input = mapping(array[i], acc)
            res[i] = pattern_input[0]
            acc = pattern_input[1]
        return (res, acc)
    


def indexed(source):
    len_1 = len(source) or 0
    target = [None]*len_1
    for i in range(0, (len_1 - 1) + 1, 1):
        target[i] = (i, source[i])
    return target


def truncate(count, array):
    count_1 = max_1(lambda x, y, count=count, array=array: compare_primitives(x, y), 0, count) or 0
    return array[0:0+count_1]


def concat(arrays, cons):
    arrays_1 = arrays if (isinstance(arrays, list)) else (list(arrays))
    match_value = len(arrays_1) or 0
    if match_value == 0:
        return Helpers_allocateArrayFromCons(cons, 0)
    
    elif match_value == 1:
        return arrays_1[0]
    
    else: 
        total_idx = 0
        total_length = 0
        for idx in range(0, (len(arrays_1) - 1) + 1, 1):
            arr_1 = arrays_1[idx]
            total_length = (total_length + len(arr_1)) or 0
        result = Helpers_allocateArrayFromCons(cons, total_length)
        for idx_1 in range(0, (len(arrays_1) - 1) + 1, 1):
            arr_2 = arrays_1[idx_1]
            for j in range(0, (len(arr_2) - 1) + 1, 1):
                result[total_idx] = arr_2[j]
                total_idx = (total_idx + 1) or 0
        return result
    


def collect(mapping, array, cons):
    return concat(map(mapping, array, None), cons)


def where(predicate, array):
    return list(builtins.filter(predicate, array))


def contains(value, array, eq):
    def loop(i_mut, value=value, array=array, eq=eq):
        while True:
            (i,) = (i_mut,)
            if i >= len(array):
                return False
            
            elif eq.Equals(value, array[i]):
                return True
            
            else: 
                i_mut = i + 1
                continue
            
            break
    
    return loop(0)


def empty(cons):
    return Helpers_allocateArrayFromCons(cons, 0)


def singleton(value, cons):
    ar = Helpers_allocateArrayFromCons(cons, 1)
    ar[0] = value
    return ar


def initialize(count, initializer, cons):
    if count < 0:
        raise Exception("The input must be non-negative\\nParameter name: count")
    
    result = Helpers_allocateArrayFromCons(cons, count)
    for i in range(0, (count - 1) + 1, 1):
        result[i] = initializer(i)
    return result


def pairwise(array):
    if len(array) < 2:
        return []
    
    else: 
        count = (len(array) - 1) or 0
        result = [None]*count
        for i in range(0, (count - 1) + 1, 1):
            result[i] = (array[i], array[i + 1])
        return result
    


def replicate(count, initial, cons):
    if count < 0:
        raise Exception("The input must be non-negative\\nParameter name: count")
    
    result = Helpers_allocateArrayFromCons(cons, count)
    for i in range(0, (len(result) - 1) + 1, 1):
        result[i] = initial
    return result


def copy(array):
    return array[:]


def reverse(array):
    array_1 = array[:]
    return array_1[::-1]


def scan(folder, state, array, cons):
    res = Helpers_allocateArrayFromCons(cons, len(array) + 1)
    res[0] = state
    for i in range(0, (len(array) - 1) + 1, 1):
        res[i + 1] = folder(res[i], array[i])
    return res


def scan_back(folder, array, state, cons):
    res = Helpers_allocateArrayFromCons(cons, len(array) + 1)
    res[len(array)] = state
    for i in range(len(array) - 1, 0 - 1, -1):
        res[i] = folder(array[i], res[i + 1])
    return res


def skip(count, array, cons):
    if count > len(array):
        raise Exception("count is greater than array length\\nParameter name: count")
    
    if count == len(array):
        return Helpers_allocateArrayFromCons(cons, 0)
    
    else: 
        count_1 = (0 if (count < 0) else (count)) or 0
        return array[count_1:]
    


def skip_while(predicate, array, cons):
    count = 0
    while predicate(array[count]) if (count < len(array)) else (False):
        count = (count + 1) or 0
    if count == len(array):
        return Helpers_allocateArrayFromCons(cons, 0)
    
    else: 
        return array[count:]
    


def take(count, array, cons):
    if count < 0:
        raise Exception("The input must be non-negative\\nParameter name: count")
    
    if count > len(array):
        raise Exception("count is greater than array length\\nParameter name: count")
    
    if count == 0:
        return Helpers_allocateArrayFromCons(cons, 0)
    
    else: 
        return array[0:0+count]
    


def take_while(predicate, array, cons):
    count = 0
    while predicate(array[count]) if (count < len(array)) else (False):
        count = (count + 1) or 0
    if count == 0:
        return Helpers_allocateArrayFromCons(cons, 0)
    
    else: 
        return array[0:0+count]
    


def add_in_place(x, array):
    ignore(array.append(x))


def add_range_in_place(range, array):
    with get_enumerator(range) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            add_in_place(enumerator.System_Collections_Generic_IEnumerator_00601_get_Current(), array)


def insert_range_in_place(index, range, array):
    i = index or 0
    with get_enumerator(range) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            x = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
            def arrow_64(_unit=None):
                index_1 = i or 0
                return array.insert(index_1, x)
            
            ignore(arrow_64())
            i = (i + 1) or 0


def remove_in_place(item_1, array):
    i = Helpers_indexOfImpl(array, item_1, 0) or 0
    if i > -1:
        ignore(Helpers_spliceImpl(array, i, 1))
        return True
    
    else: 
        return False
    


def remove_all_in_place(predicate, array):
    def count_remove_all(count, predicate=predicate, array=array):
        i = (next((i for i, x in enumerate(array) if (predicate)(x)), -1)) or 0
        if i > -1:
            ignore(Helpers_spliceImpl(array, i, 1))
            return count_remove_all(count) + 1
        
        else: 
            return count
        
    
    return count_remove_all(0)


def copy_to(source, source_index, target, target_index, count):
    diff = (target_index - source_index) or 0
    for i in range(source_index, ((source_index + count) - 1) + 1, 1):
        target[i + diff] = source[i]


def copy_to_typed_array(source, source_index, target, target_index, count):
    try: 
        target.set(source.subarray(source_index, source_index + count), target_index)
    
    except Exception as match_value:
        copy_to(source, source_index, target, target_index, count)
    


def index_of(array, item_1, start=None, count=None):
    start_1 = default_arg(start, 0) or 0
    i = Helpers_indexOfImpl(array, item_1, start_1) or 0
    if i >= (start_1 + value_1(count)) if (count is not None) else (False):
        return -1
    
    else: 
        return i
    


def partition(f, source, cons):
    len_1 = len(source) or 0
    res1 = Helpers_allocateArrayFromCons(cons, len_1)
    res2 = Helpers_allocateArrayFromCons(cons, len_1)
    i_true = 0
    i_false = 0
    for i in range(0, (len_1 - 1) + 1, 1):
        if f(source[i]):
            res1[i_true] = source[i]
            i_true = (i_true + 1) or 0
        
        else: 
            res2[i_false] = source[i]
            i_false = (i_false + 1) or 0
        
    return (truncate(i_true, res1), truncate(i_false, res2))


def find(predicate, array):
    match_value = next((x for x in array if (predicate)(x)), None)
    if match_value is None:
        return index_not_found()
    
    else: 
        return value_1(match_value)
    


def try_find(predicate, array):
    return next((x for x in array if (predicate)(x)), None)


def find_index(predicate, array):
    match_value = (next((i for i, x in enumerate(array) if (predicate)(x)), -1)) or 0
    if match_value > -1:
        return match_value
    
    else: 
        return index_not_found()
    


def try_find_index(predicate, array):
    match_value = (next((i for i, x in enumerate(array) if (predicate)(x)), -1)) or 0
    if match_value > -1:
        return match_value
    
    else: 
        return None
    


def pick(chooser, array):
    def loop(i_mut, chooser=chooser, array=array):
        while True:
            (i,) = (i_mut,)
            if i >= len(array):
                return index_not_found()
            
            else: 
                match_value = chooser(array[i])
                if match_value is not None:
                    return value_1(match_value)
                
                else: 
                    i_mut = i + 1
                    continue
                
            
            break
    
    return loop(0)


def try_pick(chooser, array):
    def loop(i_mut, chooser=chooser, array=array):
        while True:
            (i,) = (i_mut,)
            if i >= len(array):
                return None
            
            else: 
                match_value = chooser(array[i])
                if match_value is None:
                    i_mut = i + 1
                    continue
                
                else: 
                    return match_value
                
            
            break
    
    return loop(0)


def find_back(predicate, array):
    def loop(i_mut, predicate=predicate, array=array):
        while True:
            (i,) = (i_mut,)
            if i < 0:
                return index_not_found()
            
            elif predicate(array[i]):
                return array[i]
            
            else: 
                i_mut = i - 1
                continue
            
            break
    
    return loop(len(array) - 1)


def try_find_back(predicate, array):
    def loop(i_mut, predicate=predicate, array=array):
        while True:
            (i,) = (i_mut,)
            if i < 0:
                return None
            
            elif predicate(array[i]):
                return some(array[i])
            
            else: 
                i_mut = i - 1
                continue
            
            break
    
    return loop(len(array) - 1)


def find_last_index(predicate, array):
    def loop(i_mut, predicate=predicate, array=array):
        while True:
            (i,) = (i_mut,)
            if i < 0:
                return -1
            
            elif predicate(array[i]):
                return i
            
            else: 
                i_mut = i - 1
                continue
            
            break
    
    return loop(len(array) - 1)


def find_index_back(predicate, array):
    def loop(i_mut, predicate=predicate, array=array):
        while True:
            (i,) = (i_mut,)
            if i < 0:
                return index_not_found()
            
            elif predicate(array[i]):
                return i
            
            else: 
                i_mut = i - 1
                continue
            
            break
    
    return loop(len(array) - 1)


def try_find_index_back(predicate, array):
    def loop(i_mut, predicate=predicate, array=array):
        while True:
            (i,) = (i_mut,)
            if i < 0:
                return None
            
            elif predicate(array[i]):
                return i
            
            else: 
                i_mut = i - 1
                continue
            
            break
    
    return loop(len(array) - 1)


def choose(chooser, array, cons):
    res = []
    for i in range(0, (len(array) - 1) + 1, 1):
        match_value = chooser(array[i])
        if match_value is not None:
            ignore(res.append(value_1(match_value)))
        
    if equals_1(cons, None):
        return res
    
    else: 
        return map(lambda x=None, chooser=chooser, array=array, cons=cons: x, res, cons)
    


def fold_indexed(folder, state, array):
    return array.reduce((lambda delegate_arg0, delegate_arg1, delegate_arg2, folder=folder, state=state, array=array: folder(delegate_arg2, delegate_arg0, delegate_arg1), state))


def fold(folder, state, array):
    return functools.reduce((lambda acc, x=None, folder=folder, state=state, array=array: folder(acc, x)), array, state)


def iterate(action, array):
    for i in range(0, (len(array) - 1) + 1, 1):
        action(array[i])


def iterate_indexed(action, array):
    for i in range(0, (len(array) - 1) + 1, 1):
        action(i, array[i])


def iterate2(action, array1, array2):
    if len(array1) != len(array2):
        different_lengths()
    
    for i in range(0, (len(array1) - 1) + 1, 1):
        action(array1[i], array2[i])


def iterate_indexed2(action, array1, array2):
    if len(array1) != len(array2):
        different_lengths()
    
    for i in range(0, (len(array1) - 1) + 1, 1):
        action(i, array1[i], array2[i])


def is_empty(array):
    return len(array) == 0


def for_all(predicate, array):
    return all([predicate(x) for x in array])


def permute(f, array):
    size = len(array) or 0
    res = array[:]
    check_flags = [None]*size
    def arrow_67(i, x=None, f=f, array=array):
        j = f(i) or 0
        if True if (j < 0) else (j >= size):
            raise Exception("Not a valid permutation")
        
        res[j] = x
        check_flags[j] = 1
    
    iterate_indexed(arrow_67, array)
    if not (all([(lambda y, f=f, array=array: 1 == y)(x) for x in check_flags])):
        raise Exception("Not a valid permutation")
    
    return res


def set_slice(target, lower, upper, source):
    lower_1 = default_arg(lower, 0) or 0
    upper_1 = default_arg(upper, 0) or 0
    length = ((upper_1 if (upper_1 > 0) else (len(target) - 1)) - lower_1) or 0
    for i in range(0, length + 1, 1):
        target[i + lower_1] = source[i]


def sort_in_place_by(projection, xs, comparer):
    xs.sort()


def sort_in_place(xs, comparer):
    xs.sort()


def sort(xs, comparer):
    xs_1 = xs[:]
    def expr_75():
        xs_1.sort()
        return xs_1
    
    return expr_75()


def sort_by(projection, xs, comparer):
    xs_1 = xs[:]
    def expr_76():
        xs_1.sort()
        return xs_1
    
    return expr_76()


def sort_descending(xs, comparer):
    xs_1 = xs[:]
    def expr_77():
        xs_1.sort()
        return xs_1
    
    return expr_77()


def sort_by_descending(projection, xs, comparer):
    xs_1 = xs[:]
    def expr_78():
        xs_1.sort()
        return xs_1
    
    return expr_78()


def sort_with(comparer, xs):
    comparer_1 = comparer
    xs_1 = xs[:]
    def expr_79():
        xs_1.sort()
        return xs_1
    
    return expr_79()


def all_pairs(xs, ys):
    len1 = len(xs) or 0
    len2 = len(ys) or 0
    res = [None]*(len1 * len2)
    for i in range(0, (len(xs) - 1) + 1, 1):
        for j in range(0, (len(ys) - 1) + 1, 1):
            res[(i * len2) + j] = (xs[i], ys[j])
    return res


def unfold(generator, state=None):
    res = []
    def loop(state_1_mut=None, generator=generator, state=state):
        while True:
            (state_1,) = (state_1_mut,)
            match_value = generator(state_1)
            if match_value is not None:
                s = match_value[1]
                ignore(res.append(match_value[0]))
                state_1_mut = s
                continue
            
            break
    
    loop(state)
    return res


def unzip(array):
    len_1 = len(array) or 0
    res1 = [None]*len_1
    res2 = [None]*len_1
    def arrow_80(i, tupled_arg, array=array):
        res1[i] = tupled_arg[0]
        res2[i] = tupled_arg[1]
    
    iterate_indexed(arrow_80, array)
    return (res1, res2)


def unzip3(array):
    len_1 = len(array) or 0
    res1 = [None]*len_1
    res2 = [None]*len_1
    res3 = [None]*len_1
    def arrow_81(i, tupled_arg, array=array):
        res1[i] = tupled_arg[0]
        res2[i] = tupled_arg[1]
        res3[i] = tupled_arg[2]
    
    iterate_indexed(arrow_81, array)
    return (res1, res2, res3)


def zip(array1, array2):
    if len(array1) != len(array2):
        different_lengths()
    
    result = [None]*len(array1)
    for i in range(0, (len(array1) - 1) + 1, 1):
        result[i] = (array1[i], array2[i])
    return result


def zip3(array1, array2, array3):
    if True if (len(array1) != len(array2)) else (len(array2) != len(array3)):
        different_lengths()
    
    result = [None]*len(array1)
    for i in range(0, (len(array1) - 1) + 1, 1):
        result[i] = (array1[i], array2[i], array3[i])
    return result


def chunk_by_size(chunk_size, array):
    if chunk_size < 1:
        raise Exception("The input must be positive.\\nParameter name: size")
    
    if len(array) == 0:
        return [[]]
    
    else: 
        result = []
        for x in range(0, (int(math.ceil(len(array) / chunk_size)) - 1) + 1, 1):
            start = (x * chunk_size) or 0
            ignore(result.append(array[start:start+chunk_size]))
        return result
    


def split_at(index, array):
    if True if (index < 0) else (index > len(array)):
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    return (array[0:0+index], array[index:])


def compare_with(comparer, array1, array2):
    if array1 is None:
        if array2 is None:
            return 0
        
        else: 
            return -1
        
    
    elif array2 is None:
        return 1
    
    else: 
        i = 0
        result = 0
        length1 = len(array1) or 0
        length2 = len(array2) or 0
        if length1 > length2:
            return 1
        
        elif length1 < length2:
            return -1
        
        else: 
            while result == 0 if (i < length1) else (False):
                result = comparer(array1[i], array2[i]) or 0
                i = (i + 1) or 0
            return result
        
    


def equals_with(equals, array1, array2):
    if array1 is None:
        if array2 is None:
            return True
        
        else: 
            return False
        
    
    elif array2 is None:
        return False
    
    else: 
        i = 0
        result = True
        length1 = len(array1) or 0
        length2 = len(array2) or 0
        if length1 > length2:
            return False
        
        elif length1 < length2:
            return False
        
        else: 
            while result if (i < length1) else (False):
                result = equals(array1[i], array2[i])
                i = (i + 1) or 0
            return result
        
    


def exactly_one(array):
    if len(array) == 1:
        return array[0]
    
    elif len(array) == 0:
        raise Exception("The input sequence was empty\\nParameter name: array")
    
    else: 
        raise Exception("Input array too long\\nParameter name: array")
    


def try_exactly_one(array):
    if len(array) == 1:
        return some(array[0])
    
    else: 
        return None
    


def head(array):
    if len(array) == 0:
        raise Exception("The input array was empty\\nParameter name: array")
    
    else: 
        return array[0]
    


def try_head(array):
    if len(array) == 0:
        return None
    
    else: 
        return some(array[0])
    


def tail(array):
    if len(array) == 0:
        raise Exception("Not enough elements\\nParameter name: array")
    
    return array[1:]


def item(index, array):
    return array[index]


def try_item(index, array):
    if True if (index < 0) else (index >= len(array)):
        return None
    
    else: 
        return some(array[index])
    


def fold_back_indexed(folder, array, state=None):
    return array.reduceRight((lambda delegate_arg0, delegate_arg1, delegate_arg2, folder=folder, array=array, state=state: folder(delegate_arg2, delegate_arg1, delegate_arg0), state))


def fold_back(folder, array, state=None):
    return functools.reduce((lambda acc, x=None, folder=folder, array=array, state=state: folder(x, acc)), array[::-1], state)


def fold_indexed2(folder, state, array1, array2):
    acc = state
    if len(array1) != len(array2):
        raise Exception("Arrays have different lengths")
    
    for i in range(0, (len(array1) - 1) + 1, 1):
        acc = folder(i, acc, array1[i], array2[i])
    return acc


def fold2(folder, state, array1, array2):
    return fold_indexed2(lambda _arg1, acc, x, y=None, folder=folder, state=state, array1=array1, array2=array2: folder(acc, x, y), state, array1, array2)


def fold_back_indexed2(folder, array1, array2, state=None):
    acc = state
    if len(array1) != len(array2):
        different_lengths()
    
    size = len(array1) or 0
    for i in range(1, size + 1, 1):
        acc = folder(i - 1, array1[size - i], array2[size - i], acc)
    return acc


def fold_back2(f, array1, array2, state=None):
    return fold_back_indexed2(lambda _arg1, x, y, acc=None, f=f, array1=array1, array2=array2, state=state: f(x, y, acc), array1, array2, state)


def reduce(reduction, array):
    if len(array) == 0:
        raise Exception("The input array was empty")
    
    return functools.reduce(reduction, array)


def reduce_back(reduction, array):
    if len(array) == 0:
        raise Exception("The input array was empty")
    
    return functools.reduce(reduction, array[::-1])


def for_all2(predicate, array1, array2):
    return fold2(lambda acc, x, y=None, predicate=predicate, array1=array1, array2=array2: predicate(x, y) if (acc) else (False), True, array1, array2)


def exists_offset(predicate_mut, array_mut, index_mut):
    while True:
        (predicate, array, index) = (predicate_mut, array_mut, index_mut)
        if index == len(array):
            return False
        
        elif predicate(array[index]):
            return True
        
        else: 
            predicate_mut = predicate
            array_mut = array
            index_mut = index + 1
            continue
        
        break


def exists(predicate, array):
    return exists_offset(predicate, array, 0)


def exists_offset2(predicate_mut, array1_mut, array2_mut, index_mut):
    while True:
        (predicate, array1, array2, index) = (predicate_mut, array1_mut, array2_mut, index_mut)
        if index == len(array1):
            return False
        
        elif predicate(array1[index], array2[index]):
            return True
        
        else: 
            predicate_mut = predicate
            array1_mut = array1
            array2_mut = array2
            index_mut = index + 1
            continue
        
        break


def exists2(predicate, array1, array2):
    if len(array1) != len(array2):
        different_lengths()
    
    return exists_offset2(predicate, array1, array2, 0)


def sum(array, adder):
    acc = adder.GetZero()
    for i in range(0, (len(array) - 1) + 1, 1):
        acc = adder.Add(acc, array[i])
    return acc


def sum_by(projection, array, adder):
    acc = adder.GetZero()
    for i in range(0, (len(array) - 1) + 1, 1):
        acc = adder.Add(acc, projection(array[i]))
    return acc


def max_by(projection, xs, comparer):
    return reduce(lambda x, y=None, projection=projection, xs=xs, comparer=comparer: y if (comparer.Compare(projection(y), projection(x)) > 0) else (x), xs)


def max(xs, comparer):
    return reduce(lambda x, y=None, xs=xs, comparer=comparer: y if (comparer.Compare(y, x) > 0) else (x), xs)


def min_by(projection, xs, comparer):
    return reduce(lambda x, y=None, projection=projection, xs=xs, comparer=comparer: x if (comparer.Compare(projection(y), projection(x)) > 0) else (y), xs)


def min(xs, comparer):
    return reduce(lambda x, y=None, xs=xs, comparer=comparer: x if (comparer.Compare(y, x) > 0) else (y), xs)


def average(array, averager):
    if len(array) == 0:
        raise Exception("The input array was empty\\nParameter name: array")
    
    total = averager.GetZero()
    for i in range(0, (len(array) - 1) + 1, 1):
        total = averager.Add(total, array[i])
    return averager.DivideByInt(total, len(array))


def average_by(projection, array, averager):
    if len(array) == 0:
        raise Exception("The input array was empty\\nParameter name: array")
    
    total = averager.GetZero()
    for i in range(0, (len(array) - 1) + 1, 1):
        total = averager.Add(total, projection(array[i]))
    return averager.DivideByInt(total, len(array))


def windowed(window_size, source):
    if window_size <= 0:
        raise Exception("windowSize must be positive")
    
    res = None
    len_1 = max_1(lambda x, y, window_size=window_size, source=source: compare_primitives(x, y), 0, len(source) - window_size) or 0
    res = [None]*len_1
    for i in range(window_size, len(source) + 1, 1):
        res[i - window_size] = source[i - window_size:(i - 1) + 1]
    return res


def split_into(chunks, array):
    if chunks < 1:
        raise Exception("The input must be positive.\\nParameter name: chunks")
    
    if len(array) == 0:
        return [[]]
    
    else: 
        result = []
        chunks_1 = min_1(lambda x, y, chunks=chunks, array=array: compare_primitives(x, y), chunks, len(array)) or 0
        min_chunk_size = (len(array) // chunks_1) or 0
        chunks_with_extra_item = (len(array) % chunks_1) or 0
        for i in range(0, (chunks_1 - 1) + 1, 1):
            chunk_size = (min_chunk_size + 1 if (i < chunks_with_extra_item) else (min_chunk_size)) or 0
            start = ((i * min_chunk_size) + min_1(lambda x_1, y_1, chunks=chunks, array=array: compare_primitives(x_1, y_1), chunks_with_extra_item, i)) or 0
            ignore(result.append(array[start:start+chunk_size]))
        return result
    


def transpose(arrays, cons):
    arrays_1 = arrays if (isinstance(arrays, list)) else (list(arrays))
    len_1 = len(arrays_1) or 0
    if len_1 == 0:
        return [None]*0
    
    else: 
        len_inner = len(arrays_1[0]) or 0
        if not for_all(lambda a, arrays=arrays, cons=cons: len(a) == len_inner, arrays_1):
            different_lengths()
        
        result = [None]*len_inner
        for i in range(0, (len_inner - 1) + 1, 1):
            result[i] = Helpers_allocateArrayFromCons(cons, len_1)
            for j in range(0, (len_1 - 1) + 1, 1):
                result[i][j] = arrays_1[j][i]
        return result
    


def insert_at(index, y, xs):
    len_1 = len(xs) or 0
    if True if (index < 0) else (index > len_1):
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    target = [x for i, x in enumerate(xs) if i < (len_1 + 1)]
    for i in range(0, (index - 1) + 1, 1):
        target[i] = xs[i]
    target[index] = y
    for i_1 in range(index, (len_1 - 1) + 1, 1):
        target[i_1 + 1] = xs[i_1]
    return target


def insert_many_at(index, ys, xs):
    len_1 = len(xs) or 0
    if True if (index < 0) else (index > len_1):
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    ys_1 = list(ys)
    len2 = len(ys_1) or 0
    target = [x for i, x in enumerate(xs) if i < (len_1 + len2)]
    for i in range(0, (index - 1) + 1, 1):
        target[i] = xs[i]
    for i_1 in range(0, (len2 - 1) + 1, 1):
        target[index + i_1] = ys_1[i_1]
    for i_2 in range(index, (len_1 - 1) + 1, 1):
        target[i_2 + len2] = xs[i_2]
    return target


def remove_at(index, xs):
    if True if (index < 0) else (index >= len(xs)):
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    i = -1
    def predicate(_arg1=None, index=index, xs=xs):
        nonlocal i
        i = (i + 1) or 0
        return i != index
    
    return filter(predicate, xs)


def remove_many_at(index, count, xs):
    i = -1
    status = -1
    def predicate(_arg1=None, index=index, count=count, xs=xs):
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
        
    
    ys = filter(predicate, xs)
    status_1 = (1 if ((i + 1) == (index + count) if (status == 0) else (False)) else (status)) or 0
    if status_1 < 1:
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + ("index" if (status_1 < 0) else ("count")))
    
    return ys


def update_at(index, y, xs):
    len_1 = len(xs) or 0
    if True if (index < 0) else (index >= len_1):
        raise Exception((SR_indexOutOfBounds + "\\nParameter name: ") + "index")
    
    target = [x for i, x in enumerate(xs) if i < len_1]
    for i in range(0, (len_1 - 1) + 1, 1):
        target[i] = y if (i == index) else (xs[i])
    return target


