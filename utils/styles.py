"""
Custom Styling and Theming for Smart Shopping Cart
=================================================
Premium light-only glassmorphism design system featuring:
- Multi-layered frosted glass surfaces with backdrop-filter blur
- Clean ambient light gradient mesh background
- Modern responsive product cards with high-definition photography
- Glassmorphic search bar, category chips, and filter controls
- Sleek cart with realistic photo thumbnails and custom steppers
- Polished gradient buttons with smooth micro-interactions
- Strict light-only enforcement with dark mode removal
"""

CUSTOM_CSS = """
<style>
/* ===================== GOOGLE FONTS IMPORT ===================== */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ===================== GLOBAL RESET & ROOT VARIABLES ===================== */
:root {
    --primary: #4f46e5;
    --primary-hover: #4338ca;
    --primary-light: #eef2ff;
    --accent: #8b5cf6;
    --accent-pink: #ec4899;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-muted: #64748b;
    --bg-page: #f8faff;
    --glass-bg: rgba(255, 255, 255, 0.76);
    --glass-bg-hover: rgba(255, 255, 255, 0.92);
    --glass-border: rgba(255, 255, 255, 0.9);
    --glass-border-subtle: rgba(99, 102, 241, 0.12);
    --glass-shadow: 0 10px 30px -5px rgba(99, 102, 241, 0.08), 0 1px 3px rgba(0, 0, 0, 0.03);
    --glass-shadow-hover: 0 20px 40px -10px rgba(99, 102, 241, 0.18), 0 4px 16px rgba(0, 0, 0, 0.04);
    --radius-sm: 8px;
    --radius-md: 14px;
    --radius-lg: 20px;
    --radius-xl: 24px;
    --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: var(--font-main) !important;
    color: var(--text-primary) !important;
}

/* ===================== STRICT LIGHT MODE ENFORCEMENT ===================== */
/* Force light mode regardless of OS, browser, or Streamlit theme preferences */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
[data-testid="stHeader"],
.main .block-container,
.stApp {
    color-scheme: light !important;
    background-color: var(--bg-page) !important;
    color: var(--text-primary) !important;
}

/* Atmospheric light gradient mesh on main canvas */
[data-testid="stAppViewContainer"] {
    background: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.07) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(236, 72, 153, 0.05) 0px, transparent 45%),
        radial-gradient(at 50% 100%, rgba(56, 189, 248, 0.06) 0px, transparent 50%),
        linear-gradient(180deg, #f8faff 0%, #f1f5f9 100%) !important;
    background-attachment: fixed !important;
}

/* Completely suppress dark mode overrides */
@media (prefers-color-scheme: dark) {
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], section[data-testid="stSidebar"] > div, .stApp {
        color-scheme: light !important;
        background-color: #f8faff !important;
        color: #0f172a !important;
    }
    p, span, div, h1, h2, h3, h4, h5, h6, label {
        color: #0f172a !important;
    }
}

/* Hide theme toggles in Streamlit toolbar */
[data-testid="stToolbar"] button[title*="theme" i],
[data-testid="stToolbar"] button[aria-label*="theme" i] {
    display: none !important;
}

/* Streamlit Header minimal */
[data-testid="stHeader"] {
    background: rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid rgba(99, 102, 241, 0.08) !important;
}

/* Main Container spacing */
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 1380px !important;
}

/* ===================== FLOATING GLASS HEADER ===================== */
.app-header-container {
    background: rgba(255, 255, 255, 0.78);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.95);
    border-radius: var(--radius-xl);
    padding: 26px 36px;
    margin-bottom: 24px;
    box-shadow: 
        0 20px 40px -15px rgba(99, 102, 241, 0.12),
        0 1px 3px rgba(0, 0, 0, 0.03),
        inset 0 1px 2px rgba(255, 255, 255, 0.9);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 18px;
    position: relative;
    overflow: hidden;
}

.app-header-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #4f46e5, #8b5cf6, #ec4899, #38bdf8);
}

.app-title {
    font-size: 2.25rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 40%, #7c3aed 80%, #db2777 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin: 0 !important;
    letter-spacing: -0.8px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.app-subtitle {
    color: var(--text-muted) !important;
    font-size: 0.95rem;
    margin-top: 6px;
    margin-bottom: 0;
    font-weight: 400;
    line-height: 1.5;
}

/* ===================== DSA BADGE PILLS ===================== */
.dsa-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.dsa-pill:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.dsa-pill-hash {
    background: rgba(59, 130, 246, 0.12);
    color: #2563eb !important;
    border: 1px solid rgba(59, 130, 246, 0.3);
}

.dsa-pill-stack {
    background: rgba(139, 92, 246, 0.12);
    color: #7c3aed !important;
    border: 1px solid rgba(139, 92, 246, 0.3);
}

.dsa-pill-queue {
    background: rgba(16, 185, 129, 0.12);
    color: #059669 !important;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.dsa-pill-sort {
    background: rgba(245, 158, 11, 0.12);
    color: #d97706 !important;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.dsa-pill-search {
    background: rgba(236, 72, 153, 0.12);
    color: #db2777 !important;
    border: 1px solid rgba(236, 72, 153, 0.3);
}

/* ===================== MODERN GLASS PRODUCT CARDS ===================== */
.product-card {
    background: rgba(255, 255, 255, 0.78);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.95);
    border-radius: var(--radius-lg);
    padding: 0;
    margin-bottom: 16px;
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 
        0 10px 30px -5px rgba(99, 102, 241, 0.06),
        0 1px 4px rgba(0, 0, 0, 0.02),
        inset 0 1px 1px rgba(255, 255, 255, 0.95);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 440px;
    overflow: hidden;
    position: relative;
}

.product-card:hover {
    transform: translateY(-8px);
    background: rgba(255, 255, 255, 0.92);
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 
        0 24px 48px -12px rgba(99, 102, 241, 0.20),
        0 4px 16px rgba(0, 0, 0, 0.04),
        inset 0 1px 1px rgba(255, 255, 255, 1);
}

.product-image-container {
    width: 100%;
    height: 220px;
    overflow: hidden;
    position: relative;
    background: #f1f5f9;
    border-bottom: 1px solid rgba(226, 232, 240, 0.6);
}

.product-image-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    display: block;
}

.product-card:hover .product-image-container img {
    transform: scale(1.08);
}

.product-emoji-fallback {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3.8rem;
    background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
}

.product-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.9), rgba(139, 92, 246, 0.9));
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.35);
    color: #ffffff !important;
    font-size: 0.70rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 9999px;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    text-transform: uppercase;
    z-index: 2;
}

.product-card-body {
    padding: 20px 22px 22px 22px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.product-category-tag {
    font-size: 0.72rem;
    font-weight: 700;
    color: #4f46e5 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.product-title {
    font-size: 1.08rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    margin-bottom: 6px !important;
    line-height: 1.4 !important;
    height: 44px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.product-desc {
    font-size: 0.84rem !important;
    color: #64748b !important;
    margin-bottom: 14px !important;
    line-height: 1.5 !important;
    height: 40px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.product-rating {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.85rem;
    color: #f59e0b !important;
    margin-bottom: 14px;
    font-weight: 700;
}

.product-reviews_count {
    color: #94a3b8 !important;
    font-size: 0.76rem;
    font-weight: 500;
}

.product-price-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: auto;
    padding-top: 14px;
    border-top: 1px solid rgba(226, 232, 240, 0.8);
    overflow: visible !important;
    gap: 8px;
}

.product-price {
    font-size: 1.42rem !important;
    font-weight: 800 !important;
    color: #4338ca !important;
    display: inline-block !important;
    line-height: 1.3 !important;
    letter-spacing: 0px !important;
    white-space: nowrap !important;
    overflow: visible !important;
    padding: 2px 2px !important;
}

.product-stock {
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 9999px;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

.stock-in {
    background: rgba(16, 185, 129, 0.10);
    color: #059669 !important;
    border: 1px solid rgba(16, 185, 129, 0.25);
}

.stock-low {
    background: rgba(245, 158, 11, 0.10);
    color: #d97706 !important;
    border: 1px solid rgba(245, 158, 11, 0.25);
}

.stock-out {
    background: rgba(239, 68, 68, 0.10);
    color: #dc2626 !important;
    border: 1px solid rgba(239, 68, 68, 0.25);
}

/* ===================== CATEGORY FILTER CHIPS ===================== */
.category-chips-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 20px;
}

.category-chip {
    padding: 8px 18px;
    border-radius: 9999px;
    font-size: 0.84rem;
    font-weight: 600;
    color: #475569;
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.category-chip:hover {
    transform: translateY(-1px);
    color: #4f46e5;
    background: rgba(255, 255, 255, 0.95);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.12);
}

.category-chip-active {
    background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
    color: #ffffff !important;
    border-color: #4f46e5 !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
}

/* ===================== MODERN CART ITEM CARD ===================== */
.cart-item-card {
    background: rgba(255, 255, 255, 0.78);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.95);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin-bottom: 12px;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.05);
    transition: all 0.25s ease;
}

.cart-item-card:hover {
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.10);
    border-color: rgba(99, 102, 241, 0.25);
}

.cart-thumb-box {
    width: 68px;
    height: 68px;
    border-radius: 12px;
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(99, 102, 241, 0.15);
    background: #f1f5f9;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.cart-thumb-box img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.cart-line-total {
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    color: #4f46e5 !important;
    padding-top: 6px;
    letter-spacing: -0.3px;
}

.cart-qty-display {
    text-align: center;
    font-weight: 800 !important;
    font-size: 1.15rem !important;
    color: #0f172a !important;
    padding-top: 6px;
}

/* ===================== INVOICE & CHECKOUT STYLING ===================== */
.invoice-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px dashed rgba(99, 102, 241, 0.35);
    border-radius: var(--radius-lg);
    padding: 26px;
    font-family: var(--font-mono) !important;
    font-size: 0.90rem;
    color: #334155 !important;
    margin-top: 16px;
    box-shadow: 0 10px 30px -5px rgba(99, 102, 241, 0.08);
}

.invoice-header {
    text-align: center;
    font-weight: 800;
    font-size: 1.1rem;
    color: #4f46e5 !important;
    margin-bottom: 14px;
    letter-spacing: -0.2px;
}

.invoice-row {
    display: flex;
    justify-content: space-between;
    padding: 7px 0;
    color: #475569 !important;
}

.invoice-row-total {
    display: flex;
    justify-content: space-between;
    padding: 16px 0 6px 0;
    border-top: 2px dashed rgba(99, 102, 241, 0.28);
    font-size: 1.3rem;
    font-weight: 800;
    color: #4f46e5 !important;
}

.invoice-badge-green {
    color: #059669 !important;
    font-weight: 600;
}

/* ===================== TIMELINE & STACK FRAMES ===================== */
.timeline-item {
    border-left: 3px solid #818cf8;
    padding: 14px 18px;
    margin-bottom: 12px;
    position: relative;
    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    transition: all 0.2s ease;
}

.timeline-item:hover {
    transform: translateX(4px);
    background: rgba(255, 255, 255, 0.90);
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.10);
}

.timeline-item-queue {
    border-left-color: #10b981;
}

.timeline-title {
    font-weight: 700;
    font-size: 0.90rem;
    color: #0f172a !important;
}

.timeline-subtitle {
    font-size: 0.78rem;
    color: #64748b !important;
    margin-top: 4px;
}

/* ===================== CUSTOM ALERTS ===================== */
.custom-alert {
    padding: 14px 20px;
    border-radius: var(--radius-md);
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.90rem;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
}

.custom-alert-info {
    background: rgba(238, 242, 255, 0.85);
    border: 1px solid rgba(99, 102, 241, 0.25);
    color: #3730a3 !important;
}

.custom-alert-success {
    background: rgba(236, 253, 245, 0.85);
    border: 1px solid rgba(16, 185, 129, 0.25);
    color: #065f46 !important;
}

.custom-alert-warning {
    background: rgba(254, 243, 199, 0.85);
    border: 1px solid rgba(245, 158, 11, 0.25);
    color: #92400e !important;
}

/* ===================== BUTTONS OVERRIDES ===================== */
div.stButton > button {
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px !important;
    padding: 0.55rem 1.25rem !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    border: 1px solid rgba(99, 102, 241, 0.22) !important;
    background: rgba(255, 255, 255, 0.85) !important;
    color: #4338ca !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    background: rgba(238, 242, 255, 0.95) !important;
    border-color: rgba(99, 102, 241, 0.4) !important;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.15) !important;
    color: #312e81 !important;
}

div.stButton > button:active {
    transform: translateY(0px) !important;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #8b5cf6 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 20px -3px rgba(79, 70, 229, 0.4) !important;
}

div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4338ca 0%, #4f46e5 50%, #7c3aed 100%) !important;
    box-shadow: 0 10px 28px -3px rgba(79, 70, 229, 0.55) !important;
    transform: translateY(-2px) !important;
    color: #ffffff !important;
}

/* ===================== TABS OVERRIDES ===================== */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255, 255, 255, 0.70) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    padding: 6px;
    border-radius: var(--radius-lg);
    border: 1px solid rgba(255, 255, 255, 0.95);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    margin-bottom: 24px;
}

.stTabs [data-baseweb="tab"] {
    height: 46px;
    border-radius: var(--radius-md) !important;
    padding: 0 20px !important;
    font-weight: 600 !important;
    font-size: 0.90rem !important;
    color: #64748b !important;
    transition: all 0.25s ease !important;
    border: none !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #4f46e5 !important;
    background: rgba(99, 102, 241, 0.08) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.35) !important;
}

/* ===================== SIDEBAR GLASS ===================== */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.72) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.9) !important;
    box-shadow: 4px 0 24px rgba(99, 102, 241, 0.05) !important;
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

/* ===================== INPUTS & SELECTBOXES ===================== */
div[data-baseweb="input"],
div[data-baseweb="select"] > div,
div[data-baseweb="base-input"] {
    background: rgba(255, 255, 255, 0.85) !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid rgba(203, 213, 225, 0.8) !important;
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
    transition: all 0.2s ease !important;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.02) !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.18) !important;
}

/* ===================== SIDEBAR CART STATUS CARD ===================== */
.sidebar-cart-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.95);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.06);
    margin-bottom: 14px;
}

.sidebar-cart-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
}

.sidebar-cart-row:not(:last-child) {
    border-bottom: 1px dashed rgba(99, 102, 241, 0.15);
}

.sidebar-cart-label {
    font-size: 0.80rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    white-space: nowrap;
}

.sidebar-cart-val {
    font-size: 1.15rem;
    font-weight: 800;
    color: #0f172a;
    white-space: nowrap !important;
    overflow: visible !important;
}

.sidebar-total-val {
    color: #4f46e5 !important;
    font-size: 1.25rem !important;
}

/* ===================== METRIC CARDS ===================== */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.75) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.95) !important;
    border-radius: var(--radius-md) !important;
    padding: 12px 14px !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.05) !important;
    overflow: visible !important;
    min-width: 0 !important;
}

[data-testid="stMetricValue"] {
    color: #4f46e5 !important;
    font-weight: 800 !important;
    font-size: 1.25rem !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.3 !important;
}

[data-testid="stMetricValue"] > div {
    overflow: visible !important;
    text-overflow: clip !important;
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.4px !important;
    font-size: 0.76rem !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    line-height: 1.2 !important;
}

/* ===================== EXPANDER STYLING ===================== */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.70) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-radius: var(--radius-md) !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    border: 1px solid rgba(226, 232, 240, 0.8) !important;
}

/* ===================== EMPTY STATE CARDS ===================== */
.empty-state-card {
    text-align: center;
    padding: 54px 30px;
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: var(--radius-xl);
    border: 2px dashed rgba(99, 102, 241, 0.22);
    box-shadow: 0 10px 30px -5px rgba(99, 102, 241, 0.05);
    margin: 20px 0;
}

.empty-state-card .empty-icon {
    font-size: 4rem;
    margin-bottom: 14px;
}

.empty-state-card h3 {
    color: #0f172a !important;
    margin-bottom: 8px !important;
    font-weight: 800 !important;
    font-size: 1.4rem !important;
}

.empty-state-card p {
    color: #64748b !important;
    max-width: 460px;
    margin: 0 auto;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* ===================== ORDER SUMMARY BOX ===================== */
.order-summary-box {
    background: rgba(255, 255, 255, 0.78);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 18px;
    border-radius: var(--radius-md);
    border: 1px solid rgba(255, 255, 255, 0.95);
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.05);
}

.order-summary-box div {
    color: #334155 !important;
    padding: 3px 0;
    white-space: nowrap !important;
    overflow: visible !important;
}

.order-total-highlight {
    font-size: 1.2rem !important;
    color: #4f46e5 !important;
    font-weight: 800 !important;
    white-space: nowrap !important;
    overflow: visible !important;
}

/* ===================== SCROLLBAR ===================== */
::-webkit-scrollbar {
    width: 7px;
    height: 7px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.22);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.40);
}

/* ===================== SUBTLE ANIMATIONS ===================== */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

.product-card {
    animation: fadeInUp 0.4s ease-out both;
}

.product-card:nth-child(2) { animation-delay: 0.05s; }
.product-card:nth-child(3) { animation-delay: 0.10s; }
</style>
"""
