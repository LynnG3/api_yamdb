from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import IntegerField

from reviews.models import (Category, Comment, Genre, Review,
                            Title)
from users.models import CustomUser

User = CustomUser


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для Отзывов"""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context['view'].kwargs['title_id']
            if Review.objects.filter(author=request.user,
                                     title=title_id).exists():
                raise validators.ValidationError(
                    'Нельзя оставлять отзыв дважды на одно и тоже произвдение'
                )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для Комментариев"""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        fields = ['name', 'slug']
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    class Meta:
        model = Genre
        fields = ['name', 'slug']
        lookup_field = 'slug'


class TitleReaderSerializer(serializers.ModelSerializer):
    """Сериализатор произведения - чтение."""

    category = CategorySerializer(
        read_only=True,
    )

    genre = GenreSerializer(
        many=True,
        read_only=True,
    )

    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleAdminSerializer(serializers.ModelSerializer):
    """Сериализатор произведения - запись."""

    year = IntegerField(
        validators=[
            MinValueValidator(settings.THE_EARLIEST_YEAR),
            MaxValueValidator(settings.CURRENT_YEAR)
        ]
    )
    genre = SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def to_representation(self, value):
        return TitleReaderSerializer(value).data
