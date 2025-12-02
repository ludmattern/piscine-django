#!/usr/bin/env python3


class HotBeverage:

    name = "hot beverage"
    price = 0.30

    def description(self) -> str:
        return "Just some hot water in a cup."

    def __str__(self):
        return (
            f"name : {self.name}\n"
            f"price : {self.price:.2f}\n"
            f"description : {self.description()}"
        )


class Coffee(HotBeverage):

    name = "coffee"
    price = 0.40

    def description(self):
        return "A coffee, to stay awake."


class Tea(HotBeverage):

    name = "tea"


class Chocolate(HotBeverage):

    name = "chocolate"
    price = 0.50

    def description(self):
        return "Chocolate, sweet chocolate..."


class Cappuccino(HotBeverage):

    name = "cappuccino"
    price = 0.45

    def description(self):
        return "Un po’ di Italia nella sua tazza!"


def main():
    hot_beverage = HotBeverage()
    coffee = Coffee()
    tea = Tea()
    chocolate = Chocolate()
    cappuccino = Cappuccino()

    beverages = [hot_beverage, coffee, tea, chocolate, cappuccino]

    for beverage in beverages:
        print(beverage)
        print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
