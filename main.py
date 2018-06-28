from datetime import datetime
from business import ShiftSheet
from telegrambot import TelegramBot

def main():
    telebot = TelegramBot()
    googbot = ShiftSheet()
    message = telebot.get_message()
    if message['text'] == '/today_in_chel':
        dt = datetime.now()
        msg = googbot.show_day_shifts(dt.strftime('%B'),dt.strftime('%d'),'CHEL')
        telebot.send_message(279959271, msg)
        #print(dt.strftime("%A, %d. %B %Y %I:%M%p"))
    '''
    month = 'June'
    day = '26'
    location = 'CHEL'
    ss = ShiftSheet()
    shift_pairs = ss.show_day_shifts(month, day, location)
    
    print(f'Время смены и дежурный: {shift_pairs}')
    '''

if __name__ == '__main__':
    main()