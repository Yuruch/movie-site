from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from movie.models import (
    Genre,
    Director,
    Actor,
    Movie,
    Review,
    User
)


class GenreModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Action")

    def test_genre_str(self):
        self.assertEqual(str(self.genre), "Action")


class DirectorModelTest(TestCase):
    def setUp(self):
        self.director = Director.objects.create(
            first_name="John",
            last_name="Doe",
            bio="A well-known director.",
            birth_date="1970-01-01",
            age=54
        )
        self.genre = Genre.objects.create(name="Drama")
        self.movie = Movie.objects.create(
            title="A Great Film",
            release_date="2023-01-01",
            duration=timedelta(hours=2, minutes=0),  # Use timedelta object
            country="United States"
        )
        self.movie.directors.add(self.director)
        self.review = Review.objects.create(
            creator=User.objects.create_user(
                username="testuser",
                password="password"
            ),
            movie=self.movie,
            rating=8,
            comment="Great movie!"
        )

    def test_director_str(self):
        self.assertEqual(str(self.director), "John Doe")

    def test_director_best_movie(self):
        best_movie = self.director.best_movie
        self.assertEqual(best_movie, self.movie)


class ActorModelTest(TestCase):
    def setUp(self):
        self.actor = Actor.objects.create(
            first_name="Jane",
            last_name="Smith",
            bio="An acclaimed actress.",
            birth_date="1980-05-12",
            age=44
        )
        self.movie = Movie.objects.create(
            title="Another Great Film",
            release_date="2024-01-01",
            duration=timedelta(hours=1, minutes=45),  # Use timedelta object
            country="Canada"
        )
        self.movie.actors.add(self.actor)
        self.review = Review.objects.create(
            creator=User.objects.create_user(
                username="testactoruser",
                password="password"
            ),
            movie=self.movie,
            rating=9,
            comment="Excellent performance!"
        )

    def test_actor_str(self):
        self.assertEqual(str(self.actor), "Jane Smith")

    def test_actor_best_movie(self):
        best_movie = self.actor.best_movie
        self.assertEqual(best_movie, self.movie)


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reviewer",
            password="password"
        )
        self.movie = Movie.objects.create(
            title="Test Movie",
            release_date="2024-07-21",
            duration=timedelta(hours=2, minutes=30),  # Use timedelta object
            country="Germany"
        )
        self.review = Review.objects.create(
            creator=self.user,
            movie=self.movie,
            rating=7,
            comment="This is a test review."
        )

    def test_review_str(self):
        self.assertEqual(
            str(self.review),
            f"Review by {self.user.username} for {self.movie.title}"
        )

    def test_review_created_at(self):
        self.assertTrue(self.review.created_at <= timezone.now())


class MovieModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Sci-Fi")
        self.director = Director.objects.create(
            first_name="Steven",
            last_name="Spielberg",
            birth_date="1946-12-18",
            age=77
        )
        self.actor = Actor.objects.create(
            first_name="Tom",
            last_name="Hanks",
            birth_date="1956-07-09",
            age=67
        )
        self.movie = Movie.objects.create(
            title="Sci-Fi Classic",
            description="A classic science fiction film.",
            release_date="2025-05-25",
            duration=timedelta(hours=2, minutes=30),  # Use timedelta object
            country="United States"
        )
        self.movie.genres.add(self.genre)
        self.movie.directors.add(self.director)
        self.movie.actors.add(self.actor)
        self.review = Review.objects.create(
            creator=User.objects.create_user(
                username="moviereviewer",
                password="password"
            ),
            movie=self.movie,
            rating=9,
            comment="Incredible film!"
        )

    def test_movie_str(self):
        self.assertEqual(str(self.movie), "Sci-Fi Classic")

    def test_movie_average_rating(self):
        self.assertEqual(self.movie.average_rating, 9.0)


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password"
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), "testuser")

    def test_user_profile_pic_default(self):
        self.assertEqual(self.user.profile_pic.name, "blank.png")
