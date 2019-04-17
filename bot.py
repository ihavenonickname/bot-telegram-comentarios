#!/usr/bin/python3

import os
import re
import logging
from telegram.ext import Updater, CommandHandler, run_async
from xvideos import choose_random_porn_comment, XvideosException

def log_username(update):
    try:
        username = update.effective_user.username
        if update['message']['chat']['type'] == 'group':
            group = update['message']['chat']['title']
            logging.info(f'@{username} {group}')
        else:
            logging.info(f'@{username}')
    except KeyError:
        logging.warning('Could not read username')

@run_async
def comment(bot, update):
    log_username(update)

    def send(message):
        bot.send_message(chat_id=update.message.chat_id, text=message)

    match = re.match(r'^\/comment\s(([a-z]+\s)*[a-z]+)$', update.message.text, re.IGNORECASE)

    search_term = None

    if match:
        search_term = match.group(1).replace(' ', '+')

    send('Searching... Hang on!')

    try:
        author, content, country, datediff, title = choose_random_porn_comment(search_term)

        if country:
            message = f'{author} from {country}'
        else:
            message = f'{author}'

        message += f'commented {datediff}:\n{content}\n\nI found this in the video:\n{title}'

        send(message)
    except XvideosException as ex:
        logging.error(f'{ex}')
        send(f'There was an error!\n\n{ex}')
    except Exception as ex:
        logging.error(f'{ex}')
        send('There was an error! Contact @GabrielBlank on Telegram')

def start(bot, update):
    log_username(update)
    update.message.reply_text(text='Hello!\n\nSend me /comment and I will show you a random comment from my favorite website! :D')

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
