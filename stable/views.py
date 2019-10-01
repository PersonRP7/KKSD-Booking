from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from .models import Pending, Yes, No, Horse
from .models import SiteWideMessages, PM, CustomUser
from .forms import PendingForm, LoginForm
from .forms import DeleteYesForm, UserRegisterCaptchaForm
from .forms import ChangePassword, ForgotPassword

def forgot_password(request):
    if request.method == 'GET':
        form = ForgotPassword()
        return render(request, 'stable/forgot_password.html', {'form':form})
    else:
        form = ForgotPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = CustomUser.objects.get(email = email)
            if user.username != 'admin':
                messages.info(request, "Not the admin.")
                return redirect('home')
            import random
            from django.core.mail import send_mail
            new_password = ""
            for i in range(12):
                new_password += random.choice("abcdefg")
            user.set_password(new_password)
            user.save()
            send_mail(subject = "New password",
                message = new_password,
                recipient_list = (user.email,),
                fail_silently = True,
                from_email = 'k.sokol.dupci.reg@gmail.com'
            )
            messages.info(request, "Email sent.")
            return redirect('login')
        else:
            messages.info(request, "Form not correct.")
            return render(request, 'stable/forgot_password.html', {'form':form})

@login_required
def delete_account(request):
    if request.method == 'GET':
        form = DeleteYesForm()
        return render(request, 'stable/generic_form.html', {'form':form})
    else:
        form = DeleteYesForm(request.POST)
        if form.is_valid():
            confirmation = form.cleaned_data.get('confirmation')
            if confirmation == 'No':
                return redirect('profile')
            elif confirmation == 'Yes':
                user = CustomUser.objects.get(username = request.user.username)
                user.delete()
                messages.info(request, "Profile deleted.")
                return redirect('home')
        else:
            messages.info(request, 'Form incorrect.')
            return render(request, 'stable/generic_form.html', {'form':form})

def licence_eng(request):
    return render(request, 'stable/licence_eng.html')

def licence(request):
    return render(request, 'stable/licence.html')

def cookie_policy(request):
    return render(request, 'stable/cookie_policy.html')

def cookies_eng(request):
    return render(request, 'stable/cookies_eng.html')

def register(request):
    if request.method == 'GET':
        user = request.user
        user_name = user.username
        if user_name == 'admin':
            return redirect('home')
        if CustomUser.objects.filter(username = user_name).exists():
            messages.info(request, "You already have an account.")
            return redirect('profile')
        form = UserRegisterCaptchaForm()
        return render(request, 'stable/register.html', {'form':form})
    elif request.method == 'POST':
        form = UserRegisterCaptchaForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password1')
            # email = form.cleaned_data.get('email')
            CustomUser.objects.create_user(
                username = username,
                first_name = first_name,
                last_name = last_name,
                password = password
                )
            messages.success(request, "Account created.")
            user_person = authenticate(request, username = username, password = password)
            if user_person is not None:
                login(request, user_person)
                return redirect('profile')
        else:
            messages.info(request, "Form incorrect.")
            return render(request, 'stable/register.html', {'form':form})

def my_login(request):
    '''This works.'''
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'stable/login.html', {'form':form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if not user:
                messages.error(request, 'Incorrect credentials. Try again.')
                return render(request, 'stable/login.html', {'form':form})
            #print(user)
            if user is not None and not user.is_superuser:
                login(request, user)
                return redirect('profile')
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin:index')
        else:
            messages.error(request, "Form not valid.")
            return render(request, 'stable/login.html', {'form':form})


def home(request):
    return render(request, 'stable/home.html')


@login_required
def profile(request):
    '''Seems to be working.'''
    user = request.user
    user_name = user.username
    if user_name == 'admin':
        messages.error(request, "Admin does not have a profile page.")
        return redirect('home')
    user_instance = CustomUser.objects.get(username = user_name)
    if PM.objects.filter(to = user, read = False):
        messages.info(request, "You have unread private messages.")
    if SiteWideMessages.objects.exists():
        if user_instance.public_status == 'unread':
            messages.success(request, "You have unread public messages.")
    to = CustomUser.objects.get(username = user_name)
    if request.method == 'GET':
        context = {}
        context['site'] = SiteWideMessages.objects.all()
        context['private'] = PM.objects.filter(to = to)
        context['pending_context'] = Pending.objects.filter(user = user)
        context['yes_context'] = Yes.objects.filter(user = user)
        context['no_context'] = No.objects.filter(user = user)
        return render(request, 'stable/profile.html', context)

@login_required
def pending(request):
    user = request.user
    context = Yes.objects.all()
    try:
        if request.method == 'GET':
            user_status = CustomUser.objects.get(username = user.username)
            if user_status.confirmation == 'waiting':
                messages.success(request, "Cannot request a booking until the registration is accepted by the admin.")
                return redirect('profile')
            form = PendingForm()
            if user.username == 'admin':
                return redirect('home')
            if Yes.objects.filter(user = user).exists():
                messages.error(request, "You already have an accepted request.")
                return render(request, "stable/pending.html", {'context':context})

            elif Pending.objects.filter(user = user).exists():
                messages.error(request, "You have a pending request.")
                return render(request, "stable/pending.html", {'context':context})

            else:
                form.fields['horse'].queryset = Horse.objects.all()
                return render(request, 'stable/pending.html', {'form':form, 'context':context})
        else:
            form = PendingForm(request.POST)
            if form.is_valid():
                horse = form.cleaned_data.get('horse')
                year = form.cleaned_data.get('year')
                month = form.cleaned_data.get('month')
                day = form.cleaned_data.get('day')
                hour = form.cleaned_data.get('hour')
                minute = form.cleaned_data.get('minute')
                if Yes.objects.filter(horse = horse, year = year, month = month, day = day, hour = hour, minute = minute).exists():
                    messages.error(request, f"{horse} is taken on {year}/{month}/{day} {hour}:{minute}")
                    return redirect('pending')
                else:
                    form_stuff = form.save(commit = False)
                    form_stuff.user = user
                    form_stuff.save()
                    messages.success(request, "Form saved.")
                    if No.objects.filter(user = user).exists():
                        No.objects.filter(user = user).delete()
                    return redirect('pending')
            else:
                return render(request, 'stable/pending.html', {'form':form, 'context':context})
    except ObjectDoesNotExist:
        messages.error(request, "Administrator logged in.")
        return render(request, 'stable/pending.html', {'context':context})
#The try/except block might be unnecessary now, as there's no Profile model anymore.


@login_required
def cancel_yes(request):
    '''Production code.'''
    user = request.user
    if user.username == 'admin':
        messages.info(request, "Admin pls go.")
        return redirect('home')
    if request.method == 'GET':
        form = DeleteYesForm()
        if not Yes.objects.filter(user = user).exists():
            messages.info(request, "You don't have an accepted request to delete.")
            return redirect('profile')
        else:
            return render(request, 'stable/generic_form.html', {'form':form})
    else:
        form = DeleteYesForm(request.POST)
        if form.is_valid():
            confirmation = form.cleaned_data.get('confirmation')
            if confirmation == 'Yes':
                instance = Yes.objects.get(user = user)
                try:
                    instance.cancel()
                    messages.success(request, f"{instance} cancelled.")
                    return redirect('profile')
                except ValueError:
                    messages.warning(request, "Cancellations have to be made 24h in advance.")
                    return redirect('profile')
            else:
                messages.info(request, "Booking still on.")
                return redirect('profile')

@login_required
def cancel_pending(request):
    '''Production code.'''
    user = request.user
    if user.username == 'admin':
        messages.info(request, "Admin pls go.")
        return redirect('home')
    if request.method == 'GET':
        form = DeleteYesForm()
        if not Pending.objects.filter(user = user).exists():
            messages.info(request, "You don't have a pending request to delete.")
            return redirect('profile')
        else:
            return render(request, 'stable/generic_form.html', {'form':form})
    else:
        form = DeleteYesForm(request.POST)
        if form.is_valid():
            confirmation = form.cleaned_data.get('confirmation')
            if confirmation == 'Yes':
                instance = Pending.objects.get(user = user)
                instance.delete()
                messages.success(request, "Pending request cancelled.")
                return redirect('profile')
            elif confirmation == 'No':
                return redirect('profile')

@login_required
def see_pm(request):
    user = request.user
    if not PM.objects.filter(to = user):
        messages.info(request, "You don't have any private messages.")
        return redirect('profile')
    else:
        message = PM.objects.filter(to = user)
        if PM.objects.filter(to = user, read = False):
            PM.to_read(user)
            return render(request, 'stable/messages.html', {'message':message})
        elif PM.objects.filter(to = user, read = True):
            return render(request, 'stable/messages.html', {'message':message})

@login_required
def msgs(request, id = None):
    if request.method == 'GET':
        try:
            pm = PM.objects.get(to = request.user, id = id)
            return render(request, 'stable/msgs.html', {'pm':pm})
        except PM.DoesNotExist:
            messages.info(request, "That message does not exist.")
            return redirect('see_pm')
    elif request.method == 'POST':
        try:
            PM.objects.get(to = request.user, id = id).delete()
            messages.info(request, "Message deleted.")
            return redirect('see_pm')
        except:
            messages.info(request, "Something went wrong.")
            return redirect('see_pm')


@login_required
def see_public(request):
    user = request.user
    if user.username == 'admin':
        messages.info(request, "Admin get out.")
        return redirect('home')
    user_instance = CustomUser.objects.get(username = user.username)
    message = SiteWideMessages.objects.all()
    if not SiteWideMessages.objects.exists():
        messages.success(request, "There are no public messages.")
        return redirect('profile')
    if SiteWideMessages.objects.exists() and user_instance.public_status == 'unread':
        CustomUser.to_read(username = user.username)
        return render(request, 'stable/messages.html', {'message':message})
    elif SiteWideMessages.objects.exists() and user_instance.public_status == 'read':
        return render(request, 'stable/messages.html', {'message':message})

@login_required
def change_password(request):
    if request.method == 'GET':
        form = ChangePassword()
        return render(request, 'stable/generic_form.html', {'form':form})
    else:
        form = ChangePassword(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            user = request.user
            user_object = CustomUser.objects.get(username = user.username)
            if password:
                user_object.set_password(password)
                user_object.save()
                return redirect('home')
            else:
                messages.info(request, "Try again.")
                return redirect('home')
        else:
            messages.info(request, "Form not correct.")
            return render(request, 'stable/generic_form.html', {'form':form})
