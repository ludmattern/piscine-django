#!/usr/bin/python3

from elem import Elem, Text


class Html(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="html",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Head(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="head",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Body(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="body",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Title(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="title",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Meta(Elem):
    def __init__(self, attr={}):
        super().__init__(
            tag="meta",
            attr=attr,
            content=None,
            tag_type="simple",
        )


class Img(Elem):
    def __init__(self, attr={}):
        super().__init__(
            tag="img",
            attr=attr,
            content=None,
            tag_type="simple",
        )


class Table(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="table",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Th(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="th",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Tr(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="tr",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Td(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="td",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Ul(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="ul",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Ol(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="ol",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Li(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="li",
            attr=attr,
            content=content,
            tag_type="double",
        )


class H1(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="h1",
            attr=attr,
            content=content,
            tag_type="double",
        )


class H2(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="h2",
            attr=attr,
            content=content,
            tag_type="double",
        )


class P(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="p",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Div(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="div",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Span(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(
            tag="span",
            attr=attr,
            content=content,
            tag_type="double",
        )


class Hr(Elem):
    def __init__(self, attr={}):
        super().__init__(
            tag="hr",
            attr=attr,
            content=None,
            tag_type="simple",
        )


class Br(Elem):
    def __init__(self, attr={}):
        super().__init__(
            tag="br",
            attr=attr,
            content=None,
            tag_type="simple",
        )


def main():
    print("Structure de l'exercice précédent")
    html = Html(
        [
            Head(Title(Text('"Hello ground!"'))),
            Body(
                [
                    H1(Text('"Oh no, not again!"')),
                    Img(attr={"src": "http://i.imgur.com/pfp3T.jpg"}),
                ]
            ),
        ]
    )
    print(html)
    print()

    print("Test complet")
    page_complete = Html(
        [
            Head(
                [
                    Meta(attr={"charset": "UTF-8"}),
                    Meta(
                        attr={
                            "name": "viewport",
                            "content": "width=device-width",
                        }
                    ),
                    Title(Text("Page de test complète")),
                ]
            ),
            Body(
                [
                    H1(Text("Titre principal")),
                    H2(Text("Sous-titre")),
                    P(Text("Ceci est un paragraphe.")),
                    Hr(),
                    Div(
                        [
                            P(
                                Text("Paragraphe dans une div"),
                                attr={
                                    "class": "text",
                                },
                            ),
                            Span(Text("Texte dans un span")),
                        ],
                        attr={"id": "main-div", "class": "container"},
                    ),
                    Br(),
                    Ul(
                        [
                            Li(Text("Item 1")),
                            Li(Text("Item 2")),
                            Li(Text("Item 3")),
                        ]
                    ),
                    Ol([Li(Text("Premier")), Li(Text("Deuxième"))]),
                    Table(
                        [
                            Tr([Th(Text("Colonne 1")), Th(Text("Colonne 2"))]),
                            Tr([Td(Text("Donnée 1")), Td(Text("Donnée 2"))]),
                        ]
                    ),
                    Img(attr={"src": "image.jpg", "alt": "Une image"}),
                ]
            ),
        ]
    )
    print(page_complete)


if __name__ == "__main__":
    main()
