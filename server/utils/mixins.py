from json import dumps, loads

from server.db.controller import ClientMessages
from server.db.models import BaseModel, ClientModel
from server.constants import ENCODING, DEFAULT_CLIENT_IP_ADDR


class DbInterfaceMixin:
    def __init__(self, db_path: str):
        self.cm = ClientMessages(db_path, BaseModel, echo=False)

    def add_client(self, username: str, info=None) -> str | bool:
        return self.cm.add_client(username, info)

    def get_client_by_username(self, username: str) -> ClientModel | None:
        return self.cm.get_client_by_username(username=username)

    def add_client_history(self, client_username: str, ip_addr: str = DEFAULT_CLIENT_IP_ADDR) -> None | str:
        return self.cm.add_client_history(client_username, ip_addr)

    def set_user_online(self, client_username: str) -> None | str:
        return self.cm.set_user_online(client_username)


class ConvertMixin:
    @staticmethod
    def dict_to_bytes(message: dict) -> bytes:
        if not isinstance(message, dict):
            raise TypeError

        json_message = dumps(message)
        bytes_json_message = json_message.encode(ENCODING)
        return bytes_json_message

    @staticmethod
    def bytes_to_dict(message: bytes) -> dict:
        if not isinstance(message, bytes):
            raise TypeError

        json_message = message.decode(ENCODING)
        dict_message = loads(json_message)

        if not isinstance(dict_message, dict):
            raise TypeError

        return dict_message
