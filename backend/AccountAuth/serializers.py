from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    def get_image(self, obj):
        if obj.image:
            return obj.image.url  # This should return the full Cloudinary URL
        return None
    
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "username", "phone_number", "password", "address", "image", "date_joined", "updated_at", "last_login"]
        extra_kwargs = {
            "password": {"write_only": True},  # Hide password in responses
        }
        
    def create(self, validated_data):
        password = validated_data.pop("password", None)  # Remove password from validated data
        User = User(**validated_data)
        if password:
            User.set_password(password)  # Hash the password before saving
        User.save()
        return User