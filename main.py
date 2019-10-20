from datetime import datetime
import socket
import socks
import json
from business import ShiftSheet
from telegrambot import TelegramBot

def main():
    #telebot = TelegramBot()
    business = ShiftSheet()

    dt = datetime.now()
    month = dt.strftime('%B')
    day = dt.strftime('%d')
    business.show_day_shifts(month, day, 'CHEL')

    #message = telebot.get_message()
    '''if message['text'] == '/today_in_chel':
        dt = datetime.now()
        month = dt.strftime('%B')
        day = dt.strftime('%d')
        answer = business.show_day_shifts(month,day,'CHEL')
        print(answer)
        #telebot.send_message(279959271, msg)
        #print(dt.strftime("%A, %d. %B %Y %I:%M%p"))'''

'''
    dt = datetime.now()
    month = dt.strftime('%B')
    day = dt.strftime('%d')
    location = 'CHEL'
    ss = ShiftSheet()
    shift_pairs = ss.show_day_shifts(month, day, location)
    
    print(f'Время смены и дежурный: {shift_pairs}')
'''
'''    
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
'''

if __name__ == '__main__':
    main()