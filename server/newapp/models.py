from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, user, nome, criado_por, data_registo=None, tipo_user=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        u = self.model(
            email=self.normalize_email(email),
            user=user,
            nome=nome,
            criado_por=criado_por,
        )
        u.tipo_user=1
        u.set_password(password)
        u.save(using=self._db)
        return u

    def create_superuser(self, email, password, user, nome, criado_por):
        """
        Creates and saves a superuser with the given email and password.
        """
        u = self.create_user(
            email,
            user=user,
            nome=nome,
            password=password,
            criado_por=criado_por,
        )
        user.tpo_user=2
        u.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()
    REQUIRED_FIELDS = ('email', 'password', 'tipo_user', 'criado_por')
    USERNAME_FIELD = 'user'
    user=models.CharField(max_length=50, unique=True)
    nome=models.CharField(max_length=100)
    email=models.EmailField(max_length=100, unique=True)
    data_registo=models.DateTimeField(default=timezone.now)
    password=models.CharField(max_length=30)
    tipo_user=models.IntegerField(default=1)
    criado_por=models.IntegerField(default=None)
    def __str__(self):
        return self.user