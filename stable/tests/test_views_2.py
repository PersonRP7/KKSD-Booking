from django.test import TestCase
from django.urls import reverse
from stable.models import CustomUser, PM, SiteWideMessages
from stable.models import Pending, Yes, No

class TestRegisterAdmin(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser(
            username = "admin",
            email = "admin@example.com",
            password = "testing321"
        )

    def test_redirects_to_home_if_admin(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('home'),
        status_code = 302, target_status_code = 200)

class TestRegisteredUser(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )
        self.client.force_login(self.user)

    def test_redirects_to_profile_if_registered(self):
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('profile'),
        status_code = 302, target_status_code = 200)

    def test_registered_user_shown_redirect_message(self):
        response = self.client.get(reverse('register'), follow = True)
        messages = list(response.context['messages'])
        # self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You already have an account.")

class TestProfileAdmin(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            username = 'admin',
            email = "testing321",
            password = "testing321"
        )
        self.client.force_login(self.admin)

    def test_admin_shooed_away_from_profile(self):
        admin_user = CustomUser.objects.get(
            username = "admin"
        )
        response = self.client.get(
            reverse('profile')
        )
        self.assertRedirects(
            response,
            reverse('home')
        )


    def test_admin_shooed_away_with_message(self):
        response = self.client.get(
            reverse('profile'),
            follow = True
        )
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]),
        "Admin does not have a profile page.")

class TestProfileUser(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )
        self.client.force_login(self.user)

    def test_user_sees_pm(self):
        PM.objects.create(
            to = self.user,
            subject = "A subject.",
            message = "A message."
        )
        response = self.client.get(
            reverse('profile')
        )
        messages = list(response.context['messages'])
        self.assertEqual(
            str(messages[0]),
            "You have unread private messages."
        )

    def test_user_sees_public(self):
        SiteWideMessages.objects.create(
            subject = "A subject.",
            message = "A message."
        )
        response = self.client.get(
            reverse('profile')
        )
        messages = list(response.context['messages'])
        self.assertEqual(
            str(messages[0]),
            "You have unread public messages."
        )

class TestProfileContext(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )
        SiteWideMessages.objects.create(
            subject = "A subject.",
            message = "A message."
        )
        PM.objects.create(
            to = self.user,
            subject = "A subject.",
            message = "A message."
        )
        self.client.force_login(self.user)

    def test_public_msgs_passed_to_tmplt(self):
        response = self.client.get(
            reverse('profile')
        )
        site = list(response.context['site'])
        self.assertTrue(site)

    def test_private_msgs_passed_to_tmplt(self):
        response = self.client.get(
            reverse('profile')
        )
        private = list(response.context['private'])
        self.assertTrue(private)

class TestProfileBookingsYes(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )
        self.client.force_login(self.user)

        Yes.objects.create(
            user = self.user,
            horse = "Graf",
            year = 2019,
            month = 6,
            day = 17,
            hour = 15,
            minute = 30
        )

    def test_yes_booking_sent_to_tmplt_context(self):
        response = self.client.get(
            reverse('profile')
        )
        yes_context = list(response.context['yes_context'])
        self.assertTrue(yes_context)

class TestProfileBookingsNo(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )
        self.client.force_login(self.user)

        No.objects.create(
            user = self.user,
            horse = "Graf",
            year = 2019,
            month = 6,
            day = 17,
            hour = 15,
            minute = 30
        )

    def test_no_booking_sent_to_tmplt_context(self):
        response = self.client.get(
            reverse('profile')
        )
        no_context = list(response.context['no_context'])
        self.assertTrue(no_context)


class TestProfileBookingsPending(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )
        self.client.force_login(self.user)

        Pending.objects.create(
            user = self.user,
            horse = "Graf",
            year = 2019,
            month = 6,
            day = 17,
            hour = 15,
            minute = 30
        )

    def test_pending_booking_sent_to_tmplt_context(self):
        response = self.client.get(
            reverse('profile')
        )
        pending_context = list(response.context['pending_context'])
        self.assertTrue(pending_context)

class TestPendingViewLoggedIn(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )
        self.client.force_login(self.user)

    def test_user_cannot_request_bookings_until_verified_redirects(self):
        response = self.client.get(
            reverse('pending')
        )

        self.assertRedirects(
            response,
            reverse('profile')
        )

    def test_user_sees_message_if_not_verified(self):
        response = self.client.get(
            reverse('pending'),
            follow = True
        )

        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]),
        "Cannot request a booking until the registration is accepted by the admin.")

class TestPendingViewUserLoggedInAndVerified(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321",
            confirmation = "accept"
        )

        self.client.force_login(
            self.user
        )

        Yes.objects.create(
            user = self.user,
            horse = "Graf",
            year = 2019,
            month = 6,
            day = 17,
            hour = 15,
            minute = 30
        )

    def test_user_shown_message_if_request_already_accepted(self):
        response = self.client.get(
            reverse('pending')
            )

        messages = list(
            response.context['messages']
        )

        self.assertEqual(
            str(messages[0]),
            "You already have an accepted request."
        )

class TestPendingViewLoggedInVerifiedPendingBooking(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321",
            confirmation = "accept"
        )
        self.client.force_login(self.user)
        Pending.objects.create(
            user = self.user,
            horse = "Graf",
            year = 2019,
            month = 6,
            day = 17,
            hour = 15,
            minute = 30
        )

    def test_user_shown_message_if_request_already_pending(self):
        response = self.client.get(
            reverse('pending')
        )
        messages = list(response.context['messages'])
        self.assertEqual(
            str(messages[0]),
            "You have a pending request."
        )
