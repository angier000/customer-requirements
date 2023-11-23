from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from inventory_app.models import Inventory, Item, Owner
from inventory_app.forms import ItemForm
from django.contrib.auth.models import Group


class TestViews(TestCase):

    def setUp(self):
        self.owner_user = User.objects.create_user(username='testuser', email='test@uccs.edu', password='testpassword')
        self.owner_user.first_name = 'testname'
        self.owner_user.save()

         # Add the 'owner' group to the user
        owner_group = Group.objects.create(name='owner') # create new group 'owner'
        self.owner_user.groups.add(owner_group) # assocuate self.user_owner with 'owner' group

        self.inventory = Inventory.objects.create()
        self.owner = Owner.objects.create(user=self.owner_user, inventory=self.inventory)

        self.url = reverse('create_item', args=[self.inventory.id])
        #self.item = Item.objects.create(name='Test Item', price=10.00)

    def test_create_item_valid_form(self):
        self.client.login(username='testuser', password='testpassword') # log in user
        response = self.client.post(self.url, {'name': 'Test Item', 'price': 10.00})
        print('response: ', response)
        self.assertEqual(response.status_code, 302)
        print('debug: ', response.url)

        # Check that the item was added to the database
        self.assertTrue(Item.objects.filter(name='Test Item').exists())
        self.assertRedirects(response, reverse('inventory-detail', args=[self.inventory.id])) # redirect to inventory page



    def test_register_page(self):
        # send post request to url
        response = self.client.post('/accounts/register/', {
            'username': 'TestUsername',
            'name': 'Test Name',
            'email': 'test@uccs.edu',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        #print('debug: ', response.context['form'].errors)
        
        self.assertEqual(response.status_code, 302)

        # check if owner is created with correct name
        user = User.objects.get(username='TestUsername')
        self.assertTrue(user.groups.filter(name='owner').exists()) # check if assocuated with 'owner' group

        # check if associated owner is created with the correct name and email
        owner = Owner.objects.get(user=user)
        self.assertEqual(owner.name, 'Test Name')
        self.assertEqual(owner.email, 'test@uccs.edu')

        self.assertTrue(owner.inventory is not None) # check for inventory







# reverse('inventory-detail', args=[str(self.id)])


    def test_create_item_unauthenticated_user_get(self):
        self.client.logout() # log out user
        # Attempt to access the view without logging in
        response = self.client.get(self.url)

        # Check that the response status code is 302, indicating a redirect to the login page
        self.assertEqual(response.status_code, 302)
        # Check that the login page is the target of the redirect
        self.assertRedirects(response, reverse('login') + '?next=' + self.url)

    def test_create_item_unauthenticated_user_post(self):
        self.client.logout() # log out user
        response = self.client.post(self.url, {'name': 'Test Name', 'price': 10.00}) # Make a POST request to create a new item
        self.assertRedirects(response, reverse('login') + '?next=' + self.url) # check if redirected to login page
        