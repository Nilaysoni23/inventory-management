from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from users.models import User
from .models import (
    Supplier,
    Buyer,
    Season,
    Drop,
    Product,
    Order,
    Delivery
)

# Import ONLY forms (NOT edit/delete views)
from .forms import (
    SupplierForm,
    EditSupplierForm,
    BuyerForm,
    EditBuyerForm,
    SeasonForm,
    DropForm,
    ProductForm,
    OrderForm,
    DeliveryForm,
)
from .permissions import role_required


# ---------------- SUPPLIER ----------------

@login_required(login_url='login')
@role_required('supplier')
def create_supplier(request):
    forms = SupplierForm()
    if request.method == 'POST':
        forms = SupplierForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']

            if password == retype_password:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    is_supplier=True
                )
                Supplier.objects.create(
                    user=user,
                    name=name,
                    address=address
                )
                return redirect('supplier-list')

    return render(request, 'store/create_supplier.html', {'form': forms})


@method_decorator([login_required(login_url='login'), role_required('supplier')], name='dispatch')
class SupplierListView(ListView):
    model = Supplier
    template_name = 'store/supplier_list.html'
    context_object_name = 'supplier'


@login_required(login_url='login')
@role_required('supplier')
def edit_supplier(request, pk):
    supplier = Supplier.objects.get(pk=pk)

    if request.method == 'POST':
        form = EditSupplierForm(request.POST)
        if form.is_valid():
            supplier.name = form.cleaned_data['name']
            supplier.address = form.cleaned_data['address']
            supplier.user.email = form.cleaned_data['email']
            supplier.user.username = form.cleaned_data['username']
            
            password = form.cleaned_data.get('password')
            if password:
                supplier.user.set_password(password)
            
            supplier.user.save()
            supplier.save()
            return redirect('supplier-list')
    else:
        form = EditSupplierForm(initial={
            'name': supplier.name,
            'address': supplier.address,
            'email': supplier.user.email,
            'username': supplier.user.username,
        })

    return render(request, 'store/edit_supplier.html', {'form': form})


@login_required(login_url='login')
@role_required('supplier')
def delete_supplier(request, pk):
    supplier = Supplier.objects.get(pk=pk)
    supplier.user.delete()  # deletes supplier + user
    return redirect('supplier-list')



# ---------------- BUYER ----------------

@login_required(login_url='login')
@role_required('buyer')
def create_buyer(request):
    forms = BuyerForm()
    if request.method == 'POST':
        forms = BuyerForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']

            if password == retype_password:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    is_buyer=True
                )
                Buyer.objects.create(
                    user=user,
                    name=name,
                    address=address
                )
                return redirect('buyer-list')

    return render(request, 'store/create_buyer.html', {'form': forms})


@method_decorator([login_required(login_url='login'), role_required('supplier')], name='dispatch')
class BuyerListView(ListView):
    model = Buyer
    template_name = 'store/buyer_list.html'
    context_object_name = 'buyer'


@login_required(login_url='login')
@role_required('supplier')
def edit_buyer(request, pk):
    buyer = Buyer.objects.get(pk=pk)

    if request.method == 'POST':
        form = EditBuyerForm(request.POST)
        if form.is_valid():
            buyer.name = form.cleaned_data['name']
            buyer.address = form.cleaned_data['address']
            buyer.user.email = form.cleaned_data['email']
            buyer.user.username = form.cleaned_data['username']
            
            password = form.cleaned_data.get('password')
            if password:
                buyer.user.set_password(password)
            
            buyer.user.save()
            buyer.save()
            return redirect('buyer-list')
    else:
        form = EditBuyerForm(initial={
            'name': buyer.name,
            'address': buyer.address,
            'email': buyer.user.email,
            'username': buyer.user.username,
        })

    return render(request, 'store/edit_buyer.html', {'form': form})


@login_required(login_url='login')
@role_required('supplier')
def delete_buyer(request, pk):
    buyer = Buyer.objects.get(pk=pk)
    buyer.user.delete()  # deletes buyer + user
    return redirect('buyer-list')



# ---------------- SEASON ----------------

@login_required(login_url='login')
def create_season(request):
    forms = SeasonForm()
    if request.method == 'POST':
        forms = SeasonForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('season-list')

    return render(request, 'store/create_season.html', {'form': forms})


class SeasonListView(ListView):
    model = Season
    template_name = 'store/season_list.html'
    context_object_name = 'season'


@login_required(login_url='login')
def edit_season(request, pk):
    season = Season.objects.get(pk=pk)

    if request.method == 'POST':
        form = SeasonForm(request.POST, instance=season)
        if form.is_valid():
            form.save()
            return redirect('season-list')
    else:
        form = SeasonForm(instance=season)

    return render(request, 'store/edit_season.html', {'form': form})


@login_required(login_url='login')
def delete_season(request, pk):
    season = Season.objects.get(pk=pk)
    season.delete()
    return redirect('season-list')



# ---------------- DROP ----------------

@login_required(login_url='login')
def create_drop(request):
    forms = DropForm()
    if request.method == 'POST':
        forms = DropForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('drop-list')

    return render(request, 'store/create_drop.html', {'form': forms})


class DropListView(ListView):
    model = Drop
    template_name = 'store/drop_list.html'
    context_object_name = 'drop'


@login_required(login_url='login')
def edit_drop(request, pk):
    drop = Drop.objects.get(pk=pk)

    if request.method == 'POST':
        form = DropForm(request.POST, instance=drop)
        if form.is_valid():
            form.save()
            return redirect('drop-list')
    else:
        form = DropForm(instance=drop)

    return render(request, 'store/edit_drop.html', {'form': form})


@login_required(login_url='login')
def delete_drop(request, pk):
    drop = Drop.objects.get(pk=pk)
    drop.delete()
    return redirect('drop-list')



# ---------------- PRODUCT ----------------

@login_required(login_url='login')
@role_required('supplier')
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('product-list')

    return render(request, 'store/create_product.html', {'form': forms})


@method_decorator([login_required(login_url='login'), role_required('buyer', 'supplier')], name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'


@login_required(login_url='login')
@role_required('supplier')
def edit_product(request, pk):
    product = Product.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/edit_product.html', {'form': form})


@login_required(login_url='login')
@role_required('supplier')
def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('product-list')



# ---------------- ORDER ----------------

@login_required(login_url='login')
@login_required(login_url='login')
@role_required('buyer')
def create_order(request):
    forms = OrderForm()
    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():
            Order.objects.create(
                supplier=forms.cleaned_data['supplier'],
                product=forms.cleaned_data['product'],
                design=forms.cleaned_data['design'],
                color=forms.cleaned_data['color'],
                buyer=forms.cleaned_data['buyer'],
                season=forms.cleaned_data['season'],
                drop=forms.cleaned_data['drop'],
                status='pending'
            )
            return redirect('order-list')

    return render(request, 'store/create_order.html', {'form': forms})


class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all().order_by('-id')
        elif user.is_supplier:
            return Order.objects.filter(supplier__user=user).order_by('-id')
        elif user.is_buyer:
            return Order.objects.filter(buyer__user=user).order_by('-id')
        else:
            return Order.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # provide status choices to the template for rendering change form
        if user.is_staff or user.is_superuser:
            context['status_choices'] = Order.STATUS_CHOICE
        elif user.is_supplier:
            context['status_choices'] = [('pending', 'Pending'), ('done', 'Done'), ('cancelled', 'Cancelled')]
        else:
            context['status_choices'] = []
        return context


@login_required(login_url='login')
@csrf_exempt
def update_order_status(request, pk):
    # only staff/superuser/supplier can update order status
    if not request.user.is_authenticated:
        return redirect('login')
    # allow staff, superuser, or supplier for their orders
    user = request.user
    can_update = False
    if user.is_staff or user.is_superuser:
        can_update = True
    elif user.is_supplier:
        order = Order.objects.get(pk=pk)
        if order.supplier.user == user:
            can_update = True
    
    if not can_update:
        return redirect('order-list')

    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        # validate status based on user role
        if user.is_staff or user.is_superuser:
            valid_statuses = [s[0] for s in Order.STATUS_CHOICE]
        elif user.is_supplier:
            valid_statuses = ['pending', 'done', 'cancelled']
        else:
            valid_statuses = []
        
        if new_status in valid_statuses:
            order.status = new_status
            order.save()
    return redirect('order-list')



# ---------------- DELIVERY ----------------

@login_required(login_url='login')
def create_delivery(request):
    forms = DeliveryForm()
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('delivery-list')

    return render(request, 'store/create_delivery.html', {'form': forms})


class DeliveryListView(ListView):
    model = Delivery
    template_name = 'store/delivery_list.html'
    context_object_name = 'delivery'
