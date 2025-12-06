from django.shortcuts import HttpResponse
import psycopg2
from django.conf import settings


def init(request):
    try:
        db_settings = settings.DATABASES["default"]
        conn = psycopg2.connect(
            dbname=db_settings["NAME"],
            user=db_settings["USER"],
            password=db_settings["PASSWORD"],
            host=db_settings["HOST"],
            port=db_settings["PORT"],
        )
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ex00_movies (
                title VARCHAR(64) UNIQUE NOT NULL,
                episode_nb INTEGER PRIMARY KEY,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL
            );
        """
        )
        conn.commit()
        cur.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
