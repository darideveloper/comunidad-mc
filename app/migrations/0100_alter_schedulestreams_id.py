# Generated by Django 4.2.7 on 2023-12-28 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0099_schedulestreams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulestreams',
            name='id',
            field=models.AutoField(editable=False, help_text='id del stream programado', primary_key=True, serialize=False, verbose_name='id'),
        ),
    ]
