# Generated by Django 4.0.4 on 2023-06-28 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0085_delete_whatchcheck'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalpoint',
            name='details',
            field=models.CharField(blank=True, help_text='detalles del punto', max_length=100, verbose_name='detalles'),
        ),
    ]
