from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token

from .views import UserViewSet, GoogleAuthViewSet

urlpatterns = [
    path("user", UserViewSet.as_view({
        "get":"list",
        "put":"edit",
        "delete":"destroy",
        "post":"create",
        })),
    path("auth", obtain_auth_token, name='api_token_auth'),
    path("gauth", GoogleAuthViewSet.as_view({"post":"get_id_token"}), name='google_auth'),
]