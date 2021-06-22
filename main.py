from twisted.internet import reactor
from twisted.web.server import Site
import argparse
import game_lib as gl

description = 'Tycoon Game - Final Project for Distributed and Parallel Systems using RPC'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=description
    )

    parser.add_argument(
        '--uri', type=str, help='URI for connecting to server.', default='http://localhost:7080')
    parser.add_argument(
        '--port', type=int, help='Port for servers listener.', default=7080
    )
    parser.add_argument(
        '--role', type=str, help='The program role, either "server" or "player".', default='player')
    parser.add_argument('--name', type=str,
                        help='The name of player.', default='PLAYER_NAME')
    parser.add_argument('--n_broker', type=int,
                        help='Number of brokers on the server.', default=4)

    args = parser.parse_args()
    if args.role == 'player':
        gl.PlayerMenu(args.name, args.uri).prompt_command()
    else:
        game_handler = gl.GameHandler(args.n_broker)
        reactor.listenTCP(args.port, Site(game_handler))
        reactor.run()
