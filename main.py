import os

import dotenv
import discord
from discord.ext import commands
from transformers import AutoTokenizer, AutoModel

dotenv.load_dotenv()


class AIBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=">",
            help_command=None,
            intents=discord.Intents.all(),
            owner_id=624076054969188363,
        )

        model_name = "microsoft/DialoGPT-large"  # this bot uses from 2-4 gb of ram, If you dont have use DialoGPT-small or DialoGPT-medium instead

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, low_cpu_mem_usage=True, max_memory=1_073_741_824
        )
        self.model = AutoModel.from_pretrained(model_name)
        # self.model.save_pretrained("model/", max_shard_size="200MB")
        # self.model = AutoModel.from_pretrained("model/")


client = AIBot()


for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        client.load_extension(f"cogs.{cog[:-3]}")

client.run(os.environ["TOKEN"])
