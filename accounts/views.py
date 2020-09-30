from django.shortcuts import render, redirect

from django.forms import inlineformset_factory
#import model data and pass by render
from .models import *
from .forms import OrderForm
from .filters import OrderFilter

# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_order = orders.count()
    
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()

    contex = {'orders' : orders, 'customers' : customers, 
        'total_order' : total_order, 'delivered' : delivered, 'pending' : pending }

    return render(request, 'accounts/dashboard.html', contex)


def products(request):
    products = Product.objects.all()
    return render(request,  'accounts/products.html', {'products':products})


def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs


    context = {'customer':customer , 'orders':orders , 
            'orders_count':orders_count, 'myFilter' : myFilter, }
    return render(request, 'accounts/customer.html', context )



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
    return render(request, 'accounts/order_form.html', context)



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


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request,'accounts/delete.html', context )



