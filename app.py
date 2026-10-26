"""
Smart Shopping Cart - Streamlit Application
===========================================
Enterprise-grade e-commerce application demonstrating core Data Structures & Algorithms:
    - Hash Table: O(1) Product lookup, inventory mapping & coupon resolution
    - Stack: LIFO Undo mechanism for all cart mutations
    - Queue: FIFO Warehouse fulfillment pipeline
    - Sorting: Merge Sort & Quick Sort algorithms for dynamic price and rating ordering
    - Searching: Linear Search & Binary Search for fast catalog querying

Author: Google Antigravity Agent
"""

import time
from typing import List, Optional
import streamlit as st

# Custom DSA Modules
from dsa.hash_table import HashTable
from dsa.stack import CartAction
from dsa.searching import linear_search, binary_search_by_name, binary_search_price_bounds
from dsa.sorting import merge_sort, quick_sort, sort_catalog

# Models & Business Logic
from models.product import (
    Product,
    SAMPLE_PRODUCTS,
    AVAILABLE_COUPONS,
    build_catalog_hashtable,
    build_coupon_hashtable,
)
from models.cart import ShoppingCart, CartItem
from models.order import Order, OrderManager
from utils.styles import CUSTOM_CSS


# -----------------------------------------------------------------------------
# 1. STREAMLIT CONFIGURATION & CUSTOM STYLES
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart Shopping Cart",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.html(CUSTOM_CSS)


# -----------------------------------------------------------------------------
# 2. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
def initialize_session_state():
    """Initializes persistent session objects across Streamlit reruns."""
    if "catalog_ht" not in st.session_state:
        st.session_state.catalog_ht = build_catalog_hashtable()

    if "coupon_ht" not in st.session_state:
        st.session_state.coupon_ht = build_coupon_hashtable()

    if "cart" not in st.session_state:
        st.session_state.cart = ShoppingCart(
            coupon_table=st.session_state.coupon_ht,
            max_undo_history=50,
        )

    if "order_manager" not in st.session_state:
        st.session_state.order_manager = OrderManager()

    if "toast_msg" not in st.session_state:
        st.session_state.toast_msg = None

    if "active_category" not in st.session_state:
        st.session_state.active_category = "All Categories"


initialize_session_state()

cart: ShoppingCart = st.session_state.cart
catalog_ht: HashTable = st.session_state.catalog_ht
coupon_ht: HashTable = st.session_state.coupon_ht
order_manager: OrderManager = st.session_state.order_manager


# -----------------------------------------------------------------------------
# 3. TOP APP HEADER
# -----------------------------------------------------------------------------
st.html(
    """
    <div class="app-header-container">
        <div>
            <h1 class="app-title">🛒 Smart Shopping Cart</h1>
            <p class="app-subtitle">
                Discover curated lifestyle essentials, high-performance tech, apparel & gourmet treats.
            </p>
        </div>
    </div>
    """
)


# -----------------------------------------------------------------------------
# 4. SIDEBAR CONTROLS & CART STATUS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛒 Active Cart Status")
    
    # Cart Quick Summary with zero clipping
    cart_items_count = cart.total_items_count()
    bill_summary = cart.calculate_bill()
    
    st.html(
        f"""
        <div class="sidebar-cart-card">
            <div class="sidebar-cart-row">
                <span class="sidebar-cart-label">Total Items</span>
                <span class="sidebar-cart-val">{cart_items_count} pcs</span>
            </div>
            <div class="sidebar-cart-row">
                <span class="sidebar-cart-label">Current Total</span>
                <span class="sidebar-cart-val sidebar-total-val">₹{bill_summary['final_total']:,.2f}</span>
            </div>
        </div>
        """
    )

    # Undo Button in Sidebar (Internal LIFO Stack)
    next_undo = cart.undo_stack.peek()
    undo_label = f"↩️ Undo: {next_undo.description[:24]}..." if next_undo else "↩️ Undo Last Action"
    
    if st.button(undo_label, disabled=cart.undo_stack.is_empty(), use_container_width=True, type="secondary"):
        success, message = cart.undo_with_catalog(catalog_ht)
        if success:
            st.toast(message, icon="✅")
        else:
            st.toast(message, icon="⚠️")
        st.rerun()

    if st.button("🗑️ Clear Entire Cart", disabled=cart.is_empty(), use_container_width=True):
        success, message = cart.clear(record=True)
        if success:
            st.toast(message, icon="ℹ️")
        st.rerun()

    st.markdown("---")
    st.markdown("### 🔍 Filters & Options")

    # Search query
    search_query = st.text_input("Search catalog", placeholder="Search by name, tag, category...")
    
    # Internal algorithmic search engine mode
    search_mode = "Linear Search (Multi-field substring)"

    # Product Category Filter
    all_categories = ["All Categories", "Electronics", "Fashion", "Home & Kitchen", "Books", "Fitness", "Groceries"]
    cur_cat = st.session_state.get("active_category", "All Categories")
    cat_idx = all_categories.index(cur_cat) if cur_cat in all_categories else 0
    selected_category = st.selectbox("Product Category", all_categories, index=cat_idx, key="sidebar_category_select")
    if selected_category != st.session_state.active_category:
        st.session_state.active_category = selected_category
        st.rerun()

    # Sorting options
    st.markdown("### 🔀 Sorting Controls")
    sort_option = st.selectbox(
        "Sort Catalog By",
        [
            "Price: Low to High",
            "Price: High to Low",
            "Rating: High to Low",
            "Name: A to Z",
            "Stock: High to Low",
        ],
    )

    # Internal sorting algorithm (Merge Sort O(n log n))
    chosen_sort_algo = "Merge Sort"


# -----------------------------------------------------------------------------
# 5. CORE CATALOG FILTERING & SORTING ENGINE (DSA POWERED INTERNALLY)
# -----------------------------------------------------------------------------
def get_filtered_and_sorted_products() -> List[Product]:
    """
    Applies DSA searching, category filtering, price filtering,
    and DSA sorting to the product catalog internally.
    """
    # 1. Base list of all products from Hash Table values
    all_products: List[Product] = catalog_ht.values()

    # 2. Category filtering using active_category
    cur_cat = st.session_state.get("active_category", "All Categories")
    if cur_cat != "All Categories":
        filtered = [p for p in all_products if p.category.lower() == cur_cat.lower()]
    else:
        filtered = list(all_products)

    # 3. Search Algorithm Execution
    if search_query.strip():
        filtered = linear_search(filtered, search_query)

    # 4. Sorting algorithm (Merge Sort)
    sorted_result = sort_catalog(filtered, sort_option=sort_option, algorithm=chosen_sort_algo)
    return sorted_result


# -----------------------------------------------------------------------------
# 6. MAIN APPLICATION TABS
# -----------------------------------------------------------------------------
tab_catalog, tab_cart, tab_checkout, tab_queue, tab_history = st.tabs(
    [
        "🛍️ Product Catalog",
        f"🛒 Cart ({cart.total_items_count()})",
        "💳 Checkout & Bill",
        f"📦 Fulfillment Pipeline ({order_manager.order_queue.size()})",
        f"📜 Order History ({len(order_manager.order_history)})",
    ]
)


# =============================================================================
# TAB 1: PRODUCT CATALOG
# =============================================================================
with tab_catalog:
    # 1. Quick Category Filter Pills
    category_list = ["All Categories", "Electronics", "Fashion", "Home & Kitchen", "Books", "Fitness", "Groceries"]
    category_labels = {
        "All Categories": "✨ All Items",
        "Electronics": "💻 Tech & Audio",
        "Fashion": "🧥 Apparel",
        "Home & Kitchen": "☕ Home & Kitchen",
        "Books": "📚 Books",
        "Fitness": "🏋️ Fitness",
        "Groceries": "🥑 Groceries",
    }
    
    chip_cols = st.columns(len(category_list))
    active_cat = st.session_state.get("active_category", "All Categories")
    for c_i, cat in enumerate(category_list):
        with chip_cols[c_i]:
            is_active = (cat == active_cat)
            if st.button(
                category_labels.get(cat, cat),
                key=f"cat_pill_{c_i}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
            ):
                st.session_state.active_category = cat
                st.rerun()

    st.html("<div style='margin-bottom: 8px;'></div>")

    # Catalog Items
    products_to_show = get_filtered_and_sorted_products()
    st.caption(f"Showing **{len(products_to_show)}** products in **{active_cat}**")

    if not products_to_show:
        st.html(
            """
            <div class="empty-state-card">
                <div class="empty-icon">🔍</div>
                <h3>No matching products found</h3>
                <p>Try clearing your search query or selecting a different category from the filter pills above.</p>
            </div>
            """
        )
    else:
        # Display in a clean 3-column responsive grid
        cols_per_row = 3
        for i in range(0, len(products_to_show), cols_per_row):
            batch = products_to_show[i : i + cols_per_row]
            cols = st.columns(cols_per_row)

            for col_idx, product in enumerate(batch):
                with cols[col_idx]:
                    # Stock badge formatting
                    if product.stock > 10:
                        stock_html = f"<span class='product-stock stock-in'>● In Stock ({product.stock})</span>"
                    elif product.stock > 0:
                        stock_html = f"<span class='product-stock stock-low'>● Low Stock ({product.stock} left)</span>"
                    else:
                        stock_html = "<span class='product-stock stock-out'>● Out of Stock</span>"

                    badge_html = f"<div class='product-badge'>{product.badge}</div>" if product.badge else ""

                    # High-definition image container with realistic photo & smooth zoom
                    if product.image_url:
                        image_html = (
                            f'<div class="product-image-container">'
                            f'<img src="{product.image_url}" alt="{product.name}" loading="lazy" '
                            f'onerror="this.parentElement.innerHTML=\'<div class=product-emoji-fallback>{product.image_emoji}</div>\'" />'
                            f'{badge_html}'
                            f'</div>'
                        )
                    else:
                        image_html = (
                            f'<div class="product-image-container">'
                            f'<div class="product-emoji-fallback">{product.image_emoji}</div>'
                            f'{badge_html}'
                            f'</div>'
                        )

                    # Card body with glassmorphic typography and pricing
                    card_html = (
                        f'<div class="product-card">'
                        f'{image_html}'
                        f'<div class="product-card-body">'
                        f'<div class="product-category-tag">{product.category} • {product.id}</div>'
                        f'<div class="product-title" title="{product.name}">{product.name}</div>'
                        f'<div class="product-desc" title="{product.description}">{product.description}</div>'
                        f'<div class="product-rating">★ <b>{product.rating}</b> <span class="product-reviews_count">({product.reviews_count:,} reviews)</span></div>'
                        f'<div class="product-price-row"><span class="product-price">{product.formatted_price}</span>{stock_html}</div>'
                        f'</div>'
                        f'</div>'
                    )
                    st.html(card_html)

                    # Controls: Quantity input & Add to Cart button
                    c_qty, c_btn = st.columns([1, 2])
                    with c_qty:
                        qty_input = st.number_input(
                            f"Qty_{product.id}",
                            min_value=1,
                            max_value=max(1, product.stock),
                            value=1,
                            step=1,
                            key=f"qty_{product.id}",
                            label_visibility="collapsed",
                        )
                    with c_btn:
                        btn_disabled = not product.is_in_stock
                        btn_text = "Add to Cart 🛒" if product.is_in_stock else "Out of Stock"
                        if st.button(
                            btn_text,
                            key=f"add_{product.id}",
                            disabled=btn_disabled,
                            use_container_width=True,
                            type="primary" if product.is_in_stock else "secondary",
                        ):
                            # Add item and push mutation onto LIFO Stack
                            success, msg = cart.add_item(product, quantity=qty_input, record=True)
                            if success:
                                st.toast(msg, icon="🛒")
                            else:
                                st.toast(msg, icon="⚠️")
                            st.rerun()

                    # Spacing between rows
                    st.html("<div style='margin-bottom: 24px;'></div>")


# =============================================================================
# TAB 2: SHOPPING CART & LIFO UNDO TIMELINE
# =============================================================================
with tab_cart:
    st.markdown("### 🛒 Active Shopping Cart")

    if cart.is_empty():
        st.html(
            """
            <div class="empty-state-card">
                <div class="empty-icon">🛒</div>
                <h3>Your cart is empty</h3>
                <p>
                    Explore our product catalog and click "Add to Cart". Any action you make can be easily undone at any time!
                </p>
            </div>
            """
        )
    else:
        # Cart Header Actions
        col_c_info, col_c_undo, col_c_clear = st.columns([3, 2, 1])
        with col_c_info:
            st.markdown(f"**{cart_items_count} items** currently in your cart.")
        with col_c_undo:
            if st.button("↩️ Undo Last Action", use_container_width=True, type="secondary"):
                success, msg = cart.undo_with_catalog(catalog_ht)
                if success:
                    st.toast(msg, icon="🔄")
                else:
                    st.toast(msg, icon="⚠️")
                st.rerun()
        with col_c_clear:
            if st.button("🗑️ Clear", use_container_width=True):
                success, msg = cart.clear(record=True)
                if success:
                    st.toast(msg, icon="🗑️")
                st.rerun()

        st.markdown("---")

        # Itemized Cart List with Realistic Product Photos
        cart_items_list = cart.get_items_list()
        for item in cart_items_list:
            p = item.product
            c_img, c_detail, c_stepper, c_line_total, c_del = st.columns([1, 4, 3, 2, 1])

            with c_img:
                if p.image_url:
                    st.html(
                        f"""
                        <div class="cart-thumb-box">
                            <img src="{p.image_url}" alt="{p.name}" 
                                 onerror="this.parentElement.innerHTML='<div class=product-emoji-fallback style=\\'font-size:1.8rem;height:100%;\\'>{p.image_emoji}</div>'" />
                        </div>
                        """
                    )
                else:
                    st.html(f"<div class='cart-item-emoji'>{p.image_emoji}</div>")

            with c_detail:
                st.markdown(f"**{p.name}**")
                st.caption(f"Category: {p.category} | Unit Price: **{p.formatted_price}**")

            with c_stepper:
                # Stepper adjustment
                col_minus, col_q_display, col_plus = st.columns([1, 1, 1])
                with col_minus:
                    if st.button("➖", key=f"minus_{p.id}", use_container_width=True):
                        cart.update_quantity(p.id, item.quantity - 1, record=True)
                        st.rerun()
                with col_q_display:
                    st.html(
                        f"<div class='cart-qty-display'>{item.quantity}</div>"
                    )
                with col_plus:
                    plus_disabled = item.quantity >= p.stock
                    if st.button("➕", key=f"plus_{p.id}", disabled=plus_disabled, use_container_width=True):
                        cart.update_quantity(p.id, item.quantity + 1, record=True)
                        st.rerun()

            with c_line_total:
                st.html(
                    f"<div class='cart-line-total'>{item.formatted_line_total}</div>"
                )

            with c_del:
                if st.button("🗑️", key=f"del_{p.id}", use_container_width=True):
                    cart.remove_item(p.id, record=True)
                    st.toast(f"Removed {p.name}", icon="🗑️")
                    st.rerun()

            st.html("<hr style='margin: 10px 0; border: none; border-top: 1px solid rgba(99,102,241,0.12);'>")

        # Cart Subtotal Banner
        sub_col1, sub_col2 = st.columns([2, 1])
        with sub_col1:
            st.markdown(f"#### Subtotal: :indigo[₹{bill_summary['subtotal']:,.2f}] ({cart_items_count} items)")
        with sub_col2:
            st.info("💡 Ready to place your order? Head to the **💳 Checkout & Bill** tab.")

    # -------------------------------------------------------------------------
    # RECENT CART ACTIVITY (AUDIT TRAIL)
    # -------------------------------------------------------------------------
    st.markdown("### 🕒 Recent Cart Activity")
    st.caption("Audit trail of recent cart actions. Click 'Undo' to revert your most recent change.")

    stack_actions: List[CartAction] = cart.undo_stack.get_items()
    if not stack_actions:
        st.info("No recent cart actions recorded.")
    else:
        for idx, act in enumerate(stack_actions):
            is_top = idx == 0
            badge = "Latest Action (Next to Undo)" if is_top else f"Action #{len(stack_actions) - idx}"
            top_border = "border-left: 4px solid #4f46e5;" if is_top else "border-left: 3px solid #cbd5e1;"
            badge_color = "#4f46e5" if is_top else "#64748b"

            st.html(
                f'<div class="timeline-item" style="{top_border}">'
                f'<div class="timeline-title">'
                f'<span style="color: {badge_color}; font-weight: 700;">[{badge}]</span> {act.description}'
                f'</div>'
                f'<div class="timeline-subtitle">'
                f'Status: <b>{act.action_type.replace("_", " ").title()}</b> | Recorded at: <b>{act.formatted_time}</b>'
                f'</div>'
                f'</div>'
            )


# =============================================================================
# TAB 3: CHECKOUT & ITEMIZED BILL
# =============================================================================
with tab_checkout:
    st.markdown("### 💳 Checkout & Order Finalization")

    if cart.is_empty():
        st.warning("Your cart is empty. Add at least one item before proceeding to checkout.")
    else:
        col_form, col_bill = st.columns([1, 1], gap="large")

        with col_form:
            st.markdown("#### 1. Customer Shipping Details")
            c_name = st.text_input("Full Name", value="Alex Rivera", placeholder="John Doe")
            c_email = st.text_input("Email Address", value="alex.rivera@example.com", placeholder="alex@example.com")
            c_address = st.text_area("Delivery Address", value="742 Evergreen Terrace, Springfield, OR 97477", height=80)
            
            c_payment = st.selectbox(
                "Payment Method",
                ["Credit / Debit Card (Stripe)", "Apple Pay / Google Pay", "PayPal Express", "Cash on Delivery"],
            )

            st.markdown("#### 2. Promo / Coupon Code")
            col_cp_input, col_cp_btn = st.columns([2, 1])
            with col_cp_input:
                coupon_code_input = st.text_input("Enter Promo Code", value="WELCOME10", label_visibility="collapsed")
            with col_cp_btn:
                if st.button("Apply Code", use_container_width=True):
                    ok, msg = cart.apply_coupon(coupon_code_input)
                    if ok:
                        st.toast(msg, icon="🎉")
                    else:
                        st.toast(msg, icon="⚠️")
                    st.rerun()

            if cart.applied_coupon_code:
                st.success(f"Active Coupon: **{cart.applied_coupon_code}** applied!")
                if st.button("Remove Coupon", key="remove_coupon_btn"):
                    cart.remove_coupon()
                    st.rerun()

            # Coupon cheat-sheet expander
            with st.expander("🎟️ Available Coupon Codes Cheat Sheet", expanded=False):
                st.caption("Available promotional discount codes:")
                for c_code, c_det in AVAILABLE_COUPONS.items():
                    st.markdown(f"- **`{c_code}`**: {c_det['description']} *(Min cart: ₹{c_det['min_cart']})*")

        with col_bill:
            st.markdown("#### 3. Itemized Receipt & Summary")
            bill = cart.calculate_bill()

            # Render styled invoice box with non-clipping amounts
            discount_html = ""
            if bill["coupon_discount"] > 0:
                discount_html += f"""
                <div class="invoice-row invoice-badge-green">
                    <span>Coupon ({bill['coupon_code']}):</span>
                    <span style="white-space: nowrap;">-₹{bill['coupon_discount']:,.2f}</span>
                </div>
                """
            if bill["tiered_discount"] > 0:
                discount_html += f"""
                <div class="invoice-row invoice-badge-green">
                    <span>Tiered Loyalty Savings:</span>
                    <span style="white-space: nowrap;">-₹{bill['tiered_discount']:,.2f}</span>
                </div>
                """

            shipping_display = "FREE" if bill["shipping"] == 0.0 else f"₹{bill['shipping']:,.2f}"

            st.html(
                f"""
                <div class="invoice-card">
                    <div style="text-align: center; font-weight: 700; margin-bottom: 12px; font-size: 1.05rem; color: #4f46e5;">
                        🧾 SMART SHOPPING CART INVOICE
                    </div>
                    <div style="border-bottom: 1px dashed rgba(99,102,241,0.20); margin-bottom: 12px;"></div>
                    <div class="invoice-row">
                        <span>Items Subtotal ({bill['item_count']} units):</span>
                        <span style="white-space: nowrap;">₹{bill['subtotal']:,.2f}</span>
                    </div>
                    {discount_html}
                    <div class="invoice-row">
                        <span>Standard Shipping:</span>
                        <span style="white-space: nowrap;">{shipping_display}</span>
                    </div>
                    <div class="invoice-row">
                        <span>Estimated Tax (8%):</span>
                        <span style="white-space: nowrap;">₹{bill['tax']:,.2f}</span>
                    </div>
                    <div class="invoice-row-total">
                        <span>FINAL GRAND TOTAL:</span>
                        <span style="white-space: nowrap; font-size: 1.35rem; color: #4f46e5;">₹{bill['final_total']:,.2f}</span>
                    </div>
                </div>
                """
            )

            st.html("<br>")

            # Confirm and Place Order Button
            if st.button("🚀 Confirm Order & Dispatch", type="primary", use_container_width=True):
                # Validate inputs
                if not c_name.strip() or not c_email.strip() or not c_address.strip():
                    st.error("Please fill in all shipping details before placing the order.")
                else:
                    new_order = order_manager.create_order(
                        customer_name=c_name,
                        customer_email=c_email,
                        delivery_address=c_address,
                        payment_method=c_payment,
                        cart_items=cart.get_items_list(),
                        bill_summary=bill,
                    )
                    # Clear cart after placing order
                    cart.clear(record=False)
                    cart.remove_coupon()

                    st.balloons()
                    st.success(
                        f"Order **{new_order.order_id}** placed successfully!"
                    )
                    st.rerun()


# =============================================================================
# TAB 4: ORDER FULFILLMENT PIPELINE
# =============================================================================
with tab_queue:
    st.markdown("### 📦 Order Fulfillment Pipeline")
    st.html(
        """
        <div class="custom-alert custom-alert-info">
            <span>Orders are processed in the sequence they were confirmed. Earliest submitted orders are dispatched first.</span>
        </div>
        """
    )

    queued_orders = order_manager.get_queued_orders()

    # Queue controls
    col_q_act1, col_q_act2, col_q_stat = st.columns([2, 2, 3])
    with col_q_act1:
        if st.button("⚡ Process Next Order", disabled=len(queued_orders) == 0, use_container_width=True, type="primary"):
            dequeued = order_manager.process_next_order()
            if dequeued:
                st.toast(f"Fulfilled Order {dequeued.order_id} (Customer: {dequeued.customer_name})", icon="📦")
            st.rerun()

    with col_q_act2:
        if st.button("🚀 Process All Queued Orders", disabled=len(queued_orders) == 0, use_container_width=True):
            all_proc = order_manager.process_all_orders()
            st.toast(f"Fulfilled all {len(all_proc)} pending orders!", icon="🎉")
            st.rerun()

    with col_q_stat:
        st.markdown(f"**Orders Pending Fulfillment:** `{len(queued_orders)}`")

    st.markdown("---")

    if not queued_orders:
        st.html(
            """
            <div class="empty-state-card">
                <div class="empty-icon">📦 ✨</div>
                <h3>All orders have been fulfilled!</h3>
                <p>There are currently no orders waiting in the fulfillment pipeline. Place a new order from Checkout.</p>
            </div>
            """
        )
    else:
        # Live visual representation of the Queue from Front to Rear
        for idx, ord_item in enumerate(queued_orders):
            is_head = idx == 0
            position_tag = "🌟 Next to Dispatch" if is_head else f"Position #{idx + 1}"
            border_style = "border-left: 4px solid #10b981;" if is_head else "border-left: 3px solid #94a3b8;"
            head_text_color = "#059669" if is_head else "#64748b"
            st.html(
                f'<div class="timeline-item timeline-item-queue" style="{border_style}; margin-bottom: 16px;">'
                f'<div class="timeline-title" style="display: flex; justify-content: space-between;">'
                f'<span><b style="color: {head_text_color};"> [{position_tag}]</b> Order ID: <b>{ord_item.order_id}</b></span>'
                f'<span style="color: #4f46e5; font-weight: 700; white-space: nowrap;">₹{ord_item.final_total:,.2f}</span>'
                f'</div>'
                f'<div class="timeline-subtitle" style="margin-top: 4px;">'
                f'Customer: <b>{ord_item.customer_name}</b> ({ord_item.customer_email}) | '
                f'Items: <b>{ord_item.total_items_count} pcs</b> | '
                f'Confirmed at: <b>{ord_item.created_at.strftime("%H:%M:%S")}</b> | '
                f'Status: <span style="color: #d97706; font-weight: 600;">{ord_item.status}</span>'
                f'</div>'
                f'</div>'
            )


# =============================================================================
# TAB 5: ORDER HISTORY
# =============================================================================
with tab_history:
    st.markdown("### 📜 Session Order History")

    all_history = order_manager.order_history

    if not all_history:
        st.info("No orders placed yet during this session. Check out items to build your order history.")
    else:
        # Status Filter for history
        h_filter = st.radio("Filter History by Status", ["All", "Queued", "Delivered"], horizontal=True)

        displayed_history = all_history
        if h_filter != "All":
            displayed_history = [o for o in all_history if o.status.lower() == h_filter.lower()]

        for ord_obj in displayed_history:
            status_color = "#34d399" if ord_obj.status == "Delivered" else "#fbbf24"

            with st.expander(
                f"Order {ord_obj.order_id} • {ord_obj.customer_name} • ₹{ord_obj.final_total:,.2f} • [{ord_obj.status}]",
                expanded=False,
            ):
                c_h1, c_h2 = st.columns([2, 1])

                with c_h1:
                    st.markdown(f"**Customer:** {ord_obj.customer_name} (`{ord_obj.customer_email}`)")
                    st.markdown(f"**Address:** {ord_obj.delivery_address}")
                    st.markdown(f"**Payment:** {ord_obj.payment_method}")
                    st.markdown(f"**Date:** {ord_obj.formatted_created_at}")

                    st.markdown("##### Purchased Items:")
                    for itm in ord_obj.items:
                        img_url = itm.get("image_url", "")
                        img_tag = (
                            f'<img src="{img_url}" style="width:36px;height:36px;border-radius:8px;object-fit:cover;border:1px solid rgba(99,102,241,0.2);" '
                            f'onerror="this.style.display=\'none\'" />'
                            if img_url else f'<span style="font-size:1.3rem;">{itm.get("emoji", "📦")}</span>'
                        )
                        st.html(
                            f"""
                            <div style="display:flex;align-items:center;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(0,0,0,0.04);">
                                <div style="display:flex;align-items:center;gap:10px;">
                                    {img_tag}
                                    <div>
                                        <div style="font-weight:600;font-size:0.88rem;color:#0f172a;">{itm['name']}</div>
                                        <div style="font-size:0.75rem;color:#64748b;">Qty: {itm['quantity']} × ₹{itm['price']:,.2f}</div>
                                    </div>
                                </div>
                                <div style="font-weight:700;color:#4f46e5;font-size:0.92rem;">₹{itm['line_total']:,.2f}</div>
                            </div>
                            """
                        )

                with c_h2:
                    status_color_light = "#059669" if ord_obj.status == "Delivered" else "#d97706"
                    st.html(
                        f"""
                        <div class="order-summary-box">
                            <div>Subtotal: <b>₹{ord_obj.subtotal:,.2f}</b></div>
                            <div>Discount: <b style="color: #059669;">-₹{ord_obj.total_discount:,.2f}</b></div>
                            <div>Shipping: <b>₹{ord_obj.shipping:,.2f}</b></div>
                            <div>Tax: <b>₹{ord_obj.tax:,.2f}</b></div>
                            <hr style="margin: 6px 0; border-color: rgba(99,102,241,0.10);">
                            <div class="order-total-highlight">Total: ₹{ord_obj.final_total:,.2f}</div>
                            <div style="margin-top: 6px;">Status: <span style="color: {status_color_light}; font-weight: 700;">{ord_obj.status}</span></div>
                        </div>
                        """
                    )

                    # Download text receipt button
                    invoice_text = OrderManager.generate_text_invoice(ord_obj)
                    st.download_button(
                        label="📄 Download Official Invoice",
                        data=invoice_text,
                        file_name=f"Invoice_{ord_obj.order_id}.txt",
                        mime="text/plain",
                        key=f"dl_{ord_obj.order_id}",
                        use_container_width=True,
                    )
