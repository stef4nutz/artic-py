import discord
from discord.ext import commands
import os
import sys, traceback

def get_prefix(bot, message):

    prefixes = ['artic ', '$']

    if message.author.id == yourid:
        return ['artic ', " "]

    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['ext.informatii', "ext.moderare"]

bot = commands.Bot(command_prefix=get_prefix, description='This is a bot summoned by some black wizard. Ya will like it.')

bot.remove_command("help")

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    game = discord.Game("cu frigideru")
    await bot.change_presence(status=discord.Status.dnd, activity=game)
    print(f'Successfully logged in and booted...!')

bot.run('yourtoken', bot=True, reconnect=True)
