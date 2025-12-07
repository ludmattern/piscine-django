"""
URL configuration for loremipsum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from .views import (
    ArticleListView,
    HomeView,
    CustomLoginView,
    CustomLogoutView,
    ArticleDetailView,
    PublicationListView,
    FavouriteListView,
    RegisterView,
    PublishArticleView,
    FavouriteCreateView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("articles/", ArticleListView.as_view(), name="articles"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("detail/<int:pk>/", ArticleDetailView.as_view(), name="detail"),
    path("publications/", PublicationListView.as_view(), name="publications"),
    path("favourites/", FavouriteListView.as_view(), name="favourites"),
    path("register/", RegisterView.as_view(), name="register"),
    path("publish/", PublishArticleView.as_view(), name="publish"),
    path("favourite/", FavouriteCreateView.as_view(), name="favourite_create"),
]
