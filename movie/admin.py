from django.contrib import admin
from .models import (
    Genre,
    Director,
    Actor,
    Review,
    Movie,
    User
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_date", "age")
    search_fields = ("first_name", "last_name")
    list_filter = ("birth_date", "age")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_date", "age")
    search_fields = ("first_name", "last_name")
    list_filter = ("birth_date", "age")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("creator", "rating", "movie", "created_at")
    search_fields = ("creator__username", "movie__title", "rating")
    list_filter = ("created_at", "rating")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "release_date",
        "duration",
        "country",
        "average_rating"
    )
    search_fields = (
        "title",
        "directors__first_name",
        "directors__last_name",
        "actors__first_name",
        "actors__last_name",
    )
    list_filter = ("release_date", "country")
    filter_horizontal = ("directors", "genres", "actors")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active")
    filter_horizontal = ("favourite_movies",)
