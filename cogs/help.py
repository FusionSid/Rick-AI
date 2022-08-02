import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="help", description="Get help on the bot")
    async def _help(self, ctx):
        em = discord.Embed(
            title="This bot is still under construction",
            description="Send a message to the bot to interact with the ai\nuse `>reset` to reset the ai. (do this after like 25 messages cause the ai forgets to speak sometimes)",
        )
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Help(client))
