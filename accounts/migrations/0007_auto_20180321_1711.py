# Generated by Django 2.0 on 2018-03-21 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20180321_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gravatar_url',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
