#!/usr/bin/python3

import os
import re
import logging
from telegram.ext import Updater, CommandHandler, run_async
from xvideos import choose_random_porn_comment, XvideosException

@run_async
def comment(bot, update):
    def send(message):
        bot.send_message(chat_id=update.message.chat_id, text=message)

    match = re.match(r'^\/comment\s(([a-z]+\s)*[a-z]+)$', update.message.text, re.IGNORECASE)

    search_term = None

    if match:
        search_term = match.group(1).replace(' ', '+')

    send('Searching... Hang on!')

    try:
        comment = choose_random_porn_comment(search_term)
        message = f'{comment.author} from {comment.country} commented {comment.datediff} with a score of {comment.score}:\n{comment.content}'
        send(message)
    except XvideosException as ex:
        logging.error(f'{ex}')
        send(f'There was an error:\n\n{ex}')
    except Exception as ex:
        logging.error(f'{ex}')
        send('There was an unknown error! Contact @GabrielBlank on Telegram')

def start(bot, update):
    update.message.reply_text(text='Hello!\n\nSend me /comment and I will show you a random comment from my favorite website! You can also specify a nice keyword as in /comment creampie\n\n:D')

def main():
    logging.basicConfig(
        filename='/var/log/bot-telegram-xvideos.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%m-%d-%Y %H:%M:%S')

    try:
        updater = Updater(os.environ['BOT_TELEGRAM_XVIDEOS_TOKEN'])
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(CommandHandler('comment', comment))

        updater.start_polling()

        print('Running!')

        updater.idle()

        print()
    except Exception as ex:
        logging.critical(f'{ex}')

if __name__ == '__main__':
    main()
