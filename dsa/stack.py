"""
Custom Stack Implementation for Cart Action History & Undo
=========================================================
DSA Concept: Stack (LIFO - Last In, First Out)
Time Complexity:
    - Push:     O(1)
    - Pop:      O(1)
    - Peek:     O(1)
    - Is Empty: O(1)
Space Complexity: O(k) where k is the number of recorded actions (bounded by max history)

Features:
    - Bounded history stack (prevents memory bloat)
    - CartAction record encapsulation
    - Full stack inspection for UI rendering
    - Clear, descriptive human-readable audit messages
"""

from datetime import datetime
from typing import Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class CartAction:
    """
    Encapsulates an atomic cart mutation to enable inverse execution during undo.
    """
    action_type: str  # "ADD_ITEM", "REMOVE_ITEM", "UPDATE_QTY", "CLEAR_CART"
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    prev_qty: int = 0
    new_qty: int = 0
    # Snapshot of all items for bulk actions like CLEAR_CART: {prod_id: (product, qty)}
    snapshot_items: Optional[dict] = None
    description: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def formatted_time(self) -> str:
        return self.timestamp.strftime("%H:%M:%S")


class Stack:
    """
    A custom Generic Stack implementation with LIFO semantics.
    Used in the shopping cart to record user actions and enable 'Undo' functionality.
    """

    def __init__(self, max_size: int = 50):
        self._items: List[Any] = []
        self.max_size: int = max_size

    def push(self, item: Any) -> None:
        """
        Pushes an item onto the top of the stack.
        Time Complexity: O(1)
        """
        if len(self._items) >= self.max_size:
            # Drop oldest action from bottom if stack exceeds capacity
            self._items.pop(0)
        self._items.append(item)

    def pop(self) -> Optional[Any]:
        """
        Removes and returns the item at the top of the stack (most recently added).
        Time Complexity: O(1)
        """
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self) -> Optional[Any]:
        """
        Returns the top item without removing it.
        Time Complexity: O(1)
        """
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        """Checks if the stack has no elements."""
        return len(self._items) == 0

    def size(self) -> int:
        """Returns the number of elements on the stack."""
        return len(self._items)

    def clear(self) -> None:
        """Removes all elements from the stack."""
        self._items.clear()

    def get_items(self) -> List[Any]:
        """
        Returns elements from top of stack to bottom of stack (LIFO order)
        for UI inspection.
        """
        return list(reversed(self._items))

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack(size={len(self._items)}, top={self.peek()})"
