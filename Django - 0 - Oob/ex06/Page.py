#!/usr/bin/python3

from elem import Elem, Text
from elements import (
    Html,
    Head,
    Body,
    Title,
    Meta,
    Img,
    Table,
    Th,
    Tr,
    Td,
    Ul,
    Ol,
    Li,
    H1,
    H2,
    P,
    Div,
    Span,
    Hr,
    Br,
)


class Page:

    def __init__(self, elem):
        if not isinstance(elem, Elem):
            raise TypeError("L'élément doit être une instance d'Elem")
        self.elem = elem

    def __str__(self):
        result = ""
        if isinstance(self.elem, Html):
            result = "<!DOCTYPE html>\n"
        result += str(self.elem)
        return result

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(str(self))

    def is_valid(self):
        return self._validate_elem(self.elem)

    def _validate_elem(self, elem):
        valid_types = (
            Html,
            Head,
            Body,
            Title,
            Meta,
            Img,
            Table,
            Th,
            Tr,
            Td,
            Ul,
            Ol,
            Li,
            H1,
            H2,
            P,
            Div,
            Span,
            Hr,
            Br,
            Text,
        )
        if not isinstance(elem, valid_types):
            return False

        # Règles spécifiques par type d'élément avec match/case
        match elem:
            case Html():
                return self._validate_html(elem)
            case Head():
                return self._validate_head(elem)
            case Body() | Div():
                return self._validate_body_or_div(elem)
            case Title() | H1() | H2() | Li() | Th() | Td():
                return self._validate_single_text(elem)
            case P():
                return self._validate_p(elem)
            case Span():
                return self._validate_span(elem)
            case Ul() | Ol():
                return self._validate_list(elem)
            case Tr():
                return self._validate_tr(elem)
            case Table():
                return self._validate_table(elem)
            case _:
                if hasattr(elem, "content"):
                    for child in elem.content:
                        if not self._validate_elem(child):
                            return False
                return True

    def _validate_html(self, elem):
        if len(elem.content) != 2:
            return False
        if not isinstance(elem.content[0], Head):
            return False
        if not isinstance(elem.content[1], Body):
            return False
        return self._validate_elem(elem.content[0]) and self._validate_elem(
            elem.content[1]
        )

    def _validate_head(self, elem):
        if len(elem.content) != 1:
            return False
        if not isinstance(elem.content[0], Title):
            return False
        return self._validate_elem(elem.content[0])

    def _validate_body_or_div(self, elem):
        if len(elem.content) == 0:
            return True
        for child in elem.content:
            if not isinstance(child, (H1, H2, Div, Table, Ul, Ol, Span, Text)):
                return False
            if not self._validate_elem(child):
                return False
        return True

    def _validate_single_text(self, elem):
        if len(elem.content) != 1:
            return False
        if not isinstance(elem.content[0], Text):
            return False
        return True

    def _validate_p(self, elem):
        if len(elem.content) == 0:
            return False
        for child in elem.content:
            if not isinstance(child, Text):
                return False
        return True

    def _validate_span(self, elem):
        if len(elem.content) == 0:
            return False
        for child in elem.content:
            if not isinstance(child, (Text, P)):
                return False
            if isinstance(child, P) and not self._validate_elem(child):
                return False
        return True

    def _validate_list(self, elem):
        if len(elem.content) == 0:
            return False
        for child in elem.content:
            if not isinstance(child, Li):
                return False
            if not self._validate_elem(child):
                return False
        return True

    def _validate_tr(self, elem):
        if len(elem.content) == 0:
            return False
        has_th = False
        has_td = False
        for child in elem.content:
            if isinstance(child, Th):
                has_th = True
            elif isinstance(child, Td):
                has_td = True
            else:
                return False
            if not self._validate_elem(child):
                return False
        # Th et Td doivent être mutuellement exclusifs
        if has_th and has_td:
            return False
        return True

    def _validate_table(self, elem):
        if len(elem.content) == 0:
            return False
        for child in elem.content:
            if not isinstance(child, Tr):
                return False
            if not self._validate_elem(child):
                return False
        return True


def test_valid_page():
    print("Page HTML valide")
    page = Page(
        Html(
            [
                Head(Title(Text("Page valide"))),
                Body(
                    [
                        H1(Text("Titre")),
                        Div([H2(Text("Sous-titre")), Text("Texte simple")]),
                        Table([Tr([Th(Text("Col1")), Th(Text("Col2"))])]),
                        Ul([Li(Text("Item 1")), Li(Text("Item 2"))]),
                    ]
                ),
            ]
        )
    )
    print(f"Validation: {page.is_valid()}")
    print(page)
    print()
    return page


def test_invalid_cases():
    tests = [
        ("Html sans Head", Html([Body([H1(Text("Test"))])])),
        (
            "Plus d'un Title",
            Html([Head([Title(Text("Test")), Title(Text("Test2"))]), Body([])]),
        ),
        (
            "Body avec Img",
            Html([Head(Title(Text("Test"))), Body([Img(attr={"src": "test.jpg"})])]),
        ),
        (
            "H1 avec plusieurs Text",
            Html([Head(Title(Text("Test"))), Body([H1([Text("A"), Text("B")])])]),
        ),
        ("Ul vide", Html([Head(Title(Text("Test"))), Body([Ul([])])])),
        (
            "Tr avec Th et Td mélangés",
            Html(
                [
                    Head(Title(Text("Test"))),
                    Body([Table([Tr([Th(Text("A")), Td(Text("B"))])])]),
                ]
            ),
        ),
    ]

    for name, elem in tests:
        page = Page(elem)
        print(f"{name} (invalide): {page.is_valid()}")
    print()


def test_file_writing(page):
    print("Écriture dans un fichier")
    filename = "test_page.html"
    page.write_to_file(filename)
    print(f"Fichier '{filename}' créé avec succès")
    print()


def test_simple_page():
    print("Page simple sans Html (valide)")
    page = Page(Div([H1(Text("Simple page")), Text("Contenu")]))
    print(f"Validation: {page.is_valid()}")
    print(page)


def main():
    valid_page = test_valid_page()
    test_invalid_cases()
    test_file_writing(valid_page)
    test_simple_page()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erreur: {e}")
