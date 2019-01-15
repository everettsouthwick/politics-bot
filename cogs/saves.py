import datetime, sqlite3, modules.sql_init
from discord.ext import commands

sql = modules.sql_init.SQLInit()

class Saves():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get", aliases="g", pass_context=True)
    async def get_save(self, ctx, save_name):
        """Searches for a saved item and returns it if a match is found."""
        try:
            sql.cur.execute("select content, uses from saves where name = ?", [save_name])
            results = sql.cur.fetchone()
            if results is not None:
                try:
                    uses = results[1] + 1
                    sql.cur.execute("update saves set uses = ?, last_used = ? where name = ?", [uses, str(datetime.datetime.now()), save_name])
                    sql.conn.commit()
                    await self.bot.say('{0}, {1}'.format(ctx.message.author.mention, results[0]))
                except:
                    await self.bot.say('{0}, some error has occured for "{1}".'.format(ctx.message.author.mention, save_name))
            else:
                await self.bot.say('{0}, there is no saved item for "{1}".'.format(ctx.message.author.mention, save_name))
        except:
            await self.bot.say('{0}, there is no saved item for "{1}".'.format(ctx.message.author.mention, save_name))

    @commands.command(name="save", aliases="s", pass_context=True)
    async def save_item(self, ctx, save_name, content):
        """Saves an item."""
        try:
            sql.cur.execute("insert into saves (name, content, uses, saved_by, time_added, approved_by) values (?, ?, ?, ?, ?, ?)", [save_name, content, 0, str(ctx.message.author), str(datetime.datetime.now()), str(ctx.message.author)])
            sql.conn.commit()
            await self.bot.say('{0}, {1} has been saved.'.format(ctx.message.author.mention, save_name))
        except:
            await self.bot.say('{0}, some error has occured. {1} has not been saved.'.format(ctx.message.author.mention, save_name))

def setup(bot):
    bot.add_cog(Saves(bot))
