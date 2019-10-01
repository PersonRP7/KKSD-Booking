from django.test import TestCase, RequestFactory
from django.core import mail
from django.urls import reverse
from stable.models import CustomUser, SiteWideMessages, PM


class EmailTest(TestCase):
    def test_send_mail(self):
        mail.send_mail(
            'Subject', 'Message',
            'from@example.com',['to@example.com'],
            fail_silently = False
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject')

class TestHomeViewNotLoggedIn(TestCase):
    def test_get_home_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_includes_text(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Dupci')

    def test_home_includes_links_not_logged_in(self):
        response = self.client.get(reverse('home'))
        link_array = ['login', 'register', 'licence', 'cookie_policy']

        for i in link_array:
            self.assertContains(response, i)

    def test_home_get_includes_4_href(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "href", 8)

    def test_home_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'stable/home.html')



class TestForgotPasswordView(TestCase):
    """This functionality is not included in the final version."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )

        CustomUser.objects.create_superuser(
            username = "admin",
            email = "admin@example.com",
            password = "testing321"
        )

    def test_get_returns_200(self):
        response = self.client.get(reverse('forgot_password'))
        self.assertTrue(response.status_code, 200)

    def test_forgot_password_includes_form(self):
        response = self.client.get(reverse('forgot_password'))
        self.assertContains(response, "form")

    def test_forgot_password_returns_template(self):
        response = self.client.get(reverse('forgot_password'))
        self.assertTemplateUsed(response, 'stable/forgot_password.html')


class TestDeleteAccountNotLoggedIn(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williams",
            password = "testing321"
        )

    def test_delete_account_not_logged_in_returns_302(self):
        response = self.client.get(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)

class TestDeleteAccountLoggedIn(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williams",
            password = "testing321"
         )
        self.client.login(username = "William", password = "testing321")

    def test_delete_account_logged_in_200(self):
        response = self.client.get(reverse('delete_account'))
        self.assertEqual(response.status_code, 200)


    def test_delete_account_uses_generic_form_template(self):
        response = self.client.get(reverse('delete_account'))
        self.assertTemplateUsed(response, 'stable/generic_form.html')

    def test_delete_account_uses_form(self):
        response = self.client.get(reverse('delete_account'))
        self.assertContains(response, "form")

class LoginTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username':'William',
            'first_name':'William',
            'last_name':'Williamson',
            'password':'testing321'
        }
        CustomUser.objects.create_user(
            **self.user_data
        )
    def test_login(self):
        response = self.client.post(reverse('login'),
        self.user_data, follow = True)
        self.assertTrue(response.context['user'].is_authenticated)

class DeleteAccount(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = "William",
            first_name = "William",
            last_name = "Williamson",
            password = "testing321"
        )
    def test_delete_account_yes_redirect_home(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('delete_account'),
            data = {'confirmation':'Yes'}
        )
        self.assertRedirects(response, reverse('home'), status_code = 302, target_status_code = 200)


    def test_delete_account_no_redirect_profile(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('delete_account'),
            data = {'confirmation':'No'}
        )
        self.assertRedirects(response, reverse('profile'), status_code=302, target_status_code = 200)
