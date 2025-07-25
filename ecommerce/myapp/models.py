from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from parler.models import TranslatableModel


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, unique=True)
    )
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, db_index=True),
        description=models.TextField(blank=True)
    )
    
    # Nicht übersetzbare Felder
    sku = models.CharField(max_length=20, unique=True, null=True)
    category = models.ForeignKey(
        Category, 
        related_name='products',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='products/images/')
    alt_text = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Image for {self.product.name}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50, choices=[
        ('credit', 'Kreditkarte'),
        ('paypal', 'PayPal'),
        ('transfer', 'Überweisung')
    ])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"