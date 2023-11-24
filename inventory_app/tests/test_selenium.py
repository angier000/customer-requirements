from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User, Group
from inventory_app.models import Inventory, Owner

SERVER_URL = 'http://127.0.0.1:8000'
#SERVER_URL = self.live_server_url

class Hosttest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

        '''
        # register user
        self.owner_user = User.objects.create_user(username='testusername', email='test@uccs.edu', password='testpassword')
        self.owner_user.first_name = 'testname'
        self.owner_user.save()

        # Add the 'owner' group to the user
        owner_group = Group.objects.create(name='owner') # create new group 'owner'
        self.owner_user.groups.add(owner_group) # assocuate self.user_owner with 'owner' group

        self.inventory = Inventory.objects.create()
        self.owner = Owner.objects.create(user=self.owner_user, inventory=self.inventory)
    
        
        print('debug: ', type(self.driver))
        print('User registered:', self.owner_user.username)
        '''



    def get_server_url(self):
        # Check if running in GitHub Actions
        if os.getenv('GITHUB_ACTIONS'):
            return self.live_server_url
        else:
            return SERVER_URL


    def test_homepage(self):

        server_url = self.get_server_url()
        self.driver.get(server_url)

        self.assertIn("Inventory Tracker", self.driver.title)
        time.sleep(1)




    def test_login_logout(self):
        print('TEST------ In test_login_logout unction')
        server_url = self.get_server_url()
        print('TEST------ server_url = ', server_url)

        self.driver.get(server_url  + '/accounts/register/')

        username_input = self.driver.find_element(By.NAME, 'username')
        email_input = self.driver.find_element(By.NAME, 'email')
        name_input = self.driver.find_element(By.NAME, 'name')
        password1_input = self.driver.find_element(By.NAME, 'password1')
        password2_input = self.driver.find_element(By.NAME, 'password2')

        username_input.send_keys('testusername')
        email_input.send_keys('test@uccs.edu')
        name_input.send_keys('testname')
        password1_input.send_keys('testpassword')
        password2_input.send_keys('testpassword')


        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submit_button.click()


        #self.driver.get(self.live_server_url + '/accounts/login/')
        self.driver.get(server_url  + '/accounts/login/')
        print("Current URL:", self.driver.current_url)
        print("TEST-----------Constructed URL:", server_url + '/accounts/login/')

        # define username and p[assword
        user_name = self.driver.find_element(By.NAME, 'username')
        user_password = self.driver.find_element(By.NAME, 'password')
        submit = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')

        # log in user
        user_name.send_keys('testusername')
        user_password.send_keys('testpassword')
        submit.send_keys(Keys.RETURN)

        time.sleep(3)
        message = self.driver.find_element(By.XPATH, '//span[contains(text(), "Welcome, testusername")]')
        print("Current URL after waiting:", self.driver.current_url)

        # check for welcome message ensuring the correct user is logged in
        time.sleep(3)
        self.assertTrue(message.is_displayed(), "Welcome, testusername")

        # log out user
        logout = self.driver.find_element(By.XPATH, '//a[@href="/accounts/logout/"]')
        logout.click()

        # Verify that the user is redirected to the login page
        login_url = server_url + '/accounts/login/'
        self.assertEqual(self.driver.current_url, login_url, "Logout redirection issue")


        time.sleep(3)



    

    def tearDown(self):
        '''
        # Clean up the test data after the test is complete
        self.owner_user.delete()
        self.owner.delete()
        self.inventory.delete()

        # Remove the user from the 'owner' group
        owner_group = Group.objects.get(name='owner')
        owner_group.user_set.remove(self.owner_user)
        '''

        self.driver.quit