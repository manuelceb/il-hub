from django.test import TestCase
from hub.api_errors import ClientHandlerNotConfigured, ContextualProfileNotFound
from hub.models import LibraryInterestTopics
from hub.profile_services import get_user_profile

from .factories import UserFactory


class ContextProfileServiceTests(TestCase):
    def setUp(self):
        self.user = UserFactory(
            email="test@example.com",
            password="password123",
        )

        # library context is created by the User post_save signal
        self.library_profile = self.user.library_context
        self.library_profile.nickname = "Test Reader"
        self.library_profile.email_notifications = True
        self.library_profile.save()

    def test_library_profile_is_retrieved(self):
        data = get_user_profile(
            user=self.user,
            client_name="library",
        )

        self.assertEqual(
            data["client"],
            "library",
        )

        self.assertEqual(
            data["profile"]["nickname"],
            "Test Reader",
        )

        self.assertTrue(data["profile"]["email_notifications"])

    def test_response_contains_correct_user_uid(self):
        data = get_user_profile(
            user=self.user,
            client_name="library",
        )

        self.assertEqual(
            str(data["user_uid"]),
            str(self.user.user_uid),
        )

    def test_library_interest_topics_are_serialized(self):
        topic_1 = LibraryInterestTopics.objects.create(topics="Cybersecurity")

        topic_2 = LibraryInterestTopics.objects.create(topics="Artificial Intelligence")

        self.library_profile.interest_topics.add(
            topic_1,
            topic_2,
        )

        data = get_user_profile(
            user=self.user,
            client_name="library",
        )

        self.assertCountEqual(
            data["profile"]["interest_topics"],
            [
                "Cybersecurity",
                "Artificial Intelligence",
            ],
        )

    def test_unknown_client_raises_handler_not_configured(self):
        with self.assertRaises(ClientHandlerNotConfigured):
            get_user_profile(
                user=self.user,
                client_name="unknown-client",
            )

    def test_missing_profile_raises_contextual_profile_not_found(self):
        self.library_profile.delete()

        with self.assertRaises(ContextualProfileNotFound):
            get_user_profile(
                user=self.user,
                client_name="library",
            )
