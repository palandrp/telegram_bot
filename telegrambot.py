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

        self.URL = 'https://api.telegram.org/'
        self.API_URL = self.URL + 'bot' + self.TOKEN + '/'

    def get_updates(self):
        #socket.socket.connect('149.154.167.199',80)
        url = self.API_URL + 'getUpdates'
        r = requests.get(url)
        return r.json()

    def send_message(self, chat_id, text):
        url = self.API_URL + 'sendMessage?'
        requests.get(url+'chat_id='+str(chat_id)+'&'+'text='+text)
        return url


def main():
    bot = TelegramBot()
    bot.send_message(279959271,'hell eeee!')


if __name__ == '__main__':
    main()