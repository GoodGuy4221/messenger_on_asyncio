from datetime import datetime


class JimServerMessage:
    @staticmethod
    def probe(sender: str, status: str = 'Are you there?') -> dict:
        data = {
            'action': 'probe',
            'time': datetime.now().timestamp(),
            'type': 'status',
            'user': {
                'account_name': sender,
                'status': status,
            }
        }
        return data

    @staticmethod
    def response(code: int | None = None, error: str | None = None) -> dict:
        data = {
            'action': 'response',
            'code': code,
            'time': datetime.now().timestamp(),
            'error': error,
        }
        return data
