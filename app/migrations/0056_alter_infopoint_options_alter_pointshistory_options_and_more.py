# Generated by Django 4.0.4 on 2023-02-28 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0055_rename_vip_streamvip'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='infopoint',
            options={'verbose_name': 'Información de punto', 'verbose_name_plural': 'Puntos información'},
        ),
        migrations.AlterModelOptions(
            name='pointshistory',
            options={'verbose_name': 'Historial de puntos generales y semanales', 'verbose_name_plural': 'Puntos historial'},
        ),
        migrations.AlterModelOptions(
            name='streamvip',
            options={'verbose_name': 'Stream Vip', 'verbose_name_plural': 'Streams Vip'},
        ),
        migrations.AlterModelOptions(
            name='topdailypoint',
            options={'verbose_name': 'Top', 'verbose_name_plural': 'Puntos diarios top'},
        ),
    ]