from Utilities import custom_logger as cl
from Base.basepage import BasePage
import logging
from Captcha.Harvester import harvest
from Captcha.Fetch import main as getToken
import time
from selenium.webdriver.support.select import Select
import json

class CheckoutPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _recaptcha = "g-recaptcha"
    _email = "checkout_email"
    _first_name = "checkout_shipping_address_first_name"
    _last_name = "checkout_shipping_address_last_name"
    _shipping_address = "checkout_shipping_address_address1"
    _apartment = "checkout_shipping_address_address2"
    _city = "checkout_shipping_address_city"
    _shipping_country_option = "United States"
    _zip = "checkout_shipping_address_zip"
    _state = "checkout_shipping_address_province"
    _phone = "checkout_shipping_address_phone"
    _shipping_method_button = "icon-svg--spinner-button"   #class
    _continue_to_payment_method = "icon-svg--spinner-button" #class
    g_recaptcha_response = "g-recaptcha-response"
    _iframe_credit_card_number = ""
    _nameOnCard_iframe = "card-fields-iframe:first:child"
    _nameOnCard = "name"
    _creditCardNumber = "number"
    _expDate = "expiry"
    _cvv = "verification_value"
    _completeOrderBtn = ".step__footer__continue-btn .btn__content" #css
    _webScroll = "step__footer__previous-link-content"

    def queueBypass(self):
        checkoutToken = self.driver.execute_script("return DF_CHECKOUT_TOKEN")   # still working on this, supposed to bypass queue if there is one

    #checks if there is a queue and checks the page till the user gets past
    def checkWaitingInQueue(self):
        currentUrl = self.getCurrentUrl()
        queue = 'queue'
        if queue in currentUrl:
            print("Waiting in queue")
            self.queueBypass()
        else:
            print("Passed queue")

    def getData(self):
        with open('C:\\Users\\frank\\PycharmProjects\\DigiBot\\Json_Files\\config.json') as f:
            data = json.load(f)
        return data

    #checks if there is google recaptcha, and if there is, the user has to solve in another window
    def checkForCaptcha(self):
        Present = self.isElementPresent(self._recaptcha)
        return Present

    #actually the solving captcha method
    def solveCaptcha(self):
        data = self.getData()
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        print("Solving Captcha")
        s = harvest('6LeoeSkTAAAAAA9rkZs5oS82l69OEYjKRZAiKdaF', 'http://' + data["store"] + '.com/random', '127.0.0.1', self.driver)
        s.solve()
        serverIP = '127.0.0.1'
        token = getToken(serverIP)
        print('Token : ' + token)
        self.driver.switch_to.window(self.driver.window_handles[0])
        return token

    #enters shipping
    def enteringShipping(self, email, firstName, lastName, address, apartment, state, city, zipcode, phone):
        Present = self.checkForCaptcha()
        token = None
        if Present is True:
            token = self.solveCaptcha()

        #entering shipping details
        self.sendKeys(email, locator=self._email, locatorType='id')
        self.sendKeys(firstName, locator=self._first_name, locatorType='id')
        self.sendKeys(lastName, locator=self._last_name, locatorType='id')
        self.sendKeys(address, self._shipping_address, locatorType='id')
        self.webScroll(self._webScroll, locatorType='class')
        self.sendKeys(apartment, self._apartment, locatorType='id')

        select = Select(self.driver.find_element_by_id(self._state))
        select.select_by_value(state)

        self.sendKeys(city, locator=self._city, locatorType='id')
        self.sendKeys(zipcode, locator=self._zip, locatorType='id')
        self.sendKeys(phone, locator=self._phone, locatorType='id')

        if Present is True:
            # Posting the recaptcha validation token in the g-recaptcha-reponse text box
            self.driver.execute_script("document.getElementById('g-recaptcha-response').style.display = 'block';")
            self.sendKeys(token, locator=self.g_recaptcha_response, locatorType='id')

        self.elementClick(locator=self._shipping_method_button, locatorType='class')

        print("Going to shipping method")

        self.elementClick(locator=self._continue_to_payment_method, locatorType='class')

        print("Going to payment")

    #enters payment, but need to actually be done through a server... for a later time
    def enteringPayment(self, nameOnCard, cardNumber, expMonth, expYear, CVV):
        time.sleep(1)
        self.switchToFrame()
        self.sendKeys(cardNumber, locator=self._creditCardNumber, locatorType='id')
        self.sendKeys(nameOnCard, locator=self._nameOnCard, locatorType='id')
        self.sendKeys(expMonth, locator=self._expDate, locatorType='id')
        self.sendKeys(expYear, locator=self._expDate, locatorType='id')
        self.sendKeys(CVV, locator=self._cvv, locatorType='id')
        self.webScroll(self._webScroll, locatorType='class')

    #don't call this function if you don't wanna actually order something
    def submitPayment(self):
        self.elementClick(locator=self._completeOrderBtn, locatorType='xpath')

