from django.db import models

# Create your models here.
class Character(models.Model):
    data = models.JSONField(null=False)