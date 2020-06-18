from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.transaction import atomic

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import User
from .mixins import DynamicFieldsSerializerMixin

from urllib.request import urlopen

#Serializer de users
class UserSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ('id', 'user', 'nome', 'email', 'data_registo', "password", 'tipo_user', 'criado_por', 'photo')
        fields = "__all__"

    @atomic
    def update(self, instance, validated_data):
        user = instance
        if validated_data.get('password', None) is not None:
            user.set_password(validated_data['password'])
        return user
  
    @atomic
    def create(self, validated_data):
        user = super().create(validated_data)
        if validated_data.get('password', None) is not None:
            user.set_password(validated_data['password'])

        try:
            u = self.context['request'].user
            user.criado_por = User.objects.filter(email=u)[0].id
        except:
            pass
        #if getattr(self.context['request'], None) is not None:
            #u = self.context['request'].user
            #user.criado_por = User.objects.filter(email=u)[0].id

        #Download de imagem do url
        try:
            image_url = self.context['photo']
            img_temp = NamedTemporaryFile("w+b")
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()
            user.photo = File(img_temp)
            user.photo.name = f"image_{user.id}.PNG"
        except:
            pass

        user.save()
        return user