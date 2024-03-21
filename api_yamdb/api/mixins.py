from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from users.permissions import IsAdminOrReadOnly


class CategoryGengeMixin(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    """Миксин для представлений жанра и категории."""
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
