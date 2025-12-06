from django.shortcuts import render
from .models import People, Movies
from .forms import SearchForm
from django.db.models import Q


def index(request):
    results = []
    has_searched = False
    if request.method == "POST":
        has_searched = True
        form = SearchForm(request.POST)
        if form.is_valid():
            min_date = form.cleaned_data["min_release_date"]
            max_date = form.cleaned_data["max_release_date"]
            diameter = form.cleaned_data["planet_diameter"]
            gender = form.cleaned_data["gender"]

            characters = People.objects.filter(
                gender=gender,
                homeworld__diameter__gte=diameter,
                movies__release_date__range=(min_date, max_date),
            ).distinct()

            for char in characters:
                movies = char.movies.filter(release_date__range=(min_date, max_date))
                for movie in movies:
                    results.append(
                        {
                            "character_name": char.name,
                            "gender": char.gender,
                            "movie_title": movie.title,
                            "planet_name": (
                                char.homeworld.name if char.homeworld else "Unknown"
                            ),
                            "planet_diameter": (
                                char.homeworld.diameter if char.homeworld else "Unknown"
                            ),
                        }
                    )
    else:
        form = SearchForm()

    return render(
        request,
        "ex10/index.html",
        {"form": form, "results": results, "has_searched": has_searched},
    )
