from django.core.exceptions import ValidationError
from .models import CustomUser

# def admin_email_in_database(value):
#     if CustomUser.objects.get(email = value).username != 'admin':
#         raise ValidationError(
#             "That email is not in the database.",
#             params = {'value':value}
#         )

def admin_email_in_database(value):
    try:
        user = CustomUser.objects.get(email = value)
        if user.username != 'admin':
            raise ValidationError(
                "Not the admin.",
                params = {'value':value}
            )
    except CustomUser.DoesNotExist:
        raise ValidationError(
           "That email is not in the database.",
           params = {'value':value}
         )

def validate_captcha(value):
    if value != 'No':
        raise ValidationError(
            ("You are a robot."),
            params = {'value':value}
        )

def username_in_database(value):
    if not CustomUser.objects.filter(username = value).exists():
        raise ValidationError(
            ("That username is not in the database"),
            params = {'value':value}
        )


def validate_username(value):
    if CustomUser.objects.filter(username = value).exists():
        raise ValidationError(
            (f"{value} is taken."),
            params = {'value':value}
        )

def validate_password_length(value):
    if len(value) < 10:
        raise ValidationError(
            ("Password has to be longer than 9 characters."),
            params = {'value':value}
        )

def validate_password_number(value):
    isdigit_values = []
    for i in value:
        isdigit_values.append(i.isdigit())
    if True not in isdigit_values:
        raise ValidationError(
            ("Password has to include at least one number."),
            params = {'value':value}
        )


def validate_password_password(value):
    if 'password' in value or 'Password' in value:
        string = ""
        for i in value:
            if i.isalpha():
                string += i
        raise ValidationError(f"Password cannot contain {string}.", params = {'value':value})
