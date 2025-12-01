#!/usr/bin/env python3


def read_and_display_numbers():
    with open("numbers.txt", "r") as file:
        content = file.read()
        numbers = content.strip().split(",")
        for number in numbers:
            print(number)


if __name__ == "__main__":
    try:
        read_and_display_numbers()
    except Exception as e:
        print(f"Erreur: {e}")
