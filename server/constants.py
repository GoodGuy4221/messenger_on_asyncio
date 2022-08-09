from pathlib import Path

ENCODING = 'utf-8'
DEFAULT_CLIENT_IP_ADDR = '1.1.1.1'

HOME = str(Path.home())

PORT = 5151

DB_PROTOCOL = 'sqlite:///'
DB_NAME = '/client_contacts.db'
DB_PATH = f'{DB_PROTOCOL}{HOME}{DB_NAME}'

SALT = 'd5065fbb34b28d1c84a9d6fde2c388e834e061628466328ba95331dbe5b5be30'
