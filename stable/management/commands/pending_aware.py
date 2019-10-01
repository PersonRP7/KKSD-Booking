from django.core.management.base import BaseCommand
from stable.models import Pending

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        '''Seems to be working.'''
        from django.utils import timezone
        from django.utils.dateparse import parse_datetime
        import pytz
        current_dt = timezone.now()
        for i in Pending.objects.all():
            naive = parse_datetime(f"{i.year}-{i.month}-{i.day} {i.hour}:{i.minute}")
            aware_dt = pytz.timezone("Europe/Zagreb").localize(naive, is_dst = None)
            if current_dt >= aware_dt:
                i.delete()
                self.stdout.write("Instance pruned")
            else:
                self.stdout.write("No instance to prune.")
