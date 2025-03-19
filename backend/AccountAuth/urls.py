from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileView, approve_seller, deny_seller

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users') 

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    re_path(r'^auth/', include('djoser.social.urls')),
    path('sellers/approve/<int:user_id>/', approve_seller, name='approve_seller'),
    path('sellers/deny/<int:user_id>/', deny_seller, name='deny_seller'),
]
