#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup


def error_exit(message):
    print(f"Erreur: {message}", file=sys.stderr)
    sys.exit(1)


def get_wikipedia_page(title):
    url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
    headers = {"User-Agent": "PythonWikipediaBot/1.0 (Educational Project)"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        error_exit(f"Erreur de connexion: {e}")


def get_page_title(soup):
    title_tag = soup.find("h1", class_="firstHeading")
    if not title_tag:
        error_exit("Impossible de trouver le titre de la page")
    return title_tag.get_text()


def get_redirect_from(soup):
    """
    Détecte si la page affiche une redirection et retourne le titre d'origine.
    Retourne None s'il n'y a pas de redirection.
    """
    redirect_span = soup.find("span", class_="mw-redirectedfrom")
    if redirect_span:
        redirect_link = redirect_span.find("a")
        if redirect_link:
            href = redirect_link.get("href", "")
            if href.startswith("/wiki/"):
                return href.replace("/wiki/", "").replace("_", " ")
    return None


def is_valid_link(link, base_url="/wiki/"):
    href = link.get("href", "")

    if not href.startswith(base_url):
        return False

    invalid_prefixes = [
        "/wiki/Help:",
        "/wiki/Wikipedia:",
        "/wiki/File:",
        "/wiki/Special:",
        "/wiki/Portal:",
        "/wiki/Talk:",
        "/wiki/Category:",
        "/wiki/Template:",
        "/wiki/User:",
        "/wiki/Main_Page",
    ]

    for prefix in invalid_prefixes:
        if href.startswith(prefix):
            return False

    if "#" in href:
        return False

    return True


def is_in_parentheses(element):
    text_before = ""
    for sibling in element.previous_siblings:
        if hasattr(sibling, "get_text"):
            text_before = sibling.get_text() + text_before
        else:
            text_before = str(sibling) + text_before

    open_parens = text_before.count("(") - text_before.count(")")
    return open_parens > 0


def find_first_link(soup):
    content = soup.find("div", id="mw-content-text")
    if not content:
        return None

    parser_output = content.find("div", class_="mw-parser-output")
    if parser_output:
        content = parser_output

    paragraphs = content.find_all("p")

    for paragraph in paragraphs:
        if len(paragraph.get_text().strip()) < 10:
            continue

        links = paragraph.find_all("a")

        for link in links:
            if not is_valid_link(link):
                continue

            if link.find_parent(["i", "em"]):
                continue

            if is_in_parentheses(link):
                continue

            href = link.get("href")
            article_title = href.replace("/wiki/", "").replace("_", " ")
            return article_title

    return None


def roads_to_philosophy(starting_title):
    visited = []
    current_title = starting_title

    while True:
        soup = get_wikipedia_page(current_title)

        redirect_from = get_redirect_from(soup)
        if redirect_from:
            if redirect_from in visited:
                print(redirect_from)
                print("It leads to an infinite loop !")
                return
            print(redirect_from)
            visited.append(redirect_from)

        page_title = get_page_title(soup)

        if page_title in visited:
            print("It leads to an infinite loop !")
            return

        print(page_title)
        visited.append(page_title)

        if page_title == "Philosophy":
            count = len(visited)
            print(f"{count} roads from {visited[0]} to philosophy !")
            return

        next_title = find_first_link(soup)

        if next_title is None:
            print("It leads to a dead end !")
            return

        current_title = next_title


def main():
    if len(sys.argv) != 2:
        error_exit("Usage: python3 roads_to_philosophy.py <search>")

    query = sys.argv[1]

    if not query.strip():
        error_exit("The search cannot be empty")

    roads_to_philosophy(query)


if __name__ == "__main__":
    main()
