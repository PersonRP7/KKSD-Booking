from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Horse, Pending
from django.core.exceptions import ValidationError
from .validators import validate_captcha, validate_username, validate_password_password
from .validators import validate_password_length, validate_password_number
from .validators import admin_email_in_database

class CaptchaMixin(forms.Form):
    Yes = 'Yes'
    No = 'No'
    Maybe = 'Maybe'
    Perhaps = 'Perhaps'
    CAPTCHA_BOOLEANS = (
        (Yes, 'Yes'),
        (Maybe, 'Maybe'),
        (No, 'No'),
        (Perhaps, 'Perhaps')
    )

    captcha = forms.ChoiceField(choices = CAPTCHA_BOOLEANS,
    label = "Are you a robot?", validators = [validate_captcha])

class ForgotPassword(CaptchaMixin):
    email = forms.CharField(
        max_length = 50,
        validators = [admin_email_in_database]
    )

class PasswordMixin(forms.Form):
    password1 = forms.CharField(widget = forms.PasswordInput(), max_length = 50, validators = [validate_password_length, validate_password_number, validate_password_password])
    password2 = forms.CharField(widget = forms.PasswordInput(), max_length = 50)


class UserRegisterForm(UserCreationForm):
    #Used in the admin.
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


# class CaptchaForm(forms.Form):
#     Yes = 'Yes'
#     No = 'No'
#     Maybe = 'Maybe'
#     Perhaps = 'Perhaps'
#     CAPTCHA_BOOLEANS = (
#         (Yes, 'Yes'),
#         (Maybe, 'Maybe'),
#         (No, 'No'),
#         (Perhaps, 'Perhaps')
#     )
#
#     text = forms.ChoiceField(choices = CAPTCHA_BOOLEANS,
#     label = "Are you a robot?")
#
#     def clean_text(self):
#         data = self.cleaned_data
#         if 'No' not in data:
#             raise ValidationError("You are a robot.")
#         return data

class UserRegisterCaptchaForm(CaptchaMixin, PasswordMixin):
    #Newest version. Also includes the password mixin.
    username = forms.CharField(max_length = 50, validators = [validate_username])
    first_name = forms.CharField(max_length = 50)
    last_name = forms.CharField(max_length = 50)

    def clean(self):
        data = self.cleaned_data
        if 'password1' in data and 'password2' in data and data['password1'] != data['password2']:
            raise ValidationError("Passwords don't match.")
        if 'first_name' in data and 'last_name' in data:
             if CustomUser.objects.filter(first_name = data['first_name'], last_name = data['last_name']).exists():
                 raise ValidationError(f"{data['first_name']} {data['last_name']} is taken.")
        return data

# class UserRegisterCaptchaForm(CaptchaMixin):
#     #New version. Includes the CaptchaMixin.
#     username = forms.CharField(max_length = 50, validators = [validate_username])
#     first_name = forms.CharField(max_length = 50)
#     last_name = forms.CharField(max_length = 50)
#     email = forms.EmailField(widget = forms.EmailInput())
#     password1 = forms.CharField(widget = forms.PasswordInput(), max_length = 50, validators = [validate_password_length, validate_password_number, validate_password_password])
#     password2 = forms.CharField(widget = forms.PasswordInput(), max_length = 50)
#
#     def clean(self):
#         data = self.cleaned_data
#         if 'password1' in data and 'password2' in data and data['password1'] != data['password2']:
#             raise ValidationError("Passwords don't match.")
#         if CustomUser.objects.filter(first_name = data['first_name'], last_name = data['last_name']).exists():
#             raise ValidationError(f"{data['first_name']} {data['last_name']} is taken.")
#         return data

# class UserRegisterCaptchaForm(forms.Form):
#     username = forms.CharField(max_length = 50, validators = [validate_username])
#     first_name = forms.CharField(max_length = 50)
#     last_name = forms.CharField(max_length = 50)
#     email = forms.EmailField(widget = forms.EmailInput())
#     password1 = forms.CharField(widget = forms.PasswordInput(), max_length = 50, validators = [validate_password_length, validate_password_number, validate_password_password])
#     password2 = forms.CharField(widget = forms.PasswordInput(), max_length = 50)
#
#     Yes = 'Yes'
#     No = 'No'
#     Maybe = 'Maybe'
#     Perhaps = 'Perhaps'
#     CAPTCHA_BOOLEANS = (
#         (Yes, 'Yes'),
#         (Maybe, 'Maybe'),
#         (No, 'No'),
#         (Perhaps, 'Perhaps')
#     )
#
#     captcha = forms.ChoiceField(choices = CAPTCHA_BOOLEANS,
#     label = "Are you a robot?", validators = [validate_captcha])
#
#
#     def clean(self):
#         data = self.cleaned_data
#         if 'password1' in data and 'password2' in data and data['password1'] != data['password2']:
#             raise ValidationError("Passwords don't match.")
#         if CustomUser.objects.filter(first_name = data['first_name'], last_name = data['last_name']).exists():
#             raise ValidationError(f"{data['first_name']} {data['last_name']} is taken.")
#         return data


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name']

class PendingForm(forms.ModelForm):
    horse = forms.ModelChoiceField(queryset = Horse.objects.all())

    class Meta:
        model = Pending
        fields = ['horse', 'year', 'month', 'day', 'hour', 'minute']

    def clean(self):
        try:
            data = self.cleaned_data
            from django.utils import timezone
            from django.utils.dateparse import parse_datetime
            import pytz
            import datetime
            current_dt = timezone.now()
            naive = parse_datetime(f"{data['year']}-{data['month']}-{data['day']} {data['hour']}:{data['minute']}")
            aware_dt = pytz.timezone("Europe/Zagreb").localize(naive, is_dst = None)
            if aware_dt.strftime("%A") == 'Sunday':
                raise ValidationError("Cannot select sunday.")

            if aware_dt <= timezone.now():
                raise ValidationError("Date cannot be in the past.")
            if timezone.now().year == aware_dt.year and timezone.now().month == aware_dt.month and timezone.now().day == aware_dt.day:
                raise ValidationError("Cannot book the current day.")
            return data
        except ValueError:
            raise ValidationError(f"{data['year']}/{data['month']}/{data['day']} doesn't exist.")

class DeleteYesForm(forms.Form):
    Yes = 'Yes'
    No = 'No'
    CONFIRMATION_BOOLEANS = (
        (Yes, 'Yes'),
        (No, 'No')
    )
    confirmation = forms.ChoiceField(choices = CONFIRMATION_BOOLEANS)

class LoginForm(forms.Form):
    '''This works'''
    username = forms.CharField(max_length = 50)
    password = forms.CharField(max_length = 50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(attrs = {'placeholder':''})

class ChangePassword(PasswordMixin):
   def clean(self):
       data = self.cleaned_data
       if 'password1' in data and 'password2' in data and data['password1'] != data['password2']:
           raise ValidationError("Passwords don't match.")
       return data
