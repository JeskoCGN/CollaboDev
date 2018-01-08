# Generated by Django 2.0 on 2018-01-01 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_description',
            field=models.CharField(default='null', max_length=400),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='task_name',
            field=models.CharField(max_length=100),
        ),
    ]
