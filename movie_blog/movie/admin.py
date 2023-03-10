from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Настройка CKEDITOR для проекта.
class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url',)
    list_display_links = ('name', )


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ('name', 'email', 'parent')


class MoviewShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 0
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft') # какие поля отображать
    list_filter = ('category', 'year') # Меню фильтрации
    search_fields = ('title', 'category__name') # Меню поиска
    inlines = [MoviewShotsInline, ReviewInline, ] # инлайн блоки
    save_on_top = True # Меню сверху
    save_as = True  # Сохранение записи
    actions = ['unpublish', 'publish'] # Регистрация собственных actions
    list_editable = ('draft', )
    form = MovieAdminForm # Регистрация CKEDITOR
    readonly_fields = ('get_image', ) # Добавляем функция возврата изображения
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa",),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    #функция возврата изображения
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')


    #Написание собственных action - 'Действий в админке'
    def unpublish(self, request, queryset):
        '''Снять с публикации'''
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обелвена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        '''опубликовать'''
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обелвена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать' # Как это всё будет отображаться в админке
    publish.alloweb_permissions = ('change', )

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change', )

    get_image.short_description = 'Постер'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.Image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "ip")


admin.site.register(RatingStar)
admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'