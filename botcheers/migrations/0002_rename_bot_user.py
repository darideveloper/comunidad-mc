# Generated by Django 4.0.4 on 2023-05-15 03:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('botcheers', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bot',
            new_name='User',
        ),
    ]
