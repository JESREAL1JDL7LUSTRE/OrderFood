from django.contrib import admin
from .models import Delivery

# Register your models here.

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("order", "company_name", "status", "created_at")
    list_filter = ("status", "company_name")
    search_fields = ("order__id", "company_name")