from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.db.models import Q, Sum, Count, F, Avg
from django.contrib.auth import get_user_model

from .models import Category, Product, ProductVariant, Order, OrderItem, CartItem, Review, Wishlist
from .serializers import (
    UserSerializer, UserProfileUpdateSerializer, ChangePasswordSerializer,
    RegisterSerializer, CategorySerializer, ProductSerializer, ProductVariantSerializer,
    CartItemSerializer, SyncCartItemInputSerializer, OrderSerializer,
    ReviewSerializer, WishlistSerializer, CheckoutSerializer, DirectCheckoutSerializer
)
from .permissions import IsAdminUserRole, IsOwnerOrAdmin

User = get_user_model()

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        return Response({
            'message': 'User registered successfully',
            'user': user_serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def get_user_profile(request):
    user = request.user
    if request.method in ['PUT', 'PATCH']:
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def sync_cart(request):
    """
    Merges items from client-side guest cart into the authenticated user's cart database.
    Input payload: list of { product_id: int, variant_id: int|null, quantity: int }
    """
    items = request.data.get('items', [])
    for item in items:
        product_id = item.get('product_id')
        variant_id = item.get('variant_id') or item.get('variant')
        qty = int(item.get('quantity', 1))
        if product_id and qty > 0:
            try:
                product = Product.objects.get(id=product_id)
                variant = None
                if variant_id:
                    try:
                        variant = ProductVariant.objects.get(id=variant_id, product=product)
                    except ProductVariant.DoesNotExist:
                        variant = None

                cart_item, created = CartItem.objects.get_or_create(
                    user=request.user,
                    product=product,
                    variant=variant,
                    defaults={'quantity': qty}
                )
                if not created:
                    cart_item.quantity += qty
                    cart_item.save()
            except Product.DoesNotExist:
                continue

    user_cart = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(user_cart, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        return [permissions.AllowAny()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        brand = self.request.query_params.get('brand', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        in_stock = self.request.query_params.get('in_stock', None)
        is_featured = self.request.query_params.get('is_featured', None)
        is_new = self.request.query_params.get('is_new', None)
        ordering = self.request.query_params.get('ordering', None)

        if category:
            if category.isdigit():
                queryset = queryset.filter(category_id=category)
            else:
                queryset = queryset.filter(category__name__iexact=category)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search) |
                Q(brand__icontains=search)
            )

        if brand:
            queryset = queryset.filter(brand__iexact=brand)

        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass

        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        if in_stock:
            if in_stock.lower() == 'true':
                queryset = queryset.filter(stock_qty__gt=0)
            elif in_stock.lower() == 'false':
                queryset = queryset.filter(stock_qty__lte=0)

        if is_featured:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')

        if is_new:
            queryset = queryset.filter(is_new=is_new.lower() == 'true')

        if ordering:
            if ordering == 'price_low':
                queryset = queryset.order_by('price')
            elif ordering == 'price_high':
                queryset = queryset.order_by('-price')
            elif ordering == 'rating':
                queryset = queryset.order_by('-rating')
            elif ordering == 'newest':
                queryset = queryset.order_by('-created_at')
            elif ordering == 'popularity':
                queryset = queryset.order_by('-num_reviews', '-rating')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        product = self.get_object()
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id).order_by('-rating')[:4]
        serializer = self.get_serializer(related_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'])
    def reviews(self, request, pk=None):
        product = self.get_object()
        if request.method == 'GET':
            reviews = product.reviews.all().order_by('-created_at')
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            if not request.user or not request.user.is_authenticated:
                return Response({'error': 'Authentication required to post a review'}, status=status.HTTP_401_UNAUTHORIZED)
            
            rating = request.data.get('rating')
            comment = request.data.get('comment', '')

            if not rating or not (1 <= int(rating) <= 5):
                return Response({'error': 'Rating must be an integer between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)

            review, created = Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={'rating': int(rating), 'comment': comment}
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if self.action in ['my_reviews']:
            return Review.objects.filter(user=user)
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticatedOrReadOnly()]


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
        if wishlist_item:
            wishlist_item.delete()
            return Response({'status': 'removed', 'message': 'Product removed from wishlist'}, status=status.HTTP_200_OK)
        else:
            wishlist_item = Wishlist.objects.create(user=request.user, product=product)
            serializer = self.get_serializer(wishlist_item)
            return Response({'status': 'added', 'data': serializer.data}, status=status.HTTP_201_CREATED)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product') or request.data.get('product_id')
        variant_id = request.data.get('variant') or request.data.get('variant_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        variant = None
        if variant_id:
            try:
                variant = ProductVariant.objects.get(id=variant_id, product=product)
            except ProductVariant.DoesNotExist:
                return Response({'error': 'Selected variant does not exist for this product'}, status=status.HTTP_400_BAD_REQUEST)

        if variant:
            if variant.stock_qty <= 0:
                return Response({'error': f'Selected color "{variant.color_name}" is out of stock'}, status=status.HTTP_400_BAD_REQUEST)
        elif product.stock_qty <= 0:
            return Response({'error': 'Product is out of stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response({'message': 'Cart cleared successfully'}, status=status.HTTP_200_OK)



class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.all().order_by('-created_at')
        if not (user.role == 'admin' or user.is_staff or user.is_superuser):
            queryset = queryset.filter(user=user)

        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    @transaction.atomic
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user).select_related('product', 'variant')

        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate stock for all items (both variant stock and product stock)
        out_of_stock_items = []
        for item in cart_items:
            if item.variant:
                if item.variant.stock_qty < item.quantity:
                    out_of_stock_items.append(
                        f"{item.product.name} ({item.variant.color_name}) - requested: {item.quantity}, available: {item.variant.stock_qty}"
                    )
            elif item.product.stock_qty < item.quantity:
                out_of_stock_items.append(
                    f"{item.product.name} - requested: {item.quantity}, available: {item.product.stock_qty}"
                )

        if out_of_stock_items:
            return Response({
                'error': 'Insufficient stock for items',
                'details': out_of_stock_items
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        shipping_address = data.get('shipping_address') or user.shipping_address or 'Standard Express Delivery'
        city = data.get('city') or user.city or ''
        postal_code = data.get('postal_code') or user.postal_code or ''
        country = data.get('country') or user.country or 'United States'
        payment_method = data.get('payment_method', 'Credit Card')
        notes = data.get('notes', '')

        from decimal import Decimal
        items_subtotal = Decimal('0.00')
        for item in cart_items:
            unit_price = item.product.price + (item.variant.price_delta if item.variant else Decimal('0.00'))
            items_subtotal += unit_price * item.quantity

        shipping_cost = Decimal('0.00') if items_subtotal >= Decimal('500') else Decimal('25.00')
        total_amount = items_subtotal + shipping_cost

        order = Order.objects.create(
            user=user,
            status='pending',
            payment_status='paid',
            total_amount=total_amount,
            shipping_cost=shipping_cost,
            shipping_address=shipping_address,
            city=city,
            postal_code=postal_code,
            country=country,
            payment_method=payment_method,
            notes=notes
        )

        for item in cart_items:
            unit_price = item.product.price + (item.variant.price_delta if item.variant else Decimal('0.00'))
            v_name = item.variant.color_name if item.variant else ''
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                product_name_snapshot=item.product.name,
                variant_name_snapshot=v_name,
                quantity=item.quantity,
                price_at_purchase=unit_price
            )
            # Reduce inventory stock
            if item.variant:
                item.variant.stock_qty = max(0, item.variant.stock_qty - item.quantity)
                item.variant.save()
            item.product.stock_qty = max(0, item.product.stock_qty - item.quantity)
            item.product.save()

        # Clear user cart
        cart_items.delete()

        order_serializer = self.get_serializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    @action(detail=False, methods=['post'])
    def direct_checkout(self, request):
        """
        Allows buying a single item directly without modifying or clearing the main cart.
        """
        user = request.user
        serializer = DirectCheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            product = Product.objects.get(id=data['product_id'])
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        variant = None
        variant_id = data.get('variant_id')
        if variant_id:
            try:
                variant = ProductVariant.objects.get(id=variant_id, product=product)
            except ProductVariant.DoesNotExist:
                return Response({'error': 'Selected variant not found'}, status=status.HTTP_404_NOT_FOUND)

        quantity = data.get('quantity', 1)
        if variant:
            if variant.stock_qty < quantity:
                return Response({
                    'error': f'Insufficient stock for {product.name} ({variant.color_name}). Available: {variant.stock_qty}'
                }, status=status.HTTP_400_BAD_REQUEST)
        elif product.stock_qty < quantity:
            return Response({
                'error': f'Insufficient stock for {product.name}. Available: {product.stock_qty}'
            }, status=status.HTTP_400_BAD_REQUEST)

        shipping_address = data.get('shipping_address') or user.shipping_address or 'Standard Express Delivery'
        city = data.get('city') or user.city or ''
        postal_code = data.get('postal_code') or user.postal_code or ''
        country = data.get('country') or user.country or 'United States'
        payment_method = data.get('payment_method', 'Credit Card')
        notes = data.get('notes', '')

        from decimal import Decimal
        unit_price = product.price + (variant.price_delta if variant else Decimal('0.00'))
        items_subtotal = unit_price * quantity
        shipping_cost = Decimal('0.00') if items_subtotal >= Decimal('500') else Decimal('25.00')
        total_amount = items_subtotal + shipping_cost

        order = Order.objects.create(
            user=user,
            status='pending',
            payment_status='paid',
            total_amount=total_amount,
            shipping_cost=shipping_cost,
            shipping_address=shipping_address,
            city=city,
            postal_code=postal_code,
            country=country,
            payment_method=payment_method,
            notes=notes
        )

        v_name = variant.color_name if variant else ''
        OrderItem.objects.create(
            order=order,
            product=product,
            variant=variant,
            product_name_snapshot=product.name,
            variant_name_snapshot=v_name,
            quantity=quantity,
            price_at_purchase=unit_price
        )

        if variant:
            variant.stock_qty = max(0, variant.stock_qty - quantity)
            variant.save()
        product.stock_qty = max(0, product.stock_qty - quantity)
        product.save()

        order_serializer = self.get_serializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['pending', 'processing']:
            return Response({
                'error': f'Order cannot be cancelled in status "{order.status}".'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not (request.user == order.user or request.user.role == 'admin' or request.user.is_staff):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        # Restore product stock
        with transaction.atomic():
            for item in order.items.all():
                if item.product:
                    item.product.stock_qty += item.quantity
                    item.product.save()

            order.status = 'cancelled'
            order.payment_status = 'refunded'
            order.save()

        return Response(self.get_serializer(order).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUserRole])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        tracking_number = request.data.get('tracking_number')
        payment_status = request.data.get('payment_status')

        if new_status and new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status choice'}, status=status.HTTP_400_BAD_REQUEST)

        if payment_status and payment_status not in dict(Order.PAYMENT_STATUS_CHOICES):
            return Response({'error': 'Invalid payment status choice'}, status=status.HTTP_400_BAD_REQUEST)

        if new_status:
            order.status = new_status
        if tracking_number is not None:
            order.tracking_number = tracking_number
        if payment_status:
            order.payment_status = payment_status

        order.save()
        return Response(self.get_serializer(order).data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUserRole])
    def analytics(self, request):
        total_orders = Order.objects.count()
        total_revenue = Order.objects.exclude(status='cancelled').aggregate(
            total=Sum('total_amount')
        )['total'] or 0.00

        pending_orders = Order.objects.filter(status='pending').count()
        processing_orders = Order.objects.filter(status='processing').count()
        shipped_orders = Order.objects.filter(status='shipped').count()
        completed_orders = Order.objects.filter(status='delivered').count()
        cancelled_orders = Order.objects.filter(status='cancelled').count()

        low_stock_products = Product.objects.filter(stock_qty__lte=5).values(
            'id', 'name', 'stock_qty', 'brand'
        )

        category_sales = OrderItem.objects.exclude(order__status='cancelled').values(
            'product__category__name'
        ).annotate(
            total_sales=Sum(F('quantity') * F('price_at_purchase')),
            total_units=Sum('quantity')
        ).order_by('-total_sales')

        top_products = OrderItem.objects.exclude(order__status='cancelled').values(
            'product__id', 'product__name'
        ).annotate(
            units_sold=Sum('quantity'),
            revenue=Sum(F('quantity') * F('price_at_purchase'))
        ).order_by('-units_sold')[:5]

        return Response({
            'total_revenue': float(total_revenue),
            'total_orders': total_orders,
            'orders_by_status': {
                'pending': pending_orders,
                'processing': processing_orders,
                'shipped': shipped_orders,
                'delivered': completed_orders,
                'cancelled': cancelled_orders,
            },
            'low_stock_count': len(low_stock_products),
            'low_stock_items': list(low_stock_products),
            'category_sales': list(category_sales),
            'top_products': list(top_products),
        })
