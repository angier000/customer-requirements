from django.forms import ModelForm
from .models import Item, Owner
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#create class for item form
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields =('name', 'price', 'serial_number', 'description', 'image')

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'
        exclude = ['user', 'inventory']