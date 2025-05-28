# users/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

@receiver(post_save, sender=User)
def assign_user_to_default_group(sender, instance, created, **kwargs):
    if created:
        try:
            default_group = Group.objects.get(name='user') # REPLACE with the exact name of your group
            instance.groups.add(default_group)
            # Optional: Print a message to the console for debugging
            print(f"User {instance.username} added to group '{default_group.name}'.")
        except Group.DoesNotExist:
            print("Warning: Default group 'Blog Readers' not found. Please create it in Django admin.")