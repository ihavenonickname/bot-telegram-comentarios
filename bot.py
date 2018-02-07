import discord
import os
from discord.ext import commands
from xvideos import choose_random_porn_comment

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='!')

def format_comment(author, content, title):
    mask = '**O {0}  comentou o seguinte:**\n`{1}`\n'
    return mask.format(author, content, title)


@bot.event
async def on_ready():
    print("Bot online!")
    await bot.change_presence(game=discord.Game(name='digite !recadinho ou !telemensagem'))


@bot.command(description='Procura um comentário no xvideos.')
async def recadinho():
    await bot.say('**Psicografando...\n**')

    try:
        comment = choose_random_porn_comment()
        await bot.say(format_comment(*comment))
    except Exception:
        bot.say('Houve uma falha no broadcast divino.')

@bot.command(description='Procura um comentário no xvideos.')
async def telemensagem():
    await bot.say('**Psicografando audio...\n**')

    try:
        comment = choose_random_porn_comment()
        await bot.say(format_comment(*comment), tts=True)
    except Exception:
        bot.say('Houve uma falha no broadcast divino.')


bot.run(BOT_TOKEN)
