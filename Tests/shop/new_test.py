# from Pages.home.login_page import LoginPage
from Pages.shop.new_page_two import NewShoePage
from Pages.shop.product_page import ProductPage
from Pages.shop.checkout_page import CheckoutPage
from Captcha.LoginChrome import ChromeLogin
import unittest
import pytest
import json
from Utilities.teststatus import TestStatus

@pytest.mark.useFixtures("oneTimeSetUp", "setUp")
class NewPageTests(unittest.TestCase):

    #calls the classes
    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.nsp = NewShoePage(self.driver)
        self.pp = ProductPage(self.driver)
        self.cp = CheckoutPage(self.driver)
        self.ts = TestStatus(self.driver)
        self.cl = ChromeLogin(self.driver)

    #gets the data from the config.json that you modified
    def getData(self):
        with open('C:\\Users\\frank\\PycharmProjects\\DigiBot\\Json_Files\\config.json') as f:
            data = json.load(f)
        return data

    #calling all functions within classes and running them through py.test using config.json data
    @pytest.mark.run(order=1)
    def test_productData(self):
        data = self.getData()
        self.cl.login()
        self.cl.redirectToStore(data["store"])
        productFound = self.nsp.searchForKeywords(keywords=data["keywords"], monitorDelay=data["monitorDelay"])
        self.nsp.redirectToProductPage(productFound)
        self.pp.addToCart(size=data["size"])
        self.pp.checkForStock(monitorDelay=data["monitorDelay"])
        self.cp.checkWaitingInQueue()
        self.cp.enteringShipping(data["email"], data["firstName"], data["lastName"], data["streetAddress"], data["apartmentNumber"], data["state"],
                                 data["city"], data["zipCode"], data["phoneNumber"])
        self.cp.enteringPayment(data["nameOnCard"], data["cardNumber"], data["expMonth"], data["expYear"], data["cvv"])


