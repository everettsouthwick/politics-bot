import discord, datetime
from datetime import timedelta
from discord.ext import commands
from babel.dates import format_timedelta
import modules.member_helper as helper

class Members():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def role(self, ctx, role_name, color):
        """Gives the specified role to the user."""

    @commands.command(pass_context=True)
    async def joined(self, ctx, member : discord.Member = None):
        """Says when a member joined."""
        if member is None:
            member = ctx.message.author
        elif member.name is None:
            member = find(lambda m: m.name == member, channel.server.members)
                
        avatar_url = helper.get_avatar_url(member)
        nick = helper.get_nick(member)
        join_date = self.pretty_date(member.joined_at)
        relative_join = self.pretty_relative_time(member.joined_at)

        description = "{0} first joined the server on **{1} UTC ({2} ago)**.".format(nick, join_date, relative_join)

        embed = discord.Embed(description=description, color=5025616)
        embed.set_author(name=member.name, icon_url=avatar_url)
        await self.bot.say(embed=embed)

    @joined.error
    async def joined_handler(self, ctx, error):
        embed = discord.Embed(title="Error", description="There is no matching user. 🔍", color=12000284)
        await self.bot.say(embed=embed)

    def pretty_date(self, date : datetime):
        return date.strftime('%Y-%m-%d at %H:%M:%S')

    def pretty_relative_time(self, date : datetime):
        now = datetime.datetime.now()
        delta = now - date
        return format_timedelta(delta, locale='en_US')

def setup(bot):
    bot.add_cog(Members(bot))
