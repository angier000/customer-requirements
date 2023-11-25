from django.contrib import admin
from .models import Item, Inventory, Owner, Tag

# Register your models here.
admin.site.register(Item)
admin.site.register(Inventory)
admin.site.register(Owner)
admin.site.register(Tag)
