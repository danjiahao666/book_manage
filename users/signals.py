from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    当用户创建时，自动创建用户配置文件
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    当用户保存时，自动保存用户配置文件
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # 如果用户没有配置文件，创建一个
        UserProfile.objects.create(user=instance) 