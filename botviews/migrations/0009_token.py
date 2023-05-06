# Generated by Django 4.0.4 on 2023-04-20 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botviews', '0008_user_last_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(help_text='Token de validación', max_length=50, verbose_name='Valor')),
                ('is_active', models.BooleanField(default=True, help_text='Indica si el token está activo', verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
            },
        ),
    ]