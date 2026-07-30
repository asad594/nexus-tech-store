from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Product, Order, OrderItem, CartItem, Review, Wishlist

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'name', 'role', 'is_staff',
            'phone_number', 'shipping_address', 'city', 'postal_code',
            'country', 'avatar_url'
        )

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'name', 'phone_number', 'shipping_address',
            'city', 'postal_code', 'country', 'avatar_url'
        )

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.CharField(required=False, default='customer')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'name', 'role',
            'phone_number', 'shipping_address', 'city', 'postal_code', 'country'
        )

    def create(self, validated_data):
        role = validated_data.pop('role', 'customer')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            name=validated_data.get('name', validated_data['username']),
            role=role,
            phone_number=validated_data.get('phone_number', ''),
            shipping_address=validated_data.get('shipping_address', ''),
            city=validated_data.get('city', ''),
            postal_code=validated_data.get('postal_code', ''),
            country=validated_data.get('country', 'United States')
        )
        if role == 'admin':
            user.is_staff = True
            user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'icon', 'description', 'product_count', 'created_at')

    def get_product_count(self, obj):
        return obj.products.count()

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'category_name', 'category_icon',
            'price', 'description', 'specs', 'stock_qty', 'in_stock',
            'image_url', 'brand', 'is_featured', 'is_new', 'rating',
            'num_reviews', 'created_at'
        )

    def get_in_stock(self, obj):
        return obj.stock_qty > 0

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_avatar = serializers.CharField(source='user.avatar_url', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Review
        fields = (
            'id', 'product', 'product_name', 'user', 'user_name',
            'user_avatar', 'rating', 'comment', 'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'created_at', 'updated_at')

class WishlistSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'product', 'product_detail', 'created_at')

class CartItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_detail', 'quantity', 'subtotal', 'updated_at')

    def get_subtotal(self, obj):
        return str(round(obj.product.price * obj.quantity, 2))

class SyncCartItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)

class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'id', 'product', 'product_name_snapshot', 'product_detail',
            'quantity', 'price_at_purchase', 'subtotal'
        )

    def get_subtotal(self, obj):
        return str(round(obj.price_at_purchase * obj.quantity, 2))

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'user_name', 'user_email', 'status', 'payment_status',
            'total_amount', 'shipping_cost', 'shipping_address', 'city',
            'postal_code', 'country', 'payment_method', 'tracking_number',
            'notes', 'created_at', 'updated_at', 'total_items', 'items'
        )
        read_only_fields = ('user', 'created_at', 'updated_at')

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True, default='United States')
    payment_method = serializers.CharField(required=False, default='Credit Card')
    notes = serializers.CharField(required=False, allow_blank=True)

class DirectCheckoutSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
    shipping_address = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True, default='United States')
    payment_method = serializers.CharField(required=False, default='Credit Card')
    notes = serializers.CharField(required=False, allow_blank=True)
