"""
Shopping Cart Model with LIFO Undo Stack Integration
====================================================
Manages the user's active shopping cart session.
Integrates:
    - Stack for undoing cart actions (LIFO - Last In First Out)
    - HashTable for O(1) coupon validation
    - OOP encapsulation of CartItem and ShoppingCart state
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from dsa.stack import Stack, CartAction
from dsa.hash_table import HashTable
from models.product import Product


@dataclass
class CartItem:
    """Represents a product item line in the shopping cart."""
    product: Product
    quantity: int

    @property
    def line_total(self) -> float:
        return self.quantity * self.product.price

    @property
    def formatted_line_total(self) -> str:
        return f"₹{self.line_total:,.2f}"


class ShoppingCart:
    """
    Manages active cart items, calculates itemized totals, applies coupons,
    and maintains an Undo Stack (LIFO) for reverting operations.
    """

    def __init__(self, coupon_table: HashTable, max_undo_history: int = 50):
        # Maps product_id -> CartItem
        self._items: Dict[str, CartItem] = {}
        # Custom LIFO Stack for undoing cart modifications
        self.undo_stack: Stack = Stack(max_size=max_undo_history)
        # Custom HashTable storing promo discount definitions
        self.coupon_table: HashTable = coupon_table
        self.applied_coupon_code: Optional[str] = None

    @property
    def items(self) -> Dict[str, CartItem]:
        return self._items

    def get_items_list(self) -> List[CartItem]:
        """Returns list of active CartItem instances."""
        return list(self._items.values())

    def total_items_count(self) -> int:
        """Calculates total quantity of all items in cart."""
        return sum(item.quantity for item in self._items.values())

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def get_item(self, product_id: str) -> Optional[CartItem]:
        return self._items.get(product_id)

    # -------------------------------------------------------------
    # CART MUTATIONS WITH STACK RECORDING
    # -------------------------------------------------------------

    def add_item(self, product: Product, quantity: int = 1, record: bool = True) -> Tuple[bool, str]:
        """
        Adds a product to the cart or increments its quantity.
        Validates inventory stock.
        Records CartAction onto the LIFO Stack if record=True.
        """
        if quantity <= 0:
            return False, "Quantity must be greater than zero."

        current_qty = self._items[product.id].quantity if product.id in self._items else 0
        new_qty = current_qty + quantity

        if new_qty > product.stock:
            available = product.stock - current_qty
            if available <= 0:
                return False, f"Sorry, '{product.name}' is already at maximum available stock ({product.stock})."
            return False, f"Cannot add {quantity} units. Only {available} more units available in stock."

        self._items[product.id] = CartItem(product=product, quantity=new_qty)

        if record:
            action = CartAction(
                action_type="ADD_ITEM",
                product_id=product.id,
                product_name=product.name,
                prev_qty=current_qty,
                new_qty=new_qty,
                description=f"Added {quantity}x '{product.name}' (Total: {new_qty})",
            )
            self.undo_stack.push(action)

        return True, f"Added {quantity}x '{product.name}' to cart."

    def remove_item(self, product_id: str, record: bool = True) -> Tuple[bool, str]:
        """
        Removes an entire product line from the cart.
        Records CartAction onto LIFO Stack with previous quantity.
        """
        if product_id not in self._items:
            return False, "Item not found in cart."

        item = self._items[product_id]
        prev_qty = item.quantity
        product = item.product
        product_name = product.name

        del self._items[product_id]

        if record:
            action = CartAction(
                action_type="REMOVE_ITEM",
                product_id=product_id,
                product_name=product_name,
                prev_qty=prev_qty,
                new_qty=0,
                snapshot_items={product_id: (product, prev_qty)},
                description=f"Removed '{product_name}' ({prev_qty} units) from cart",
            )
            self.undo_stack.push(action)

        return True, f"Removed '{product_name}' from cart."

    def update_quantity(self, product_id: str, new_quantity: int, record: bool = True) -> Tuple[bool, str]:
        """
        Updates the exact quantity of an existing item in the cart.
        If new_quantity is 0, removes the item.
        """
        if product_id not in self._items:
            return False, "Item not found in cart."

        item = self._items[product_id]
        product = item.product
        prev_qty = item.quantity

        if new_quantity == prev_qty:
            return True, "No change in quantity."

        if new_quantity <= 0:
            return self.remove_item(product_id, record=record)

        if new_quantity > product.stock:
            return False, f"Cannot set quantity to {new_quantity}. Maximum stock is {product.stock}."

        self._items[product_id].quantity = new_quantity

        if record:
            action = CartAction(
                action_type="UPDATE_QTY",
                product_id=product_id,
                product_name=product.name,
                prev_qty=prev_qty,
                new_qty=new_quantity,
                description=f"Updated '{product.name}' quantity from {prev_qty} to {new_quantity}",
            )
            self.undo_stack.push(action)

        return True, f"Updated quantity of '{product.name}' to {new_quantity}."

    def clear(self, record: bool = True) -> Tuple[bool, str]:
        """
        Clears all items from the cart.
        Takes a full snapshot before clearing and pushes onto LIFO Stack so user can undo!
        """
        if self.is_empty():
            return False, "Cart is already empty."

        # Take full snapshot of cart
        snapshot = {
            pid: (item.product, item.quantity)
            for pid, item in self._items.items()
        }
        cleared_count = len(self._items)

        self._items.clear()

        if record:
            action = CartAction(
                action_type="CLEAR_CART",
                snapshot_items=snapshot,
                description=f"Cleared cart ({cleared_count} items emptied)",
            )
            self.undo_stack.push(action)

        return True, f"Cart cleared ({cleared_count} items)."

    # -------------------------------------------------------------
    # LIFO STACK UNDO EXECUTION
    # -------------------------------------------------------------

    def undo_last_action(self) -> Tuple[bool, str]:
        """
        Pops the most recent CartAction from the LIFO Stack and executes
        the exact inverse operation to restore previous state.
        
        Time Complexity: O(1) for item actions, O(k) for restored bulk clear.
        """
        if self.undo_stack.is_empty():
            return False, "No previous actions to undo."

        action: CartAction = self.undo_stack.pop()

        if action.action_type == "ADD_ITEM":
            # Inverse of ADD: revert quantity back to prev_qty
            if action.product_id is None:
                return False, "Corrupted action record."

            if action.prev_qty == 0:
                # Was newly added -> remove completely
                if action.product_id in self._items:
                    del self._items[action.product_id]
                msg = f"Undone: Removed '{action.product_name}' which was newly added."
            else:
                # Had existing quantity -> revert to prev_qty
                if action.product_id in self._items:
                    self._items[action.product_id].quantity = action.prev_qty
                msg = f"Undone: Reverted '{action.product_name}' quantity back to {action.prev_qty}."
            return True, msg

        elif action.action_type == "REMOVE_ITEM":
            # Inverse of REMOVE: restore product with prev_qty
            if action.product_id is None:
                return False, "Corrupted action record."

            if action.snapshot_items and action.product_id in action.snapshot_items:
                product, _ = action.snapshot_items[action.product_id]
                self._items[action.product_id] = CartItem(product=product, quantity=action.prev_qty)
                return True, f"Undone: Restored '{action.product_name}' ({action.prev_qty} units) to cart."
            return False, "Cannot undo removal without product object."

        elif action.action_type == "UPDATE_QTY":
            # Inverse of UPDATE_QTY: revert to prev_qty
            if action.product_id is None:
                return False, "Corrupted action record."

            if action.prev_qty == 0:
                if action.product_id in self._items:
                    del self._items[action.product_id]
            else:
                if action.product_id in self._items:
                    self._items[action.product_id].quantity = action.prev_qty
            return True, f"Undone: Reverted '{action.product_name}' quantity from {action.new_qty} back to {action.prev_qty}."

        elif action.action_type == "CLEAR_CART":
            # Inverse of CLEAR_CART: restore all snapshot items
            if action.snapshot_items:
                for pid, (product, qty) in action.snapshot_items.items():
                    self._items[pid] = CartItem(product=product, quantity=qty)
                return True, f"Undone: Restored {len(action.snapshot_items)} items to cart."
            return False, "Snapshot data unavailable to undo clear."

        return False, f"Unknown action type '{action.action_type}'."

    def undo_with_catalog(self, catalog_hashtable: HashTable) -> Tuple[bool, str]:
        """
        Enhanced undo handler that resolves product references from the catalog HashTable
        for REMOVE_ITEM actions.
        """
        if self.undo_stack.is_empty():
            return False, "No previous actions to undo."

        action: CartAction = self.undo_stack.pop()

        if action.action_type == "ADD_ITEM":
            assert action.product_id is not None
            if action.prev_qty == 0:
                self._items.pop(action.product_id, None)
                return True, f"Undone: Removed '{action.product_name}' (added recently)."
            else:
                if action.product_id in self._items:
                    self._items[action.product_id].quantity = action.prev_qty
                return True, f"Undone: Reverted '{action.product_name}' quantity to {action.prev_qty}."

        elif action.action_type == "REMOVE_ITEM":
            assert action.product_id is not None
            # Retrieve product from action snapshot or catalog HashTable in O(1)
            product = None
            if action.snapshot_items and action.product_id in action.snapshot_items:
                product, _ = action.snapshot_items[action.product_id]
            if product is None:
                product = catalog_hashtable.get(action.product_id)
            if product:
                self._items[action.product_id] = CartItem(product=product, quantity=action.prev_qty)
                return True, f"Undone: Restored '{action.product_name}' ({action.prev_qty} units) to cart."
            return False, f"Could not find product '{action.product_id}' in catalog."

        elif action.action_type == "UPDATE_QTY":
            assert action.product_id is not None
            product = catalog_hashtable.get(action.product_id)
            if action.prev_qty == 0:
                self._items.pop(action.product_id, None)
            else:
                if product:
                    self._items[action.product_id] = CartItem(product=product, quantity=action.prev_qty)
            return True, f"Undone: Reverted '{action.product_name}' quantity to {action.prev_qty}."

        elif action.action_type == "CLEAR_CART":
            if action.snapshot_items:
                for pid, (product, qty) in action.snapshot_items.items():
                    self._items[pid] = CartItem(product=product, quantity=qty)
                return True, f"Undone: Restored {len(action.snapshot_items)} items into cart."
            return False, "Snapshot data missing."

        return False, "Unrecognized action."

    # -------------------------------------------------------------
    # BILL & DISCOUNT COMPUTATION
    # -------------------------------------------------------------

    def apply_coupon(self, code: str) -> Tuple[bool, str]:
        """
        Validates coupon code using the custom HashTable in O(1) time.
        """
        clean_code = code.strip().upper()
        coupon = self.coupon_table.get(clean_code)

        if not coupon:
            return False, f"Coupon code '{clean_code}' is invalid."

        subtotal = sum(item.line_total for item in self._items.values())
        if subtotal < coupon["min_cart"]:
            return False, f"Coupon '{clean_code}' requires a minimum subtotal of ₹{coupon['min_cart']:.2f} (Current: ₹{subtotal:.2f})."

        self.applied_coupon_code = clean_code
        return True, f"Coupon '{clean_code}' applied successfully! {coupon['description']}."

    def remove_coupon(self) -> None:
        self.applied_coupon_code = None

    def calculate_bill(
        self,
        tax_rate: float = 0.08,
        standard_shipping: float = 9.99,
        free_shipping_threshold: float = 120.0,
    ) -> Dict[str, Any]:
        """
        Computes complete itemized financial breakdown:
        Subtotal, Promo Coupon Discount, Tiered Loyalty Savings, Shipping, Tax, and Final Total.
        """
        subtotal = sum(item.line_total for item in self._items.values())
        item_count = sum(item.quantity for item in self._items.values())

        if subtotal <= 0:
            return {
                "subtotal": 0.0,
                "item_count": 0,
                "coupon_code": None,
                "coupon_discount": 0.0,
                "tiered_discount": 0.0,
                "total_discount": 0.0,
                "shipping": 0.0,
                "taxable_amount": 0.0,
                "tax": 0.0,
                "tax_rate": tax_rate,
                "final_total": 0.0,
                "is_empty": True,
            }

        # 1. Tiered Volume Discount (automatic rewards)
        tiered_discount = 0.0
        if subtotal >= 300.0:
            tiered_discount = 25.0  # ₹25 off orders >= ₹300
        elif subtotal >= 150.0:
            tiered_discount = 10.0  # ₹10 off orders >= ₹150

        # 2. Promo Coupon Discount via HashTable lookup
        coupon_discount = 0.0
        shipping_discount = 0.0
        coupon_info = None

        if self.applied_coupon_code:
            coupon_info = self.coupon_table.get(self.applied_coupon_code)
            if coupon_info:
                if coupon_info["type"] == "percentage":
                    coupon_discount = (coupon_info["value"] / 100.0) * subtotal
                elif coupon_info["type"] == "fixed":
                    coupon_discount = min(coupon_info["value"], subtotal)
                elif coupon_info["type"] == "shipping":
                    shipping_discount = standard_shipping

        # Total combined item discount (cannot exceed subtotal)
        item_discounts = min(subtotal, coupon_discount + tiered_discount)

        # 3. Shipping Calculation
        if subtotal >= free_shipping_threshold or shipping_discount > 0:
            shipping = 0.0
        else:
            shipping = standard_shipping

        # 4. Tax Calculation (8% on post-discount subtotal)
        taxable_amount = max(0.0, subtotal - item_discounts)
        tax = round(taxable_amount * tax_rate, 2)

        # 5. Grand Total
        final_total = round(taxable_amount + tax + shipping, 2)

        return {
            "subtotal": round(subtotal, 2),
            "item_count": item_count,
            "coupon_code": self.applied_coupon_code,
            "coupon_info": coupon_info,
            "coupon_discount": round(coupon_discount, 2),
            "tiered_discount": round(tiered_discount, 2),
            "total_discount": round(item_discounts, 2),
            "shipping": round(shipping, 2),
            "shipping_waived": shipping == 0.0,
            "taxable_amount": round(taxable_amount, 2),
            "tax": tax,
            "tax_rate": tax_rate,
            "final_total": final_total,
            "is_empty": False,
        }
