# Generated by Django 2.2.1 on 2019-05-29 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_group_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='thumb',
            field=models.URLField(blank=True, null=True, verbose_name='Thumbnail'),
        ),
    ]