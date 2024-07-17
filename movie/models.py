from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE


class Genre(models.Model):
    name = models.CharField(max_length=255)


class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(
        validators=(
            MinValueValidator(6),
            MaxValueValidator(100)
        )
    )


class Actor(models.Model):
    bio = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(
        validators=(
            MinValueValidator(6),
            MaxValueValidator(100)
        )
    )


class Review(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="reviews"
    )
    rating = models.IntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(10),
        )
    )
    film = models.ForeignKey("Movie", on_delete=CASCADE, related_name="reviews")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Movie(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    director = models.ManyToManyField(Director, related_name="movies")
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")
    rating = models.DecimalField(max_digits=4, decimal_places=2)

    # poster = models.ImageField()


class User(AbstractUser):
    # profile_pic = models.ImageField()
    favourite_films = models.ManyToManyField(Movie, related_name="users")
