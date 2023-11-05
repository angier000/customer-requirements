from django.forms import ModelForm
from .models import Item


#create class for item form
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields =('name', 'price', 'serial_number', 'description', 'image')
        #fields =('name', 'description', 'image')