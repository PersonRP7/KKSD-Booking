from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.db import transaction, IntegrityError

from .models import Pending, Yes, No, CustomUser, Horse
from .models import SiteWideMessages, PM
from .forms import UserRegisterForm, CustomUserChangeForm

class DoNotLog:
    def log_addition(self, *args):
        pass

    def log_change(self, *args):
        pass

    def log_deletion(self, *args):
        pass

class MyAdminSite(AdminSite):
    @never_cache
    def index(self, request, extra_context = None):
        CustomUser.confirmation_status(request)
        Pending.show_pending(request)
        return super().index(request, extra_context)


admin_site = MyAdminSite(name = 'myadmin')
admin_site.site_header = 'KK Sokol Dupci'
admin_site.site_title = 'KK Sokol Dupci'
admin_site.index_title = "KK Sokol Dupci"

class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['first_name', 'last_name']

    def make_accept(self, request, queryset):
        queryset.update(confirmation = 'accept')
        messages.info(request, "Registered.")
    make_accept.short_description = "Mark selected users as accepted."
    actions = ['make_accept']

admin_site.register(CustomUser, CustomUserAdmin)
admin_site.register(Horse)

class PendingAdmin(DoNotLog, admin.ModelAdmin):
    readonly_fields = ['user', 'horse', 'year', 'month', 'day', 'hour', 'minute']
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj = None):
        return None
    def message_user(self, *args):
        pass


    def save_model(self, request, obj, form, change):
        '''Seems to work.'''
        self.request = request
        try:
            with transaction.atomic():
                super().save_model(request, obj, form, change)
                obj.move_to(request)
        except IntegrityError:
            messages.error(request, "This time slot is already taken.")
    #Might be an error
    # def queryset(self, request):
    #     qs = super().queryset(request)
    #     return qs.select_related()


admin_site.register(Pending, PendingAdmin)

class YesAdmin(DoNotLog, admin.ModelAdmin):
    readonly_fields = ['user', 'horse', 'year', 'month', 'day', 'hour', 'minute']
    def has_add_permission(self, request):
        return False
    # list_select_related = (
    #     'user',
    # )
    #list_select_related = True

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

admin_site.register(Yes, YesAdmin)

class NoAdmin(DoNotLog, admin.ModelAdmin):
    readonly_fields = ['user', 'horse', 'year', 'month', 'day', 'hour', 'minute']
    def has_add_permission(self, request):
        return False
    list_select_related = (
        'user',
    )
admin_site.register(No, NoAdmin)

class PMAdmin(DoNotLog, admin.ModelAdmin):
    exclude = ['read']
    list_select_related = (
        'to',
    )
admin_site.register(PM, PMAdmin)
admin_site.register(SiteWideMessages)
