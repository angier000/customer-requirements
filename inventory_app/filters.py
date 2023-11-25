import django_filters
from .models import *
from django_filters import CharFilter

# fields for filters.serch
class ItemFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Item
        fields = Itemfields = ('name', 'serial_number')