from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, token_auth

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/', token_auth, name='token-auth'),
]