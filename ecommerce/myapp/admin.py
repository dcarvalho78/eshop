from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Product, ProductImage, Category


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    classes = ['collapse']
    fields = ('image', 'alt_text')

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'slug')
    search_fields = ('translations__name',)
    prepopulated_fields = {'slug': ('name',)}

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('name', 'category', 'price', 'available', 'stock', 'created')
    list_filter = ('available', 'created', 'updated', 'category')
    list_editable = ('price', 'available', 'stock')
    search_fields = ('translations__name', 'translations__description')
    inlines = [ProductImageInline]
    
    fieldsets = (
        (None, {
            'fields': (('name', 'slug'), 'category', 'description')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'available', 'stock')
        }),
        ('Additional Information', {
            'fields': ('brand', 'specification'),
            'classes': ('collapse',)
        })
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

# Only include Order models if the orders app is properly installed
try:
    from orders.models import Order, OrderItem
    
    class OrderItemInline(admin.TabularInline):
        model = OrderItem
        raw_id_fields = ['product']
        extra = 0
        fields = ('product', 'price', 'quantity')
        readonly_fields = ('price',)

    @admin.register(Order)
    class OrderAdmin(admin.ModelAdmin):
        list_display = ('id', 'customer_email', 'created', 'total_amount', 'paid')
        list_filter = ('paid', 'created', 'updated')
        search_fields = ('email', 'first_name', 'last_name')
        inlines = [OrderItemInline]
        readonly_fields = ('created', 'updated')
        
        fieldsets = (
            ('Customer Information', {
                'fields': ('customer', 'email', 'phone_number')
            }),
            ('Shipping Information', {
                'fields': ('address', 'postal_code', 'city')
            }),
            ('Order Details', {
                'fields': ('paid', 'total_price', 'discount', 'created', 'updated')
            })
        )

        def customer_email(self, obj):
            return obj.email
        customer_email.short_description = 'Email'

        def total_amount(self, obj):
            return f"€{obj.total_price}"
        total_amount.short_description = 'Total'

except ImportError:
    # Silently ignore if orders app isn't available
    pass