from django.db.models import QuerySet, Avg
from django.db.models.functions import Round

from movie.models import (
    Movie,
    User,
    Genre
)


def best_movies(number: int) -> QuerySet:
    return Movie.objects.annotate(
        avg_rating=Round(Avg("reviews__rating"), 2)
    ).order_by("-avg_rating")[:number]


def movie_you_like(user: User, number: int) -> QuerySet:
    genres = Genre.objects.filter(movies__users=user).distinct()
    return Movie.objects.filter(
        genres__in=genres
    ).annotate(
        avg_rating=Round(Avg("reviews__rating"), 2)
    ).filter(
        avg_rating__gte=5
    ).order_by("-avg_rating")[:number]
