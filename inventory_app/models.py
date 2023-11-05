from django.db import models
from django.urls import reverse

class Item(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    # inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, default = None)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('item-detail', args=[str(self.id)])
