from django.contrib import admin
from .models import User, BuyerProfile, SellerProfile, Address

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "birth_date", "age", "phone_number", "is_active", "is_staff", "is_seller", "updated_at")
    search_fields = ("email", "username")
    list_filter = ("is_active", "is_staff", "groups")
    ordering = ("email",)

@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    search_fields = ("user__email", "user__username")
    ordering = ("-created_at",)

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "sold_products", "revenue", "top_selling_products", "created_at", "updated_at")
    search_fields = ("user__email", "user__username")
    ordering = ("-created_at",)

    def sold_products(self, obj):
        return obj.sold_products

    def revenue(self, obj):
        return obj.revenue()

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "address")
    search_fields = ("user__email", "user__username")

