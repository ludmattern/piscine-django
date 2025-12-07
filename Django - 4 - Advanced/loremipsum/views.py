from django.views.generic import ListView, RedirectView, DetailView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import Article, UserFavouriteArticle
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.shortcuts import redirect


class RegisterView(CreateView):
    template_name = "loremipsum/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")


class PublishArticleView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "loremipsum/publish.html"
    fields = ["title", "synopsis", "content"]
    success_url = reverse_lazy("publications")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class FavouriteCreateView(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    fields = ["article"]
    success_url = reverse_lazy("favourites")

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            # Handle case where favourite already exists if unique constraint exists
            # For now, just redirect to success_url
            return redirect(self.success_url)


class ArticleListView(ListView):
    model = Article
    template_name = "loremipsum/article_list.html"
    context_object_name = "articles"


class HomeView(RedirectView):
    pattern_name = "articles"


class CustomLoginView(LoginView):
    template_name = "loremipsum/login.html"
    next_page = reverse_lazy("home")


class CustomLogoutView(LogoutView):
    http_method_names = ["get", "post", "options"]

    # Allow GET request for logout to satisfy "Link" requirement in exercise context
    # though not recommended in production for Django 5+
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "loremipsum/article_detail.html"
    context_object_name = "article"


class PublicationListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "loremipsum/publication_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class FavouriteListView(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = "loremipsum/favourite_list.html"
    context_object_name = "favourites"

    def get_queryset(self):
        return UserFavouriteArticle.objects.filter(user=self.request.user)
