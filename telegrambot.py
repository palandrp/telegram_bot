# -*- coding: utf-8 -*-
from config import myprivat
from telegram import ChatAction
from telegram.ext import Updater, \
                         CommandHandler, \
                         MessageHandler, \
                         Filters
from datetime import datetime
from business import ShiftSheet
from functools import wraps
import traceback
import logging


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

        self.DEV_IDs = [myprivat.devid]

        def error(update, context):
            devs = self.DEV_IDs
            if update.effective_message:
                text = "Оооопс! Какая-то ошибочка произошла! " \
                       "Без паники, скоро мы всё починим! " \
                       "Разработчик(и) уже уведомлен(ы)!"
                update.effective_message.reply_text(text)
            trace = "".join(traceback.format_tb(sys.exc_info()[2]))
            payload = ""
            if update.effective_user:
                payload += f' with the user ' \
                           f'{mention_html(update.effective_user.id,update.effective_user.first_name)}'
            if update.effective_chat:
                payload += f' within the chat <i>{update.effective_chat.title}</i>'
                if update.effective_chat.username:
                    payload += f' (@{update.effective_chat.username})'
            if update.poll:
                payload += f' with the poll id {update.poll.id}.'
            text = f"Hey.\n The error <code>{context.error}</code> happened{payload}. " \
                   f"The full traceback:\n\n<code>{trace}" \
                   f"</code>"
            for dev_id in devs:
                context.bot.send_message(dev_id, text, parse_mode=ParseMode.HTML)
            raise

        logging.basicConfig(
            filename='/var/log/lt-bot/lt-bot.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        def send_action(action):
            def decorator(func):
                @wraps(func)
                def command_func(update, context, *args, **kwargs):
                    context.bot.send_chat_action(
                        chat_id=update.effective_message.chat_id,
                        action=action)
                    return func(update, context, *args, **kwargs)
                return command_func
            return decorator
        send_typing_action = send_action(ChatAction.TYPING)

        updater = Updater(token=self.TOKEN, use_context=True,
                          request_kwargs=self.REQUEST_KWARGS)
        dispatcher = updater.dispatcher

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        business = ShiftSheet()

        @send_typing_action
        def start(update, context):
            try:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Available commands:\n"
                                              "/who_is_duty_today_chel\n"
                                              "/who_is_duty_today_msk")
            except:
                error(update, context)

        @send_typing_action
        def echo(update, context):
            try:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=update.message.text)
            except:
                error(update, context)

        @send_typing_action
        def unknown(update, context):
            try:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Sorry, I didn't understand that command.")
            except:
                error(update, context)

        @send_typing_action
        def who_is_duty_today_ch(update, context):
            try:
                dt = datetime.now()
                month = dt.strftime('%B')
                day = dt.strftime('%d')
                text = business.show_day_shifts(month, day, 'CHEL')
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=text)
            except:
                error(update, context)

        @send_typing_action
        def who_is_duty_today_ms(update, context):
            try:
                dt = datetime.now()
                month = dt.strftime('%B')
                day = dt.strftime('%d')
                text = business.show_day_shifts(month, day, 'MSK')
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=text)
            except:
                error(update, context)


        start_handler = CommandHandler('start', start)
        echo_handler = MessageHandler(Filters.text, echo)
        who_is_duty_today_ch_handler = CommandHandler('who_is_duty_today_chel', who_is_duty_today_ch)
        who_is_duty_today_ms_handler = CommandHandler('who_is_duty_today_msk', who_is_duty_today_ms)
        unknown_handler = MessageHandler(Filters.command, unknown)


        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(echo_handler)
        dispatcher.add_handler(who_is_duty_today_ch_handler)
        dispatcher.add_handler(who_is_duty_today_ms_handler)
        dispatcher.add_handler(unknown_handler)


        updater.start_polling()


TelegramBot()