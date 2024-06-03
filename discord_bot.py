import os
import discord
import asyncio
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
SERVER_ID = int(os.getenv("SERVER_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

async def fetch_channel_attachments():
    attachments = []
    server = client.get_guild(SERVER_ID)
    if not server:
        print('Could not find server')
        return attachments
    channel = server.get_channel(CHANNEL_ID)
    if not channel:
        print('Could not find channel')
        return attachments
    async for message in channel.history(limit=None):
        for attachment in message.attachments:
            attachments.append({
                "message_id": message.id,
                "filename": attachment.filename,
                "size": attachment.size,
                "url": attachment.url,
                "filetype": attachment.filename.split(".")[-1]
            })
    return attachments

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

async def run_discord_bot():
    await client.start(BOT_TOKEN)
