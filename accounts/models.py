from hashlib import md5

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.timezone import now

from tasks.models import Task


class Profile(models.Model):
    """
    Extension of user model, added automatically upon user creation.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )

    avatar = models.ImageField(
        blank=True,
        upload_to='profile_avatars/'
    )
    background = models.ImageField(
        blank=True,
        upload_to='profile_backgrounds/'
    )
    gravatar_url = models.URLField(
        default='',
        max_length=1000,
    )

    url = models.URLField(max_length=2000,
                          blank=True)
    biography = models.CharField(max_length=1500, blank=True)
    tasks_completed = models.IntegerField(default=0)
    dark_mode = models.BooleanField(default=True)
    last_ping = models.DateTimeField(default=now)


# pylint: disable=unused-argument
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create profile model upon user creation
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save user profile on user save
    """
    email_hash = md5(instance.email.encode('utf-8').lower()).hexdigest()
    instance.profile.gravatar_url = ('https://www.gravatar.com/avatar/' +
                                     email_hash + '?d=404')
    instance.profile.save()
