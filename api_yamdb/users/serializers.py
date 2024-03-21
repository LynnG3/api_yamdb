import math
import random

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import CustomUser


class UserCodeSerializer(serializers.ModelSerializer):
    '''Класс-сериализатор для модели CustomUser

    Поле username проходит валидацию как регулярное выражение,
    ограничено в длине переменной USERNAME_MAX_LEN и не может
    быть равно значению 'me'.
    Поле confirmation_code доступно только для записи и не
    отправляет пользователю в ответе на запрос.
    Поле email проверяется на уникальность и ограничено в длине
    переменной EMAIL_MAX_LEN.
    '''

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def get_confirmation_code(self):
        "Функция генерации кода подтверждения."
        string = ('0123456789abcdefghijklmnopqrstuvwxyz'
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        OTP = ""
        length = len(string)
        for i in range(settings.CONFIRMATION_CODE_LENGHT):
            OTP += string[math.floor(random.random() * length)]

        return OTP

    def validate(self, data):
        confirmation_code = self.get_confirmation_code()
        validated_data = super(UserCodeSerializer, self).validate(data)
        validated_data['confirmation_code'] = confirmation_code
        return validated_data


class UserJWTSerializer(serializers.Serializer):
    "Класс-сериализатор для отправки пользователю JWT-токена"

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
        read_only_fields = ('username', 'confirmation_code')

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(CustomUser, username=username)

        if user:
            if user.confirmation_code == confirmation_code:
                return data

            raise serializers.ValidationError(
                {"confirmation_code": "Confirmation code is wrong."})


class UserSerializer(serializers.ModelSerializer):
    "Класс-сериализатор для модели CustomUser"

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
