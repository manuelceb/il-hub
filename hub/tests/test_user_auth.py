from django.test import TestCase
from allauth.socialaccount.models import SocialApp
from .factories import UserFactory


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.login_url = "/hub/login/"

        self.user = UserFactory(
            email="test@example.com",
            password="password123",
        )

        # SocialApp is required only because the login template renders
        # the Google social-login provider.
        SocialApp.objects.create(
            provider="google",
            name="Google Test",
            client_id="test-client-id",
            secret="test-secret",
        )

    # Authentication tests
    def test_user_can_login_with_valid_credentials(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "test@example.com",
                "password": "password123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/hub/",
        )
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            self.user.pk,
        )

    def test_user_cannot_login_with_invalid_password(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "test@example.com",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )

    def test_inactive_user_cannot_login(self):
        self.user.is_active = False
        self.user.save()

        response = self.client.post(
            self.login_url,
            {
                "username": "test@example.com",
                "password": "password123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_unregistered_user_cannot_login(self):
        response = self.client.post(
            self.login_url,
            {
                "username": "unknown@example.com",
                "password": "password123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_unauthenticated_user_cannot_access_home(self):
        response = self.client.get("/hub/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/hub/login/", response.url)

    def test_authenticated_user_can_access_home(self):
        self.client.force_login(self.user)

        response = self.client.get("/hub/")

        self.assertEqual(response.status_code, 200)
