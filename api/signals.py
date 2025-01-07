from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import BlogPost, AuthorSubscription, Notification

@receiver(post_save, sender=BlogPost)
def send_post_notification(sender, instance, created, **kwargs):
    if created:
        author_subscriptions = AuthorSubscription.objects.filter(author=instance.author)
        for subscription in author_subscriptions:
            Notification.objects.create(user=subscription.user, message=f"New post published by {instance.author.username}: {instance.title}.")