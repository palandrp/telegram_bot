import requests
import json


class TelegramBot:
    def __init__(self):
        with open('token.json', 'r') as f:
            token = json.load(f)
            self.TOKEN = f'{token["bot_id"]}:{token["bot_password"]}'
        with open('socks5.json', 'r') as f:
            self.SOCKS5 = json.load(f)
        self.URL = 'https://api.telegram.org/bot' + self.TOKEN + '/'

    def get_updates(self):
        url = self.URL + 'getUpdates'
        r = requests.get(url)
        return r.json()


def main():
    d = TelegramBot().get_updates()

    with open('updates.json', 'w') as file:
        json.dump(d, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()