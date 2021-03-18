from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from datetime import datetime, timedelta
from dateutil import tz

from django.conf import settings

# Create your models here.
class Profile(models.Model):
    status = [
        (1,'NOT_EVALUATED'),
        (2,'EVALUATED'),
        (3,'ELIMINATED'),
    ]

    user = models.OneToOneField(User,on_delete=CASCADE)
    curr_round = models.IntegerField(default=1)
    current_status = models.IntegerField(choices=status,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    member= models.BooleanField(default=False)
    completed=models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    def get_completion_time(self):
        two_hours_from_now = self.created_at + timedelta(hours=3)
        ist = two_hours_from_now.astimezone(tz.tzlocal())
        date_data = {
            'year':ist.year,
            'month':ist.month,
            'day':ist.day,
            'hours' : ist.hour,
            'mins': ist.minute,
            'seconds':ist.second
        }
        js_date_string = "{} {}, {} {}:{}:{}".format(date_data['month'],date_data['day'],date_data['year'],date_data['hours'],date_data['mins'],date_data['seconds'])
        return js_date_string


from django.dispatch import receiver
from django.db.models.signals import post_save
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
        print(profile.get_completion_time())


