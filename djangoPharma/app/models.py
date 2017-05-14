from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street = models.TextField(max_length=100, blank=True)
    streetno = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    zip = models.CharField(max_length=5, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserAddress.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.useraddress.save()

