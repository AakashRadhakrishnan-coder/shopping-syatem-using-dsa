"""
Custom Hash Table Implementation with Separate Chaining
======================================================
DSA Concept: Hash Table
Time Complexity:
    - Search / Lookup: O(1) average, O(n) worst-case (all keys collide)
    - Insertion:       O(1) average, O(n) during resize
    - Deletion:        O(1) average, O(n) worst-case
Space Complexity: O(n + m) where n is number of elements and m is bucket capacity

Features:
    - Separate Chaining (bucket array of key-value pairs)
    - Dynamic Resizing & Rehashing when load factor >= 0.75
    - Polynomial rolling hash for string keys
    - Collision tracking and load factor inspection
"""

from typing import Any, List, Optional, Tuple


class HashTable:
    """
    A custom Hash Table implementation for O(1) average time product lookup,
    inventory caching, and discount coupon resolution.
    """

    DEFAULT_CAPACITY = 17  # Prime initial capacity for better hash distribution
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self, initial_capacity: int = DEFAULT_CAPACITY):
        self.capacity: int = initial_capacity
        self.size: int = 0
        # Buckets are lists of [key, value] pairs (separate chaining)
        self.buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(self.capacity)]
        self.collision_count: int = 0

    def _hash(self, key: str) -> int:
        """
        Custom hash function using a polynomial rolling hash algorithm.
        hash = (s[0]*p^0 + s[1]*p^1 + ... + s[k-1]*p^(k-1)) mod capacity
        p = 31 is a commonly chosen prime for ASCII strings.
        """
        p = 31
        hash_value = 0
        p_pow = 1
        for char in str(key):
            hash_value = (hash_value + (ord(char) * p_pow)) % self.capacity
            p_pow = (p_pow * p) % self.capacity
        return hash_value

    @property
    def load_factor(self) -> float:
        """Calculates current load factor = size / capacity."""
        return self.size / self.capacity if self.capacity > 0 else 0.0

    def _resize(self, new_capacity: int) -> None:
        """
        Dynamic resizing: Allocates a new bucket array and rehashes all existing
        key-value pairs. This keeps the load factor below 0.75 and guarantees
        amortized O(1) operations.
        """
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(new_capacity)]
        self.size = 0
        self.collision_count = 0

        # Rehash all entries into the newly sized buckets
        for bucket in old_buckets:
            for key, val in bucket:
                self.put(key, val)

    def put(self, key: str, value: Any) -> None:
        """
        Insert or update a key-value pair in the Hash Table.
        Average Time Complexity: O(1)
        """
        # Check if resize is required
        if (self.size + 1) / self.capacity >= self.LOAD_FACTOR_THRESHOLD:
            # Double capacity plus one to favor odd/prime capacities
            self._resize(self.capacity * 2 + 1)

        index = self._hash(key)
        bucket = self.buckets[index]

        # Check if key already exists in bucket -> update
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        # Key is new: if bucket already had items, this is a collision
        if len(bucket) > 0:
            self.collision_count += 1

        bucket.append((key, value))
        self.size += 1

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve value by key.
        Average Time Complexity: O(1)
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return default

    def contains(self, key: str) -> bool:
        """
        Checks if a key exists in the Hash Table.
        Average Time Complexity: O(1)
        """
        return self.get(key) is not None

    def remove(self, key: str) -> bool:
        """
        Removes a key from the Hash Table.
        Average Time Complexity: O(1)
        Returns True if removed, False if key was not found.
        """
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                self.size -= 1
                return True
        return False

    def keys(self) -> List[str]:
        """Returns list of all keys in the hash table."""
        all_keys = []
        for bucket in self.buckets:
            for key, _ in bucket:
                all_keys.append(key)
        return all_keys

    def values(self) -> List[Any]:
        """Returns list of all values in the hash table."""
        all_vals = []
        for bucket in self.buckets:
            for _, val in bucket:
                all_vals.append(val)
        return all_vals

    def items(self) -> List[Tuple[str, Any]]:
        """Returns list of all (key, value) pairs."""
        all_items = []
        for bucket in self.buckets:
            for key, val in bucket:
                all_items.append((key, val))
        return all_items

    def get_diagnostics(self) -> dict:
        """Returns statistical diagnostics of the hash table for DSA visualization."""
        non_empty_buckets = sum(1 for b in self.buckets if len(b) > 0)
        max_chain = max((len(b) for b in self.buckets), default=0)
        return {
            "capacity": self.capacity,
            "size": self.size,
            "load_factor": round(self.load_factor, 3),
            "non_empty_buckets": non_empty_buckets,
            "empty_buckets": self.capacity - non_empty_buckets,
            "max_chain_length": max_chain,
            "collision_count": self.collision_count,
        }

    def __getitem__(self, key: str) -> Any:
        val = self.get(key)
        if val is None:
            raise KeyError(f"Key '{key}' not found in HashTable.")
        return val

    def __setitem__(self, key: str, value: Any) -> None:
        self.put(key, value)

    def __contains__(self, key: str) -> bool:
        return self.contains(key)

    def __len__(self) -> int:
        return self.size
