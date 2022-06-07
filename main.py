import os

import dotenv
import discord
from discord.ext import commands
from transformers import AutoModelForCausalLM, AutoTokenizer

dotenv.load_dotenv()


class AIBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=">",
            help_command=None,
            intents=discord.Intents.all(),
            owner_id=624076054969188363,
        )

        model_name = "microsoft/DialoGPT-large"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)


client = AIBot()


for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")

client.run(os.environ["TOKEN"])
