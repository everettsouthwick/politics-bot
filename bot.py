import os, sys, json, traceback
from discord.ext import commands
from os import listdir
from os.path import isfile, join
import sqlite3
import modules.sql_init

sql = modules.sql_init.SQLInit()

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

# this specifies what extensions to load when the bot starts up (from this directory)
COGS_DIR = "cogs"
BOT_PREFIX = ("!", ".")

bot = commands.Bot(command_prefix=BOT_PREFIX, description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in listdir(COGS_DIR) if isfile(join(COGS_DIR, f))]:
        try:
            bot.load_extension(COGS_DIR + "." + extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

    with open("{}/config.json".format(os.path.dirname(os.path.realpath(sys.argv[0])))) as properties:
        data = json.load(properties)
        bot.run(data["discord"]["token"], bot=True, reconnect=True)



