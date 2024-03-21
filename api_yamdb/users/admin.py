from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    "Регистрация кастомных полей модели в админ-панели"

    fieldsets = UserAdmin.fieldsets + (
        ('Права доступа API',
            {'fields': ('role',), },
         ),
        ('Информация о пользователе',
            {'fields': ('bio',), },
         ),
    )
    list_display = (
        'username',
        'email',
        'role',
        'first_name',
        'last_name',
        'is_staff',
    )
    list_editable = ('role',)
