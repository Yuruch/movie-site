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
    MovieCreateView,
    DirectorCreateView,
    DirectorUpdateView,
    add_review,
    user_detail_view,
    toggle_add_to_favourites,
    UserUpdateView,
    MovieDeleteView,
    DirectorDeleteView,
    ActorDeleteView,
    update_review,
    delete_review,
)

urlpatterns = [
    path("", index, name="home"),
    path("user/<int:pk>/", user_detail_view, name="user-detail"),
    path("user/<int:pk>/update", UserUpdateView.as_view(), name="user-update"),
    path("actors/", ActorListView.as_view(), name="actor-list"),
    path("actors/create/", ActorCreateView.as_view(), name="actor-create"),
    path(
        "actors/<int:pk>/update/",
        ActorUpdateView.as_view(),
        name="actor-update"
    ),
    path("actors/<int:pk>/", ActorDetailView.as_view(), name="actor-detail"),
    path(
        "actors/<int:pk>/delete/",
        ActorDeleteView.as_view(),
        name="actor-delete"
    ),
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("movies/create/", MovieCreateView.as_view(), name="movie-create"),
    path(
        "movies/<int:pk>/add_favourite/",
        toggle_add_to_favourites,
        name="toggle-add-to-favourites",
    ),
    path(
        "movies/<int:pk>/update/",
        MovieUpdateView.as_view(),
        name="movie-update"
    ),
    path(
        "movies/<int:pk>/delete/",
        MovieDeleteView.as_view(),
        name="movie-delete"
    ),
    path("movie/<int:pk>/add_review/", add_review, name="review-create"),
    path(
        "movie/<int:movie_pk>/review/<int:review_pk>/update/",
        update_review,
        name="review-update"
    ),
    path(
        "movie/<int:movie_pk>/review/<int:review_pk>/delete/",
        delete_review,
        name="review-delete"
    ),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("directors/", DirectorListView.as_view(), name="director-list"),
    path(
        "directors/create/",
        DirectorCreateView.as_view(),
        name="director-create"
    ),
    path(
        "directors/<int:pk>/update/",
        DirectorUpdateView.as_view(),
        name="director-update"
    ),
    path(
        "directors/<int:pk>/delete/",
        DirectorDeleteView.as_view(),
        name="director-delete"
    ),
    path(
        "directors/<int:pk>/",
        DirectorDetailView.as_view(),
        name="director-detail"
    ),

]

app_name = "movies"
