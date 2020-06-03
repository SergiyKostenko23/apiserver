from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# Create your views here.
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': user,
            'nome': user.nome,
            'email': user.email,
            'data_registo': user.data_registo,
            'tipo_user': user.tipo_user,
            'criado_por': user.criado_por
        })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    def edit(self, request):
        user_to_update = User.objects.get(id=request.data["id"])
        serializer = UserSerializer(user_to_update, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request):
        user_to_destroy = User.objects.get(id=request.data["id"])
        user_to_destroy.delete()
        return Response(status=status.HTTP_200_OK)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)