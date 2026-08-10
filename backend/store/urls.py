from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    register_user, get_user_profile, change_password, sync_cart, health_check,
    CategoryViewSet, ProductViewSet, ReviewViewSet,
    WishlistViewSet, CartViewSet, OrderViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')
router.register('reviews', ReviewViewSet, basename='review')
router.register('wishlist', WishlistViewSet, basename='wishlist')
router.register('cart', CartViewSet, basename='cart')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('auth/register/', register_user, name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', get_user_profile, name='user_profile'),
    path('auth/change-password/', change_password, name='change_password'),
    path('auth/sync-cart/', sync_cart, name='sync_cart'),
    path('', include(router.urls)),
]
