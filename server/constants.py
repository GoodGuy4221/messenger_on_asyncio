from pathlib import Path

ENCODING = 'utf-8'
DEFAULT_CLIENT_IP_ADDR = '1.1.1.1'

HOME = str(Path.home())

PORT = 5151

DB_PROTOCOL = 'sqlite:///'
DB_NAME = '/client_contacts.db'
DB_PATH = f'{DB_PROTOCOL}{HOME}{DB_NAME}'
