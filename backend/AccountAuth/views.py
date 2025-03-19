from AccountAuth.serializers import UserSerializer
from .models import User
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets, permissions, generics
from sendEmail import send_email
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import SellerProfile


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

@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_seller(request, token):
    user_id = verify_token(token)
    if not user_id:
        return Response({"message": "Invalid or expired token."}, status=400)

    user = get_object_or_404(User, id=user_id)

    if hasattr(user, 'seller_profile'):
        return Response({"message": "User is already a seller."}, status=400)

    # Create seller profile
    SellerProfile.objects.create(user=user)

    # Send approval email
    send_email(user.email, "seller_approval", username=user.username)

    return Response({"message": f"User {user.username} approved as a seller."}, status=200)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def deny_seller(request, token):
    user_id = verify_token(token)
    if not user_id:
        return Response({"message": "Invalid or expired token."}, status=400)

    user = get_object_or_404(User, id=user_id)

    if hasattr(user, 'seller_profile'):
        return Response({"message": "User is already a seller."}, status=400)

    # Send denial email
    send_email(user.email, "seller_denial", username=user.username)

    return Response({"message": f"User {user.username} was denied seller status."}, status=200)
