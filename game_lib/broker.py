from random import randint
from pprint import pformat
from item import Item


class Broker:
    def __init__(self, name: str = ''):
        self.name = name
        self.cash = randint(1500, 2000)
        self.inventory = dict(
            Silk=Item(
                cost=randint(250, 300),
                amount=randint(3, 5)
            ),
            Silver=Item(
                cost=randint(450, 600),
                amount=randint(2, 3)
            ),
            Gold=Item(
                cost=randint(750, 1000),
                amount=randint(1, 2)
            ),
            Diamond=Item(
                cost=randint(1800, 2000),
                amount=randint(0, 1)
            )
        )

    def __repr__(self) -> str:
        return pformat(self.__dict__).replace('\'', '"')

    def sell(self, item_name: str, amount: int) -> (int, bool):
        sell_success = False
        total_cost = amount * self.inventory[item_name].cost
        if self.inventory[item_name].amount > amount:
            sell_success = True
            self.inventory[item_name].amount -= amount
            self.cash += total_cost
        return total_cost, sell_success

    def refresh(self):
        self.inventory['Silk'].update_amount(2, 5)
        self.inventory['Silver'].update_amount(1, 3)
        self.inventory['Gold'].update_amount(0, 2)
        self.inventory['Diamond'].update_amount(0, 1)

        for item_name in self.inventory.keys():
            self.inventory[item_name].update_cost()


if __name__ == '__main__':
    print(Broker('PlayerA'))
