#this file searches for the product on the current site through its xml file
from Utilities import custom_logger as cl
from Base.basepage import BasePage
import logging
import time
import re

class ProductPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    checkoutPage = "checkout_shipping_address_first_name"

    #variants are long numbers that are assigned to every product, and every size of that product, this pulls size variants
    def pullVariantsShoe(self):
        self.driver.implicitly_wait(15)
        print("Pulling variants")
        meta = self.driver.execute_script('return meta')
        variantsLength = len(meta["product"]["variants"])
        variantDict = {}

        for variant in range(variantsLength):
            meta = self.driver.execute_script('return meta')
            metaVariant = meta["product"]["variants"][variant]["id"]
            variantSizePublicName = meta["product"]["variants"][variant]["public_title"]
            variantSize = re.findall('\d*\.?\d+',variantSizePublicName)[0]
            variantDict.update({variantSize: metaVariant})

        print(variantDict)
        return variantDict

    # def pullVariantsShoe(self):
    #
    #     html = self.driver.page_source
    #     soup = BeautifulSoup(html, 'lxml')
    #     productName = soup.find('title').text
    #     print(productName)
    #
    #     print("Pulling variants")
    #     sizeToVariantDict = {}
    #     for variant in soup.find_all('variant'):
    #         variantId = variant.find('id', type="integer").text
    #         variantSize = variant.find('option1').text          # change for option 2 for most sites
    #         sizeToVariantDict.update({variantSize:variantId})
    #
    #     return sizeToVariantDict

    #adds the product to cart using http requests, you can add a sold out item too
    def addToCart(self, size):
        print("Adding to cart")
        domain = self.driver.execute_script("return document.domain")
        variantDict = self.pullVariantsShoe()
        variant = variantDict[str(size)]
        self.driver.get("http://" + domain + "/cart/" + str(variant) + ":1")
        print("Added to cart")

    #if an item is out of stock, it refreshes every monitor delay you set in seconds, until back in stock
    def checkForStock(self, monitorDelay):
        currentUrl = self.getCurrentUrl()
        stock_problems = "stock_problems"
        outOfStock = True
        while outOfStock is True:
            if stock_problems in currentUrl:
                print("Sold Out, retrying...")
                time.sleep(monitorDelay)
                self.driver.refresh()
                outOfStock = True
            else:
                print("In Stock")
                outOfStock = False
