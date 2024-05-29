import os
import discord
import asyncio
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
SERVER_ID = int(os.getenv("SERVER_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

attachments = []

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    fetch_channel_attachments.start()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    attachments = await fetch_channel_attachments()
    return templates.TemplateResponse("index.html", {"request": request, "attachments": attachments})

async def fetch_channel_attachments():
    attachments = []
    server = client.get_guild(SERVER_ID)
    if not server:
        print(f'Could not find server with ID {SERVER_ID}')
        return attachments
    channel = server.get_channel(CHANNEL_ID)
    if not channel:
        print(f'Could not find channel with ID {CHANNEL_ID}')
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

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        return {"error": "Channel not found"}
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())
    await channel.send(file=discord.File(file_location))
    os.remove(file_location)
    return {"filename": file.filename}

@app.delete("/delete/{message_id}")
async def delete_file(message_id: int):
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        return {"error": "Channel not found"}
    try:
        message = await channel.fetch_message(message_id)
        await message.delete()
        return {"message": "File deleted successfully"}
    except discord.NotFound:
        return {"error": "Message not found"}
    
async def run_discord_bot():
    await client.start(BOT_TOKEN)

async def main():
    loop = asyncio.get_event_loop()
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    bot_task = loop.create_task(run_discord_bot())
    api_task = loop.create_task(server.serve())
    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    import uvicorn
    asyncio.run(main())
