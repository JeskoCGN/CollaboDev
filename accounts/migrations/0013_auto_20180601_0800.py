# Generated by Django 2.0 on 2018-06-01 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_profile_last_action'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='last_action',
            new_name='last_ping',
        ),
    ]
