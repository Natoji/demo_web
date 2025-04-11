from django.urls import path
from store.views.auth_views import RegisterView, LogoutView, UserProfileView ,CustomLoginView
from store.views.cart_views import CartDetailView, AddToCartView, RemoveFromCartView, UpdateCartItemQuantityView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from store.views import (
    user_views, product_views, order_views, orderitem_views,
    category_views, brand_views, cart_views, wishlist_views,
    payment_views, shipping_views, review_views,
)

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),

    # User
    path('users/', user_views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', user_views.UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),

    # Product
    path('products/', product_views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', product_views.ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),

    # Category
    path('categories/', category_views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', category_views.CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    # Brand
    path('brands/', brand_views.BrandListCreateView.as_view(), name='brand-list-create'),
    path('brands/<int:pk>/', brand_views.BrandRetrieveUpdateDestroyView.as_view(), name='brand-detail'),

    # Order
    path('orders/', order_views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', order_views.OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),

    # OrderItem
    path('order-items/', orderitem_views.OrderItemListCreateView.as_view(), name='orderitem-list-create'),
    path('order-items/<int:pk>/', orderitem_views.OrderItemRetrieveUpdateDestroyView.as_view(), name='orderitem-detail'),

    # Cart
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/update/', UpdateCartItemQuantityView.as_view(), name='update-cart-item'),

    # Wishlist
    path('wishlists/', wishlist_views.WishlistListCreateView.as_view(), name='wishlist-list-create'),
    path('wishlists/<int:pk>/', wishlist_views.WishlistRetrieveUpdateDestroyView.as_view(), name='wishlist-detail'),

    # Payment
    path('payments/', payment_views.PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', payment_views.PaymentRetrieveUpdateDestroyView.as_view(), name='payment-detail'),

    # ShippingInfo
    path('shipping/', shipping_views.ShippingInfoListCreateView.as_view(), name='shipping-list-create'),
    path('shipping/<int:pk>/', shipping_views.ShippingInfoRetrieveUpdateDestroyView.as_view(), name='shipping-detail'),

    # Review
    path('reviews/', review_views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', review_views.ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),
]
