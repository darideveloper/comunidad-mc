# Generated by Django 4.0.4 on 2023-02-04 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_generalpoint_point_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generalpoint',
            name='point_type',
        ),
        migrations.DeleteModel(
            name='TypePoint',
        ),
    ]
