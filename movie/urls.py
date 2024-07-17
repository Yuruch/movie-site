from django.urls import path

from movie.views import (
    index,
    ActorListView,
    ActorDetailView,
    MovieListView,
    DirectorListView,
)

urlpatterns = [
    path("", index, name="home"),
    path("actors/", ActorListView.as_view(), name="actor_list"),
    path("movies/", MovieListView.as_view(), name="movie_list"),
    path("directors/", DirectorListView.as_view(), name="directors_list"),

]

app_name = "movies"
