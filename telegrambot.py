import requests
import socket
import socks
import json


class TelegramBot:
    def __init__(self):
        try:
            with open('token.json', 'r') as f:
                token = json.load(f)
                self.TOKEN = f'{token["bot_id"]}:{token["bot_password"]}'
        except Exception:
            raise Exception('File "token.json" not found of invalid...')
        try:
            with open('socks5.json', 'r') as f:
                proxy = json.load(f)
                socks.set_default_proxy(socks.SOCKS5, proxy['address'],
                                        proxy['port'], True,
                                        proxy['user'],
                                        proxy['password'])
                socket.socket = socks.socksocket
        except Exception:
            raise Exception('File "socks5.json" not found on invalid...')

        self.URL = 'https://api.telegram.org/bot'
        self.API_URL = self.URL + self.TOKEN + '/'

    def get_updates(self):
        socket.socket.connect('api.telegram.org',80)
        url = self.URL + 'getUpdates'
        r = requests.get(url)
        return r.json()


def main():
    d = TelegramBot().get_updates()

    with open('updates.json', 'w') as file:
        json.dump(d, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()