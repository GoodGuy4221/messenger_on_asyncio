from asyncio import Protocol
from binascii import hexlify
from hashlib import pbkdf2_hmac

from server.utils.mixins import ConvertMixin, DbInterfaceMixin
from server.utils.server_messages import JimServerMessage
from server.constants import (ENCODING, SALT, ACTION, PRESENCE, USER, ACCOUNT_NAME, AUTHENTICATE,
                              PASSWORD, USERNAME, CODE_OK, CODE_WRONG_MESS, OUT_WRONG_MESS, TRANSPORT,
                              CODE_WRONG_CREDENTIAL, OUT_WRONG_CREDENTIAL, OUT_INSUFFICIENT_DATA)


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

        if data:
            try:
                if data[ACTION] == PRESENCE:
                    if data[USER][ACCOUNT_NAME]:
                        resp_mess = self.jim.response(code=CODE_OK)
                        self.transport.write(self.dict_to_bytes(resp_mess))
                    else:
                        resp_mess = self.jim.response(code=CODE_WRONG_MESS, error=OUT_WRONG_MESS)
                        self.transport.write(self.dict_to_bytes(resp_mess))

                elif data[ACTION] == AUTHENTICATE:
                    if self.authenticate(data[USER][ACCOUNT_NAME], data[USER][PASSWORD]):
                        if data[USER][ACCOUNT_NAME] not in self.users:
                            self.user = data[USER][ACCOUNT_NAME]

                            self.connections[self.transport][USERNAME] = self.user

                            self.users[data[USER][ACCOUNT_NAME]] = self.connections[self.transport]

                            self.set_user_online(data[USER][ACCOUNT_NAME])

                        resp_mess = self.jim.probe(self.user)
                        self.users[data[USER][ACCOUNT_NAME]][TRANSPORT].write(self.dict_to_bytes(resp_mess))
                    else:
                        resp_mess = self.jim.response(code=CODE_WRONG_CREDENTIAL, error=OUT_WRONG_CREDENTIAL)
                        self.transport.write(self.dict_to_bytes(resp_mess))
            except Exception as error:
                resp_mess = self.jim.response(code=CODE_WRONG_MESS, error=str(error))
                self.transport.write(self.dict_to_bytes(resp_mess))
        else:
            resp_mess = self.jim.response(code=CODE_WRONG_MESS, error=OUT_INSUFFICIENT_DATA)
            self.transport.write(self.dict_to_bytes(resp_mess))
