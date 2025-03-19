from django.db import models
from Store.models import Order

# Create your models here.

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery")  
    company_name = models.CharField(max_length=100)
    delivery_person_name = models.CharField(max_length=50)
    delivery_person_contact = models.CharField(max_length=15)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("In Transit", "In Transit"),
            ("Delivered", "Delivered"),
            ("Failed", "Failed"),
        ],
        default="Pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.id} - {self.status}"
