from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
    

class Inventory(models.Model):
    #title = models.CharField(max_length = 200)
    #about = models.TextField(blank = True)
    #owner = models.OneToOneField(Owner, on_delete=models.CASCADE, unique=True, null=True)

    #def __str__(self):
    #    return self.title
    
    def get_absolute_url(self):
        return reverse('inventory-detail', args=[str(self.id)])


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    inventory = models.OneToOneField(Inventory, on_delete=models.CASCADE, unique=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True)
    tag = models.ManyToManyField(to=Tag, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('item-detail', args=[str(self.id)])
    