from django.test import TestCase
from django.core import mail
from django.urls import reverse
from stable.models import CustomUser, SiteWideMessages, PM


class TestUser(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )

        SiteWideMessages.objects.create(
            subject = "Subject one.",
            message = "Message one."
        )
    def test_public_message_exists(self):
        self.assertTrue(SiteWideMessages.objects.count() > 0)

    def test_user_exists(self):
        user = CustomUser.objects.get(username = "William")
        self.assertEqual(user.username, "William")

    def test_default_public_messages_unread(self):
        user = CustomUser.objects.get(username = "William")
        self.assertEqual(user.public_status, "unread")

    def test_to_read(self):
        CustomUser.to_read(username = "William")
        user = CustomUser.objects.get(username = "William")
        self.assertEqual(user.public_status, "read")

    def test_to_unread(self):
        CustomUser.to_unread()
        user = CustomUser.objects.get(username = "William")
        self.assertEqual(user.public_status, "unread")

    def test_default_account_confirmation_waiting(self):
        user = CustomUser.objects.get(username = "William")
        self.assertEqual(user.confirmation, "waiting")

class TestPM(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )
        user = CustomUser.objects.get(username = "William")
        PM.objects.create(
            to = user,
            subject = "Private message subject",
            message = "Private message, message."
        )

    def test_pm_default_unread(self):
        user = CustomUser.objects.get(username = "William")
        pm_object = PM.objects.get(to = user, read = False)
        self.assertTrue(pm_object)
