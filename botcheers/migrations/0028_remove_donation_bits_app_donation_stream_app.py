# Generated by Django 4.0.4 on 2023-08-03 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0095_remove_topdailypoint_position_topdailypoint_amount'),
        ('botcheers', '0027_donation_bits_app'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='bits_app',
        ),
        migrations.AddField(
            model_name='donation',
            name='stream_app',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.stream', verbose_name='Stream de bits realizados'),
        ),
    ]
