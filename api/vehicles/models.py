from django.db import models

# Create your models here.
class Vehicle(models.Model):
    data = models.JSONField(null=False)