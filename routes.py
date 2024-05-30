import io
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from discord_bot import fetch_channel_attachments, client, CHANNEL_ID
import discord

router = APIRouter()
templates = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    attachments = await fetch_channel_attachments()
    return templates.TemplateResponse("index.html", {"request": request, "attachments": attachments})

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        return {"error": "Channel not found"}
    file_data = io.BytesIO(await file.read())
    await channel.send(file=discord.File(file_data, filename=file.filename))
    return {"filename": file.filename}

@router.get("/check-file/{message_id}")
async def check_file(message_id: int):
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        return {"error": "Channel not found"}
    try:
        await channel.fetch_message(message_id)
        return {"message": "File exists"}
    except discord.NotFound:
        return {"error": "Message not found"}

@router.delete("/delete/{message_id}")
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
