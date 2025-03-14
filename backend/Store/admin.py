from django.contrib import admin
from .models import (
    Promotion, Category, Product, Recipe, Order, OrderItem,
    WishList, Review, Delivery
)
# Register your models here.


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("id", "is_discount", "discount_percentage", "is_featured")
    list_filter = ("is_discount", "is_featured")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("-created_at",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "seller", "category", "price", "available", "created_at")
    search_fields = ("name", "seller__user__email")
    list_filter = ("available", "category", "created_at")
    ordering = ("-created_at",)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "created_at")
    search_fields = ("product__name",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "status", "total_price", "created_at")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "subtotal", "created_at")
    search_fields = ("order__id", "product__name")
    ordering = ("-created_at",)

@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "product", "created_at")
    search_fields = ("buyer__user__email", "product__name")
    ordering = ("-created_at",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "buyer", "rating", "created_at")
    search_fields = ("product__name", "buyer__user__email")
    list_filter = ("rating", "created_at")
    ordering = ("-created_at",)

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "company_name", "delivery_person_name", "delivery_person_contact")
    search_fields = ("company_name", "delivery_person_name")
    ordering = ("-order__created_at",)
