# Generated by Django 2.0 on 2018-06-19 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20180619_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='associated_image',
            field=models.ImageField(blank=True, upload_to='user_content/profile_images/'),
        ),
    ]
