from Utilities import custom_logger as cl
import logging
from Base.basepage import BasePage
import time

# FOR UNDEFEATED ONLY AS OF NOW, not for project
class LoginPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locaters
    _user_email = "customer_email"
    _user_password = "customer_password"
    _login_button = "//button[contains(text(),'Login')]"    # xpath
    _signed_in = "view_address"
    _signed_in_false = "alert alert-error"
    _shop_button_hover = "//div[@class='collapse navbar-collapse']//span[contains(text(),'Shop')]"
    _shop_button_link = "NEW"


    def enterEmail(self, email):
        self.sendKeys(email, self._user_email)

    def enterPassword(self, password):
        self.sendKeys(password, self._user_password)

    def clickLoginButton(self):
        self.elementClick(self._login_button, locatorType="xpath")

    def login(self, email="", password=""):
        print("Logging in")
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickLoginButton()

    def verifyLoginSuccess(self):
        result = self.isElementPresent("view_address")
        return result

    def verifyLoginFailed(self):
        result = self.isElementPresent("//div[@class='alert alert-error']",
                                       locatorType="xpath")
        return result

    def redirectToShop(self):
        self.driver.get("https://undefeated.com/sitemap_products_1.xml")

    def loginAndRedirect(self, email="", password=""):
        self.login(email, password)
        self.redirectToShop()

