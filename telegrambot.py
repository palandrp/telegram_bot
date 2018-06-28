import requests
import myprivat


class TelegramBot:
    def __init__(self):
        self.TOKEN = myprivat.token
        self.URL = 'https://api.telegram.org/'
        self.API_URL = self.URL + 'bot' + self.TOKEN + '/'

    def get_updates(self):
        #socket.socket.connect('149.154.167.199',80)
        url = self.API_URL + 'getUpdates'
        r = requests.get(url)
        return r.json()

    def get_message(self):
        data = self.get_updates()
        chat_id = data['result'][-1]['message']['chat']['id']
        message_text = data['result'][-1]['message']['text']
        message = {'chat_id': chat_id, 'text': message_text}
        return message

    def send_message(self, chat_id, text='Wait a second, please...'):
        url = self.API_URL + 'sendMessage?'
        requests.get(url+'chat_id='+str(chat_id)+'&'+'text='+text)

