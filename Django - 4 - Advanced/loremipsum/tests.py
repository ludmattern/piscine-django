from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Article, UserFavouriteArticle
from django.db.utils import IntegrityError


class AccessControlTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_favourites_view_requires_login(self):
        """Verifies that the favourites view is only accessible to logged-in users."""
        response = self.client.get(reverse("favourites"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/en/login/?next=/en/favourites/")

        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("favourites"))
        self.assertEqual(response.status_code, 200)

    def test_publications_view_requires_login(self):
        """Verifies that the publications view is only accessible to logged-in users."""
        response = self.client.get(reverse("publications"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/en/login/?next=/en/publications/")

        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("publications"))
        self.assertEqual(response.status_code, 200)

    def test_publish_view_requires_login(self):
        """Verifies that the publish view is only accessible to logged-in users."""
        response = self.client.get(reverse("publish"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/en/login/?next=/en/publish/")

        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("publish"))
        self.assertEqual(response.status_code, 200)


class RegistrationAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_logged_in_user_cannot_access_register(self):
        """Verifies that a logged-in user cannot access the registration form."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("register"))
        self.assertNotEqual(response.status_code, 200)


class DuplicateFavouriteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.article = Article.objects.create(
            title="Test Article", author=self.user, content="Content"
        )

    def test_user_cannot_add_same_favourite_twice(self):
        """Verifies that a user cannot add the same article to favourites twice."""
        self.client.login(username="testuser", password="password")

        UserFavouriteArticle.objects.create(user=self.user, article=self.article)

        with self.assertRaises(IntegrityError):
            UserFavouriteArticle.objects.create(user=self.user, article=self.article)
