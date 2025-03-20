from rest_framework.response import Response
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.views import APIView
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTPONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTPONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        
        return response
    
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")
        
        if refresh_token:
            request.data["refresh"] = refresh_token
            
            response=super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                access_token = response.data.get("access")
                
                response.set_cookie(
                    'access',
                    access_token,
                    max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTPONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE
                )
        
        return response

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        
        access_token = request.COOKIES.get("access")
        
        if access_token:
            request.data["access"] = access_token
            
        return super().post(request, *args, **kwargs)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
    

"""
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
"""