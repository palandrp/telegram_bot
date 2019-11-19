# -*- coding: utf-8 -*-
from config import myprivat
from telegram import ParseMode, \
                     ChatAction, \
                     InlineQueryResultArticle, \
                     InputTextMessageContent
from telegram.ext import Updater, \
                         CommandHandler, \
                         MessageHandler, \
                         Filters, \
                         InlineQueryHandler
from telegram.utils.helpers import mention_html
from datetime import datetime
from business import ShiftSheet
from functools import wraps
from uuid import uuid4
import traceback
import logging
import sys


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

        self.DEV_IDs = myprivat.devid

        logging.basicConfig(
            filename='/var/log/lanit_shifts_bot/lanit-shifts.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

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

        @send_typing_action
        def start(update, context):
            try:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Наберите '@имя_бота' и пробел,\n"
                                              "загрузятся доступные варианты.",
                                         parse_mode=ParseMode.HTML)
            except:
                error(update, context)

        @send_typing_action
        def unknown(update, context):
            try:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Sorry, I didn't understand that command.",
                                         parse_mode=ParseMode.HTML)
            except:
                error(update, context)

        business = ShiftSheet()
        def inlinequery(update, context):
            dt = datetime.now()
            month = dt.strftime('%B')
            day = dt.strftime('%d')
            results = [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Кто сегодня на смене? (время Мск)",
                    input_message_content=InputTextMessageContent(
                        business.show_day_shifts(month, day, 'MSK')
                    )),
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Кто сегодня на смене? (время Члб)",
                    input_message_content=InputTextMessageContent(
                        business.show_day_shifts(month, day, 'CHEL')
                    ))
            ]
            update.inline_query.answer(results)

        updater = Updater(token=self.TOKEN, use_context=True,
                          request_kwargs=self.REQUEST_KWARGS)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', start)
        unknown_handler = MessageHandler(Filters.command, unknown)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(unknown_handler)
        dispatcher.add_handler(InlineQueryHandler(inlinequery))

        updater.start_polling()


TelegramBot()