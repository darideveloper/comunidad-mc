# Generated by Django 4.0.4 on 2023-07-11 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0090_alter_log_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='id',
            field=models.AutoField(editable=False, help_text='id del log', primary_key=True, serialize=False, verbose_name='id'),
        ),
    ]
