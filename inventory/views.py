from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from store.models import Product, Supplier, Buyer, Order, Delivery

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    if user.is_superuser:
        # Admin: full access
        total_product = Product.objects.count()
        total_supplier = Supplier.objects.count()
        total_buyer = Buyer.objects.count()
        total_order = Order.objects.count()
        orders = Order.objects.all().order_by('-id')[:10]  # Limit to recent 10
        deliveries = Delivery.objects.all().order_by('-id')[:10]
        context = {
            'product': total_product,
            'supplier': total_supplier,
            'buyer': total_buyer,
            'order': total_order,
            'orders': orders,
            'deliveries': deliveries,
            'role': 'admin'
        }
    elif user.is_buyer:
        # Buyer: view their orders and track deliveries
        orders = Order.objects.filter(buyer__user=user).order_by('-id')
        deliveries = Delivery.objects.filter(order__buyer__user=user).order_by('-id')
        context = {
            'orders': orders,
            'deliveries': deliveries,
            'role': 'buyer'
        }
    elif user.is_supplier:
        # Supplier: their products, orders, deliveries
        products = Product.objects.filter(order__supplier__user=user).distinct()
        orders = Order.objects.filter(supplier__user=user).order_by('-id')
        deliveries = Delivery.objects.filter(order__supplier__user=user).order_by('-id')
        context = {
            'products': products,
            'orders': orders,
            'deliveries': deliveries,
            'role': 'supplier'
        }
    else:
        # Fallback
        context = {'role': 'unknown'}
    
    return render(request, 'dashboard.html', context)