"""
Product Model and Sample Catalog
================================
Encapsulates product entity data and sample catalog initialization.
Products are stored in a custom HashTable for O(1) key-based lookup by ID.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from dsa.hash_table import HashTable


@dataclass
class Product:
    """Represents a product in the ecommerce inventory."""
    id: str
    name: str
    category: str
    price: float
    rating: float
    reviews_count: int
    stock: int
    image_emoji: str
    badge: Optional[str]
    description: str
    tags: List[str] = field(default_factory=list)
    image_url: str = ""

    @property
    def formatted_price(self) -> str:
        return f"₹{self.price:,.2f}"

    @property
    def is_in_stock(self) -> bool:
        return self.stock > 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "rating": self.rating,
            "reviews_count": self.reviews_count,
            "stock": self.stock,
            "image_emoji": self.image_emoji,
            "badge": self.badge,
            "description": self.description,
            "tags": self.tags,
            "image_url": self.image_url,
        }


# Sample dataset of 24 realistic products with high-resolution photography
SAMPLE_PRODUCTS: List[Product] = [
    # Electronics
    Product(
        id="PROD-101",
        name="AuraPro Noise-Canceling Headphones",
        category="Electronics",
        price=199.99,
        rating=4.8,
        reviews_count=1240,
        stock=25,
        image_emoji="🎧",
        badge="Bestseller",
        description="Premium active noise cancellation with 40-hour battery life and spatial audio.",
        tags=["audio", "wireless", "bluetooth", "noise canceling"],
        image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-102",
        name="Titan Ultra Smartwatch v3",
        category="Electronics",
        price=249.50,
        rating=4.7,
        reviews_count=890,
        stock=18,
        image_emoji="⌚",
        badge="Popular",
        description="AMOLED always-on display, ECG, blood oxygen monitor, and 7-day battery life.",
        tags=["smartwatch", "fitness", "wearable", "health"],
        image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-103",
        name="MechVibe RGB Mechanical Keyboard",
        category="Electronics",
        price=89.99,
        rating=4.6,
        reviews_count=640,
        stock=30,
        image_emoji="⌨️",
        badge="Sale",
        description="Hot-swappable linear switches, per-key RGB backlighting, and aluminum chassis.",
        tags=["keyboard", "gaming", "mechanical", "rgb"],
        image_url="https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-104",
        name="Lumix 4K Ultra Webcam",
        category="Electronics",
        price=79.00,
        rating=4.5,
        reviews_count=430,
        stock=15,
        image_emoji="📹",
        badge=None,
        description="Crystal clear 4K 60FPS streaming webcam with dual noise-reduction microphones.",
        tags=["camera", "webcam", "streaming", "video"],
        image_url="https://images.unsplash.com/photo-1588702547919-26089e690ecc?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-105",
        name="SoundPulse Waterproof Speaker",
        category="Electronics",
        price=49.99,
        rating=4.6,
        reviews_count=980,
        stock=40,
        image_emoji="🔊",
        badge=None,
        description="IPX7 waterproof rating, 360-degree surround sound, and 16-hour playtime.",
        tags=["speaker", "audio", "waterproof", "portable"],
        image_url="https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=600&q=80",
    ),
    # Fashion
    Product(
        id="PROD-201",
        name="UrbanFit Merino Wool Hoodie",
        category="Fashion",
        price=68.50,
        rating=4.9,
        reviews_count=520,
        stock=22,
        image_emoji="🧥",
        badge="Bestseller",
        description="100% breathable organic merino wool hoodie tailored for all-weather comfort.",
        tags=["hoodie", "wool", "winter", "apparel"],
        image_url="https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-202",
        name="AeroGlide Performance Sneakers",
        category="Fashion",
        price=119.00,
        rating=4.7,
        reviews_count=815,
        stock=14,
        image_emoji="👟",
        badge="Trending",
        description="Cloud-cushioned running sneakers featuring breathable mesh and grip outsoles.",
        tags=["shoes", "sneakers", "running", "sportswear"],
        image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-203",
        name="Classic Polarized Aviator Sunglasses",
        category="Fashion",
        price=42.00,
        rating=4.4,
        reviews_count=310,
        stock=35,
        image_emoji="🕶️",
        badge=None,
        description="UV400 scratch-resistant polarized lenses with lightweight titanium wire frames.",
        tags=["sunglasses", "eyewear", "accessories", "summer"],
        image_url="https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-204",
        name="Heritage Genuine Leather Backpack",
        category="Fashion",
        price=135.00,
        rating=4.8,
        reviews_count=420,
        stock=12,
        image_emoji="🎒",
        badge="Handcrafted",
        description="Full-grain cowhide leather backpack with padded 16-inch laptop compartment.",
        tags=["backpack", "leather", "travel", "bags"],
        image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80",
    ),
    # Home & Kitchen
    Product(
        id="PROD-301",
        name="Barista Touch Espresso Machine",
        category="Home & Kitchen",
        price=449.99,
        rating=4.9,
        reviews_count=1680,
        stock=8,
        image_emoji="☕",
        badge="Top Rated",
        description="15-bar Italian pump espresso machine with automatic steam milk texturing wand.",
        tags=["coffee", "espresso", "kitchen", "appliance"],
        image_url="https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-302",
        name="CrispAir 6-in-1 Digital Air Fryer",
        category="Home & Kitchen",
        price=95.00,
        rating=4.7,
        reviews_count=1320,
        stock=20,
        image_emoji="🍳",
        badge="Sale",
        description="5.8-quart family capacity with 360 rapid air circulation and touch presets.",
        tags=["air fryer", "cooking", "kitchen", "healthy"],
        image_url="https://images.unsplash.com/photo-1585515320310-259814833e62?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-303",
        name="Ceramic Pour-Over Kettle & Dripper Set",
        category="Home & Kitchen",
        price=34.99,
        rating=4.5,
        reviews_count=290,
        stock=25,
        image_emoji="🫖",
        badge=None,
        description="Gooseneck precision flow kettle and artisanal ceramic filter cone dripper.",
        tags=["coffee", "tea", "pour-over", "ceramic"],
        image_url="https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-304",
        name="Ergonomic Memory Foam Lumbar Pillow",
        category="Home & Kitchen",
        price=29.99,
        rating=4.6,
        reviews_count=770,
        stock=45,
        image_emoji="🛋️",
        badge=None,
        description="High-density memory foam cushion with cooling gel insert for desk chairs.",
        tags=["pillow", "ergonomic", "office", "comfort"],
        image_url="https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?auto=format&fit=crop&w=600&q=80",
    ),
    # Books & Learning
    Product(
        id="PROD-401",
        name="Introduction to Algorithms & Data Structures",
        category="Books",
        price=54.99,
        rating=4.9,
        reviews_count=2100,
        stock=50,
        image_emoji="📚",
        badge="Bestseller",
        description="The definitive handbook covering trees, graphs, sorting, dynamic programming, and complexity.",
        tags=["algorithms", "programming", "dsa", "computer science"],
        image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-402",
        name="Designing Data-Intensive Applications",
        category="Books",
        price=48.00,
        rating=4.9,
        reviews_count=1890,
        stock=32,
        image_emoji="📖",
        badge="Must Read",
        description="In-depth principles of distributed systems, storage engines, and replication models.",
        tags=["system design", "distributed systems", "database", "backend"],
        image_url="https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-403",
        name="Atomic Habits: Micro-Changes, Remarkable Results",
        category="Books",
        price=18.50,
        rating=4.8,
        reviews_count=4500,
        stock=60,
        image_emoji="📘",
        badge="Bestseller",
        description="Proven framework for improving every day through compounding habit loops.",
        tags=["self-help", "productivity", "psychology", "mindset"],
        image_url="https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-404",
        name="Python Programming: Clean Code & Architecture",
        category="Books",
        price=39.99,
        rating=4.7,
        reviews_count=850,
        stock=28,
        image_emoji="📕",
        badge="Recommended",
        description="Master modern Pythonic idioms, design patterns, and enterprise testing practices.",
        tags=["python", "coding", "software engineering"],
        image_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&q=80",
    ),
    # Fitness & Sports
    Product(
        id="PROD-501",
        name="ProGrip Adjustable Dumbbell Set (5-52.5 lbs)",
        category="Fitness",
        price=299.00,
        rating=4.8,
        reviews_count=740,
        stock=10,
        image_emoji="🏋️",
        badge="Popular",
        description="Rapid-dial weight selection replaces 15 sets of dumbbells in a compact footprint.",
        tags=["fitness", "weights", "workout", "gym"],
        image_url="https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-502",
        name="EcoFlex Alignment Yoga Mat (6mm)",
        category="Fitness",
        price=36.00,
        rating=4.6,
        reviews_count=610,
        stock=38,
        image_emoji="🧘",
        badge=None,
        description="Non-slip natural rubber yoga mat with laser-etched posture alignment guidelines.",
        tags=["yoga", "pilates", "exercise", "mat"],
        image_url="https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-503",
        name="HydroShield Insulated Gallon Bottle",
        category="Fitness",
        price=24.99,
        rating=4.7,
        reviews_count=1150,
        stock=55,
        image_emoji="💧",
        badge="Sale",
        description="Double-wall vacuum insulation keeps water ice-cold for 36 hours with straw lid.",
        tags=["hydration", "water bottle", "sports", "vacuum"],
        image_url="https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=600&q=80",
    ),
    # Gourmet Groceries
    Product(
        id="PROD-601",
        name="Artisanal Single-Origin Arabica Beans (1kg)",
        category="Groceries",
        price=26.50,
        rating=4.8,
        reviews_count=920,
        stock=40,
        image_emoji="🫘",
        badge="Organic",
        description="Medium roast Ethiopian Yirgacheffe notes of bergamot, floral jasmine, and honey.",
        tags=["coffee", "beans", "gourmet", "organic"],
        image_url="https://images.unsplash.com/photo-1587734195503-904fca47e0e9?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-602",
        name="Raw Wildflower Manuka Honey UMF 15+",
        category="Groceries",
        price=45.00,
        rating=4.9,
        reviews_count=480,
        stock=20,
        image_emoji="🍯",
        badge="Pure Honey",
        description="Certified UMF 15+ authentic New Zealand raw medicinal honey.",
        tags=["honey", "superfood", "natural", "health"],
        image_url="https://images.unsplash.com/photo-1587049352846-4a222e784d38?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-603",
        name="Extra Virgin Cold-Pressed Olive Oil (750ml)",
        category="Groceries",
        price=22.00,
        rating=4.7,
        reviews_count=390,
        stock=30,
        image_emoji="🫒",
        badge=None,
        description="First cold-pressed Koroneiki olives from Crete with rich polyphenols and grassy finish.",
        tags=["olive oil", "cooking", "mediterranean", "healthy"],
        image_url="https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=600&q=80",
    ),
    Product(
        id="PROD-604",
        name="Organic Ceremonial Grade Matcha (100g)",
        category="Groceries",
        price=32.99,
        rating=4.8,
        reviews_count=670,
        stock=24,
        image_emoji="🍵",
        badge="Imported",
        description="First-harvest stone-ground Japanese green tea from Uji, Kyoto.",
        tags=["matcha", "green tea", "antioxidant", "japanese"],
        image_url="https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80",
    ),
]


# Available Discount Coupons stored in coupon HashTable
AVAILABLE_COUPONS: Dict[str, dict] = {
    "WELCOME10": {
        "code": "WELCOME10",
        "type": "percentage",
        "value": 10.0,
        "min_cart": 0.0,
        "description": "10% off entire order",
    },
    "SAVE20": {
        "code": "SAVE20",
        "type": "percentage",
        "value": 20.0,
        "min_cart": 80.0,
        "description": "20% off orders over ₹80",
    },
    "FLAT50": {
        "code": "FLAT50",
        "type": "fixed",
        "value": 50.0,
        "min_cart": 200.0,
        "description": "₹50 off orders over ₹200",
    },
    "FREESHIP": {
        "code": "FREESHIP",
        "type": "shipping",
        "value": 100.0,
        "min_cart": 30.0,
        "description": "Free standard shipping on orders over ₹30",
    },
    "TECH15": {
        "code": "TECH15",
        "type": "percentage",
        "value": 15.0,
        "min_cart": 150.0,
        "description": "15% off cart on tech orders over ₹150",
    },
}


def build_catalog_hashtable() -> HashTable:
    """
    Initializes and populates a custom HashTable with all sample products.
    Key: product.id (e.g. 'PROD-101') -> Value: Product instance.
    Provides average O(1) lookup during search, cart modifications, and bill calculation.
    """
    table = HashTable(initial_capacity=31)
    for prod in SAMPLE_PRODUCTS:
        table.put(prod.id, prod)
    return table


def build_coupon_hashtable() -> HashTable:
    """
    Initializes a custom HashTable with promo coupon definitions for O(1) coupon verification.
    """
    table = HashTable(initial_capacity=17)
    for code, details in AVAILABLE_COUPONS.items():
        table.put(code, details)
    return table
