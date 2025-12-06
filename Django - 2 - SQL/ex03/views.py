from django.shortcuts import HttpResponse
from .models import Movies


def populate(request):
    movies_data = [
        (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
        (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
        (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
        (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
        (
            5,
            "The Empire Strikes Back",
            "Irvin Kershner",
            "Gary Kutz, Rick McCallum",
            "1980-05-17",
        ),
        (
            6,
            "Return of the Jedi",
            "Richard Marquand",
            "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "1983-05-25",
        ),
        (
            7,
            "The Force Awakens",
            "J. J. Abrams",
            "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "2015-12-11",
        ),
    ]

    response_text = ""

    for episode_nb, title, director, producer, release_date in movies_data:
        try:
            Movies.objects.create(
                episode_nb=episode_nb,
                title=title,
                director=director,
                producer=producer,
                release_date=release_date,
            )
            response_text += "OK<br>"
        except Exception as e:
            response_text += f"{title}: {e}<br>"

    return HttpResponse(response_text)


def display(request):
    try:
        movies = Movies.objects.all()
        if not movies:
            return HttpResponse("No data available")

        html = "<table border='1'><thead><tr><th>Title</th><th>Episode</th><th>Opening Crawl</th><th>Director</th><th>Producer</th><th>Release Date</th></tr></thead><tbody>"
        for movie in movies:
            html += "<tr>"
            html += f"<td>{movie.title}</td>"
            html += f"<td>{movie.episode_nb}</td>"
            html += f"<td>{movie.opening_crawl if movie.opening_crawl else ''}</td>"
            html += f"<td>{movie.director}</td>"
            html += f"<td>{movie.producer}</td>"
            html += f"<td>{movie.release_date}</td>"
            html += "</tr>"
        html += "</tbody></table>"

        return HttpResponse(html)
    except Exception as e:
        return HttpResponse("No data available")
