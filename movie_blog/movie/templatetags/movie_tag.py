from django import template

from movie.models import Movie, Category

register = template.Library()

# Отличие simple от inclusion тега, в том что inclusion - умеет генерировать шаблон



@register.simple_tag()
def get_categories():
    '''Вывод всех категорий'''
    return Category.objects.all()


@register.inclusion_tag('movie/tags/last_movie.html')
def get_last_movie(count=5):
    '''Вывод последних фильмов'''
    movies = Movie.objects.order_by('id')[:count]
    return {'last_movies': movies}
