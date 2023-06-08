# Generated by Django 4.0.4 on 2023-06-08 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0083_streamfree'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyPointBackup',
            fields=[
                ('id', models.AutoField(editable=False, help_text='id del punto', primary_key=True, serialize=False, verbose_name='id')),
                ('general_point', models.ForeignKey(help_text='punto general al que pertenece el punto', on_delete=django.db.models.deletion.CASCADE, to='app.generalpoint', verbose_name='punto general')),
            ],
            options={
                'verbose_name': 'Punto semanal respaldo',
                'verbose_name_plural': 'Puntos semanales respaldo',
            },
        ),
    ]
