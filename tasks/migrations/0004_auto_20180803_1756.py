# Generated by Django 2.0 on 2018-08-03 16:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_bumped'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='bumped',
        ),
        migrations.AddField(
            model_name='task',
            name='bump_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
