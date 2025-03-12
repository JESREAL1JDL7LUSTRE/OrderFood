from datetime import date
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(unique=True, max_length=150, blank=False)
    birth_date = models.DateField(blank=False)
    @property
    def age(self):
        """Calculate user's age from birth_date."""
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, null=True)
    image = CloudinaryField("profile", null=True, blank=True)

    # Ensure email is used as the unique identifier instead of username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "birth_date"]  # ✅ Added birth_date since it's required

    def is_creator(self):
        return self.groups.filter(name='Seller').exists()

    def is_viewer(self):
        return self.groups.filter(name='Buyer').exists()

    def is_admin(self):
        return self.is_superuser  # Django's built-in admin check

    def __str__(self):
        return self.email

class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    