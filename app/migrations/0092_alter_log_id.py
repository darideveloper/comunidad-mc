# Generated by Django 4.0.4 on 2023-07-11 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0091_alter_log_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]