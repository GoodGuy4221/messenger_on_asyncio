from asyncio import Protocol
from binascii import hexlify
from hashlib import pbkdf2_hmac

from server.utils.mixins import ConvertMixin, DbInterfaceMixin
from server.utils.server_messages import JimServerMessage
from server.constants import ENCODING, SALT


class ChatServerProtocol(Protocol, ConvertMixin, DbInterfaceMixin):
    def __init__(self, db_path: str, connections, users):
        super().__init__(db_path)
        self.connections = connections
        self.users = users
        self.jim = JimServerMessage()

        self.user = None
        self.transport = None

    def connection_made(self, transport):
        self.connections[transport] = {
            'peername': transport.get_extra_info('peername'),
            'username': '',
            'transport': transport,
        }
        self.transport = transport

    def authenticate(self, username: str, password: str):
        if username and password:
            user = self.get_client_by_username(username)
            dk = pbkdf2_hmac('sha256',
                             password.encode(ENCODING),
                             SALT.encode(ENCODING),
                             100000)
            hashed_password = hexlify(dk)

            if user:
                if hashed_password == user.password:
                    return True
                else:
                    return False
            else:
                print('new user')
                self.add_client(username, hashed_password)
                self.add_client_history(username)
                return True
        else:
            return False

    def data_received(self, data):
        data = self.bytes_to_dict(data)
