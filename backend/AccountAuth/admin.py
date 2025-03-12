from django.contrib import admin
from .models import Group, Permission
from .serializers import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(Group)
admin.site.register(Permission)

class UserAdmin(UserAdmin):  
    model = User

    # Fields to display in the list view
    list_display = ("email", "username", "first_name", "last_name", "phone_number", "address", "is_active", "is_staff", "image_display")

    # Fields to search in the admin panel
    search_fields = ("email", "username", "phone_number")

    # Filters available on the right side
    list_filter = ("is_active", "is_staff")

    # Organizing fields in the edit page
    fieldsets = (
        ("Personal Info", {"fields": ("email", "username", "first_name", "last_name", "phone_number", "address", "image")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        ("Create User", {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "phone_number", "address", "password1", "password2"),
        }),
    )
    
    def image_display(self, obj):
        return obj.image.url if obj.image else "No Image"
    image_display.short_description = "Image"

    ordering = ("email",)

# Register the model with the customized admin panel
admin.site.register(User, UserAdmin)