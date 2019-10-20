from telegram.ext import Updater
from telegram.ext import CommandHandler
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

        def start(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Test message 1...")

        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)

        updater.start_polling()


TelegramBot()