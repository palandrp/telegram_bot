# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import CommandHandler
from datetime import datetime
from business import ShiftSheet
import logging
import myprivat


class TelegramBot:

    def __init__(self):
        self.TOKEN = myprivat.token
        self.REQUEST_KWARGS={
            'proxy_url': myprivat.proxy_url,
            'urllib3_proxy_kwargs': {
                'username': myprivat.proxy_user,
                'password': myprivat.proxy_pass,
            }
        }

        updater = Updater(token=self.TOKEN, use_context=True,
                          request_kwargs=self.REQUEST_KWARGS)
        dispatcher = updater.dispatcher

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        business = ShiftSheet()

        def start(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Available commands:\n"
                                          "/who_is_duty_today_chel\n"
                                          "/who_is_duty_today_msk")

        def who_is_duty_today_ch(update, context):
            dt = datetime.now()
            month = dt.strftime('%B')
            day = dt.strftime('%d')
            text = business.show_day_shifts(month, day, 'CHEL')
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=text)

        def who_is_duty_today_ms(update, context):
            dt = datetime.now()
            month = dt.strftime('%B')
            day = dt.strftime('%d')
            text = business.show_day_shifts(month, day, 'MSK')
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=text)

        start_handler = CommandHandler('start', start)
        who_is_duty_today_ch_handler = CommandHandler('who_is_duty_today_chel', who_is_duty_today_ch)
        who_is_duty_today_ms_handler = CommandHandler('who_is_duty_today_msk', who_is_duty_today_ms)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(who_is_duty_today_ch_handler)
        dispatcher.add_handler(who_is_duty_today_ms_handler)

        updater.start_polling()


TelegramBot()