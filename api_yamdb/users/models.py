from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import check_me_name


class CustomUser(AbstractUser):
    "Кастомная модель пользователя."

    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = ((ROLE_USER, 'user'), (ROLE_MODERATOR, 'moderator'),
                    (ROLE_ADMIN, 'admin'))

    username = models.CharField(
        'Никнейм пользователя',
        unique=True,
        help_text=('Обязательное. 150 знаков или менее. Допустимы буквы, '
                   'цифры и @/./+/-/_.'),
        max_length=settings.USERNAME_MAX_LEN,
        validators=(RegexValidator(regex=r'^[\w.@+-]+\Z',
                                   message='Forbidden symbol in username!'),
                    check_me_name))
    confirmation_code = models.CharField(
        'Код подтверждения',
        blank=True,
        max_length=settings.CONFIRMATION_CODE_LENGHT)
    email = models.EmailField('Электронная почта',
                              unique=True,
                              max_length=settings.EMAIL_MAX_LEN)
    bio = models.TextField('О себе', blank=True)
    role = models.CharField('Права доступа',
                            max_length=len(
                                max(ROLE_CHOICES, key=lambda t: len(t[0]))[0]),
                            blank=False,
                            choices=ROLE_CHOICES,
                            default=ROLE_USER)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR
