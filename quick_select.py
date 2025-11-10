def quickselect(arr, left, right, k, steps=None, pivot_strategy=None, stats=None):
    if left == right:
        return arr[left]
    
    if stats is None:
        stats = {'comparisons': 0, 'partitions': 0}
    
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
            'k': k,
            'type': 'partition'
        }
        steps.append(state)
    
    stats['partitions'] += 1
    
    pivot_idx = partition(arr, left, right, pivot_idx, stats)
    
    if steps is not None:
        state = {
            'array': arr.copy(),
            'left': left,
            'right': right,
            'pivot_idx': pivot_idx,
            'k': k,
            'type': 'after_partition'
        }
        steps.append(state)
    
    if k == pivot_idx:
        if steps is not None:
            state = {
                'array': arr.copy(),
                'left': left,
                'right': right,
                'pivot_idx': pivot_idx,
                'k': k,
                'type': 'found'
            }
            steps.append(state)
        return arr[k]
    elif k < pivot_idx:
        return quickselect(arr, left, pivot_idx - 1, k, steps, pivot_strategy, stats)
    else:
        return quickselect(arr, pivot_idx + 1, right, k, steps, pivot_strategy, stats)


def partition(arr, left, right, pivot_idx, stats=None):
    if stats is None:
        stats = {'comparisons': 0}
    
    pivot = arr[pivot_idx]
    arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
    
    i = left - 1
    for j in range(left, right):
        stats['comparisons'] += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    
    return i + 1


def find_kth_smallest(arr, k, pivot_strategy=None):
    if k < 1 or k > len(arr):
        raise ValueError(f"k deve estar entre 1 e {len(arr)}")
    
    k_index = k - 1
    
    arr_copy = arr.copy()
    
    stats = {'comparisons': 0, 'partitions': 0}
    result = quickselect(arr_copy, 0, len(arr_copy) - 1, k_index, 
                        pivot_strategy=pivot_strategy, stats=stats)
    
    return result


def find_median(arr, pivot_strategy=None):
    n = len(arr)
    if n == 0:
        raise ValueError("Array vazio")
    
    median_idx = n // 2
    
    return find_kth_smallest(arr, median_idx + 1, pivot_strategy)


def select(arr, k):
    return find_kth_smallest(arr, k)