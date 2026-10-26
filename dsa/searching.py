"""
Searching Algorithms Implementation
===================================
DSA Concepts:
    1. Linear Search (Multi-field substring & keyword scanning)
       - Time Complexity: O(n * m) where n is list size, m is attribute text length
       - Space Complexity: O(k) for matched results
       - Best for: Unsorted or multi-criteria ad-hoc filters

    2. Binary Search by Name (Divide and Conquer on Sorted Catalog)
       - Time Complexity: O(log n)
       - Space Complexity: O(1) auxiliary
       - Best for: Fast exact or prefix lookup in pre-sorted catalog

    3. Binary Search Price Range (Lower and Upper Bound)
       - Time Complexity: O(log n) to locate range boundaries
       - Space Complexity: O(1) auxiliary
       - Best for: Filtering items between min_price and max_price on price-sorted list
"""

from typing import Any, Callable, List, Optional, Tuple


def linear_search(products: List[Any], query: str) -> List[Any]:
    """
    Scans every product sequentially to check if query matches name,
    category, tags, or description.
    
    Time Complexity: O(n)
    """
    if not query:
        return list(products)

    normalized_query = query.strip().lower()
    matches: List[Any] = []

    for product in products:
        name_match = normalized_query in product.name.lower()
        cat_match = normalized_query in product.category.lower()
        desc_match = normalized_query in product.description.lower()
        tag_match = any(normalized_query in tag.lower() for tag in product.tags)

        if name_match or cat_match or desc_match or tag_match:
            matches.append(product)

    return matches


def binary_search_by_name(sorted_products: List[Any], target_name: str) -> Optional[Any]:
    """
    Performs standard Binary Search on a list of products sorted alphabetically by name.
    
    Time Complexity: O(log n)
    Returns: The matching Product object, or None if not found.
    """
    if not sorted_products or not target_name:
        return None

    target = target_name.strip().lower()
    low = 0
    high = len(sorted_products) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_name = sorted_products[mid].name.lower()

        if mid_name == target:
            return sorted_products[mid]
        elif mid_name < target:
            low = mid + 1
        else:
            high = mid - 1

    return None


def binary_search_prefix_range(sorted_products: List[Any], prefix: str) -> List[Any]:
    """
    Uses binary search to find all products whose names start with the given prefix.
    Assumes `sorted_products` is sorted alphabetically by product name.
    
    Time Complexity: O(log n + k) where k is the number of matching items.
    """
    if not sorted_products or not prefix:
        return list(sorted_products)

    target_prefix = prefix.strip().lower()
    n = len(sorted_products)

    # 1. Binary search for the first product whose name >= prefix
    low, high = 0, n - 1
    first_idx = n
    while low <= high:
        mid = (low + high) // 2
        mid_name = sorted_products[mid].name.lower()
        if mid_name >= target_prefix:
            first_idx = mid
            high = mid - 1
        else:
            low = mid + 1

    # 2. Collect all contiguous products starting with the prefix
    matches = []
    idx = first_idx
    while idx < n and sorted_products[idx].name.lower().startswith(target_prefix):
        matches.append(sorted_products[idx])
        idx += 1

    return matches


def binary_search_price_bounds(
    price_sorted_products: List[Any], min_price: float, max_price: float
) -> List[Any]:
    """
    Finds the sub-array of products that fall inside [min_price, max_price]
    using binary search for lower and upper bounds.
    Assumes `price_sorted_products` is sorted ascending by price.
    
    Time Complexity: O(log n) to locate boundaries + O(k) slicing.
    """
    if not price_sorted_products:
        return []

    n = len(price_sorted_products)

    # Lower bound: first index where product.price >= min_price
    low, high = 0, n - 1
    start_idx = n
    while low <= high:
        mid = (low + high) // 2
        if price_sorted_products[mid].price >= min_price:
            start_idx = mid
            high = mid - 1
        else:
            low = mid + 1

    # Upper bound: last index where product.price <= max_price
    low, high = 0, n - 1
    end_idx = -1
    while low <= high:
        mid = (low + high) // 2
        if price_sorted_products[mid].price <= max_price:
            end_idx = mid
            low = mid + 1
        else:
            high = mid - 1

    if start_idx <= end_idx and start_idx < n and end_idx >= 0:
        return price_sorted_products[start_idx : end_idx + 1]
    return []
