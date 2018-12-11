"""
@package base

WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations

Example:
    wdf = WebDriverFactory(browser)
    wdf.getWebDriverInstance()
"""

import traceback
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
import json


class WebDriverFactory():

    def __init__(self, browser):
        self.browser = browser

    def getWebDriverInstance(self):

        with open('C:\\Users\\frank\\PycharmProjects\\DigiBot\\Json_Files\\config.json') as f:
            data = json.load(f)

        driverLocation = "C:\\Users\\frank\\PycharmProjects\\Lib\\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = driverLocation
        options = Options()

        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')

        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(executable_path=driverLocation, options=options)

        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(10)
        return driver
