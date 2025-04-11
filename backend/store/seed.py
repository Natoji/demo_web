import sys
import os
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from store.models import (
    Brand, Category, Product, Wishlist, Cart, CartItem, Order,
    OrderItem, Payment, ShippingInfo, Review
)

User = get_user_model()

# ===== XÓA DỮ LIỆU CŨ =====
Review.objects.all().delete()
Payment.objects.all().delete()
OrderItem.objects.all().delete()
Order.objects.all().delete()
ShippingInfo.objects.all().delete()
CartItem.objects.all().delete()
Cart.objects.all().delete()
Wishlist.objects.all().delete()
Product.objects.all().delete()
Brand.objects.all().delete()
Category.objects.all().delete()
User.objects.all().delete()

# ===== 1. USERS =====
user1 = User.objects.create_user(email="john@example.com", password="123456", fullname="John Doe", phone_number="0123456789", address="123 Street", role="client")
user2 = User.objects.create_user(email="admin@example.com", password="admin123", fullname="Admin", phone_number="0987654321", address="Admin HQ", role="admin")

# ===== 2. BRANDS & CATEGORIES =====
brand1 = Brand.objects.create(name="Luxury Line", description="High-end luxury brand")
brand2 = Brand.objects.create(name="Everyday Sparkle", description="Casual and elegant")

cat1 = Category.objects.create(name="Rings", description="Various ring styles")
cat2 = Category.objects.create(name="Necklaces", description="Elegant necklaces")

# ===== 3. PRODUCTS =====
product1 = Product.objects.create(
    name="Diamond Ring",
    description="A sparkling diamond ring.",
    price=1999.99,
    stock=10,
    brand=brand1,
    category=cat1
)

product2 = Product.objects.create(
    name="Gold Necklace",
    description="24K pure gold necklace.",
    price=2599.50,
    stock=5,
    brand=brand2,
    category=cat2
)

# ===== 4. WISHLIST =====
Wishlist.objects.create(user=user1, product=product1)
Wishlist.objects.create(user=user1, product=product2)

# ===== 5. CART =====
cart = Cart.objects.create(user=user1)
CartItem.objects.create(cart=cart, product=product1, quantity=2)
CartItem.objects.create(cart=cart, product=product2, quantity=1)

# ===== 6. ORDER =====
order = Order.objects.create(
    user=user1,
    status="processing",
    total_amount=1999.99 + 2599.50  # = 4599.49
)

# ===== 7. SHIPPING INFO
shipping_info = ShippingInfo.objects.create(
    order=order,
    address="123 Delivery Street",
    city="Hanoi",
    postal_code="100000",
    country="Vietnam",
    phone="123456789"
)

# ===== 8. ORDER ITEMS =====
OrderItem.objects.create(order=order, product=product1, quantity=1, price=1999.99)
OrderItem.objects.create(order=order, product=product2, quantity=1, price=2599.50)

# ===== 9. PAYMENT =====
Payment.objects.create(
    order=order,
    method="credit_card",
    amount=4599.49,
    paid_at=datetime.now()
)

# ===== 10. REVIEW =====
Review.objects.create(user=user1, product=product1, rating=5, comment="Amazing ring!")
Review.objects.create(user=user1, product=product2, rating=4, comment="Beautiful necklace.")

print("✅ Dummy data seeded successfully.")
