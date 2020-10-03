from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # restiction login
from django.contrib import messages  # for flash message
from django.contrib.auth.models import Group  # add user to group

from django.forms import inlineformset_factory
#import model data and pass by render
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_user, admin_only

# Create your views here.

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            #get userName
            username = form.cleaned_data.get('username')

            # auto add register username to customer group
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            # auto add register customer username to user 
            Customer.objects.create(
                user = user,
                name=user.username,
            )

            messages.success(request, "Account was created for " + username)

            return redirect("login")

    context = {'form':form }
    return render(request, 'accounts/register.html', context)



@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect !')

    context = {}
    return render(request, 'accounts/login.html', context)



def logoutUser(request):
    logout(request)

    return redirect('login')


@allowed_user(allowed_rools=['customer'])
@login_required(login_url='login')
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_order = orders.count()    
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    # print('ORDERS', orders, )

    context = {'orders':orders, 'total_order' : total_order, 
                'delivered' : delivered, 'pending' : pending }
    return render(request, 'accounts/user.html', context)


@allowed_user(allowed_rools=['customer'])
@login_required(login_url='login')
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
        
    if request.method == "POST":

        form = CustomerForm(request.POST, request.FILES , instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)



@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_order = orders.count()    
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()

    contex = {'orders' : orders, 'customers' : customers, 
        'total_order' : total_order, 'delivered' : delivered, 'pending' : pending }

    return render(request, 'accounts/dashboard.html', contex)


@allowed_user(allowed_rools=['admin'])
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request,  'accounts/products.html', {'products':products})


@allowed_user(allowed_rools=['admin'])
@login_required(login_url='login')
def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs


    context = {'customer':customer , 'orders':orders , 
            'orders_count':orders_count, 'myFilter' : myFilter, }
    return render(request, 'accounts/customer.html', context )




@login_required(login_url='login')
def createOrderCustomet(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order,
                    fields=('product','status'), extra=7)  # (parentModel, ChildModel)

    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == "POST":

        formset = OrderFormSet(request.POST,instance=customer)
        # form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/order_form_customer.html', context)



@allowed_user(allowed_rools=['admin'])
@login_required(login_url='login')
def createOrder(request):

    form = OrderForm()
    if request.method == "POST":
        #print("printing post : ",request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)



@allowed_user(allowed_rools=['admin'])
@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        #print("printing post : ",request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


@allowed_user(allowed_rools=['admin'])
@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request,'accounts/delete.html', context )



