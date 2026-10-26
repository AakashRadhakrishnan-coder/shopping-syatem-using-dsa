"""
Sorting Algorithms Implementation
=================================
DSA Concepts:
    1. Merge Sort (Divide-and-Conquer)
       - Time Complexity: O(n log n) in all cases (Best, Average, Worst)
       - Space Complexity: O(n) auxiliary memory
       - Stability: Stable (preserves relative order of equal keys)
       - Mechanism: Recursively bisects list, sorts each half, and zips them back together.

    2. Quick Sort (In-Place / Partition-based)
       - Time Complexity: O(n log n) average, O(n^2) worst case
       - Space Complexity: O(log n) call stack
       - Mechanism: Selects pivot element, partitions elements into smaller and larger subsets.
"""

from typing import Any, Callable, List


def merge_sort(items: List[Any], key_func: Callable[[Any], Any], reverse: bool = False) -> List[Any]:
    """
    Recursively sorts a list using the Merge Sort algorithm.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        items: List of objects to sort
        key_func: Extraction function returning comparable key (e.g., lambda p: p.price)
        reverse: If True, sorts descending, otherwise ascending
    """
    # Base case: lists of size 0 or 1 are already sorted
    if len(items) <= 1:
        return list(items)

    mid = len(items) // 2
    left_half = merge_sort(items[:mid], key_func, reverse=reverse)
    right_half = merge_sort(items[mid:], key_func, reverse=reverse)

    return _merge(left_half, right_half, key_func, reverse=reverse)


def _merge(
    left: List[Any], right: List[Any], key_func: Callable[[Any], Any], reverse: bool = False
) -> List[Any]:
    """
    Merges two already sorted sub-lists into a single sorted list using two pointers.
    """
    merged: List[Any] = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        left_val = key_func(left[i])
        right_val = key_func(right[j])

        # Comparison determines ascending vs descending
        condition = (left_val >= right_val) if reverse else (left_val <= right_val)

        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append remaining items from either half
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


def quick_sort(items: List[Any], key_func: Callable[[Any], Any], reverse: bool = False) -> List[Any]:
    """
    Sorts a list using the Quick Sort algorithm (Divide-and-Conquer with Pivot).
    
    Time Complexity: O(n log n) average
    Space Complexity: O(n) for recursive partition lists
    """
    if len(items) <= 1:
        return list(items)

    # Choose middle element as pivot to reduce worst-case on already sorted inputs
    pivot_idx = len(items) // 2
    pivot = items[pivot_idx]
    pivot_val = key_func(pivot)

    less = []
    equal = []
    greater = []

    for item in items:
        val = key_func(item)
        if val < pivot_val:
            less.append(item)
        elif val > pivot_val:
            greater.append(item)
        else:
            equal.append(item)

    if reverse:
        # Descending: greater first, then equal, then less
        return quick_sort(greater, key_func, reverse=True) + equal + quick_sort(less, key_func, reverse=True)
    else:
        # Ascending: less first, then equal, then greater
        return quick_sort(less, key_func, reverse=False) + equal + quick_sort(greater, key_func, reverse=False)


def sort_catalog(
    products: List[Any], sort_option: str, algorithm: str = "Merge Sort"
) -> List[Any]:
    """
    Convenience orchestrator for sorting products based on user criteria.
    
    Available sort options:
        - "Price: Low to High": Ascending price
        - "Price: High to Low": Descending price
        - "Rating: High to Low": Descending rating
        - "Name: A to Z": Ascending alphabetical
        - "Stock: High to Low": Descending inventory level
    """
    sort_configs = {
        "Price: Low to High": (lambda p: p.price, False),
        "Price: High to Low": (lambda p: p.price, True),
        "Rating: High to Low": (lambda p: p.rating, True),
        "Name: A to Z": (lambda p: p.name.lower(), False),
        "Stock: High to Low": (lambda p: p.stock, True),
    }

    if sort_option not in sort_configs:
        return list(products)

    key_fn, is_reverse = sort_configs[sort_option]

    if algorithm == "Quick Sort":
        return quick_sort(products, key_fn, reverse=is_reverse)
    # Default to Merge Sort
    return merge_sort(products, key_fn, reverse=is_reverse)
