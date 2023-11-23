from django.test import TestCase
from django.urls import reverse
from inventory_app.models import Item

class TestModels(TestCase):

    def setUp(self):
        self.item = Item.objects.create(name="Test Name", price=10.00)

    # testing if the item name will match the name returned from __str__
    def test_model_str(self):
        item = self.item
        self.assertEqual(str(item), "Test Name") # str calls __str__() from item model


    def test_item_get_absolute_url(self):
        item = self.item
        expected_url = reverse('item-detail', args=[str(item.id)])
        self.assertEqual(item.get_absolute_url(), expected_url)