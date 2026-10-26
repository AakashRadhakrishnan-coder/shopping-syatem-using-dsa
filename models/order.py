"""
Order and OrderManager Models with FIFO Queue Integration
=========================================================
Manages order generation, FIFO queue dispatching, and persistent session history.
DSA Concept: Queue (FIFO - First In, First Out)
    - Orders placed are enqueued at the rear.
    - Fulfillment processing dequeues the oldest order from the front.
"""

from dataclasses import dataclass, field
from datetime import datetime
import random
from typing import Any, Dict, List, Optional
from dsa.queue import Queue


@dataclass
class Order:
    """Represents a finalized customer checkout order."""
    order_id: str
    customer_name: str
    customer_email: str
    delivery_address: str
    payment_method: str
    items: List[Dict[str, Any]]
    subtotal: float
    coupon_discount: float
    tiered_discount: float
    total_discount: float
    tax: float
    shipping: float
    final_total: float
    status: str = "Queued"  # "Queued" -> "Processing" -> "Shipped" -> "Delivered"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status_timeline: List[Dict[str, str]] = field(default_factory=list)

    def __post_init__(self):
        if not self.status_timeline:
            self.status_timeline.append({
                "status": self.status,
                "timestamp": self.created_at.strftime("%H:%M:%S"),
                "note": "Order enqueued into fulfillment queue (FIFO).",
            })

    def advance_status(self, new_status: str, note: str = "") -> None:
        """Transitions order status and records timestamp in history."""
        self.status = new_status
        self.updated_at = datetime.now()
        self.status_timeline.append({
            "status": new_status,
            "timestamp": self.updated_at.strftime("%H:%M:%S"),
            "note": note or f"Status updated to {new_status}.",
        })

    @property
    def formatted_created_at(self) -> str:
        return self.created_at.strftime("%b %d, %Y - %I:%M %p")

    @property
    def total_items_count(self) -> int:
        return sum(item["quantity"] for item in self.items)


class OrderManager:
    """
    Manages the live order processing queue (FIFO) and the persistent
    order history during the user's Streamlit session.
    """

    def __init__(self):
        # FIFO Queue for orders awaiting warehouse fulfillment
        self.order_queue: Queue = Queue()
        # Full chronological audit list for the session
        self.order_history: List[Order] = []

    def create_order(
        self,
        customer_name: str,
        customer_email: str,
        delivery_address: str,
        payment_method: str,
        cart_items: List[Any],
        bill_summary: Dict[str, Any],
    ) -> Order:
        """
        Creates an Order entity, adds it to the FIFO queue, and archives in history.
        
        DSA Complexity: O(1) enqueue
        """
        order_num = random.randint(10000, 99999)
        order_id = f"ORD-{order_num}"

        serialized_items = [
            {
                "product_id": item.product.id,
                "name": item.product.name,
                "category": item.product.category,
                "price": item.product.price,
                "quantity": item.quantity,
                "line_total": item.line_total,
                "emoji": item.product.image_emoji,
                "image_url": item.product.image_url,
            }
            for item in cart_items
        ]

        order = Order(
            order_id=order_id,
            customer_name=customer_name.strip(),
            customer_email=customer_email.strip(),
            delivery_address=delivery_address.strip(),
            payment_method=payment_method,
            items=serialized_items,
            subtotal=bill_summary["subtotal"],
            coupon_discount=bill_summary["coupon_discount"],
            tiered_discount=bill_summary["tiered_discount"],
            total_discount=bill_summary["total_discount"],
            tax=bill_summary["tax"],
            shipping=bill_summary["shipping"],
            final_total=bill_summary["final_total"],
            status="Queued",
        )

        # Enqueue into FIFO queue for warehouse processing
        self.order_queue.enqueue(order)
        # Store in historical session list
        self.order_history.insert(0, order)  # Most recent first in history view

        return order

    def process_next_order(self) -> Optional[Order]:
        """
        Dequeues the head of the FIFO queue and progresses its fulfillment status.
        FIFO Rule: The order that arrived first gets processed first.
        
        DSA Complexity: O(1) dequeue
        """
        if self.order_queue.is_empty():
            return None

        order: Order = self.order_queue.dequeue()
        order.advance_status(
            "Delivered", note="Fulfillment completed. Order dispatched & delivered."
        )
        return order

    def process_all_orders(self) -> List[Order]:
        """
        Empties the FIFO queue, fulfilling all pending customer orders.
        """
        processed_orders = []
        while not self.order_queue.is_empty():
            order = self.process_next_order()
            if order:
                processed_orders.append(order)
        return processed_orders

    def get_queued_orders(self) -> List[Order]:
        """Returns pending orders in FIFO order (front to rear)."""
        return self.order_queue.get_items()

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        for o in self.order_history:
            if o.order_id == order_id:
                return o
        return None

    @staticmethod
    def generate_text_invoice(order: Order) -> str:
        """Generates a formatted plain-text receipt / invoice for downloading."""
        divider = "=" * 54
        thin_divider = "-" * 54
        lines = [
            divider,
            "           SMART SHOPPING CART - OFFICIAL INVOICE",
            divider,
            f"Order ID:       {order.order_id}",
            f"Date & Time:    {order.formatted_created_at}",
            f"Status:         {order.status.upper()}",
            f"Customer:       {order.customer_name}",
            f"Email:          {order.customer_email}",
            f"Delivery To:    {order.delivery_address}",
            f"Payment Method: {order.payment_method}",
            thin_divider,
            f"{'Item':<28} {'Qty':<5} {'Price':<10} {'Total':<10}",
            thin_divider,
        ]

        for itm in order.items:
            short_name = itm['name'][:26]
            lines.append(
                f"{short_name:<28} {itm['quantity']:<5} ₹{itm['price']:<9.2f} ₹{itm['line_total']:<9.2f}"
            )

        lines.extend([
            thin_divider,
            f"{'Subtotal:':<44} ₹{order.subtotal:,.2f}",
            f"{'Promotional Discount:':<44} -₹{order.coupon_discount:,.2f}",
            f"{'Loyalty / Tiered Savings:':<44} -₹{order.tiered_discount:,.2f}",
            f"{'Total Discounts:':<44} -₹{order.total_discount:,.2f}",
            f"{'Estimated Tax (8%):':<44} ₹{order.tax:,.2f}",
            f"{'Shipping Fee:':<44} ₹{order.shipping:,.2f}",
            divider,
            f"{'FINAL TOTAL PAID:':<44} ₹{order.final_total:,.2f}",
            divider,
            "     Thank you for shopping with Smart Shopping Cart!",
            "             We appreciate your business!",
            divider,
        ])
        return "\n".join(lines)
