from django.forms import ModelForm
from .models import Item, Owner, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


#create class for item form
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields =('name', 'price', 'serial_number', 'description', 'image')

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class CreateUserForm(UserCreationForm):
    name = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']

class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'
        exclude = ['user', 'inventory']