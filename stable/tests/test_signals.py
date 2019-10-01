from django.test import TestCase
from stable.models import SiteWideMessages
from stable.signals import all_to_unread
from unittest.mock import patch
from django.db.models.signals import post_save

class TestAllToUnread(TestCase):

    def test_post_save_signal(self):
        with patch('stable.signals.all_to_unread', autospec=True) as mocked_handler:
            post_save.connect(mocked_handler, sender = SiteWideMessages)
            SiteWideMessages.objects.create(
                subject = "subject",
                message = "message"
            )

        self.assertEqual(mocked_handler.call_count, 1)
