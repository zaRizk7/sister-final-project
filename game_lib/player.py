from xmlrpc.client import ServerProxy
from game_lib.broker import Broker


class PlayerMenu(ServerProxy):
    def __init__(self, name, *args, **kwargs):
        super(PlayerMenu, self).__init__(*args, **kwargs)
        self.player = Broker(name)

    def prompt_command(self):
        self.identifier(self.player.name)
        command = self.get_input()
        while command[0] != 'quit':
            try:
                self.execute_command(command)
            except Exception as e:
                print(e)
            finally:
                command = self.get_input()
        end_state = 'WIN' if self.player.cash > 20000 else 'LOSE'
        print(f'You have ${self.player.cash:,.2f} remaining. You {end_state}!')

    def execute_command(self, command):
        if len(command) == 1:
            action = command[0]
            if action == "ping":
                self.ping(self.player.name)
        elif len(command) == 2:
            action, obj = command
            if action == 'view':
                if obj == 'broker':
                    for i, name in enumerate(self.get_broker_list()):
                        print(f'{i+1}. {name}')
                elif obj == 'inventory':
                    print(f'{self.player.name}\'s inventory:')
                    for item_name, item_obj in self.player.inventory.items():
                        cost, amount = item_obj.cost, item_obj.amount
                        print(
                            f'\t{item_name}\tCost: {cost}\tAvailable Amount: {amount}')
                    print(f'Remaining cash: ${self.player.cash:,.2f}')
                else:
                    raise self.command_exception()
        elif len(command) == 3:
            action, obj, broker_id = command
            if action == 'view' and obj == 'broker':
                print(self.preview(self.player.name, broker_id))
            else:
                raise self.command_exception()
        elif len(command) == 4:
            action, broker_id, item_name, amount = command
            item_name = item_name.capitalize()
            if action == 'buy':
                total_cost, message = self.buy(
                    self.player.name, broker_id, item_name, amount, self.player.cash)
                if total_cost > 0:
                    self.player.inventory[item_name].amount += amount
                self.player.cash -= total_cost
                print(message)
            elif action == 'sell':
                total_cost = self.player.calculate_cost(item_name, amount)
                if self.player.inventory[item_name].amount - amount>= 0:
                    success = self.sell(self.player.name, broker_id, item_name, amount, total_cost)
                    if success:
                        self.player.cash += total_cost
                        self.player.inventory[item_name].amount -= amount
                        message = f'Successfully sell {item_name} to broker {broker_id}. You have ${self.player.cash:,.2f}!'
                    else:
                        message = f'Broker {broker_id} does not have enough cash!'
                    print(message)
                else :
                    print(f"Insufficient item quantity!")
            else:
                raise self.command_exception()

    def command_exception(self):
        return Exception('Invalid command, please try again!')

    def get_input(self):
        return [int(x) if x.isdigit() else x for x in input(f'{self.update()} Input command: ').split()]


if __name__ == '__main__':
    with PlayerMenu('a', 'http://localhost:7080') as proxy:
        proxy.prompt_command()
