#this file searches for products on the site using the xml page all Shopify sites have except yeezysupply and kith which use .atam
from Utilities import custom_logger as cl
from Base.basepage import BasePage
import logging
import time
from bs4 import BeautifulSoup
import re
import json
import bs4

class NewShoePage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # gets the data from the config.json that you modified
    def getData(self):
        with open('C:\\Users\\frank\\PycharmProjects\\DigiBot\\Json_Files\\config.json') as f:
            data = json.load(f)
        return data


    #searches the entire site for a product with a certain keyword or keywords, I use regex in these
    def searchForKeywords(self, keywords, monitorDelay):
        print("Keywords are:")
        print(keywords)

        if len(keywords) == 1:
            keyword1 = re.escape(keywords[0])

            print("Searching for product...")
            keywordLinkFound = False
            while keywordLinkFound is False:
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                try:
                    keywordLink = soup.find('image:title', text=re.compile(keyword1))
                    print(keywordLink.text)
                    url = keywordLink.parent.parent
                    keywordLink = url.find('loc').text
                    return keywordLink
                except AttributeError:
                    print("Product not found on site, retrying...")
                    time.sleep(monitorDelay)
                    self.driver.refresh()

        elif len(keywords) == 2:
            keyword1 = keywords[0]
            keyword2 = keywords[1]

            print("Searching for product...")
            keywordLinkFound = False
            while keywordLinkFound is False:
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                try:
                    regexp = "%s.*%s|%s.%s" % (keyword1, keyword2, keyword2, keyword1)
                    keywordLink = soup.find('image:title', text=re.compile(regexp))
                    print(keywordLink.text)
                    url = keywordLink.parent.parent
                    keywordLink = url.find('loc').text
                    return keywordLink
                except AttributeError:
                    print("Product not found on site, retrying...")
                    time.sleep(monitorDelay)
                    self.driver.refresh()

        elif len(keywords) == 3:
            keyword1 = re.escape(keywords[0])
            keyword2 = re.escape(keywords[1])
            keyword3 = re.escape(keywords[2])

            print("Searching for product...")
            keywordLinkFound = False
            while keywordLinkFound is False:
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                try:
                    regexp = "%s.*%s|%s.%s|%s.%s" % (keyword1, keyword2, keyword3, keyword3, keyword2, keyword1)
                    keywordLink = soup.find('image:title', text=re.compile(regexp))
                    print(keywordLink.text)
                    url = keywordLink.parent.parent
                    keywordLink = url.find('loc').text
                    return keywordLink
                except AttributeError:
                    print("Product not found on site, retrying...")
                    time.sleep(monitorDelay)
                    self.driver.refresh()

    #once a product is found, it will redirect to that product's page
    def redirectToProductPage(self, url):
        Url = str(url)
        self.driver.get(Url)
