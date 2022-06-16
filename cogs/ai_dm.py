import discord
from discord.ext import commands

from utils import run_ai

class DM_AI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id:
            return

        if not isinstance(message.channel, discord.DMChannel):
            return

        response = await run_ai(
            self.client.model,
            self.client.tokenizer,
            message
        )
        if not response:
            return

        if response.replace(" ", "") == "":
            response = "ERROR! (The bot had a skill issue)"

        await message.reply(response)


def setup(client):
    client.add_cog(DM_AI(client))
