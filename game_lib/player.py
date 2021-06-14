from xmlrpc.client import ServerProxy
from broker import Broker


class PlayerMenu(ServerProxy):
    def __init__(self, name, *args, **kwargs):
        super(PlayerMenu, self).__init__(*args, **kwargs)
        self.player = Broker(name)

    def prompt_command(self):
        print(self.update())
        command = input('Input command: ').split()
        while command[0] != 'quit':
            try:
                if len(command) > 1:
                    self.execute_command(command)
                else:
                    command = command[0]
                    if command == 'quit':
                        break
            except Exception as e:
                print('Invalid command! Please try again.')
                print(e)
            finally:
                print(self.update())
                command = input('Input command: ').split()

    def execute_command(self, command):
        if len(command) == 2:
            command, broker_id = command
            broker_id = int(broker_id)
            print(self.preview(broker_id))
        if len(command) == 4:
            command, broker_id, item_name, amount = command
            print(command, broker_id, item_name, amount)
            broker_id = int(broker_id)
            amount = int(amount)
            if command == 'buy':
                total_cost, message = self.buy(broker_id, item_name, amount, self.player.cash)
                self.player.cash -= total_cost
                print(message)
            else:
                total_cost = self.player.calculate_cost(item_name, amount)
                success, message = self.sell(broker_id, item_name, amount, total_cost)
                if success:
                    self.player.cash += total_cost
                print(message)


if __name__ == '__main__':

    with PlayerMenu('a', 'http://localhost:7080') as proxy:
        proxy.prompt_command()
