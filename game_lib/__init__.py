from numpy import random
from twisted.web.xmlrpc import XMLRPC
from game_lib.broker import Broker
from game_lib.player import PlayerMenu
from game_lib.item import Item


class GameHandler(XMLRPC):
    def __init__(self, n_broker, *args, **kwargs):
        super(GameHandler, self).__init__(*args, **kwargs)
        self.day = 1
        self.broker_list = {i + 1: Broker(f"Broker {i+1}") for i in range(n_broker)}

    def xmlrpc_is_affordable(
        self, broker_id: int, item_name: str, amount: int, current_cash: int
    ) -> bool:
        total_cost = self.broker_list[broker_id].calculate_cost(item_name, amount)
        return total_cost, total_cost <= current_cash

    def xmlrpc_buy(
        self,
        player_name: str,
        broker_id: int,
        item_name: str,
        amount: int,
        current_cash: int,
    ) -> (int, str):
        try:
            if self.broker_list[broker_id].inventory[item_name].amount - amount >= 0:
                total_cost, is_affordable = self.xmlrpc_is_affordable(
                    broker_id, item_name, amount, current_cash
                )
                diff = abs(current_cash - total_cost)
                if is_affordable:
                    total_cost, sell_success = self.broker_list[broker_id].sell(
                        item_name, amount
                    )
                    # if not sell_success:
                    #     print(f"{player_name} : failed to buy because broker ")
                    #     return 0, f'Broker {broker_id} does not have enough {item_name}!'
                    print(f"{player_name} : Buy Successful")
                    return (
                        total_cost,
                        f"Successful purchase! Remaining cash is ${diff:,.2f}.",
                    )
                print(f"{player_name} : Buy Failed")
                return 0, f"Insufficient fund! Need ${diff:,.2f} more!"
            else:
                print(f"{player_name} : Buy Failed")
                return 0, f"Broker ran out of stock"
        except:
            return 0, f"No Broker {broker_id} registered"

    def xmlrpc_sell(
        self,
        player_name: str,
        broker_id: int,
        item_name: str,
        amount: int,
        total_cost: int,
    ) -> bool:
        try:
            print(f"{player_name} : Sell Successful")
            return self.broker_list[broker_id].buy(item_name, amount, total_cost)
        except:
            print(f"{player_name} : Sell Failed")
            return False

    def xmlrpc_update(self):
        if random.uniform() < 0.05:
            for i in self.broker_list:
                self.broker_list[i].refresh()
            self.day += 1
        return f"[DAY {self.day}]" if self.day != 1 else "[DAY 1]"

    def xmlrpc_preview(self, player_name: str, broker_id: int):
        try:
            result = f"Broker {broker_id}'s inventory:\n"
            for item_name, item_obj in self.broker_list[broker_id].inventory.items():
                cost, amount = item_obj.cost, item_obj.amount
                result += f"\t{item_name}\tCost: {cost}\tAvailable Amount: {amount}\n"
            print(f"{player_name} : Viewing Broker {broker_id} Successful")
            return result
        except:
            print(f"{player_name} : Viewing Broker {broker_id} Failed")
            return f"No Broker {broker_id} registered"

    def xmlrpc_get_broker_list(self):
        return ["Broker "+str(b) for b in self.broker_list]

    def xmlrpc_identifier(self, player_name: str):
        print(f"{player_name} : Connected to server.")
        return 0


if __name__ == "__main__":
    from twisted.internet import reactor
    from twisted.web.server import Site

    game_handler = GameHandler(4)
    reactor.listenTCP(7080, Site(game_handler))
    reactor.run()
