from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, SiteWideMessages

@receiver(post_save, sender = SiteWideMessages)
def all_to_unread(sender, **kwargs):
    CustomUser.to_unread()
