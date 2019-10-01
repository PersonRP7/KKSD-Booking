from django.core.management.base import BaseCommand
from stable.models import SiteWideMessages, PM

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        PM.delete_if_expired(PM)
        SiteWideMessages.delete_if_expired(SiteWideMessages)
