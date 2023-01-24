# Generated by Django 4.0.4 on 2023-01-23 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_status_options_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(editable=False, help_text='id del ranking', primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(help_text='nombre del ranking', max_length=100, verbose_name='nombre')),
                ('points', models.IntegerField(help_text='puntos requeridos para el ranking', verbose_name='puntos')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, help_text='indica si el usuario es administrador', verbose_name='administrador'),
        ),
    ]