from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE, Avg


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(default="1994-07-19")
    age = models.IntegerField(
        validators=(
            MinValueValidator(6),
            MaxValueValidator(100)
        )
    )
    photo = models.ImageField(
        default="blank_people.jpg",
        blank=True
    )

    @property
    def best_movie(self):
        return Movie.objects.filter(
            directors=self.id
        ).annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating').first()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(default="2004-05-12")
    age = models.IntegerField(
        validators=(
            MinValueValidator(6),
            MaxValueValidator(100)
        )
    )
    photo = models.ImageField(
        default="blank_people.jpg",
        blank=True
    )

    @property
    def best_movie(self):
        return Movie.objects.filter(
            actors=self.id
        ).annotate(
            avg_rating=Avg('reviews__rating')
        ).order_by('-avg_rating').first()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Review(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="reviews",
        blank=True,
    )
    rating = models.IntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(10),
        )
    )
    movie = models.ForeignKey("Movie", on_delete=CASCADE, related_name="reviews")
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    directors = models.ManyToManyField(
        Director,
        related_name="movies",
        blank=True,
    )
    genres = models.ManyToManyField(
        Genre,
        related_name="movies",
        blank=True
    )
    actors = models.ManyToManyField(
        Actor,
        related_name="movies",
        blank=True
    )

    @property
    def average_rating(self) -> float:
        return Review.objects.filter(
            movie=self
        ).aggregate(Avg("rating"))["rating__avg"] or 0
    poster = models.ImageField(
        default="blank_poster.webp",
        blank=True
    )

    def __str__(self):
        return self.title


class User(AbstractUser):
    profile_pic = models.ImageField(
        default="blank.png",
        blank=True,
    )
    favourite_movies = models.ManyToManyField(
        Movie,
        related_name="users",
        blank=True
    )
