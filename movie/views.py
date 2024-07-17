from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from movie.models import Movie, Actor, Director


def index(request: HttpRequest) -> HttpResponse:
    num_movies = Movie.objects.count()
    num_actors = Actor.objects.count()
    num_directors = Director.objects.count()
    context = {
        "num_movies": num_movies,
        "num_actors": num_actors,
        "num_directors": num_directors,
    }
    return render(request, "movie/index.html", context)


def user_logout(request):
    logout(request)
    return render(request, "registration/logged_out.html")


class ActorListView(generic.ListView):
    model = Actor
    fields = "__all__"


class MovieListView(generic.ListView):
    model = Movie
    fields = "__all__"


class DirectorListView(generic.ListView):
    model = Director
    fields = "__all__"


class ActorDetailView(generic.DetailView):
    model = Actor
    fields = "__all__"
    queryset = Actor.objects.prefetch_related("films")


class DirectorDetailView(generic.DetailView):
    model = Director
    fields = "__all__"
    queryset = Director.objects.prefetch_related("films")


class MovieDetailView(generic.DetailView):
    model = Movie
    fields = "__all__"
    queryset = Movie.objects.select_related("reviews")

