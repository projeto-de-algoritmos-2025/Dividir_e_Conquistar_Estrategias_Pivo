def quicksort(arr, left=None, right=None, steps=None, pivot_strategy=None, stats=None):
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1
    
    if stats is None:
        stats = {'comparisons': 0, 'swaps': 0}
    
    if left >= right:
        return
    
    if pivot_strategy is not None:
        comparisons_counter = [stats['comparisons']]
        pivot_idx = pivot_strategy(arr, left, right, comparisons_counter)
        stats['comparisons'] = comparisons_counter[0]
    else:
        pivot_idx = right
    
    if steps is not None:
        state = {
            'array': arr.copy(),
            'left': left,
            'right': right,
            'pivot_idx': pivot_idx,
            'type': 'partition'
        }
        steps.append(state)
    
    pivot_idx = partition(arr, left, right, pivot_idx, stats)
    
    if steps is not None:
        state = {
            'array': arr.copy(),
            'left': left,
            'right': right,
            'pivot_idx': pivot_idx,
            'type': 'after_partition'
        }
        steps.append(state)
    
    quicksort(arr, left, pivot_idx - 1, steps, pivot_strategy, stats)
    quicksort(arr, pivot_idx + 1, right, steps, pivot_strategy, stats)


def partition(arr, left, right, pivot_idx, stats=None):
    if stats is None:
        stats = {'comparisons': 0, 'swaps': 0}
    
    pivot = arr[pivot_idx]
    arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
    stats['swaps'] += 1
    
    i = left - 1
    for j in range(left, right):
        stats['comparisons'] += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            if i != j:
                stats['swaps'] += 1
    
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    stats['swaps'] += 1
    
    return i + 1


def sort(arr, pivot_strategy=None):
    arr_copy = arr.copy()
    stats = {'comparisons': 0, 'swaps': 0}
    quicksort(arr_copy, pivot_strategy=pivot_strategy, stats=stats)
    return arr_copy


def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def quicksort_iterative(arr, pivot_strategy=None):
    if len(arr) <= 1:
        return
    
    stats = {'comparisons': 0, 'swaps': 0}
    
    stack = [(0, len(arr) - 1)]
    
    while stack:
        left, right = stack.pop()
        
        if left >= right:
            continue
        
        if pivot_strategy is not None:
            comparisons_counter = [stats['comparisons']]
            pivot_idx = pivot_strategy(arr, left, right, comparisons_counter)
            stats['comparisons'] = comparisons_counter[0]
        else:
            pivot_idx = right
        
        pivot_idx = partition(arr, left, right, pivot_idx, stats)
        
        if pivot_idx - left < right - pivot_idx:
            stack.append((pivot_idx + 1, right))
            stack.append((left, pivot_idx - 1))
        else:
            stack.append((left, pivot_idx - 1))
            stack.append((pivot_idx + 1, right))


def quicksort_3way(arr, left=None, right=None):
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1
    
    if left >= right:
        return
    
    pivot = arr[left]
    
    i = left
    lt = left
    gt = right
    
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1
    
    quicksort_3way(arr, left, lt - 1)
    quicksort_3way(arr, gt + 1, right)