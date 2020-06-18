from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.parsers import FileUploadParser
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token

from google.oauth2 import id_token
from google.auth.transport import requests

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication
from .models import User
from .serializers import UserSerializer
from .mixins import DynamicFieldsViewMixin
from .permissions import CreateUserPermssion

#View para contornar CSRF
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

#View de users
class UserViewSet(DynamicFieldsViewMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, OAuth2Authentication,)
    permission_classes = (IsAuthenticated, CreateUserPermssion,)
    parser_class = (FileUploadParser,)
    SAFE_METHODS = ['GET']

    def edit(self, request):
        user_to_update = get_object_or_404(User, id=request.data["id"])
        serializer = UserSerializer(user_to_update, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request):
        user_to_destroy = get_object_or_404(User, id=request.data["id"])
        user_to_destroy.delete()
        return Response(_("User Successfully Deleted."), status=status.HTTP_200_OK)

    def create(self, request):
            serializer = UserSerializer(data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        if "id" in request.query_params:
            if User.objects.filter(id=request.query_params["id"]):
                queryset = User.objects.filter(id=request.query_params["id"])
            else:
                return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#View de autenticação a partir de Google
class GoogleAuthViewSet(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_id_token(self, request):
        token = request.data["idtoken"]
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Erro ao fazer autenticação com o Google.')
        except ValueError:
            return Response("Token inválido", status=status.HTTP_400_BAD_REQUEST)
        data = {
            "email":idinfo['email'],
            "nome":idinfo['name']
        }
        photo = idinfo['picture']
        if User.objects.filter(email=data['email']).count()>0:
            token = Token.objects.get_or_create(user=User.objects.get(email=data['email']))
            t = {
                "token": Token.objects.get(user=User.objects.get(email=data['email'])).key
                }
            return Response(t, status.HTTP_200_OK)
        else:            
            serializer = UserSerializer(data=data, context={'photo':photo})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            uid = User.objects.get(email=data['email']).id
            Token.objects.get_or_create(user=User.objects.get(id=uid))
            t = {
                "token": Token.objects.get(user=uid).key
                }
            return Response(t, status=status.HTTP_200_OK)