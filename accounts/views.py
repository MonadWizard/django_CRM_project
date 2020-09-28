from django.shortcuts import render

#import model data and pass by render
from .models import *

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


def customers(request):
    return render(request, 'accounts/customer.html' )













