from django.contrib import admin
from .models import PaymentMethod, PaymentBank, Payment

# Register your models here.

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(PaymentBank)
class PaymentBankAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "buyer", "order", "payment_method", "payment_bank", "status", "amount", "currency", "created_at")
    search_fields = ("transaction_id", "buyer__user__email", "order__id")
    list_filter = ("status", "payment_method", "currency", "created_at")
    ordering = ("-created_at",)

