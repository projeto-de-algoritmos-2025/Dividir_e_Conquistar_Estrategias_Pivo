class PivotStrategy:
    
    @staticmethod
    def last_element(arr, left, right, comparisons_counter=None):
        return right
    
    @staticmethod
    def first_element(arr, left, right, comparisons_counter=None):
        return left
    
    @staticmethod
    def middle_element(arr, left, right, comparisons_counter=None):
        return (left + right) // 2
    
    @staticmethod
    def median_of_three(arr, left, right, comparisons_counter=None):
        mid = (left + right) // 2
        
        if comparisons_counter is not None:
            comparisons_counter[0] += 3
        
        candidates = [
            (arr[left], left),
            (arr[mid], mid),
            (arr[right], right)
        ]
        candidates.sort()
        
        return candidates[1][1]
    
    @staticmethod
    def median_of_medians(arr, left, right, comparisons_counter=None):
        if right - left < 5:
            return PivotStrategy._median_of_small_group(
                arr, left, right, comparisons_counter
            )
        
        medians = []
        for i in range(left, right + 1, 5):
            sub_right = min(i + 4, right)
            sub_arr = []
            
            for j in range(i, sub_right + 1):
                sub_arr.append(arr[j])
            
            sub_arr.sort()
            if comparisons_counter is not None:
                comparisons_counter[0] += len(sub_arr)
            
            medians.append(sub_arr[len(sub_arr) // 2])
        
        medians.sort()
        pivot_value = medians[len(medians) // 2]
        
        for i in range(left, right + 1):
            if arr[i] == pivot_value:
                return i
        
        return left
    
    @staticmethod
    def _median_of_small_group(arr, left, right, comparisons_counter=None):
        sub_arr = []
        for i in range(left, right + 1):
            sub_arr.append((arr[i], i))
        
        sub_arr.sort()
        if comparisons_counter is not None:
            comparisons_counter[0] += len(sub_arr)
        
        median_idx = sub_arr[len(sub_arr) // 2][1]
        return median_idx
    
    @staticmethod
    def random_element(arr, left, right, comparisons_counter=None):
        import random
        return random.randint(left, right)


PIVOT_STRATEGIES = {
    'last': PivotStrategy.last_element,
    'first': PivotStrategy.first_element,
    'middle': PivotStrategy.middle_element,
    'median3': PivotStrategy.median_of_three,
    'median_of_medians': PivotStrategy.median_of_medians,
    'random': PivotStrategy.random_element,
}


def get_strategy(name):
    if name not in PIVOT_STRATEGIES:
        available = ', '.join(PIVOT_STRATEGIES.keys())
        raise KeyError(
            f"Estratégia '{name}' não encontrada. "
            f"Estratégias disponíveis: {available}"
        )
    return PIVOT_STRATEGIES[name]