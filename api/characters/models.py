from django.db import models

# Create your models here.
class Character(models.Model):
    name = models.CharField(max_length=255, default="null")
    link = models.CharField(max_length=255, default="null")
    info = models.JSONField(null=False)