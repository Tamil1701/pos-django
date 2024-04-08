from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from inventory.forms import UserRegistry, ProductForm, OrderForm, EditProductForm
from inventory.models import Product, Order

@login_required
def index(request):
    orders_user = Order.objects.all()
    users = User.objects.all()[:2]
    orders_adm = Order.objects.all()[:2]
    products = Product.objects.all()[:2]
    reg_users = len(User.objects.all())
    all_prods = len(Product.objects.all())
    all_orders = len(Order.objects.all())
    context = {
        "title": "Home",
        "orders": orders_user,
        "orders_adm": orders_adm,
        "users": users,
        "products": products,
        
        "count_users": reg_users,
        "count_products": all_prods,
        "count_orders": all_orders

    }
    return render(request, 'inventory/index.html', context)

@login_required
def products(request):
    # Retrieve all existing products
    products = Product.objects.all()

    # Initialize forms for adding and editing products
    add_form = ProductForm(request.POST or None)
    edit_form = EditProductForm(request.POST or None)

    # Handle form submission for adding a new product
    if request.method == 'POST' and 'add_product' in request.POST:
        add_form = ProductForm(request.POST)
        if add_form.is_valid():
            add_form.save()
            return redirect('products')

    # Handle form submission for editing an existing product
    if request.method == 'POST' and 'edit_product' in request.POST:
        edit_form = EditProductForm(request.POST)
        if edit_form.is_valid():
            selected_product_id = edit_form.cleaned_data['product_choice'].id
            selected_product = Product.objects.get(id=selected_product_id)
            selected_product.quantity = edit_form.cleaned_data['quantity']
            selected_product.price = edit_form.cleaned_data['price']
            selected_product.description = edit_form.cleaned_data['description']
            selected_product.save()
            return redirect('products')

    # Calculate total price for each existing product
    for product in products:
        product.total_price = product.price * product.quantity
    
    # Retrieve products with low stock (quantity <= 2) and out-of-stock products (quantity <= 0)
    low_stock_products = Product.objects.filter(quantity__lte=10)
    out_of_stock_products = Product.objects.filter(quantity__lte=0)


    context = {
        "title": "Products",
        "products": products,
        "add_form": add_form,
        "edit_form": edit_form,
        "low_stock_products": low_stock_products,
        "out_of_stock_products": out_of_stock_products
    }
    return render(request, 'inventory/products.html', context)


@login_required
def orders(request):
    # Retrieve all orders
    orders = Order.objects.all()

    # Retrieve low-stock and out-of-stock products
    low_stock_products = Product.objects.filter(quantity__gt=2, quantity__lte=20)
    out_of_stock_products = Product.objects.filter(quantity__lte=2)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            return redirect('orders')
    else:
        form = OrderForm()

    context = {
        "title": "Orders",
        "orders": orders,
        "form": form,
        "low_stock_products": low_stock_products,
        "out_of_stock_products": out_of_stock_products
    }
    return render(request, 'inventory/orders.html', context)


@login_required
def users(request):
    users = User.objects.all()
    context = {
        "title": "Users",
        "users": users
    }
    return render(request, 'inventory/users.html', context)

@login_required
def user(request):
    context = {
        "profile": "User Profile"
    }
    return render(request, 'inventory/user.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistry(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistry()
    context = {
        "register": "Register",
        "form": form
    }
    return render(request, 'inventory/register.html', context)

# @login_required
# def products(request):
#     products = Product.objects.all()

#     # Calculate total price for each product
#     for product in products:
#         product.total_price = product.price * product.quantity

#     context = {
#         "title": "Products",
#         "products": products
#     }
#     return render(request, 'inventory/products.html', context)