from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileView, become_seller, send_test_email

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users') 

urlpatterns = [
    path('', include(router.urls)),
    path('seller/', become_seller, name='become_seller'), 
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    re_path(r'^auth/', include('djoser.social.urls')),
    path("send-test-email/", send_test_email, name="send_test_email"),
]
