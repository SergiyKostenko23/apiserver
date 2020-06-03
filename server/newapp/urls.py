from django.urls import path, include
from .views import UserViewSet, CustomAuthToken
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path("user", UserViewSet.as_view({
        "get":"list",
        "put":"edit",
        "delete":"destroy",
        "post":"create",
        })),
    path("auth", CustomAuthToken.as_view())
]