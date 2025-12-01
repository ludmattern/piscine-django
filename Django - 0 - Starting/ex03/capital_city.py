#!/usr/bin/env python3

import sys

def capital_city():
    states = {
        "Oregon" : "OR",
        "Alabama" : "AL",
        "New Jersey": "NJ",
        "Colorado" : "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }
    
    if len(sys.argv) != 2:
        return
    
    state = sys.argv[1]
    
    if state in states:
        state_code = states[state]
        print(capital_cities[state_code])
    else:
        print("Unknown state")


if __name__ == '__main__':
    try:
        capital_city()
    except Exception as e:
        print(f"Erreur: {e}")
