from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('products', views.products, name="products"),
    path('customer/<str:pk_test>/', views.customers, name="customer"),

    
    path('create_order_customer/<str:pk>/', views.createOrderCustomet, name="create_order_customer"),
    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    

]
