import django_filters
from .models import *
from django_filters import CharFilter
from .forms import * 

# fields for filters.serch
class ItemFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tag',
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        conjoined=True
    )

    class Meta:
        model = Item
        fields = Itemfields = ('name',)