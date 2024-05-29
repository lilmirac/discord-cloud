import os
import discord
import asyncio
from discord.ext import tasks
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
SERVER_ID = int(os.getenv("SERVER_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)
app = FastAPI()

templates = Jinja2Templates(directory="templates")

attachments = []

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    fetch_channel_attachments.start()

@tasks.loop(count=1)
async def fetch_channel_attachments():
    server = client.get_guild(SERVER_ID)
    if not server:
        print(f'Could not find server with ID {SERVER_ID}')
        return
    channel = server.get_channel(CHANNEL_ID)
    if not channel:
        print(f'Could not find channel with ID {CHANNEL_ID}')
        return

    async for message in channel.history(limit=None):
        for attachment in message.attachments:
            print(attachment)
            attachments.append({
                "filename": attachment.filename,
                "size": attachment.size,
                "url": attachment.url,
                "filetype": attachment.filename.split(".")[-1]
            })

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "attachments": attachments})

async def run_discord_bot():
    await client.start(BOT_TOKEN)

async def main():
    loop = asyncio.get_event_loop()

    # Running the FastAPI server in the same event loop
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)

    # Running the Discord bot in the same event loop
    bot_task = loop.create_task(run_discord_bot())
    api_task = loop.create_task(server.serve())

    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    import uvicorn
    asyncio.run(main())
