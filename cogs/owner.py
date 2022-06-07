import datetime

import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title="Reload",
            description=f"{extension} successfully reloaded",
            color=ctx.author.color,
        )
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title="Load",
            description=f"{extension} successfully loaded",
            color=ctx.author.color,
        )
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title="Unload",
            description=f"{extension} successfully unloaded",
            color=ctx.author.color,
        )
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Owner(client))
