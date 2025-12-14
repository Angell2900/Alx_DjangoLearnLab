from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from accounts.models import CustomUser  # or your user model
from posts.models import Post, Comment, Like
from .models import Notification
from django.db.models.signals import m2m_changed
from accounts.models import CustomUser


# When a user likes a post
@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.user,
            actor=instance.user,
            verb='liked your post',
            target=instance.post
        )

# When a user comments on a post
@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.user,
            actor=instance.user,
            verb='commented on your post',
            target=instance.post
        )

# When a user follows another user
@receiver(post_save, sender=CustomUser)
def create_follow_notification(sender, instance, created, **kwargs):
    # This depends on how you implement following; if you have a M2M 'following' field, you might need m2m_changed signal instead
    pass

@receiver(m2m_changed, sender=CustomUser.following.through)
def create_follow_notification(sender, instance, action, reverse, pk_set, **kwargs):
    if action == 'post_add':
        for followed_user_id in pk_set:
            followed_user = CustomUser.objects.get(pk=followed_user_id)
            Notification.objects.create(
                recipient=followed_user,
                actor=instance,
                verb='started following you'
            )
