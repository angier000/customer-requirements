import django_filters
from .models import *

# fields for filters.serch
class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = Itemfields = ('name', 'serial_number')