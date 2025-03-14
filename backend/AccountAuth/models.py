from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, Q

from Store.models import Product  

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(unique=True, max_length=150, blank=False)
    birth_date = models.DateField(blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.URLField(blank=True, default="")

    @property
    def age(self):
        today = date.today()
        return (
            today.year - self.birth_date.year - 
            ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def save_oauth_data(self, oauth_response):
        """Updates avatar URL from OAuth2 response."""
        self.avatar = oauth_response.get("picture", self.avatar)
        self.save(update_fields=["avatar"])  # ✅ Prevents full save

    # Use email as login field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "birth_date"]

    def is_seller(self):
        return self.groups.filter(name="Seller").exists()

    def is_buyer(self):
        return self.groups.filter(name="Buyer").exists()

    def is_admin(self):
        return self.is_superuser

    def __str__(self):
        return self.email


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="buyer_profile")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def sold_products(self):
        """Counts the number of sold products."""
        return Product.objects.filter(seller=self).count()

    def revenue(self):
        """Calculates total revenue from delivered orders."""
        return Product.objects.filter(seller=self).aggregate(
            total_revenue=Sum("orderitem__subtotal", filter=Q(orderitem__order__status="delivered"))
        )["total_revenue"] or 0

    def top_selling_products(self, limit=5):
        """Returns the top N best-selling products based on order quantity."""
        return (
            Product.objects.filter(seller=self)
            .annotate(
                total_sold=Sum("orderitem__quantity", filter=Q(orderitem__order__status="delivered"))
            )
            .order_by("-total_sold")
            .values("id", "name", "total_sold")[:limit]  # ✅ Optimized selection
        )


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address = models.JSONField(default=list)  # ✅ Supports multiple addresses
