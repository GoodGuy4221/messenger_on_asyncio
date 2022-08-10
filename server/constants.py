from pathlib import Path

ENCODING: str = 'utf-8'
DEFAULT_CLIENT_IP_ADDR: str = '1.1.1.1'

HOME: str = str(Path.home())

PORT: int = 5151

DB_PROTOCOL: str = 'sqlite:///'
DB_NAME: str = '/client_contacts.db'
DB_PATH: str = f'{DB_PROTOCOL}{HOME}{DB_NAME}'

SALT: str = 'd5065fbb34b28d1c84a9d6fde2c388e834e061628466328ba95331dbe5b5be30'

ACTION: str = 'action'
PRESENCE: str = 'presence'
USER: str = 'user'
ACCOUNT_NAME: str = 'account_name'
AUTHENTICATE: str = 'authenticate'
PASSWORD: str = 'password'
USERNAME: str = 'username'
CODE_OK: int = 200
CODE_WRONG_MESS: int = 500
CODE_WRONG_CREDENTIAL: int = 402
OUT_WRONG_MESS: str = 'wrong presence message'
OUT_WRONG_CREDENTIAL: str = 'wrong login/password'
TRANSPORT: str = 'transport'
OUT_INSUFFICIENT_DATA = 'Вы отправили сообщение без имени или данных'
