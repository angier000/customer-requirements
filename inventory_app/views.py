from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views import generic

# Create your views here.

def index(request):
    return render( request, 'inventory_app/index.html')

class ItemListView(generic.ListView):
    model = Item\
    
class ItemDetailView(generic.DetailView):
    model = Item
