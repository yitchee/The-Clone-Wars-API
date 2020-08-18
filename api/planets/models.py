from django.db import models

# Create your models here.
class Planet(models.Model):
    data = models.JSONField(null=False)