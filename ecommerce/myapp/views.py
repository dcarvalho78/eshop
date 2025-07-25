from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User  # Neu hinzugefügt
from .models import Category, Product, Order, OrderItem
from .forms import ContactForm, OrderCreateForm, UserRegistrationForm  # UserRegistrationForm hinzugefügt
from .cart import Cart

def index(request):
    featured_products = Product.objects.filter(available=True, featured=True)[:4]
    return render(request, 'myapp/index.html', {
        'featured_products': featured_products
    })

def about(request):
    return render(request, 'myapp/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ihre Nachricht wurde gesendet!')
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'myapp/contact.html', {'form': form})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    query = request.GET.get('q')

    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'myapp/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    return render(request, 'myapp/product/detail.html', {
        'product': product,
        'related_products': related_products
    })

@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'myapp/cart/detail.html', {'cart': cart})

@login_required
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            cart.clear()
            return render(request, 'myapp/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'myapp/order/create.html', {
        'cart': cart,
        'form': form
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'myapp/order/history.html', {'orders': orders})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'myapp/account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'myapp/account/register.html', {'user_form': user_form})