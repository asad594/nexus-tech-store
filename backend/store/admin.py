from django.contrib import admin
from .models import User, Category, Product, ProductVariant, Order, OrderItem, CartItem, Review, Wishlist

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('color_name', 'hex_code', 'image_url', 'price_delta', 'stock_qty', 'is_default')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock_qty', 'is_featured', 'is_new')
    list_filter = ('category', 'brand', 'is_featured', 'is_new')
    search_fields = ('name', 'description', 'brand')
    inlines = [ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color_name', 'hex_code', 'price_delta', 'stock_qty', 'is_default')
    list_filter = ('product__category', 'is_default')
    search_fields = ('product__name', 'color_name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status')
    inlines = [OrderItemInline]

admin.site.register(User)
admin.site.register(CartItem)
admin.site.register(Review)
admin.site.register(Wishlist)
