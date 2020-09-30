import django_filters
from django_filters import DateFilter
# from django_filters import CharField

from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    end_date = DateFilter(field_name="date_created", lookup_expr='lte')
    # for carecter field search
    # note = CharField(field_name='note', lookup_expr='icontains')


    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer','date_created']