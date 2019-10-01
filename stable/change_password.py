# >>> def create_password(username):
# ...     number_string = ""
# ...     for i in range(3):
# ...             number_string += str(random.randint(1, 3))
# ...     password = f"{username}.{number_string}"
# ...     print(password)
# ...
# >>> create_password("Albert")



# def change_password(model, user_name):
#     import random
#     number_string = ""
#     user = model.objects.get(username = user_name)
#     for i in range(6):
#         number_string += str(random.randint(1, 9))
#     password = f"{user.username}.{number_string}"
#     user.set_password(password)
#     user.save()

# def send_password(rndr, rqst, model, user_name):
#     from django.core.mail import send_mail
#     send_mail(subject = "Password", message = password,
#     recipient_list = ['user.email'], fail_silently = True,
#     from_email = 'k.sokol.dupci.reg@gmail.com')
#     return rndr(rqst, 'languages/send.html')
#
#     def change_password(model, user_name):
#         import random
#         number_string = ""
#         user = model.objects.get(username = user_name)
#         for i in range(6):
#             number_string += str(random.randint(1, 9))
#         password = f"{user.username}.{number_string}"
#         user.set_password(password)
#         user.save()
#     return change_password

# def create_password(rndr, rqst, model, user_name):
#     import random
#     number_string = ""
#     user = model.objects.get(username = user_name)
#     for i in range(6):
#         number_string += str(random.randint(1, 9))
#     password = f"{user.username}.{number_string}"
#     user.set_password(password)
#     user.save()
#
#     def send_mail(rnd, rqst):
#         from django.core.mail import send_mail
#         send_mail(subject = "New password",
#         message = password,
#         recipient_list = [user.email],
#         fail_silently = True,
#         from_email = 'k.sokol.dupci.reg@gmail.com')
#     return send_mail
