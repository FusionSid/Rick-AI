import os
from io import BytesIO

import torch
import discord
import aiosqlite
import dotenv
from discord.ext import commands
from transformers import AutoModelForCausalLM, AutoTokenizer


dotenv.load_dotenv()

prefix = ">"
client = commands.Bot(prefix, intents=discord.Intents.all())
aitest_channel = 976787402838405140

model_name = "microsoft/DialoGPT-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


async def run_ai(message: str, author_id: int, channel) -> str:
    async with aiosqlite.connect("main.db") as db:
        cur = await db.execute("SELECT * FROM Tensors WHERE user_id=?", (author_id,))
        data = await cur.fetchall()

        if len(data) == 0:
            await db.execute("INSERT INTO Tensors (user_id) VALUES (?)", (author_id,))
            await db.commit()
            data = [(author_id, None)]

        if message == ">reset":
            await db.execute(
            "UPDATE Tensors SET context=? WHERE user_id=?",
                (
                    None,
                    author_id,
                ),
            )
            await db.commit()
            return "Good job you killed the previous AI\n--AI context/data has been reset--\nSend another message to talk to the new AI :)"

        data = data[0]

    if data[1] is None:
        context = tokenizer.encode(message + tokenizer.eos_token, return_tensors="pt")
    else:
        context = torch.load(BytesIO(data[1]))
        context = torch.cat(
            [
                context,
                tokenizer.encode((message + tokenizer.eos_token), return_tensors="pt"),
            ],
            dim=-1,
        )

    output = BytesIO()
    torch.save(context, output)
    output.seek(0)

    if message == ">send-tensor":
        await channel.send(file=discord.File(output, "output.pt"))
        return 'Sent!'

    context_bytes_data = bytes(output.read())

    async with aiosqlite.connect("main.db") as db:
        await db.execute(
            "UPDATE Tensors SET context=? WHERE user_id=?",
            (
                context_bytes_data,
                author_id,
            ),
        )
        await db.commit()

    response = model.generate(
        context,
        max_length=6942,
        do_sample=True,
        top_k=100,
        temperature=0.75,
        pad_token_id=tokenizer.eos_token_id,
    )

    ai_response = tokenizer.decode(
        response[:, context.shape[-1] :][0], skip_special_tokens=True
    )

    return ai_response


@client.event
async def on_ready():
    print("Ready")


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    
    if not isinstance(message.channel, discord.DMChannel):
        return


    response = await run_ai(message.content, message.author.id, message.channel)

    if response.replace(" ", "") == "":
        response = "IDK"

    await message.reply(response)


client.run(os.environ["TOKEN"])
