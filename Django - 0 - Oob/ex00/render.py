#!/usr/bin/env python3

import sys
import os


def error_exit(message):
    """Affiche un message d'erreur et quitte le programme."""
    print(f"Erreur: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        error_exit(
            "nombre d'arguments incorrect\nUsage: python3 render.py <fichier.template>"
        )

    template_file = sys.argv[1]

    if not template_file.endswith(".template"):
        error_exit("le fichier doit avoir l'extension .template")

    if not os.path.exists(template_file):
        error_exit(f"le fichier '{template_file}' n'existe pas")

    try:
        import settings
    except ImportError:
        error_exit("impossible d'importer settings.py")

    with open(template_file, "r") as f:
        content = f.read()

    settings_vars = {
        key: value for key, value in vars(settings).items() if not key.startswith("__")
    }

    try:
        result = content.format(**settings_vars)
    except KeyError as e:
        error_exit(f"variable manquante dans settings.py : {e}")

    output_file = template_file.replace(".template", ".html")

    with open(output_file, "w") as f:
        f.write(result)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_exit(str(e))
