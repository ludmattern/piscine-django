#!/usr/bin/env python3

import sys

def search_state(expr, states, capital_cities):
    for state_name, state_code in states.items():
        if state_name.lower() == expr.lower():
            capital = capital_cities[state_code]
            print(f"{capital} is the capital of {expr}")
            return True
    return False


def search_capital(expr, states, capital_cities):
    for code, city in capital_cities.items():
        if city.lower() == expr.lower():
            for state_name, state_code in states.items():
                if state_code == code:
                    print(f"{expr} is the capital of {state_name}")
                    return True
    return False


def all_in():
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
    
    if ',,' in sys.argv[1]:
        return
    
    expressions = sys.argv[1].split(',')
    
    for expr in expressions:
        expr_stripped = expr.strip()
        
        if not expr_stripped:
            continue
        
        if search_state(expr_stripped, states, capital_cities):
            continue
        
        if search_capital(expr_stripped, states, capital_cities):
            continue
        
        print(f"{expr_stripped} is neither a capital city nor a state")


if __name__ == '__main__':
    try:
        all_in()
    except Exception as e:
        print(f"Erreur: {e}")
