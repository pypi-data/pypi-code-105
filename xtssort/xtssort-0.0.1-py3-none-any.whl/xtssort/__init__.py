def Bubble_sorting(lt=None, Positive_or_reverse_order=1):
    c = []
    if lt == None:
        return("如果你不知道参数的意思：lt: 列表, Positive_or_reverse_order: 是正序还是倒序。If you don't know the meaning of the parameter: lt: list, Positive_or_reverse_Order: positive or reverse order.不是的话请填参数：lt, Positive_or_reverse_order。If not, please fill in the parameter: lt, positive_ or_reverse_order.")
    if Positive_or_reverse_order == 1:
        for x in range(len(lt)-1):
            for y in range(len(lt)-x-1):
                if lt[y] > lt[y+1]:
                    lt[y], lt[y+1] = lt[y+1], lt[y]
                    l = []
    elif Positive_or_reverse_order == 2:
        for x in range(len(lt)):
            for y in range(len(lt)-x-1):
                if lt[y] < lt[y+1]:
                    lt[y], lt[y+1] = lt[y+1], lt[y]
    return(lt)


def selectionSort(arr):
    for i in range(len(arr) - 1):
        # 记录最小数的索引
        minIndex = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[minIndex]:
                minIndex = j
        # i 不是最小数时，将 i 和最小数进行交换
        if i != minIndex:
            arr[i], arr[minIndex] = arr[minIndex], arr[i]
    return arr


def insertionSort(arr):
    for i in range(len(arr)):
        preIndex = i-1
        current = arr[i]
        while preIndex >= 0 and arr[preIndex] > current:
            arr[preIndex+1] = arr[preIndex]
            preIndex -= 1
        arr[preIndex+1] = current
    return arr


def shellSort(arr):
    import math
    gap = 1
    while(gap < len(arr)/3):
        gap = gap*3+1
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i-gap
            while j >= 0 and arr[j] > temp:
                arr[j+gap] = arr[j]
                j -= gap
            arr[j+gap] = temp
        gap = math.floor(gap/3)
    return arr


def mergeSort(arr):
    import math
    if(len(arr) < 2):
        return arr
    middle = math.floor(len(arr)/2)
    left, right = arr[0:middle], arr[middle:]
    return merge(mergeSort(left), mergeSort(right))


def merge(left, right):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result


def quickSort(arr, left=None, right=None):
    def partition(arr, left, right):
        pivot = left
        index = pivot+1
        i = index
        while i <= right:
            if arr[i] < arr[pivot]:
                swap(arr, i, index)
                index += 1
            i += 1
        swap(arr, pivot, index-1)
        return index-1

    def swap(arr, i, j):
        arr[i], arr[j] = arr[j], arr[i]

    left = 0 if not isinstance(left, (int, float)) else left
    right = len(arr)-1 if not isinstance(right, (int, float)) else right
    if left < right:
        partitionIndex = partition(arr, left, right)
        quickSort(arr, left, partitionIndex-1)
        quickSort(arr, partitionIndex+1, right)
    return arr


def heapSort(arr):
    def buildMaxHeap(arr):
        import math
        for i in range(math.floor(len(arr)/2), -1, -1):
            heapify(arr, i)

    def heapify(arr, i):
        left = 2*i+1
        right = 2*i+2
        largest = i
        if left < arrLen and arr[left] > arr[largest]:
            largest = left
        if right < arrLen and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            swap(arr, i, largest)
            heapify(arr, largest)

    def swap(arr, i, j):
        arr[i], arr[j] = arr[j], arr[i]
    global arrLen
    arrLen = len(arr)
    buildMaxHeap(arr)
    for i in range(len(arr)-1, 0, -1):
        swap(arr, 0, i)
        arrLen -= 1
        heapify(arr, 0)
    return arr


def countingSort(arr, maxValue):
    bucketLen = maxValue+1
    bucket = [0]*bucketLen
    sortedIndex = 0
    arrLen = len(arr)
    for i in range(arrLen):
        if not bucket[arr[i]]:
            bucket[arr[i]] = 0
        bucket[arr[i]] += 1
    for j in range(bucketLen):
        while bucket[j] > 0:
            arr[sortedIndex] = j
            sortedIndex += 1
            bucket[j] -= 1
    return arr


def bucket_sort(arr, max_num):
    buf = {i: []
           for i in range(int(max_num)+1)}  # 不能使用[[]]*(max+1)，这样新建的空间中各个[]是共享内存的
    arr_len = len(arr)
    for i in range(arr_len):
        num = arr[i]
        buf[int(num)].append(num)  # 将相应范围内的数据加入到[]中
    arr = []
    for i in range(len(buf)):
        if buf[i]:
            arr.extend(sorted(buf[i]))  # 这里还需要对一个范围内的数据进行排序，然后再进行输出
    return arr


def radix_sort(data):
    if not data:
        return []
    max_num = max(data)  # 获取当前数列中最大值
    max_digit = len(str(abs(max_num)))  # 获取最大的位数

    dev = 1  # 第几位数，个位数为1，十位数为10···
    mod = 10  # 求余数的除法
    for i in range(max_digit):
        radix_queue = [list() for k in range(mod * 2)]  # 考虑到负数，我们用两倍队列
        for j in range(len(data)):
            radix = int(((data[j] % mod) / dev) + mod)
            radix_queue[radix].append(data[j])

        pos = 0
        for queue in radix_queue:
            for val in queue:
                data[pos] = val
                pos += 1

        dev *= 10
        mod *= 10
    return data
