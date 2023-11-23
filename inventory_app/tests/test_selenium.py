from selenium import webdriver
from django.test import LiveServerTestCase
import os


class Hosttest(LiveServerTestCase):
    def setUp(self):
        #chrome_driver_path = "../chromedriver"
        #chrome_driver_path = os.path.join(os.getcwd(), "chromedriver")
        #os.environ["PATH"] += os.pathsep + chrome_driver_path
        #self.driver = webdriver.Chrome(chrome_driver_path)
        #os.environ["PATH"] += os.pathsep + chrome_driver_path
        self.driver = webdriver.Chrome()

    def test_homepage(self):
        #self.driver.get(self.live_server_url + ':8000')
        self.driver.get(self.live_server_url) 
        #self.driver.get('http://127.0.0.1:8000/')

        self.assertIn("Inventory Tracker", self.driver.title)
        #self.assertIn(1, [1,2,3])

    def tearDown(self):
        self.driver.quit