from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ('id', 'user', 'nome', 'email', 'data_registo', 'password', 'tipo_user', 'criado_por')
        fields = "__all__"
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password('password')
        return user