from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from .forms import UserRegisterForm
from .models import Product,Cart,OrderItem,Order
from .forms import ProductForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def user_page(request):
    return render(request, 'user_page.html')


def admin_page(request):
    products = Product.objects.all()
    product = products.first()
    return render(request, 'admin_page.html', {'products': products, 'product': product})


def index_page(request):
    return render(request, 'index.html')

def register_user(request):
    if request.method == 'POST':
        registration_form = UserRegisterForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect('login_user')
    else:
        registration_form = UserRegisterForm()
    return render(request, 'register.html', {'registration_form': registration_form})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin_page')  
            else:
                return redirect('user_page') 
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login_user')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
        else:
            messages.error(request, 'Failed to add product. Please check the form for errors.')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
        else:
            messages.error(request, 'Failed to update product. Please check the form for errors.')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    all_products = Product.objects.exclude(pk=pk)
    return render(request, 'product_detail.html', {'product': product, 'all_products': all_products})

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 0))
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('cart')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.calculate_total() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 0))
        cart_item = Cart.objects.get(user=request.user, product=product)
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart')

@login_required
def delete_from_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart_item = Cart.objects.get(user=request.user, product=product)
        cart_item.delete()

    return redirect('cart')

@login_required
def checkout_view(request):
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')
        shipping_postal_code = request.POST.get('shipping_postal_code')
        shipping_country = request.POST.get('shipping_country')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_postal_code=shipping_postal_code,
            shipping_country=shipping_country,
            payment_method=payment_method,
            total_price=0  
        )
        
        cart_items = Cart.objects.filter(user=request.user)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price * cart_item.quantity
            )

      
        order.total_price = sum(item.price for item in order.items.all())
        order.save()
        cart_items.delete()
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html')

def order_confirmation_view(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

@login_required
def order_history(request):
    if request.user.is_staff:  
        orders = Order.objects.all()  
    else:
        orders = Order.objects.filter(user=request.user)  
    
    return render(request, 'order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.user.is_superuser or order.user == request.user:
        if request.method == 'POST' and request.user.is_superuser:  
            new_status = request.POST.get('status')
            order.status = new_status
            order.save()
            return redirect('order_detail', order_id=order_id)

        return render(request, 'order_detail.html', {'order': order})
    else:
        return render(request, 'access_denied.html')
    

