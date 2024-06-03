import asyncio
import uvicorn
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from discord_bot import run_discord_bot, fetch_channel_attachments, client, CHANNEL_ID
import discord
import io

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    attachments = await fetch_channel_attachments()
    return templates.TemplateResponse("index.html", {"request": request, "attachments": attachments})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        return {"error": "Channel not found"}
    file_data = io.BytesIO(await file.read())
    await channel.send(file=discord.File(file_data, filename=file.filename))
    return {"filename": file.filename}

@app.get("/check-file/{message_id}")
async def check_file(message_id: int):
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        return {"error": "Channel not found"}
    try:
        await channel.fetch_message(message_id)
        return {"message": "File exists"}
    except discord.NotFound:
        return {"error": "Message not found"}

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

async def main():
    loop = asyncio.get_event_loop()
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    bot_task = loop.create_task(run_discord_bot())
    api_task = loop.create_task(server.serve())
    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    asyncio.run(main())