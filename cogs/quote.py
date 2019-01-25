import discord, sqlite3
from discord.ext import commands
import modules.member_helper as helper
import modules.sql_init as sqlinit

sql = sqlinit.SQLInit()

class Quote():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, *, author : str = "Mitt Romney"):
        try:
            sql.cur.execute("select author, quote from quotes where author = ? order by random() limit 1", [author])
            results = sql.cur.fetchone()
            if results is not None:
                try:
                    author = results[0]
                    quote = results[1]
                    embed = discord.Embed(description=quote, color=5025616)
                    embed.set_author(name=author)
                    
                    await self.bot.say(embed=embed)
                except:
                    embed = discord.Embed(title="Error", description="An unexpected error has occured. 😔", color=12000284)
                    await self.bot.say(embed=embed)
            else:
                embed = discord.Embed(title="Error", description="There is no quote for {0}. 🔍".format(author), color=12000284)
                await self.bot.say(embed=embed)
        except:
            embed = discord.Embed(title="Error", description="An unexpected error has occured. 😔", color=12000284)
            await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Quote(bot))
