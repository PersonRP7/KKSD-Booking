from django.db import models, transaction, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.contrib import messages
from django.urls import reverse

class CustomUser(AbstractUser):

    class Meta:
        unique_together = ('first_name', 'last_name')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    read = 'read'
    unread = 'unread'
    PUBLIC_STATUS_BOOLEANS = (
        (read, 'read'),
        (unread, 'unread')
    )
    public_status = models.CharField(choices = PUBLIC_STATUS_BOOLEANS, default = unread, max_length = 50)

    @staticmethod
    def to_read(username = None):
        CustomUser.objects.filter(username = username).update(public_status = 'read')

    @staticmethod
    def to_unread():
        CustomUser.objects.all().update(public_status = 'unread')

    accept = 'accept'
    deny = 'deny'
    waiting = 'waiting'

    CONFIRM_DENY_BOOLEANS = (
        (accept, 'accept'),
        (deny, 'deny'),
        (waiting, 'waiting')
    )

    confirmation = models.CharField(max_length = 50, choices = CONFIRM_DENY_BOOLEANS, default = waiting)

    @staticmethod
    def confirmation_status(req):
        for i in CustomUser.objects.all():
            if i.confirmation == 'waiting':
                messages.info(req, f"{i.first_name} {i.last_name} has registered.")

    # @property
    # def full_name(self):
    #     return f"{self.first_name} {self.last_name}"

class Horse(models.Model):
    horse_name = models.CharField(max_length = 35)


    def __str__(self):
        return self.horse_name


class Common(models.Model):
    class Meta:
        abstract = True

    import datetime
    YEAR_CHOICES = []
    for year in range(2019, 2035):
        YEAR_CHOICES.append((str(year), str(year)))

    MONTH_CHOICES = []
    for month in range(1, 13):
        MONTH_CHOICES.append((str(month), str(month)))

    DAY_CHOICES = []
    for day in range(1, 32):
        DAY_CHOICES.append((str(day), str(day)))

    HOUR_CHOICES = []
    for i in range(8, 23):
        HOUR_CHOICES.append((str(i), str(i)))

    MINUTE_CHOICES = []
    for i in range(0, 61, 15)[0:-1]:
        MINUTE_CHOICES.append((str(i), str(i)))

    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    horse = models.CharField(max_length = 50)
    year = models.CharField(max_length = 50, choices = YEAR_CHOICES)
    month = models.CharField(max_length = 50, choices = MONTH_CHOICES)
    day = models.CharField(max_length = 50, choices = DAY_CHOICES)
    hour = models.CharField(max_length = 50, choices = HOUR_CHOICES)
    minute = models.CharField(max_length = 50, choices = MINUTE_CHOICES)

class Pending(Common):
    class Meta:
        verbose_name_plural = '1. Pending'

    Accept = 'Accept'
    Deny = 'Deny'
    Waiting = 'Waiting'

    CONFIRM_DENY_BOOLEANS = (
        (Accept, 'Accept'),
        (Deny, 'Deny'),
        (Waiting, 'Waiting')
    )

    confirmation = models.CharField(
        choices = CONFIRM_DENY_BOOLEANS,
        max_length = 30,
        default = 'Waiting'
    )

    def move_to(self, req):
        if self.confirmation == 'Accept':
            Yes.objects.create(
            user = self.user,
            horse = self.horse,
            year = self.year,
            month = self.month,
            day = self.day,
            hour = self.hour,
            minute = self.minute)

            Pending.objects.filter(user = self.user).delete()
            messages.success(req, "New time slot created.")

        elif self.confirmation == 'Deny':
            No.objects.create(
            user = self.user,
            horse = self.horse,
            year = self.year,
            month = self.month,
            day = self.day,
            hour = self.hour,
            minute = self.minute)

            Pending.objects.filter(user = self.user).delete()
            messages.success(req, "Request deleted.")

    @staticmethod
    def show_pending(req):
        if Pending.objects.count() > 0:
            messages.info(req, "There are new requests.")


    def __str__(self):
        return f"{self.user} requests {self.horse} on {self.year}/{self.month}/{self.day} at {self.hour}:{self.minute}"

class Yes(Common):
    class Meta:
        verbose_name_plural = '2. Yes'
        unique_together = ('horse', 'year', 'month', 'day', 'hour', 'minute')


    def __str__(self):
        return f"{self.user}, {self.horse} on {self.year}/{self.month}/{self.day} at {self.hour}:{self.minute}"

    def cancel(self):
        from django.utils import timezone
        from django.utils.dateparse import parse_datetime
        import pytz
        current_dt = timezone.now()
        naive = parse_datetime(f"{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}")
        aware_dt = pytz.timezone("Europe/Zagreb").localize(naive, is_dst = None)
        time_delta = aware_dt - current_dt
        if (time_delta).total_seconds() < 24*3600:
            raise ValueError
        else:
            Yes.objects.get(user = self.user).delete()


class No(Common):
    class Meta:
        verbose_name_plural = '3. No'

    def __str__(self):
        return f"{self.user}, {self.horse} on {self.year}/{self.month}/{self.day} at {self.hour}:{self.minute}"


class CommonMessaging(models.Model):
    class Meta:
        abstract = True
    subject = models.CharField(max_length = 50)
    message = models.TextField(max_length = 500)
    date = models.DateTimeField(auto_now_add = True)

    @staticmethod
    def delete_if_expired(model):
        from django.utils import timezone
        from django.utils.dateparse import parse_datetime
        import pytz
        current_dt = timezone.now()
        for i in model.objects.all():
            dt = i.date
            naive = parse_datetime(f"{dt.year}-{dt.month}-{dt.day} {dt.hour}:{dt.minute}")
            aware_dt = pytz.timezone("Europe/Zagreb").localize(naive, is_dst = None)
            time_delta = current_dt - aware_dt
            if time_delta.total_seconds() > 168*3600:
                i.delete()
                print("Deleted expired instance.")
            else:
                print("Not deleted.")



class SiteWideMessages(CommonMessaging):
    class Meta:
        verbose_name_plural = 'Public messages.'

    def __str__(self):
        return self.subject

class PM(CommonMessaging):
    to = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    read = models.BooleanField(default = False)
    class Meta:
        verbose_name_plural = "Private messages"

    def __str__(self):
        return f"{self.to}, {self.subject}, {self.read}"

    def get_absolute_url(self):
        return reverse('msgs', kwargs = {'id':self.id})

    @staticmethod
    def to_read(user_inst):
        PM.objects.filter(to = user_inst, read = False).update(read = True)

    @staticmethod
    def to_unread(user_inst):
        PM.objects.filter(to = user_inst, read = True).update(read = False)
