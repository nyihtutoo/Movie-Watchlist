from django.test import TestCase
from django.urls import reverse

from .models import Movie


class MovieModelTests(TestCase):
    def test_str_returns_title(self):
        movie = Movie.objects.create(title="Inception")
        self.assertEqual(str(movie), "Inception")

    def test_default_watched_is_false(self):
        movie = Movie.objects.create(title="Dune")
        self.assertFalse(movie.watched)

    def test_ordering_is_newest_first(self):
        first = Movie.objects.create(title="Old")
        second = Movie.objects.create(title="New")
        titles = list(Movie.objects.values_list("title", flat=True))
        self.assertEqual(titles, ["New", "Old"])
        self.assertEqual(Movie.objects.first(), second)
        self.assertEqual(Movie.objects.last(), first)


class MovieViewTests(TestCase):
    def test_list_view_status_ok(self):
        response = self.client.get(reverse("movies:movie_list"))
        self.assertEqual(response.status_code, 200)

    def test_create_movie(self):
        response = self.client.post(
            reverse("movies:movie_create"),
            {"title": "Interstellar", "genre": "Sci-Fi", "release_year": 2014,
             "personal_rating": 5, "watched": False},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Movie.objects.filter(title="Interstellar").exists())

    def test_update_movie(self):
        movie = Movie.objects.create(title="Old Title")
        self.client.post(
            reverse("movies:movie_update", args=[movie.pk]),
            {"title": "New Title", "genre": "", "release_year": "",
             "personal_rating": "", "watched": False},
        )
        movie.refresh_from_db()
        self.assertEqual(movie.title, "New Title")

    def test_delete_movie(self):
        movie = Movie.objects.create(title="To Delete")
        self.client.post(reverse("movies:movie_delete", args=[movie.pk]))
        self.assertFalse(Movie.objects.filter(pk=movie.pk).exists())

    def test_toggle_watched(self):
        movie = Movie.objects.create(title="Toggle Me", watched=False)
        self.client.post(reverse("movies:movie_toggle_watched", args=[movie.pk]))
        movie.refresh_from_db()
        self.assertTrue(movie.watched)

    def test_search_by_title(self):
        Movie.objects.create(title="The Matrix")
        Movie.objects.create(title="Titanic")
        response = self.client.get(reverse("movies:movie_list"), {"q": "matrix"})
        self.assertContains(response, "The Matrix")
        self.assertNotContains(response, "Titanic")
