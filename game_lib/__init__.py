from numpy import random
from twisted.web.xmlrpc import XMLRPC
from broker import Broker
from player import PlayerMenu


class GameHandler(XMLRPC):
    def __init__(self, n_broker, *args, **kwargs):
        super(GameHandler, self).__init__(*args, **kwargs)
        self.day = 1
        self.broker_list = [Broker(f'Broker {i+1}') for i in range(n_broker)]

    def xmlrpc_is_affordable(self, broker_id: int, item_name: str, amount: int, current_cash: int) -> bool:
        total_cost = self.broker_list[broker_id].calculate_cost(
            item_name, amount)
        return total_cost, total_cost <= current_cash

    def xmlrpc_buy(self, broker_id: int, item_name: str, amount: int, current_cash: int) -> (int, str):
        total_cost, is_affordable = self.xmlrpc_is_affordable(
            broker_id, item_name, amount, current_cash)
        diff = abs(current_cash - total_cost)
        if is_affordable:
            total_cost, sell_success = self.broker_list[broker_id].sell(
                item_name, amount)
            if not sell_success:
                0, f'Broker {broker_id} does not have enough {item_name}!'
            return total_cost, f'Successful purchase! Remaining cash is ${diff:,.2f}.'
        return 0, f'Insufficient fund! Need ${diff:,.2f} more!'

    def xmlrpc_sell(self, broker_id: int, item_name: str, amount: int, total_cost: int) -> bool:
        return self.broker_list[broker_id].buy(item_name, amount, total_cost)

    def xmlrpc_update(self):
        if random.uniform() < 0.05:
            for i in range(len(self.broker_list)):
                self.broker_list[i].refresh()
            self.day += 1
        return f'[DAY {self.day}]' if self.day == 1 else '[DAY 1]'

    def xmlrpc_preview(self, broker_id: int):
        result = f'Broker {broker_id} Catalogs:\n'
        for item_name, item_obj in self.broker_list[broker_id-1].inventory.items():
            cost, amount = item_obj.cost, item_obj.amount
            result += f'\t{item_name}\tCost: {cost}\tAvailable Amount: {amount}\n'
        return result


if __name__ == '__main__':
    from twisted.internet import reactor
    from twisted.web.server import Site
    game_handler = GameHandler(4)
    reactor.listenTCP(7080, Site(game_handler))
    reactor.run()