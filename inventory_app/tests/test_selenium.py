from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SERVER_URL = 'http://127.0.0.1:8000'
#SERVER_URL = self.live_server_url

class Hosttest(LiveServerTestCase):
    def setUp(self):
        #chrome_driver_path = "../chromedriver"
        #chrome_driver_path = os.path.join(os.getcwd(), "chromedriver")
        #os.environ["PATH"] += os.pathsep + chrome_driver_path
        #self.driver = webdriver.Chrome(chrome_driver_path)
        #os.environ["PATH"] += os.pathsep + chrome_driver_path
        self.driver = webdriver.Chrome()
        print('debug: ', type(self.driver))


    def get_server_url(self):
        # Check if running in GitHub Actions
        if os.getenv('GITHUB_ACTIONS'):
            return self.live_server_url
        else:
            return SERVER_URL


    def test_homepage(self):
        print('TEST------ In test_homepage function')
        server_url = self.get_server_url()
        #self.driver.get(self.live_server_url) 
        self.driver.get(server_url)

        self.assertIn("Inventory Tracker", self.driver.title)
        #self.assertIn(1, [1,2,3])
        time.sleep(1)

    def test_login_logout(self):
        print('TEST------ In test_login_logout unction')
        server_url = self.get_server_url()
        print('TEST------ server_url = ', server_url)

        #self.driver.get(self.live_server_url + '/accounts/login/')
        self.driver.get(server_url  + '/accounts/login/')
        print("Current URL:", self.driver.current_url)
        print("TEST-----------Constructed URL:", server_url + '/accounts/login/')

        # define username and p[assword
        user_name = self.driver.find_element(By.NAME, 'username')
        user_password = self.driver.find_element(By.NAME, 'password')
        submit = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')

        # log in user
        user_name.send_keys('testuser')
        user_password.send_keys('inventorytest')
        submit.send_keys(Keys.RETURN)

        # Explicitly wait for the welcome message
        print("Current URL before waiting:", self.driver.current_url)
        wait = WebDriverWait(self.driver, 60)
        message = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Welcome, testuser")]')))
        print("Current URL after waiting:", self.driver.current_url)

        # check for welcome message ensuring the correct user is logged in
        #message = self.driver.find_element(By.XPATH, '//span[contains(text(), "Welcome, testuser")]')
        self.assertTrue(message.is_displayed(), "Welcome, testuser")

        # log out user
        logout = self.driver.find_element(By.XPATH, '//a[@href="/accounts/logout/"]')
        logout.click()

        # Verify that the user is redirected to the login page
        login_url = SERVER_URL + '/accounts/login/'
        self.assertEqual(self.driver.current_url, login_url, "Logout redirection issue")


        time.sleep(3)



    

    def tearDown(self):
        self.driver.quit