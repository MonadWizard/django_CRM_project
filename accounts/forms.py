from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        # fields = ["customer","product"]
        fields = '__all__'