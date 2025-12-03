#!/usr/bin/env python3

import sys
import json
import requests
import dewiki
import re


def error_exit(message):
    """Affiche un message d'erreur et quitte le programme."""
    print(f"Erreur: {message}", file=sys.stderr)
    sys.exit(1)


def clean_wikitext(wikitext):
    text = wikitext
    while True:
        new_text = re.sub(r"\{\{[^{}]*\}\}", "", text)
        if new_text == text:
            break
        text = new_text

    text = dewiki.from_string(text)

    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.DOTALL)
    text = re.sub(r"<ref[^>]*/>", "", text)
    text = re.sub(r"Fichier:[^\n]*", "", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    text = text.strip()

    return text


def search_wikipedia(query):
    url = "https://fr.wikipedia.org/w/api.php"

    headers = {"User-Agent": "PythonWikipediaBot/1.0 (Educational Project)"}

    content_params = {
        "action": "parse",
        "page": query,
        "prop": "wikitext",
        "format": "json",
        "redirects": "true",
    }

    try:
        response = requests.get(url, params=content_params, headers=headers)
        response.raise_for_status()
        page_data = response.json()

        if "error" in page_data:
            error_exit(
                f"Page non trouvée: {page_data['error'].get('info', 'Erreur inconnue')}"
            )

        wikitext = page_data["parse"]["wikitext"]["*"]
        page_title = page_data["parse"]["title"]

        clean_text = clean_wikitext(wikitext)

        return page_title, clean_text

    except requests.exceptions.RequestException as e:
        error_exit(f"Erreur de connexion à l'API Wikipedia: {e}")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        error_exit(f"Erreur lors du traitement de la réponse: {e}")


def write_to_file(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    except IOError as e:
        error_exit(f"Impossible d'écrire dans le fichier: {e}")


def main():
    if len(sys.argv) != 2:
        error_exit("Usage: python3 request_wikipedia.py <recherche>")

    query = sys.argv[1]

    if not query.strip():
        error_exit("La recherche ne peut pas être vide")

    page_title, content = search_wikipedia(query)

    filename = query.replace(" ", "_").lower() + ".wiki"

    write_to_file(filename, content)

    print(f"Résultat écrit dans {filename}")


if __name__ == "__main__":
    main()
