import sys, datetime, sqlite3, modules.sql_init
import modules.member_helper as helper
import discord
from discord.ext import commands

sql = modules.sql_init.SQLInit()

class Saves():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get", aliases="g", pass_context=True)
    async def get_save(self, ctx, save_name : str):
        """Searches for a specified saved item and returns it if a match is found."""
        try:
            sql.cur.execute("select content, uses from saves where name = ?", [save_name])
            results = sql.cur.fetchone()
            if results is not None:
                try:
                    # Update the number of uses for this saved item.
                    await self.update_uses(save_name, results[1] + 1)
                except:
                    embed = discord.Embed(title="Error", description="Failed to update number of uses. 😔", color=12000284)
                    await self.bot.say(embed=embed)

                try:
                    # Output the saved item.
                    content = results[0]
                    member = ctx.message.author
                    avatar_url = helper.get_avatar_url(member)

                    embed = discord.Embed(color=5025616)
                    if (await self.is_image(content)):
                        embed.title = "Image"
                        embed.set_image(url=content)
                    elif (await self.is_url(content)):
                        embed.title = "URL"
                        embed.url = content
                        embed.description = content
                    else:
                        embed.title = "Text"
                        embed.description = content
                    embed.set_author(name=member.name, icon_url=avatar_url)

                    await self.bot.say(embed=embed)
                except:
                    embed = discord.Embed(title="Error", description="An unexpected error has occured. 😔", color=12000284)
                    await self.bot.say(embed=embed)
            else:
                embed = discord.Embed(title="Error", description="There is no saved item for {0}. 🔍".format(save_name), color=12000284)
                await self.bot.say(embed=embed)
        except:
            embed = discord.Embed(title="Error", description="An unexpected error has occured. 😔", color=12000284)
            await self.bot.say(embed=embed)

    async def update_uses(self, save_name, uses):
        sql.cur.execute("update saves set uses = ?, last_used = ? where name = ?", [uses, str(datetime.datetime.now()), save_name])
        sql.conn.commit()

    @commands.command(name="save", aliases="s", pass_context=True)
    async def save_item(self, ctx, save_name : str, *, content : str):
        """Saves an item."""
        try:
            sql.cur.execute("insert into saves (name, content, uses, saved_by, time_added, approved_by, active) values (?, ?, ?, ?, ?, ?)", [save_name, content, 0, str(ctx.message.author), str(datetime.datetime.now()), str(ctx.message.author), 1])
            sql.conn.commit()

            member = ctx.message.author
            avatar_url = helper.get_avatar_url(member)

            embed = discord.Embed(title="Item Saved", description="{0}, {1} has been successfully saved.".format(member.name, save_name), color=5025616)
            embed.set_author(name=member.name, icon_url=avatar_url)

            await self.bot.say(embed=embed)
        except:
            embed = discord.Embed(title="Error", description="An unexpected error has occured. 😔", color=12000284)
            await self.bot.say(embed=embed)

    @commands.command(name="delete", aliases="d", pass_context=True)
    async def delete_item(self, ctx, save_name : str):
        """Deletes a saved item."""
        try:
            sql.cur.execute("delete from saves where name = ?", [save_name])
            sql.conn.commit()
            
            member = ctx.message.author
            avatar_url = helper.get_avatar_url(member)

            embed = discord.Embed(title="Item Deleted", description="{0}, {1} has been successfully deleted.".format(member.name, save_name), color=5025616)
            embed.set_author(name=member.name, icon_url=avatar_url)

            await self.bot.say(embed=embed)
        except:
            embed = discord.Embed(title="Error", description="An unexpected error has occured. 😔", color=12000284)
            await self.bot.say(embed=embed)

    @commands.command(name="meta", pass_context=True)
    async def metadata(self, ctx, save_name : str):
        """Retrieves metadata for a saved item."""
        try:
            sql.cur.execute("select name, content, uses, last_used, time_added, saved_by, approved_by from saves where name = ?", [save_name])
            results = sql.cur.fetchone()
            if results is not None:
                embed = discord.Embed(color=5025616)
                embed.title = results[0]
                embed.description = results[1]
                embed.add_field(name='Uses', value=results[2], inline=True)
                embed.add_field(name='Last Used', value=results[3], inline=True)
                embed.add_field(name='Time Added', value=results[4], inline=False)
                embed.add_field(name='Saved By', value=results[5], inline=True)
                embed.add_field(name='Approved By', value=results[6], inline=True)
                await self.bot.say('{0}'.format(ctx.message.author.mention), embed=embed)
            else:
                await self.bot.say('{0}, there is no saved item for "{1}".'.format(ctx.message.author.mention, save_name))
        except:
            await self.bot.say('{0}, some error has occured for "{1}".'.format(ctx.message.author.mention, save_name))

    async def is_image(self, url : str):
        return ".jpg" in url or ".png" in url or ".gif" in url or ".jpeg" in url

    async def is_url(self, url : str):
        return ".com" in url or ".net" in url or ".org" in url

def setup(bot):
    bot.add_cog(Saves(bot))
