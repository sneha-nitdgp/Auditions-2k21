from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

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
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

from django.dispatch import receiver
from django.db.models.signals import post_save
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()


