import json
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from movie.models import Genre, Director, Actor, Movie, Review


class Command(BaseCommand):
    help = "Import data from JSON files into the database"

    def handle(self, *args, **kwargs):
        self.import_genres()
        self.import_movies()
        self.import_directors()
        self.import_actors()
        self.import_users()
        self.import_reviews()
        self.create_superuser()

    def import_genres(self):
        with open("initial_data/genres.json", "r") as file:
            genres = json.load(file)
            for genre in genres:
                Genre.objects.get_or_create(name=genre["name"])
        self.stdout.write(self.style.SUCCESS("Successfully imported genres"))

    def import_directors(self):
        with open("initial_data/directors.json", "r") as file:
            directors = json.load(file)
            for director in directors:
                director_obj, created = Director.objects.get_or_create(
                    first_name=director["first_name"],
                    last_name=director["last_name"],
                    defaults={
                        "bio": director.get("bio"),
                        "birth_date": director["birth_date"],
                        "age": director["age"],
                        "photo": director.get("photo", "blank.png")
                    }
                )
                if created:
                    movies = Movie.objects.filter(
                        title__in=director.get("movies", [])
                    )
                    director_obj.movies.set(movies)
        self.stdout.write(
            self.style.SUCCESS("Successfully imported directors")
        )

    def import_actors(self):
        with open("initial_data/actors.json", "r") as file:
            actors = json.load(file)
            for actor in actors:
                actor_obj, created = Actor.objects.get_or_create(
                    first_name=actor["first_name"],
                    last_name=actor["last_name"],
                    defaults={
                        "bio": actor.get("bio"),
                        "birth_date": actor["birth_date"],
                        "age": actor["age"],
                        "photo": actor.get("photo", "blank.png")
                    }
                )
                if created:
                    movies = Movie.objects.filter(
                        title__in=actor.get("movies", [])
                    )
                    actor_obj.movies.set(movies)
        self.stdout.write(self.style.SUCCESS("Successfully imported actors"))

    def import_movies(self):
        with open("initial_data/movies.json", "r") as file:
            movies = json.load(file)
            for movie in movies:
                movie_obj, created = Movie.objects.get_or_create(
                    title=movie["title"],
                    defaults={
                        "description": movie.get("description"),
                        "release_date": movie["release_date"],
                        "duration": self.parse_duration(movie["duration"]),
                        "country": movie["country"],
                        "poster": f"{movie.get('title')}.jpg"
                    }
                )
                if created:
                    genres = Genre.objects.filter(id__lte=3)
                    movie_obj.genres.set(genres)
                    movie_obj.save()
        self.stdout.write(self.style.SUCCESS("Successfully imported movies"))

    def import_users(self):
        with open("initial_data/users.json", "r") as file:
            users = json.load(file)
            for user_data in users:
                user, created = get_user_model().objects.get_or_create(
                    username=user_data["username"],
                    defaults={
                        "email": user_data.get("email"),
                        "first_name": user_data.get("first_name"),
                        "last_name": user_data.get("last_name"),
                    }
                )
                if created:
                    user.set_password(user_data["password"])
                    user.profile_pic = "blank.png"
                    user.save()
                    favourite_movies = user_data.get("favourite_movies", [])
                    movies = Movie.objects.filter(title__in=favourite_movies)
                    user.favourite_movies.set(movies)

        self.stdout.write(self.style.SUCCESS("Successfully imported users"))

    def import_reviews(self):
        with open("initial_data/reviews.json", "r") as file:
            movies = json.load(file)
            for movie_data in movies:
                movie = Movie.objects.get(title=movie_data["title"])
                if movie:
                    for review_data in movie_data["reviews"]:
                        username = review_data.get("username")
                        user = get_user_model().objects.get(username=username)
                        if user:
                            Review.objects.get_or_create(
                                creator=user,
                                movie=movie,
                                defaults={
                                    "rating": review_data["rating"],
                                    "comment": review_data.get("comment"),
                                }
                            )
        self.stdout.write(self.style.SUCCESS("Successfully imported reviews"))

    def create_superuser(self):
        user = get_user_model()
        if not user.objects.filter(is_superuser=True).exists():
            user.objects.create_superuser(
                username="Yuruch",
                email="admin@example.com",
                first_name="Yurii",
                last_name="Yurchenko",
                profile_pic="blank.png",
                password="Fuceqwertyt1"
            )
            self.stdout.write(self.style.SUCCESS(
                "Successfully created superuser")
            )

    @staticmethod
    def parse_duration(duration_str):
        """Helper method to parse duration string to timedelta."""
        h, m, s = map(int, duration_str.split(':'))
        return timedelta(hours=h, minutes=m, seconds=s)
