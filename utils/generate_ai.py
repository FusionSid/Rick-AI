import re
from io import BytesIO

import torch
import discord
import aiosqlite
import pytesseract
from PIL import Image


async def run_ai(model, tokenizer, actual_message: discord.Message) -> str:
    author_id = actual_message.author.id
    channel = actual_message.channel
    message = actual_message.content

    if actual_message.attachments is not None:
        for attachment in actual_message.attachments:
            if "image" in attachment.content_type:
                img_save = BytesIO()
                await attachment.save(img_save)
                img = Image.open(img_save)
                text = pytesseract.image_to_string(img)
                message += re.sub("[^a-zA-Z\d\s:]", "", text)

    async with aiosqlite.connect("main.db") as db:
        cur = await db.execute("SELECT * FROM Tensors WHERE user_id=?", (author_id,))
        data = await cur.fetchall()

        if len(data) == 0:
            await db.execute("INSERT INTO Tensors (user_id) VALUES (?)", (author_id,))
            await db.commit()
            data = [(author_id, None)]
        if message == ">reset" or message == "!reset":
            await db.execute(
                "UPDATE Tensors SET context=? WHERE user_id=?",
                (
                    None,
                    author_id,
                ),
            )
            await db.commit()

            em = discord.Embed(
                title="AI reset",
                description="You have reseted the AI so it won't remember anything from before.\nSend a message to talk to the new AI:",
                color=discord.Color.random(),
            )
            await channel.send(embed=em)

            return False

        data = data[0]

    if data[1] is None:
        context = tokenizer.encode(message + tokenizer.eos_token, return_tensors="pt")
    else:
        context = torch.load(BytesIO(data[1]))
        context = torch.cat(
            [
                context,
                tokenizer.encode(((message) + tokenizer.eos_token), return_tensors="pt"),
            ],
            dim=-1,
        )

    output = BytesIO()
    torch.save(context, output)
    output.seek(0)

    if message == ">send-tensor":
        await channel.send(file=discord.File(output, "output.pt"))
        return False

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
        max_length=1000,
        top_k=100,
        temperature=0.75,
        pad_token_id=tokenizer.eos_token_id,
    
    )
    ai_response = tokenizer.decode(
        response[:, context.shape[-1] :][0], skip_special_tokens=True
    )

    return ai_response
