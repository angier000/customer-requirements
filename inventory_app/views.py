from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import ItemForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, item_permission
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import ItemFilter

#test
from django.conf import settings


# Create your views here.


#@login_required(login_url='login') # if user is not logged in, send to login page
#@allowed_users(allowed_roles=['owner']) # once logged in only users in allowed_roles can access home page
def index(request):
    #print('Django Application Database Path:', settings.DATABASES['default']['NAME'])
    return render( request, 'inventory_app/index.html')

class ItemListView(generic.ListView):
    model = Item
    
class ItemDetailView(generic.DetailView):
    model = Item

@login_required(login_url='login') # if user not authentucated, refirect to login page
@allowed_users(allowed_roles=['owner']) # once logged in only users in allowed_roles can access home page
@item_permission
def createItem(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    form = ItemForm()

    print('inventory: ', inventory.id)

    if request.method == 'POST':
        
        # create new item, this is what's being submitted
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():

            item = form.save(commit=False) # create model with input data but don't save yet
            item.inventory = inventory # set relationship to appropriate inventory
            
            # save to database
            item.save()

            # Get the tags from the form data
            tag_ids = request.POST.getlist('tags')

            # Associate the tags with the item
            item.tag.set(Tag.objects.filter(id__in=tag_ids))

            print(form.cleaned_data['image'])

            # Redirect back to the item list page
            return redirect('inventory-detail', inventory_id)
    
    context = {'form': form, 'inventory':inventory}
    return render(request, 'inventory_app/item_form.html', context)

@login_required(login_url='login') # if user not authentucated, refirect to login page
@allowed_users(allowed_roles=['owner']) # once logged in only users in allowed_roles can access home page
@item_permission
def updateItem(request, inventory_id, item_id):
    # get specified item and inventory
    inventory = get_object_or_404(Inventory, id=inventory_id)
    item = get_object_or_404(Item, pk=item_id)

    # Pass the current tags of the item to the form
    initial_tags = item.tag.all().values_list('id', flat=True)

    # fill form with specified item's data
    form = ItemForm(instance=item, initial={'tags': initial_tags})

    if request.method == 'POST':
        # set updated data to specific instance of item
        form = ItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            # save new instance to database
            form.save()

            # Get the tags from the form data
            tag_ids = request.POST.getlist('tags')

            # Associate the tags with the item
            item.tag.set(Tag.objects.filter(id__in=tag_ids))

            # Redirect back to the item list page
            return redirect('inventory-detail', inventory_id)
    
    context = {'form': form}
    return render(request, 'inventory_app/item_form.html', context)

@login_required(login_url='login') # if user not authentucated, refirect to login page
@allowed_users(allowed_roles=['owner']) # once logged in only users in allowed_roles can access home page
@item_permission
def deleteItem(request, inventory_id, item_id):
    # get specified item and inventory
    inventory = get_object_or_404(Inventory, id=inventory_id)
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        item.delete()
        return redirect('inventory-detail', inventory_id)
    
    context = {'item': item}
    return render(request, 'inventory_app/item_delete.html', context)



class InventoryDetailView(generic.DetailView):
    model = Inventory

    # override get_context_data method, change context data that will be passed to template
    def get_context_data(self, **kwargs):

        # call method parent class (InventoryDetailView) and get data from original method
        context = super().get_context_data(**kwargs)

        #context['user'] = self.request.user 

        # get current inventory
        current_inventory = self.get_object()

        # get items associated with current inventory
        #items = Item.objects.filter(inventory=current)

        # gets all items associated with current inventory (queryset)
        # request.get is the filter criteria selected by user, and apply to queryset
        # .item_set - access related item of n inventory
        item_filter = ItemFilter(self.request.GET, queryset=current_inventory.item_set.all())

        # add context info
        context['item_filter'] = item_filter
        context['items'] = item_filter.qs

        # return updated context
        return context
    

class OwnerListView(generic.ListView):
    model = Owner


@unauthenticated_user # if authenticated user tries to access login page, redirect to home page
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save() # create user
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='owner')
            user.groups.add(group) # add user to owner group

            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email') 

            owner = Owner.objects.create(user=user, name=name, email=email) # create associated owner
            inventory = Inventory.objects.create() # create an empty inventory
            owner.inventory = inventory # associate inventory with owner
            owner.save()

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


@login_required(login_url='login') # if user not authentucated, refirect to login page
@allowed_users(allowed_roles=['owner']) # once logged in only users in allowed_roles can user page
def userPage(request):
    owner = request.user.owner
    print('owner: ', owner)
    inventory = owner.inventory
    print('inventory id: ', inventory.id)
    context = {'inventory':inventory, 'owner':owner}
    return render(request, 'inventory_app/user.html', context)


@unauthenticated_user # redirect to home page if authrnticated user tries to go to login page
# runs refault login view
def loginPage(request):
    # redirects user to login page if not logged in
    return LoginView.as_view()(request)


def logoutUser(request):
    logout(request)
    return redirect('login')
