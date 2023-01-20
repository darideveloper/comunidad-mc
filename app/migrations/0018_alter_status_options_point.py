# Generated by Django 4.0.4 on 2023-01-18 20:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_comment_status_whatchcheck_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Estatus', 'verbose_name_plural': 'Estatus'},
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(editable=False, help_text='id del punto', primary_key=True, serialize=False, verbose_name='id')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, help_text='fecha y hora del punto', verbose_name='fecha y hora')),
                ('stream', models.ForeignKey(help_text='stream al que pertenece el punto', on_delete=django.db.models.deletion.CASCADE, to='app.stream', verbose_name='stream')),
                ('user', models.ForeignKey(help_text='usuario que ha hecho el punto', on_delete=django.db.models.deletion.CASCADE, to='app.user', verbose_name='usuario')),
            ],
            options={
                'verbose_name': 'Punto',
                'verbose_name_plural': 'Puntos',
            },
        ),
    ]