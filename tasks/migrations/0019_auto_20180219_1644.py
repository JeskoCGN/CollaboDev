# Generated by Django 2.0 on 2018-02-19 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0018_auto_20180219_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_task',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.Task'),
        ),
    ]