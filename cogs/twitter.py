from discord.ext import commands
import twitter
import os, sys, json

with open("{}/config.json".format(os.path.dirname(os.path.realpath(sys.argv[0])))) as properties:
    data = json.load(properties)
    data = data["twitter"]
    api = twitter.Api(consumer_key=data["consumer"]["key"], 
                        consumer_secret=data["consumer"]["secret"], 
                        access_token_key=data["access_token"]["key"], 
                        access_token_secret=data["access_token"]["secret"])




class Twitter():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="twitter")
    async def get_latest_tweet(self, handle : str):
        """Returns the most recent tweet from a specified Twitter user."""
        timeline = api.GetUserTimeline(screen_name=handle, count=1)
        tweet_id = timeline[0].id
        screen_name = timeline[0].user.screen_name
        await self.bot.say('https://twitter.com/{0}/status/{1}'.format(screen_name, tweet_id))


def setup(bot):
    bot.add_cog(Twitter(bot))
