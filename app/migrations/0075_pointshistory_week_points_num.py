# Generated by Django 4.0.4 on 2023-04-09 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0074_rename_general_points_pointshistory_general_points_num_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointshistory',
            name='week_points_num',
            field=models.IntegerField(default=0, help_text='puntos semanales obtenidos a lo largo de la semana', verbose_name='puntos semana'),
        ),
    ]