from datetime import datetime
import socket
import socks
import json
from business import ShiftSheet
from telegrambot import TelegramBot

def main():
    telebot = TelegramBot()
    googbot = ShiftSheet()
    message = telebot.get_message()
    if message['text'] == '/today_in_chel':
        dt = datetime.now()
        month = dt.strftime('%B')
        day = dt.strftime('%d')
        answer = googbot.show_day_shifts(month,day,'CHEL')
        print(answer)
        #telebot.send_message(279959271, msg)
        #print(dt.strftime("%A, %d. %B %Y %I:%M%p"))

    '''
    dt = datetime.now()
    month = dt.strftime('%B')
    day = dt.strftime('%d')
    location = 'CHEL'
    ss = ShiftSheet()
    shift_pairs = ss.show_day_shifts(month, day, location)
    
    print(f'Время смены и дежурный: {shift_pairs}')
    '''

if __name__ == '__main__':
    main()