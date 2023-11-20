from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import ItemForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


#@login_required(login_url='login') # if user is not logged in, send to login page
#@allowed_users(allowed_roles=['owner']) # once logged in only users in allowed_roles can access home page
def index(request):
    return render( request, 'inventory_app/index.html')

class ItemListView(generic.ListView):
    model = Item
    
class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Item

@login_required(login_url='login') # if user not authentucated, refirect to login page
@allowed_users(allowed_roles=['owner']) # once logged in only users in allowed_roles can access home page
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

@login_required(login_url='login') # if user not authentucated, refirect to login page
@allowed_users(allowed_roles=['owner']) # once logged in only users in allowed_roles can access home page
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

@login_required(login_url='login') # if user not authentucated, refirect to login page
@allowed_users(allowed_roles=['owner']) # once logged in only users in allowed_roles can access home page
def deleteItem(request, item_id):
    # get specified item
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        item.delete()
        return redirect('items')
    
    context = {'item': item}
    return render(request, 'inventory_app/item_delete.html', context)



@unauthenticated_user # if authenticated user tries to access login page, redirect to home page
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='owner')
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
    
    context ={'form':form}
    return render(request, 'registration/register.html', context)

'''
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'registration/login.html', context)
'''


@unauthenticated_user # redirect to home page if authrnticated user tries to go to login page
# runs refault login view
def loginPage(request):
    # redirects user to login page if not logged in
    return LoginView.as_view()(request)


def logoutUser(request):
    logout(request)
    return redirect('login')
