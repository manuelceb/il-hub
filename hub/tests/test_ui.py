from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from allauth.socialaccount.models import SocialApp
from .factories import UserFactory


class UserAuthenticationFunctionalTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("-headless")
        service = Service(executable_path="/snap/bin/firefox.geckodriver")
        cls.browser = webdriver.Firefox(
            service=service,
            options=options,
        )
        cls.browser.implicitly_wait(2)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):

        self.browser.delete_all_cookies()
        self.user = UserFactory(
            email="test@example.com",
            password="password123",
        )

        # Required for rendering purposes as detailed in functional tests
        SocialApp.objects.create(
            provider="google",
            name="Google Test",
            client_id="test-client-id",
            secret="test-secret",
        )

    def test_user_can_login_through_browser(self):
        self.browser.get(f"{self.live_server_url}/hub/login/")

        username = self.browser.find_element(
            By.NAME,
            "username",
        )
        password = self.browser.find_element(
            By.NAME,
            "password",
        )
        username.send_keys("test@example.com")
        password.send_keys("password123")
        password.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 5).until(
            EC.url_to_be(f"{self.live_server_url}/hub/")
        )

        self.assertEqual(
            self.browser.current_url,
            f"{self.live_server_url}/hub/",
        )

    def test_unauthenticated_user_cannot_access_dashboard(self):
        self.browser.get(f"{self.live_server_url}/hub/")

        WebDriverWait(self.browser, 5).until(EC.url_contains("/hub/login/"))

        self.assertIn(
            "/hub/login/",
            self.browser.current_url,
        )
