from django.db import models

# Create your models here.
class Species(models.Model):
    data = models.JSONField(null=False)