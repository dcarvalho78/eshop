"""
URL configuration for ecommerce project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp import views

urlpatterns = [
    # Admin-Seite
    path('admin/', admin.site.urls),
    
    # Haupt-App URLs
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Produkt-URLs
    path('products/', include([
        path('', views.product_list, name='product_list'),
        path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
        path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    ])),
    
    # Warenkorb-URLs
    path('cart/', include([
        path('', views.cart_detail, name='cart_detail'),
        path('add/<int:product_id>/', views.cart_add, name='cart_add'),
        path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    ])),
    
    # Bestell-URLs
    path('orders/', include([
        path('create/', views.order_create, name='order_create'),
        path('history/', views.order_history, name='order_history'),
    ])),
    
    # Benutzer-Authentifizierung
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)