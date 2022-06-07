import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="help", description="Get help on the bot")
    async def _help(self, ctx):
        em = discord.Embed()
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Help(client))
