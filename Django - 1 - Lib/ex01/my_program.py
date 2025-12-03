#!/usr/bin/env python3

from local_lib.path import Path


def create_and_write_file():
    folder = Path("test_folder")
    if not folder.exists():
        folder.mkdir()
        print(f"Dossier '{folder}' créé.")

    file = folder / "test_file.txt"

    file.write_text("test")

    read_content = file.read_text()
    print(f"\nContenu du fichier '{file}':")
    print(read_content)


if __name__ == "__main__":
    try:
        create_and_write_file()
    except Exception as e:
        print(f"Erreur: {e}")
