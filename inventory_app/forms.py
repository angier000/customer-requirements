from django.forms import ModelForm
from .models import Item, Owner, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


#create class for item form
class ItemForm(ModelForm):
    price = forms.CharField(max_length=200, label='price/estimate')

    class Meta:
        model = Item
        fields =('name', 'price', 'serial_number', 'description', 'image')

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class CreateUserForm(UserCreationForm):
    name = forms.CharField(max_length=200)

    INSURANCE_CHOICES = [
        (None, 'Select an option'),
        ('StateFarm', 'State Farm'),
        ('Allstate', 'Allstate'),
        ('USAA', 'USAA'),
        ('Lemonade', 'Lemonade'),
        ('Nationwide', 'Nationwide'),
        ('LibertyMutual', 'Liberty Mutual'),
        ('Travelers', 'Travelers'),
    ]
    insurance = forms.ChoiceField(choices=INSURANCE_CHOICES, required=False, label='Insurance (optional)')

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'insurance', 'password1', 'password2']

class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'
        exclude = ['user', 'inventory']