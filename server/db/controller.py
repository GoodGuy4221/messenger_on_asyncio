from sqlalchemy.exc import IntegrityError

from server.db.db_connector import DataAccessLayer
from server.db.models import ClientModel, HistoryModel


class ClientMessages:
    def __init__(self, conn_string, base, echo):
        """create connect to DB"""
        self.dal = DataAccessLayer(conn_string, base, echo=echo)
        self.dal.connect()
        self.dal.session = self.dal.Session()

    def add_client(self, username, password, info=None):
        """add client"""
        if self.get_client_by_username(username):
            return f'Пользователь {username} уже существует'
        else:
            new_user = ClientModel(username=username, password=password, info=info)
            self.dal.session.add(new_user)
            self.dal.session.commit()
            print(f'Добавлен пользователь: {new_user}')

    def get_client_by_username(self, username: str):
        """Getting client by name"""
        client = self.dal.session.query(ClientModel).filter(
            ClientModel.username == username
        ).first()
        return client

    def add_client_history(self, client_username, ip_addr='1.1.1.1'):
        """Added history client"""
        client = self.get_client_by_username(client_username)
        if client:
            new_history = HistoryModel(ip_addr=ip_addr, client_id=client.id)
            try:
                self.dal.session.add(new_history)
                self.dal.session.commit()
                print(f'Добавлена запись в историю :{new_history}')
            except IntegrityError as error:
                print(f'Ошибка интеграции с базой данных :{error}')
                self.dal.session.rollback()

        return f'Пользователь :{client_username} не существует'

    def set_user_online(self, client_username):
        client = self.get_client_by_username(client_username)
        if client:
            client.online_status = True
            self.dal.session.commit()
        return f'Пользователь :{client_username} не существует.'
