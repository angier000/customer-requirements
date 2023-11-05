from django.db import models
from django.urls import reverse

class Item(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    # inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, default = None)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('item-detail', args=[str(self.id)])
