from discord.ext import commands
from bs4 import BeautifulSoup
import requests

def get_polls(uri, poll_num):
    response = requests.get(uri).text
    soup = BeautifulSoup(response, 'html.parser')
    container = soup.find("div", {"id": 'polling-data-full'})
    table = container.find("table", {"class": 'data'})
    polls = []
    for row in table:
        cols = row.find_all(['th', 'td'])
        splitpoll = cols[0].find_all(['a'])
        if len(splitpoll) > 0: cols[0] = cols[0].find_all(['a'])[0]
        cols = [ele.text.strip() for ele in cols]
        polls.append(cols)
        if len(polls) > poll_num: break
    
    col_widths = []
    col_width1 = 0
    col_width2 = 0
    col_width3 = 0
    col_width4 = 0
    col_width5 = 0
    col_width6 = 0
    for row in polls:
        if len(row[0]) > col_width1:
            col_width1 = len(row[0])
        if len(row[1]) > col_width2:
            col_width2 = len(row[1])
        if len(row[2]) > col_width3:
            col_width3 = len(row[2])
        if len(row[3]) > col_width4:
            col_width4 = len(row[3])
        if len(row[4]) > col_width5:
            col_width5 = len(row[4])
        if len(row[5]) > col_width6:
            col_width6 = len(row[5])

    col_widths.append(col_width1 + 2)
    col_widths.append(col_width2 + 2)
    col_widths.append(col_width3 + 2)
    col_widths.append(col_width4 + 2)
    col_widths.append(col_width5 + 2)
    col_widths.append(col_width6 + 2)
    
    lines = '```'
    for row in polls:
        i = 0
        for word in row:
            lines += ''.join(word.ljust(col_widths[i]))
            i += 1
        lines += '\n'
    lines += '```'
    
    return lines

class Polls():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="trumpapproval")
    async def trump_approval(self, poll_num=10):
        """Returns the specified number (default=10) of polls on Trump's approval rating."""
        await self.bot.say(get_polls('https://www.realclearpolitics.com/epolls/other/president_trump_job_approval-6179.html', poll_num))

    @commands.command(name="trumpfavorable")
    async def trump_favorability(self, poll_num=10):
        """Returns the specified number (default=10) of polls on Trump's favorability rating."""
        await self.bot.say(get_polls('https://www.realclearpolitics.com/epolls/other/trump_favorableunfavorable-5493.html', poll_num))

    @commands.command(name="countrydirection")
    async def country_direction(self, poll_num=10):
        """Returns the specified number (default=10) of polls on the direction of the country."""
        await self.bot.say(get_polls('https://www.realclearpolitics.com/epolls/other/direction_of_country-902.html', poll_num))

    @commands.command(name="congressapproval")
    async def congress_approval(self, poll_num=10):
        """Returns the specified number (default=10) of polls on Congress' approval rating."""
        await self.bot.say(get_polls('https://www.realclearpolitics.com/epolls/other/congressional_job_approval-903.html', poll_num))

    @commands.command(name="rcppoll")
    async def rcp_poll(self, uri, poll_num=10):
        """Returns the specified number (default=10) of polls from a custom RCP aggregate poll."""
        await self.bot.say(get_polls(uri, poll_num))


def setup(bot):
    bot.add_cog(Polls(bot))