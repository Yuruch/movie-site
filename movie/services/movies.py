from django.db.models import QuerySet, Avg

from movie.models import Movie, User, Genre


def best_movies(number: int) -> QuerySet:
    return Movie.objects.annotate(
        avg_rating=Avg("reviews__rating")
    ).order_by("-avg_rating")[:number]


def movie_you_like(user: User, number: int) -> QuerySet:
    genres = Genre.objects.filter(movies__users=user).distinct()
    return Movie.objects.filter(
        genres__in=genres
    ).annotate(
        avg_rating=Avg("reviews__rating")
    ).filter(
        avg_rating__gte=5
    ).order_by("-avg_rating")[:number]
