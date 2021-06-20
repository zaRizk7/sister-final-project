from pprint import pformat
from random import random, randint


class Item:
    def __init__(self, cost: int, amount: int):
        self.cost = cost
        self.amount = amount

    def __repr__(self) -> str:
        return pformat(self.__dict__)

    def update_cost(self):
        if random() < 0.5:
            rate = -self.cost * randint(0, 15) // 100
            if random() < 0.7:
                rate = self.cost * randint(0, 25) // 100
            self.cost += rate

    def update_amount(self, start, stop):
        self.amount += randint(start, stop)


if __name__ == "__main__":
    print(Item(2000, 15))
