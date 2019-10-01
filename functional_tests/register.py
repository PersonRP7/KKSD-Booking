from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from stable.models import CustomUser
from django.urls import reverse

class RegisterClass(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_register(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/register/'))

        modal_input = self.selenium.find_element_by_xpath('//button[contains(text(), "OK")]').click()

        password1 = self.selenium.find_element_by_name("password1")
        password1.send_keys("testing321")

        password2 = self.selenium.find_element_by_name("password2")
        password2.send_keys("testing321")

        captcha = self.selenium.find_element_by_name("captcha")
        captcha.send_keys("No")

        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys("William")

        first_name = self.selenium.find_element_by_name("first_name")
        first_name.send_keys("William")

        last_name = self.selenium.find_element_by_name("last_name")
        last_name.send_keys("Williamson")

        button = self.selenium.find_element_by_xpath('//button[contains(text(), "Register")]').click()
