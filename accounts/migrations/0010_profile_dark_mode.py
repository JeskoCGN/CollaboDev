# Generated by Django 2.0 on 2018-04-05 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20180321_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dark_mode',
            field=models.BooleanField(default=True),
        ),
    ]
