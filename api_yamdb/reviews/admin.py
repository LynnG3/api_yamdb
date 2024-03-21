from django.contrib import admin

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

admin.site.empty_value_display = '-empty-'


class GenreInline(admin.TabularInline):
    model = GenreTitle


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс настройки раздела отзывов."""

    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'pub_date',
        'title'
    )
    list_filter = ('author', 'score', 'pub_date')
    search_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки раздела комментариев."""

    list_display = (
        'pk',
        'author',
        'text',
        'pub_date',
        'review'
    )
    list_filter = ('author', 'pub_date')
    search_fields = ('author',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры отображены в админ-панели.
    Можно найти по названию. Фильтр по названию.
    """

    model = Genre,
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Названия произведений отображены в админ-панели.
    Можно найти по названию и году. Фильтр по году.
    """

    inlines = [GenreInline]
    list_display = ('id', 'name', 'year', 'category', 'display_genres',)
    list_editable = ('category',)
    search_fields = ('name', 'year',)
    list_filter = ('year',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории отображены в админ-панели.
    Можно найти по названию. Фильтр по названию.
    """

    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
