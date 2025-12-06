from django.shortcuts import HttpResponse, render
import psycopg2
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def get_db_connection():
    db_settings = settings.DATABASES["default"]
    return psycopg2.connect(
        dbname=db_settings["NAME"],
        user=db_settings["USER"],
        password=db_settings["PASSWORD"],
        host=db_settings["HOST"],
        port=db_settings["PORT"],
    )


def init(request):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Create table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ex06_movies (
                title VARCHAR(64) UNIQUE NOT NULL,
                episode_nb INTEGER PRIMARY KEY,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL,
                created TIMESTAMP DEFAULT NOW(),
                updated TIMESTAMP DEFAULT NOW()
            );
        """
        )

        # Create function
        cur.execute(
            """
            CREATE OR REPLACE FUNCTION update_changetimestamp_column()
            RETURNS TRIGGER AS $$
            BEGIN
            NEW.updated = now();
            NEW.created = OLD.created;
            RETURN NEW;
            END;
            $$ language 'plpgsql';
        """
        )

        # Create trigger (drop if exists to avoid error on re-run if table exists but trigger logic changed or just to be safe)
        cur.execute(
            "DROP TRIGGER IF EXISTS update_films_changetimestamp ON ex06_movies;"
        )
        cur.execute(
            """
            CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
            ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
            update_changetimestamp_column();
        """
        )

        conn.commit()
        cur.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def populate(request):
    movies = [
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

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        for movie in movies:
            try:
                cur.execute(
                    """
                    INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                    movie,
                )
                conn.commit()
                response_text += "OK<br>"
            except Exception as e:
                conn.rollback()
                response_text += f"{movie[1]}: {e}<br>"

        cur.close()
        conn.close()
        return HttpResponse(response_text)

    except Exception as e:
        return HttpResponse(f"Database connection error: {e}")


def display(request):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ex06_movies")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return HttpResponse("No data available")

        html = "<table border='1'><thead><tr><th>Title</th><th>Episode</th><th>Opening Crawl</th><th>Director</th><th>Producer</th><th>Release Date</th><th>Created</th><th>Updated</th></tr></thead><tbody>"
        for row in rows:
            html += "<tr>"
            for cell in row:
                html += f"<td>{cell if cell is not None else ''}</td>"
            html += "</tr>"
        html += "</tbody></table>"

        return HttpResponse(html)

    except Exception as e:
        return HttpResponse("No data available")


@csrf_exempt
def update(request):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if request.method == "POST":
            title = request.POST.get("title")
            opening_crawl = request.POST.get("opening_crawl")
            if title:
                cur.execute(
                    "UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s",
                    (opening_crawl, title),
                )
                conn.commit()

        cur.execute("SELECT title FROM ex06_movies")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return HttpResponse("No data available")

        html = """
        <form method="post">
            <select name="title">
        """
        for row in rows:
            html += f'<option value="{row[0]}">{row[0]}</option>'

        html += """
            </select>
            <br>
            <textarea name="opening_crawl" rows="4" cols="50"></textarea>
            <br>
            <input type="submit" value="update">
        </form>
        """

        return HttpResponse(html)

    except Exception as e:
        return HttpResponse("No data available")
