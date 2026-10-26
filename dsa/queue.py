"""
Custom Queue Implementation for Order Fulfillment
=================================================
DSA Concept: Queue (FIFO - First In, First Out)
Time Complexity:
    - Enqueue:  O(1)
    - Dequeue:  O(1)
    - Peek:     O(1)
    - Is Empty: O(1)
    - Size:     O(1)
Space Complexity: O(n) where n is the number of queued orders

Design:
    - Node-based linked list implementation with `front` and `rear` pointers
    - Guarantees true O(1) constant time enqueue and dequeue operations
    - Accurately models a real-world checkout/fulfillment pipeline:
      The order placed earliest is processed first.
"""

from typing import Any, List, Optional


class QueueNode:
    """Linked list node holding the order payload and pointer to next node."""
    def __init__(self, value: Any):
        self.value: Any = value
        self.next: Optional["QueueNode"] = None


class Queue:
    """
    A custom Generic FIFO Queue implemented via singly linked list nodes
    with dedicated head (front) and tail (rear) references.
    """

    def __init__(self):
        self._front: Optional[QueueNode] = None
        self._rear: Optional[QueueNode] = None
        self._count: int = 0

    def enqueue(self, item: Any) -> None:
        """
        Adds an item to the rear (tail) of the queue.
        Time Complexity: O(1)
        """
        new_node = QueueNode(item)
        if self.is_empty():
            self._front = new_node
            self._rear = new_node
        else:
            assert self._rear is not None
            self._rear.next = new_node
            self._rear = new_node
        self._count += 1

    def dequeue(self) -> Optional[Any]:
        """
        Removes and returns the item at the front (head) of the queue.
        Time Complexity: O(1)
        """
        if self.is_empty():
            return None
        assert self._front is not None
        removed_value = self._front.value
        self._front = self._front.next
        self._count -= 1

        if self._front is None:
            self._rear = None

        return removed_value

    def peek(self) -> Optional[Any]:
        """
        Returns the front item without removing it.
        Time Complexity: O(1)
        """
        if self.is_empty():
            return None
        assert self._front is not None
        return self._front.value

    def is_empty(self) -> bool:
        """Checks if the queue is empty."""
        return self._count == 0

    def size(self) -> int:
        """Returns the number of elements in the queue."""
        return self._count

    def clear(self) -> None:
        """Clears all nodes from the queue."""
        self._front = None
        self._rear = None
        self._count = 0

    def get_items(self) -> List[Any]:
        """
        Traverses nodes from front to rear (FIFO order) and returns them as a list.
        Time Complexity: O(n)
        """
        items: List[Any] = []
        curr = self._front
        while curr is not None:
            items.append(curr.value)
            curr = curr.next
        return items

    def __len__(self) -> int:
        return self._count

    def __repr__(self) -> str:
        front_val = self.peek()
        return f"Queue(size={self._count}, front={front_val})"
