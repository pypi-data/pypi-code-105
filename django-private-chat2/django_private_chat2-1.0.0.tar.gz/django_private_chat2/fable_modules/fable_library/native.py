
def Helpers_allocateArrayFromCons(cons, len_1):
    if cons is None:
        return (list)([None]*len_1)
    
    else: 
        return cons([0]*len_1)
    


def Helpers_fillImpl(array, value, start, count):
    for i in range(0, (count - 1) + 1, 1):
        array[i + start] = value
    return array


def Helpers_spliceImpl(array, start, delete_count):
    for _ in range(1, delete_count + 1, 1):
        array.pop(start)
    return array


def Helpers_indexOfImpl(array, item, start):
    try: 
        return array.index(item, start)
    
    except Exception as ex:
        return -1
    


