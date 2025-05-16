from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Report, Notification

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

@receiver(post_save, sender=Report)
def notify_verified_user(sender, instance, created, **kwargs):
    if instance.date_submitted and not created:
        previous = sender.objects.filter(pk=instance.pk).first()
        if previous and previous.date_submitted != instance.date_submitted:
            Notification.objects.create(
                user=instance.verified_by,
                message=f"{instance.assigned_to.get_full_name()} submitted {instance.task_name}.",
                url=f"/reports/{instance.id}/" 
            )