from selenium import webdriver
from django.test import LiveServerTestCase


class Hosttest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_homepage(self):
        #self.driver.get(self.live_server_url) # http://127.0.0.1:8000/
        self.driver.get('http://127.0.0.1:8000/')

        self.assertIn("Inventory Tracker", self.driver.title)
        #self.assertIn(1, [1,2,3])

    def tearDown(self):
        self.driver.quit