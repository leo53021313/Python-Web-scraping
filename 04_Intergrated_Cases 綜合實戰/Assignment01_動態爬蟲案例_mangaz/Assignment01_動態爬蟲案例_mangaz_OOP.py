from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

class Scrape:

    def __init__(self, link):
        self.link = link
        self.options = self.create_options()
        pass

    def create_options(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        return options

    def open_browser(self):
        driver = webdriver.Chrome(self.options)
        pass

    def start_scrape(self):
        pass

    def close_browser(self):
        pass