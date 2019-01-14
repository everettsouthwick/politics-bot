import random
from discord.ext import commands

class Text():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clap(self, *, message : str):
        """Repeats the message back with claps in between each word."""
        await self.bot.say('👏 {0} 👏'.format(message.replace(' ', ' 👏 ')))

    @commands.command(name="randomcase")
    async def random_case(self, *, message: str):
        """Repeats the message back with the casing randomized."""
        random_case = ''
        for char in message:
            random_case += char.upper() if random.randint(0, 1) else char.lower()
        await self.bot.say(random_case)

    @commands.command()
    async def sponge(self, *, message: str):
        """Repeats the message back with the casing alternated."""
        sponge = ''
        nextUpper = True
        for char in message:
            sponge += char.upper() if nextUpper else char.lower()
            if char.isalpha():
                nextUpper = not nextUpper
        await self.bot.say(sponge)


def setup(bot):
    bot.add_cog(Text(bot))
