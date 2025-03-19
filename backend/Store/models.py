from django.db import models
from django.db.models import Sum, Avg
from django.core.validators import MinValueValidator, MaxValueValidator

class Promotion(models.Model):
    is_discount = models.BooleanField(default=False)
    discount_percentage = models.FloatField(null=True, default=0.0)
    is_featured = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=255, null=False)  # ✅ Added max_length
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name = models.CharField(max_length=50, null=False)
    seller = models.ForeignKey("AccountAuth.SellerProfile", on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, null=True, on_delete=models.SET_NULL)  # ✅ Fixed missing on_delete
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # ✅ Fixed missing on_delete
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500)
    image = models.URLField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def sold_count(self):
        """Returns the total quantity of this product sold in delivered orders."""
        return OrderItem.objects.filter(product=self, order__status="Delivered").aggregate(
            total_sold=Sum("quantity")
        )["total_sold"] or 0

    def average_rating(self):
        """Returns the average rating for the product."""
        return Review.objects.filter(product=self).aggregate(avg_rating=Avg("rating"))["avg_rating"] or 0

class Recipe(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # ✅ Fixed missing on_delete
    instructions = models.TextField(max_length=1000)
    ingredients = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

ORDER_STATUS = [
    ("Pending", "Pending"),
    ("Shipped", "Shipped"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
]

class Order(models.Model):
    buyer = models.ForeignKey("AccountAuth.BuyerProfile", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="Pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # ✅ Fixed field definition
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def subtotal(self):
        """Calculates the subtotal price for this order item."""
        return (self.product.price or 0) * self.quantity  # ✅ Fixed calculation

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WishList(models.Model):
    buyer = models.ForeignKey("AccountAuth.BuyerProfile", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items")  # ✅ Fixed capitalization & added related_name
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")  # ✅ Added related_name
    buyer = models.ForeignKey("AccountAuth.BuyerProfile", on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)