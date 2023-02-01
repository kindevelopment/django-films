from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Movie, Category, Actor, Genre
from .forms import ReviewForm, RatingForm


class GenreYear:
    '''Жанры и года выхода фильмов'''
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year') # Сначала мы отфильтровали список фильмов,
        # убрали те что находятся в черновике, затем методом .value вытащили поле 'year' каждого фильма


class MoviesView(GenreYear, ListView):
    '''Список фильмов'''
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 1


    #Таким образом можно вывести список всех категорий, но минус заключается в том
    # что придётся передавать данный метод каждому классу, которые формируют наши страницы - можно перебирать циклом в шаблоне
    # Вопрос решается созданием ТЕМПЛЕЙТ ТЭГОВ

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context


class AddReview(View):
    '''Отзывы'''
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            #form.movie_id = pk - Есть такой вариант установлении связи между объектами
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    '''Вывод информации о актере'''
    model = Actor
    template_name = 'movie/actor.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    '''Фильтр фильмов'''
    paginate_by = 2

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct() # - метод distinct - позволяет отсеять повторяющиеся элементы
        #Q Позволяет работать с фильрами более гибко

        #Позволяет year__in все фильмы
        # которые входят в гет запрос возвращаемый лист 'year' от клиента
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class Search(ListView):
    '''Поиск фильмов'''
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))
        # - Фильтруем по полю title, __icontains - даёт возможность отключить значение регистра строки.

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context