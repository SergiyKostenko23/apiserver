from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'nome', 'email', 'data_registo', 'tipo_user', 'criado_por', 'photo']
    readonly_fields = ('id', 'criado_por')

# Register your models here.
admin.site.register(User, UserAdmin)