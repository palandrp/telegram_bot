import requests
import myprivat

'''Возможное решение: настроить tor-прокси
https://gist.github.com/jefftriplett/9748036
api.telegram.org 149.154.167.199
Еще одно решение, научить PySocks ходить через
ipv6: https://toster.ru/q/441590.
Еще одно решение, использовать сокет, но тогда
не работает google через этот сокет...
Или, возможно, снова вернуться к варианту с
библиотекой pyTelegramBotApi и ее apihelper.proxy:
https://toster.ru/q/524178?from=questions_similar.
Еще есть MTProto, надо изучить.
(Кстати многопоточность:
https://python-scripts.com/threading)'''

class TelegramBot:
    def __init__(self):
        self.TOKEN = myprivat.token
        self.URL = 'https://149.154.167.199/'
        self.API_URL = self.URL + 'bot' + self.TOKEN + '/'
        self.proxies = {
            'http': myprivat.usa_socks5,
            'https': myprivat.usa_socks5
        }

    def get_updates(self):
        url = self.API_URL + 'getUpdates'
        r = requests.get(url, proxies=self.proxies)
        return r.json()

    def get_message(self):
        data = self.get_updates()
        chat_id = data['result'][-1]['message']['chat']['id']
        message_text = data['result'][-1]['message']['text']
        message = {'chat_id': chat_id, 'text': message_text}
        return message

    def send_message(self, chat_id, text='Wait a second, please...'):
        url = self.API_URL+'sendMessage?'+'chat_id='+str(chat_id)+'&text='+text
        requests.get(url, proxies=self.proxies)


TelegramBot().send_message(279959271)

