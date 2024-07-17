from django.urls import path

from movie.views import (
    index,
    ActorListView,
    ActorDetailView,
    MovieListView,
    MovieDetailView,
    DirectorListView,
    DirectorDetailView,
)

urlpatterns = [
    path("", index, name="home"),
    path("actors/", ActorListView.as_view(), name="actor_list"),
    path("actors/<int:pk>/", ActorDetailView.as_view(), name="actor_detail"),
    path("movies/", MovieListView.as_view(), name="movie_list"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path("directors/", DirectorListView.as_view(), name="directors_list"),
    path(
        "directors/<int:pk>/",
        DirectorDetailView.as_view(),
        name="director_detail"
    ),

]

app_name = "movies"
