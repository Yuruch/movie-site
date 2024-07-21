from django.test import TestCase
from movie.forms import (
    ActorForm,
    DirectorForm,
    MovieForm,
    ReviewForm,
    SignUpForm,
    UserUpdateForm,
    MovieSearchForm,
    ActorSearchForm,
    DirectorSearchForm
)
from movie.models import (
    Actor,
    Director,
    Movie,
    Genre
)
from datetime import timedelta


class FormTests(TestCase):
    def setUp(self):
        self.director = Director.objects.create(
            first_name="Quentin",
            last_name="Tarantino",
            birth_date="1963-03-27",
            age=60
        )
        self.actor = Actor.objects.create(
            first_name="Leonardo",
            last_name="DiCaprio",
            birth_date="1974-11-11",
            age=49
        )
        self.genre = Genre.objects.create(name="Drama")
        self.movie = Movie.objects.create(
            title="Inception",
            description="A mind-bending thriller",
            release_date="2010-07-16",
            duration=timedelta(hours=2, minutes=28),
            country="United States"
        )

    def test_actor_form(self):
        form = ActorForm(data={
            "first_name": "Leonardo",
            "last_name": "DiCaprio",
            "bio": "An amazing actor",
            "age": 49,
            "movies": [self.movie.id]
        })
        self.assertTrue(form.is_valid())

    def test_director_form(self):
        form = DirectorForm(data={
            "first_name": "Quentin",
            "last_name": "Tarantino",
            "bio": "A great director",
            "age": 60,
            "movies": [self.movie.id]
        })
        self.assertTrue(form.is_valid())

    def test_movie_form(self):
        form = MovieForm(data={
            "title": "Inception",
            "description": "A mind-bending thriller",
            "release_date": "2010-07-16",
            "duration": timedelta(hours=2, minutes=28),
            "country": "United States",
            "genres": [self.genre.id],
            "directors": [self.director.id],
            "actors": [self.actor.id]
        })
        self.assertTrue(form.is_valid())

    def test_review_form(self):
        form = ReviewForm(data={
            "rating": 9,
            "comment": "Amazing movie!"
        })
        self.assertTrue(form.is_valid())

    def test_sign_up_form(self):
        form = SignUpForm(data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "Fuceqwe1",
            "password2": "Fuceqwe1"
        })
        self.assertTrue(form.is_valid())

    def test_user_update_form(self):
        form = UserUpdateForm(data={
            "username": "updateduser",
            "email": "updateduser@example.com",
            "profile_pic": ""
        })
        self.assertTrue(form.is_valid())

    def test_movie_search_form(self):
        form = MovieSearchForm(data={
            "title": "Inception",
            "genre": self.genre.id
        })
        self.assertTrue(form.is_valid())

    def test_actor_search_form(self):
        form = ActorSearchForm(data={
            "name": "Leonardo"
        })
        self.assertTrue(form.is_valid())

    def test_director_search_form(self):
        form = DirectorSearchForm(data={
            "name": "Quentin"
        })
        self.assertTrue(form.is_valid())
