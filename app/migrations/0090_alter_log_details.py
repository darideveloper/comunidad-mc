# Generated by Django 4.0.4 on 2023-07-10 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0089_alter_log_options_alter_logorigin_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='details',
            field=models.TextField(help_text='detalles del log', verbose_name='detalles'),
        ),
    ]
