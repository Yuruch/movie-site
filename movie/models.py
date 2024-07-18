from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE, Avg


class Genre(models.Model):
    name = models.CharField(max_length=255)


class Director(models.Model):
    bio = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(
        validators=(
            MinValueValidator(6),
            MaxValueValidator(100)
        )
    )
    models.ImageField(
        default="blank_people.jpg",
        blank=True
    )


class Actor(models.Model):
    bio = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
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
    film = models.ForeignKey("Movie", on_delete=CASCADE, related_name="reviews")
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    director = models.ManyToManyField(
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
            film=self
        ).aggregate(Avg("rating"))["rating__avg"] or 0
    poster = models.ImageField(
        default="blank_poster.webp",
        blank=True
    )


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
