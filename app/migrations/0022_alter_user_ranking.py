# Generated by Django 4.0.4 on 2023-01-23 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_user_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ranking',
            field=models.ForeignKey(blank=True, default=1, help_text='ranking del usuario', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ranking', verbose_name='ranking'),
        ),
    ]
