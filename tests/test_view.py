from django.test import TestCase, Client
from django.urls import reverse
from movie.models import Actor, Director, Movie, User, Genre, Review
from datetime import timedelta


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )
        self.client.login(username="testuser", password="12345")
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
        self.movie.directors.add(self.director)
        self.movie.actors.add(self.actor)
        self.movie.genres.add(self.genre)
        self.review = Review.objects.create(
            creator=self.user,
            rating=9,
            movie=self.movie,
            comment="Amazing movie!"
        )

    def test_index_view(self):
        response = self.client.get(reverse("movies:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")

    def test_actor_list_view(self):
        response = self.client.get(reverse("movies:actor_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Leonardo")

    def test_director_list_view(self):
        response = self.client.get(reverse("movies:directors_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quentin")

    def test_movie_list_view(self):
        response = self.client.get(reverse("movies:movie_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")

    def test_movie_detail_view(self):
        response = self.client.get(
            reverse(
                "movies:movie_detail",
                kwargs={"pk": self.movie.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A mind-bending thriller")

    def test_actor_detail_view(self):
        response = self.client.get(
            reverse(
                "movies:actor_detail",
                kwargs={"pk": self.actor.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Leonardo")

    def test_director_detail_view(self):
        response = self.client.get(
            reverse(
                "movies:director_detail",
                kwargs={"pk": self.director.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quentin")

    def test_add_review(self):
        response = self.client.post(
            reverse(
                "movies:add_review",
                kwargs={"pk": self.movie.id}),
            {"rating": 8, "comment": "Great movie!"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 2)

    def test_toggle_add_to_favourites(self):
        response = self.client.get(
            reverse(
                "movies:toggle-add-to-favourites",
                kwargs={"pk": self.movie.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.user.favourite_movies.filter(id=self.movie.id).exists()
        )

        response = self.client.get(
            reverse(
                "movies:toggle-add-to-favourites",
                kwargs={"pk": self.movie.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            self.user.favourite_movies.filter(id=self.movie.id).exists()
        )
