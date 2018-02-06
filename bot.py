import discord
from discord.ext import commands
from xvideos import choose_random_porn_comment


bot = commands.Bot(command_prefix='!')

def format_comment(author, content, title):
    mask = '**O {0}  comentou o seguinte:**\n`{1}`\n\n**vi isso no video:**\n`{2}`'
    return mask.format(author, content, title)


@bot.event
async def on_ready():
    print("Bot online!")
    await bot.change_presence(game=discord.Game(name='!comentario'))


@bot.command(description='Procura um comentário no xvideos.')
async def comentario():
    await bot.say('**Vou procurar um comentario aqui, perae...\n**')

    try:
        comment = choose_random_porn_comment()
        await bot.say(format_comment(*comment))
    except Exception:
        bot.say('Houve um erro! fala com o dev dessa caralha.')


bot.run('TOKEN')
