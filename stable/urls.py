from . import views
from django.urls import path, include
from stable.admin import admin_site

urlpatterns = [
    path('', views.home, name = 'home'),
    path('register/', views.register, name = 'register'),
    path('profile/', views.profile, name = 'profile'),
    path('pending/', views.pending, name = 'pending'),
    path('cancel/', include([
        path('yes/', views.cancel_yes, name = 'cancel_yes'),
        path('pending/', views.cancel_pending, name = 'cancel_pending')
    ])),
    path('see/', include([
        path('pm/', views.see_pm, name = 'see_pm'),
        path('public/', views.see_public, name = 'see_public')
    ])),
    path('myadmin/', admin_site.urls),
    path('change_password/', views.change_password, name = 'change_password'),
    path('licence/', views.licence, name = 'licence'),
    path('delete_account/', views.delete_account, name = 'delete_account'),
    path('cookie_policy/', views.cookie_policy, name = 'cookie_policy'),
    path('licence_eng/', views.licence_eng, name = 'licence_eng'),
    path('msgs/<int:id>/', views.msgs, name = 'msgs'),
    path('cookies_eng/', views.cookies_eng, name = 'cookies_eng'),
    path('forgot_password/', views.forgot_password, name = 'forgot_password'),
]
