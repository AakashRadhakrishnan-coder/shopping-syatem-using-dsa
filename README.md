# 🛒 Smart Shopping Cart (DSA-Powered Streamlit Application)

A complete, high-performance, responsive e-commerce web application built in Python using **Streamlit**. The application meaningfully integrates core **Data Structures and Algorithms (DSA)** and object-oriented design into real, functional e-commerce workflows.

---

## 🚀 Key Features

- **Product Catalog & Search**: Browse 24+ rich sample products across 6 categories (Electronics, Fashion, Home & Kitchen, Books, Fitness, Gourmet Groceries).
- **Search Engine**: Algorithmic searching supporting:
  - **Linear Search**: Multi-field matching across name, description, category, and tags.
  - **Binary Search by Name**: Fast exact/prefix search on alphabetically sorted catalog ($O(\log N)$).
  - **Binary Search Price Range**: Locates lower and upper price bounds in $O(\log N)$ time.
- **Sorting Engine**: Sort products by *Price (Low-to-High / High-to-Low)*, *Rating*, *Name*, and *Stock* using custom-implemented **Merge Sort** ($O(N \log N)$ guaranteed) or **Quick Sort**.
- **Interactive Cart & LIFO Undo**:
  - Add products, adjust quantities with stock validation, and delete items.
  - **Undo Last Action**: Uses a custom **Stack (LIFO)** to record every mutation and revert it in reverse chronological order.
  - Clear entire cart with single-click restoration via snapshot stack frames.
- **Checkout & Promo Discounts**:
  - Customer shipping information and payment method selector.
  - Promo code discounts (`WELCOME10`, `SAVE20`, `FLAT50`, `FREESHIP`, `TECH15`) resolved in **$O(1)$** average time via a custom **Hash Table**.
  - Automatic tiered volume savings and 8% estimated tax calculation.
  - Itemized receipt breakdown and downloadable text invoice (`.txt`).
- **Order Queue & Fulfillment**:
  - Order checkout dispatches orders into a custom **FIFO Queue**.
  - Live fulfillment pipeline: "Process Next Order" dequeues the oldest pending order (FIFO fairness) and updates status to `Delivered`.
- **Session Order History**: Filter and review all orders placed during the session, with itemized receipts and downloadable invoices.
- **DSA Deep Dive Lab**: Interactive telemetry inspector for hash buckets/collisions, sorting speed benchmarks, and Big-O complexity tables.

---

## 🧠 Data Structures & Algorithms Implementation

| DSA Concept | Component | Purpose & Implementation Details | Complexity |
| :--- | :--- | :--- | :--- |
| **Hash Table** | [`dsa/hash_table.py`](file:///c:/Users/Aakash%20R/OneDrive/Desktop/dsap/dsa/hash_table.py) | **Product Lookup & Coupon Codes**: Custom implementation with polynomial rolling hash function, separate chaining (buckets), dynamic resizing/rehashing when load factor $\ge 0.75$, and collision tracking. | $O(1)$ avg lookup, insert, delete |
| **Stack** | [`dsa/stack.py`](file:///c:/Users/Aakash%20R/OneDrive/Desktop/dsap/dsa/stack.py) | **Undo Cart Operations**: LIFO (Last-In, First-Out) structure. Every cart mutation (`ADD_ITEM`, `REMOVE_ITEM`, `UPDATE_QTY`, `CLEAR_CART`) pushes a `CartAction` token. Undoing pops the top token and performs the inverse operation. | $O(1)$ push / pop / peek |
| **Queue** | [`dsa/queue.py`](file:///c:/Users/Aakash%20R/OneDrive/Desktop/dsap/dsa/queue.py) | **Order Fulfillment Pipeline**: FIFO (First-In, First-Out) structure implemented with singly linked list nodes and dedicated `front` and `rear` pointers. Ensures fairness: the earliest placed order is fulfilled first. | $O(1)$ enqueue / dequeue |
| **Sorting** | [`dsa/sorting.py`](file:///c:/Users/Aakash%20R/OneDrive/Desktop/dsap/dsa/sorting.py) | **Price & Rating Ordering**: Custom **Merge Sort** (divide-and-conquer, stable) and **Quick Sort** (partition-based) with custom key comparators. | $O(N \log N)$ |
| **Searching** | [`dsa/searching.py`](file:///c:/Users/Aakash%20R/OneDrive/Desktop/dsap/dsa/searching.py) | **Catalog Querying**: Linear Search for fuzzy multi-attribute matching; Binary Search for prefix matching on sorted names; Binary Search lower/upper bounds for price range budgeting. | $O(\log N)$ binary, $O(N)$ linear |

---

## 📁 Project Folder Structure

```
dsap/
├── dsa/                         # Core Data Structures & Algorithms
│   ├── __init__.py              # Package exports
│   ├── hash_table.py            # Separate chaining Hash Table with dynamic resizing
│   ├── stack.py                 # LIFO Stack and CartAction dataclass
│   ├── queue.py                 # Node-based FIFO Queue for order fulfillment
│   ├── searching.py             # Linear and Binary Search implementations
│   └── sorting.py               # Merge Sort and Quick Sort algorithms
├── models/                      # OOP Data Models & Domain Logic
│   ├── __init__.py              # Package exports
│   ├── product.py               # Product dataclass, sample catalog & coupon dataset
│   ├── cart.py                  # CartItem & ShoppingCart with LIFO undo integration
│   └── order.py                 # Order & OrderManager with FIFO fulfillment & invoice gen
├── utils/                       # UI Utilities & Styling
│   ├── __init__.py              # Package exports
│   └── styles.py                # Glassmorphic, modern responsive CSS theme
├── app.py                       # Main Streamlit web application
├── requirements.txt             # Project dependencies (streamlit)
└── README.md                    # Project documentation & run guide
```

---

## 🛠️ Setup & Run Instructions

### 1. Prerequisites
Ensure Python 3.9+ is installed on your machine.

### 2. Install Dependencies
Open a terminal in the project directory (`dsap`) and run:

```bash
pip install -r requirements.txt
```
*(On Windows with the Python launcher, you can also use `py -m pip install -r requirements.txt`)*

### 3. Launch the Application
Run the Streamlit development server:

```bash
streamlit run app.py
```
*(Or `py -m streamlit run app.py`)*

The web app will automatically open in your default browser at:
`http://localhost:8501`

---

## 🧪 Interactive Walkthrough / Test Scenarios

1. **Browse & Sort**:
   - Select "Price: Low to High" in the sidebar and verify products are sorted starting from the lowest price. Switch between **Merge Sort** and **Quick Sort**.
2. **Search Catalog**:
   - Type "coffee" or "headphones" in the search box. Test both **Linear Search** and **Binary Search by Name**.
3. **Add Items & Undo (Stack LIFO)**:
   - Add 2 units of "AuraPro Noise-Canceling Headphones".
   - Notice the sidebar and cart badge update.
   - Click "Undo Last Action" to see the headphones immediately removed from the cart.
   - Add multiple items, change their quantities, and click "Undo" sequentially to observe the LIFO order of reversion.
4. **Checkout & O(1) Coupon Hash Table**:
   - Add items totaling over ₹100.
   - Go to the **Checkout & Bill** tab.
   - Enter `WELCOME10` or `SAVE20` and click **Apply Code** (instant $O(1)$ Hash Table verification).
   - Review the itemized bill with subtotal, promo savings, and tax.
5. **Place Order & Process Queue (FIFO)**:
   - Click **Confirm Order & Dispatch to Queue**.
   - Navigate to the **Fulfillment Queue** tab.
   - Observe your order at the **Head of the Queue**. Place a second order to see it queued behind the first.
   - Click **Process Next Order (FIFO Dequeue)** to fulfill the oldest order first.
6. **Download Invoice & View History**:
   - Switch to the **Order History** tab, expand your order, and click **Download Official Invoice** to get a clean text receipt.
7. **DSA Deep Dive Lab**:
   - Switch to the **DSA Deep Dive Lab** tab to inspect hash bucket distributions and run benchmarks on 2,400 items.
