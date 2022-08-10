from argparse import ArgumentParser
from asyncio import get_event_loop

from server.constants import DB_PATH, PORT
from server.utils.server_proto import ChatServerProtocol


class ConsoleServerApp:
    """Console server"""

    def __init__(self, parsed_args: dict, db_path: str):
        self.args = parsed_args
        self.db_path = db_path
        self.inst = None

    def main(self):
        connections = {}
        users = {}
        loop = get_event_loop()

        self.inst = ChatServerProtocol(self.db_path, connections, users)

        core = loop.create_server(lambda: self.inst, self.args['addr'], self.args['port'])
        server = loop.run_until_complete(core)

        print(f'server on {" ".join(server.sockets[0].getsockname())}')

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print('До свидания')

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()


def parse_and_run():
    def parse_args():
        parser = ArgumentParser(description='Server settings')
        parser.add_argument('--addr', default='127.0.0.1', type=str)
        parser.add_argument('--port', default=PORT, type=int)
        parser.add_argument('--nogui', action='store_true')
        return vars(parser.parse_args())

    args = parse_args()

    if args['nogui']:
        a = ConsoleServerApp(args, DB_PATH)
        a.main()


if __name__ == '__main__':
    parse_and_run()
