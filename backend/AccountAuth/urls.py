from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileView, become_seller

router = DefaultRouter()
router.register(r'seller', become_seller, basename='seller')
router.register(r'register', UserProfileView, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileView.as_view(), name='use-profile')
]
