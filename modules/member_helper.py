import discord

def get_avatar_url(member : discord.member):
    return member.avatar_url if member.avatar_url is not "" and member.avatar_url is not None else member.default_avatar_url

def get_nick(member: discord.member):
    return member.nick if member.nick is not "" and member.nick is not None else member.name