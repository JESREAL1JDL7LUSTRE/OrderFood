import uuid
from django.db import models
from Store.models import Order
from AccountAuth.models import BuyerProfile  # Assuming users have BuyerProfiles

# Create your models here.
class PaymentMethod(models.Model):
    METHOD_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("Epay", "Electronic Payment"),
        ("Card", "Card Payment"),
    ]
    name = models.CharField(max_length=20, choices=METHOD_CHOICES, unique=True)

    def __str__(self):
        return self.name

class PaymentBank(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(max_length=255, unique=True)
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name="payments")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    payment_bank = models.ForeignKey(PaymentBank, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"