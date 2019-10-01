from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from stable.models import CustomUser
from django.urls import reverse

class LoginClass(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @staticmethod
    def create_user():
        CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )

    def test_login(self):
        LoginClass.create_user()
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))

        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys("William")

        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("testing321")

        self.selenium.find_element_by_xpath('//button[contains(text(), "Login")]').click()
