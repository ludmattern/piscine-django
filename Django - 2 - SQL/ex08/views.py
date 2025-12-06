from django.shortcuts import HttpResponse
import psycopg2
from django.conf import settings
import os


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

        # Create planets table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ex08_planets (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                climate VARCHAR,
                diameter INTEGER,
                orbital_period INTEGER,
                population BIGINT,
                rotation_period INTEGER,
                surface_water REAL,
                terrain VARCHAR(128)
            );
        """
        )

        # Create people table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ex08_people (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                birth_year VARCHAR(32),
                gender VARCHAR(32),
                eye_color VARCHAR(32),
                hair_color VARCHAR(32),
                height INTEGER,
                mass REAL,
                homeworld VARCHAR(64) REFERENCES ex08_planets(name)
            );
        """
        )

        conn.commit()
        cur.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def populate(request):
    response_text = ""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        planets_path = os.path.join(settings.BASE_DIR, "ex08/planets.csv")
        people_path = os.path.join(settings.BASE_DIR, "ex08/people.csv")

        # Populate planets
        with open(planets_path, "r") as f:
            cur.copy_expert(
                "COPY ex08_planets(name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain) FROM STDIN WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL')",
                f,
            )
        response_text += "Planets populated successfully.<br>"

        # Populate people
        with open(people_path, "r") as f:
            cur.copy_expert(
                "COPY ex08_people(name, birth_year, gender, eye_color, hair_color, height, mass, homeworld) FROM STDIN WITH (FORMAT CSV, DELIMITER E'\\t', NULL 'NULL')",
                f,
            )
        response_text += "People populated successfully.<br>"

        conn.commit()
        cur.close()
        conn.close()
        return HttpResponse(response_text)

    except Exception as e:
        return HttpResponse(f"Error: {e}")


def display(request):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            SELECT p.name, pl.name, pl.climate
            FROM ex08_people p
            JOIN ex08_planets pl ON p.homeworld = pl.name
            WHERE pl.climate LIKE '%windy%'
            ORDER BY p.name ASC;
        """

        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return HttpResponse("No data available")

        html = "<table border='1'><thead><tr><th>Name</th><th>Homeworld</th><th>Climate</th></tr></thead><tbody>"
        for row in rows:
            html += "<tr>"
            for cell in row:
                html += f"<td>{cell if cell is not None else ''}</td>"
            html += "</tr>"
        html += "</tbody></table>"

        return HttpResponse(html)

    except Exception as e:
        return HttpResponse("No data available")
