# Generated by Django 3.1 on 2020-08-18 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0002_auto_20200818_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='link',
            field=models.CharField(default='null', max_length=255),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='name',
            field=models.CharField(default='null', max_length=255),
        ),
    ]
