# Generated by Django 4.0.4 on 2023-02-28 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_rename_vips_vip'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Vip',
            new_name='StreamVip',
        ),
    ]