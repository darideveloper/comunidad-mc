# Generated by Django 4.0.4 on 2022-12-19 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_token',
            field=models.CharField(default=0, help_text='user access token', max_length=50, verbose_name='access_token'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.URLField(blank=True, help_text='user picture', verbose_name='picture'),
        ),
        migrations.AddField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(default='000', help_text='user refresh token', max_length=50, verbose_name='refresh_token'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, help_text='user email', max_length=254, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(help_text='user twitch id', primary_key=True, serialize=False, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, help_text='user name', max_length=100, verbose_name='name'),
        ),
    ]
