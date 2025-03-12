from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import User  # Import your custom user model

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """Automatically seller Viewer and Seller groups after migrations."""
    
    # Create Groups
    seller_group, _ = Group.objects.get_or_create(name="Seller")
    buyer_group, _ = Group.objects.get_or_create(name="Viewer")

    # Ensure the permission exists before adding it
    try:
        seller_perm = Permission.objects.get(codename="seller_permission")
        seller_group.permissions.add(seller_perm)
    except Permission.DoesNotExist:
        print("Permission 'seller_permission' does not exist. Run `makemigrations` and `migrate`.")
