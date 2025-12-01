#!/usr/bin/env python3

import sys


def state():
    states = {
        "Oregon": "OR",
        "Alabama": "AL",
        "New Jersey": "NJ",
        "Colorado": "CO",
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver",
    }

    if len(sys.argv) != 2:
        return

    capital = sys.argv[1]

    state_code = None
    for code, city in capital_cities.items():
        if city == capital:
            state_code = code
            break

    if state_code:
        for state_name, code in states.items():
            if code == state_code:
                print(state_name)
                return

    print("Unknown capital city")


if __name__ == "__main__":
    try:
        state()
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)
