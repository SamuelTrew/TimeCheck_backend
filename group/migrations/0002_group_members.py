# Generated by Django 2.2.1 on 2019-05-29 06:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
