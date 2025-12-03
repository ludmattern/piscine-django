#!/usr/bin/env python3

import random
from beverages import HotBeverage


class CoffeeMachine:

    def __init__(self):
        self.served_count = 0

    class EmptyCup(HotBeverage):
        name = "empty cup"
        price = 0.90

        def description(self) -> str:
            return "An empty cup?! Gimme my money back!"

    class BrokenMachineException(Exception):
        def __init__(self):
            self.message = "This coffee machine has to be repaired."
            super().__init__(self.message)

    def repair(self):
        self.served_count = 0

    def serve(self, beverage_class):
        if self.served_count >= 10:
            raise CoffeeMachine.BrokenMachineException()

        self.served_count += 1

        if random.choice([True, False]):
            return beverage_class()
        else:
            return CoffeeMachine.EmptyCup()


def main():
    from beverages import Coffee, Tea, Chocolate, Cappuccino

    machine = CoffeeMachine()
    beverages = [Coffee, Tea, Chocolate, Cappuccino]

    print("First cycle")
    try:
        for i in range(15):
            beverage_class = random.choice(beverages)
            drink = machine.serve(beverage_class)
            print(f"Serving {i + 1}:")
            print(drink)
            print()
    except CoffeeMachine.BrokenMachineException as e:
        print(f"Exception caught: {e.message}\n")

    print("Repairing machine")
    machine.repair()
    print("Machine repaired!\n")

    print("Second cycle (until breakdown)")
    try:
        for i in range(15):
            beverage_class = random.choice(beverages)
            drink = machine.serve(beverage_class)
            print(f"Serving {i + 1}:")
            print(drink)
            print()
    except CoffeeMachine.BrokenMachineException as e:
        print(f"Exception caught: {e.message}\n")


if __name__ == "__main__":
    main()
