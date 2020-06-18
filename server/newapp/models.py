import os

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin

from .validators import valida_img

root_img = os.path.normpath(os.path.join(settings.MEDIA_ROOT, "img/"))
root_img_default = os.path.normpath(os.path.join(settings.MEDIA_ROOT, "img/placeholder.jpg"))

#Model de users
class User(AbstractBaseUser, PermissionsMixin):
    objects = BaseUserManager()
    USERNAME_FIELD = 'email'
    user=models.CharField(max_length=50, unique=True, null=True, blank=True)
    nome=models.CharField(max_length=100, null=True, blank=True)
    email=models.EmailField(max_length=100, unique=True)
    data_registo=models.DateTimeField(default=timezone.now)
    password=models.CharField(max_length=30, null=True, blank=True)
    tipo_user=models.CharField(max_length=30, default="base")
    photo=models.ImageField(upload_to=root_img, default=root_img_default, validators=[valida_img])
    criado_por=models.IntegerField(null=True)
    is_staff = models.BooleanField(default=False)
    
    # def __repr__(self):
    #     return self.user