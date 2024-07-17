from django.urls import path

from movie.views import (
    index,
    ActorListView,
    ActorDetailView,
    ActorCreateView,
    ActorUpdateView,
    MovieListView,
    MovieDetailView,
    DirectorListView,
    DirectorDetailView,
    MovieUpdateView,
    MovieCreateView, DirectorCreateView, DirectorUpdateView,
)

urlpatterns = [
    path("", index, name="home"),
    path("actors/", ActorListView.as_view(), name="actor_list"),
    path("actors/create/", ActorCreateView.as_view(), name="actor_create"),
    path("actors/<int:pk>/update/", ActorUpdateView.as_view(), name="actor_update"),
    path("actors/<int:pk>/", ActorDetailView.as_view(), name="actor_detail"),
    path("movies/", MovieListView.as_view(), name="movie_list"),
    path("movies/create/", MovieCreateView.as_view(), name="movie_create"),
    path(
        "movies/<int:pk>/update/",
        MovieUpdateView.as_view(),
        name="movie_update"
    ),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path("directors/", DirectorListView.as_view(), name="directors_list"),
    path("directors/create/", DirectorCreateView.as_view(), name="director_create"),
    path(
        "directors/<int:pk>/update/",
        DirectorUpdateView.as_view(),
        name="director_update"
    ),
    path(
        "directors/<int:pk>/",
        DirectorDetailView.as_view(),
        name="director_detail"
    ),

]

app_name = "movies"
