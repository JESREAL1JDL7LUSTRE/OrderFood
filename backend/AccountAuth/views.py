from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from AccountAuth.serializers import UserSerializer
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, permissions, generics

@login_required
def become_seller(request):
    user = request.user  # Get logged-in user
    seller_group, _ = Group.objects.get_or_create(name='Seller')

    # Condition: Check if the user is at least 18 years old
    if user.profile.age < 18:
        return JsonResponse({"message": "You need to be at least 18 years old to become a seller."}, status=400)

    # Check if the user is already a Seller
    if user.groups.filter(name='Seller').exists():
        return JsonResponse({"message": "You are already a seller!"}, status=400)

    # Upgrade user to Creator
    user.groups.add(seller_group)
    return JsonResponse({"message": "You are now a seller!"})

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action == "create":  # Allow sign-up
            return [AllowAny()]
        return [IsAuthenticated()]  # Require authentication for other actions
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "put", "patch"]

    def get_object(self):
        return self.request.user
    