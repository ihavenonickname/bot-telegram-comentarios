import discord
import os
from discord.ext import commands
from xvideos import choose_random_porn_comment, choose_random_video

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='!')

def format_comment(author, content, title):
    mask = '**O {0}  comentou o seguinte:**\n`{1}`\n\n**vi isso no video:**\n`{2}`'
    return mask.format(author, content, title)

@bot.event
async def on_ready():
    print("Bot online!")
    await bot.change_presence(game=discord.Game(name='digite !meajuda para mais informações'))

@bot.command(description='Apresenta a lista de ajuda ao usuário.', pass_context=True)
async def meajuda(ctx):
    await bot.send_message(ctx.message.author, '*Olá. Aqui estão os comandos:*\n - `!mensagem` - Procura um comentario aleatório no Xvideos em Portugês\n - `!telemensagem` - Procura um comentario aleatório no Xvideos em Portugês e o envia com TTS (Text to Speech)\n - `!busca *termo*` - Procura um video pelo termo passado, se não passado nenhum, é retornado um video aleatório\n - `!meajuda` - Mostra esta mensagem.\n\n Encontrou algum problema ou tem alguma sugestão para o bot? Sinta-se livre para nos enviar uma mensagem por este link https://github.com/marquesgabriel/bot-discord-comentarios-xvideos/issues\n')

    await bot.delete_message(ctx.message)


@bot.command(description='Procura um comentário no xvideos.')
async def mensagem():
    await bot.say('**Buscando...\n**')
    try:
        comment = choose_random_porn_comment()
        await bot.say(format_comment(*comment))
    except Exception:
        bot.say('Houve uma falha na busca. Tente novamente.')

    await bot.delete_message(ctx.message)

@bot.command(description='Procura um comentário no xvideos. COM TTS.')
async def telemensagem():
    await bot.say('Buscando...')
    try:
        author, comment, title = choose_random_porn_comment()
        author = '**O '+author+'  comentou o seguinte:**\n'
        title = '**vi isso no video:**\n`'+title+'`'
        await bot.say(author)
        await bot.say(comment, tts=True)
        await bot.say(title)
    except Exception:
        bot.say('Houve uma falha na busca. Tente novamente.')

    await bot.delete_message(ctx.message)


@bot.command(description='Procura um video baseado na tag passada.', pass_context=True)
async def busca(ctx, tag=None):
    try:
        link = choose_random_video(tag)
        await bot.send_message(ctx.message.author, 'Segura esse link aí meu parceiro: ' + link)
    except Exception:
        bot.say('Houve uma falha na busca. Tente novamente.')

    await bot.delete_message(ctx.message)


bot.run(BOT_TOKEN)
