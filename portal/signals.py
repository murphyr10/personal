from django.urls import reverse
from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post, Comment, Notification

# Notify users when a new post is published
# Notify users when a new post is published (exclude post author)
@receiver(post_save, sender=Post)
def post_published(sender, instance, created, **kwargs):
    if created:
        # Notify all users except the post author
        users_to_notify = User.objects.exclude(id=instance.user.id)
        for user in users_to_notify:
            message = f"A new post titled '{instance.title}' has been published."
            post_url = reverse('post_single', args=[instance.id])  # Generate URL for the post detail
            Notification.objects.create(user=user, message=message, url=post_url)  # Create the notification

@receiver(post_save, sender=Comment)
def comment_added(sender, instance, created, **kwargs):
    if created:
        post_author = instance.post.user  # The author of the post
        # Ensure the post author doesn't get notified about their own comment
        if instance.user != post_author:  # Only notify if the comment is from a different user
            commenter_name = instance.user.username  # Get the username of the user who commented
            message = f"{commenter_name} commented on your post '{instance.post.title}'"
            post_url = reverse('post_single', args=[instance.post.id])  # URL of the post with the comment
            Notification.objects.create(user=post_author, message=message, url=post_url)  # Create the notification