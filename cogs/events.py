import datetime

import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("The bot is ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return

        if isinstance(message.channel, discord.DMChannel):
            return await self.client.process_commands(message)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = await self.client.fetch_channel(976787402838405140)
        em = discord.Embed(
            title="Leave", description=f"Left: {guild.name}", color=discord.Color.red()
        )
        em.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = await self.client.fetch_channel(976787402838405140)
        em = discord.Embed(
            title="Join",
            description=f"Joined: {guild.name}",
            color=discord.Color.green(),
        )
        em.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            raise error


def setup(client):
    client.add_cog(Events(client))
