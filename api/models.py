from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import secrets


class ApiKey(models.Model):
    key = models.CharField(max_length=64)
    daily_limit = models.IntegerField(default=settings.API_KEY_LIMIT)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)


@receiver(post_save, sender='users.User')
def generate_apikey_handler(sender, instance, **kwargs):
    apiKey = ApiKey()
    apiKey.key = secrets.token_urlsafe(32)
    apiKey.user = instance
    apiKey.save()