#!/usr/bin/python3

import re
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter, run_async
from xvideos import choose_random_porn_comment
from datetime import datetime

TOKEN = os.environ['BOT_TELEGRAM_XVIDEOS_TOKEN']

def comment_to_str(comment):
    mask = 'O {0} comentou o seguinte:\n{1}\n\nVi isso no video:\n{2}'

    return mask.format(
        comment['author'],
        comment['content'],
        comment['title']
    )

@run_async
def comentario(bot, update):
    def send(message):
        bot.send_message(chat_id=update.message.chat_id, text=message)

    send('Vou procurar um comentario aqui, perae...')
    comment = choose_random_porn_comment()
    send(comment_to_str(comment))


def start(bot, update):
    update.message.reply_text(text='Ola!\n\nEscreva /comentario para eu te mostrar algum comentario do meu site favorito!')

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('comentario', comentario))
    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()

    print('Running!')

    updater.idle()

    print()

if __name__ == '__main__':
    main()
