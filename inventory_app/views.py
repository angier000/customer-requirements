from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import ItemForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    return render( request, 'inventory_app/index.html')

class ItemListView(generic.ListView):
    model = Item
    
class ItemDetailView(generic.DetailView):
    model = Item

def createItem(request):
    form = ItemForm()

    if request.method == 'POST':
        # create new item, this is what's being submitted
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            # save to database
            form.save()

            print(form.cleaned_data['image'])

            # Redirect back to the item list page
            return redirect('items')
    
    context = {'form': form}
    return render(request, 'inventory_app/item_form.html', context)

def updateItem(request, item_id):
    # get specified item
    item = get_object_or_404(Item, pk=item_id)

    # fill form with specified item's data
    form = ItemForm(instance=item)

    if request.method == 'POST':
        # set updated data to specific instance of item
        form = ItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            # save new instance to database
            form.save()

            # Redirect back to the item list page
            return redirect('items')
    
    context = {'form': form}
    return render(request, 'inventory_app/item_form.html', context)

def deleteItem(request, item_id):
    # get specified item
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        item.delete()
        return redirect('items')
    
    context = {'item': item}
    return render(request, 'inventory_app/item_delete.html', context)


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

    context ={'form':form}
    return render(request, 'registration/register.html', context)

