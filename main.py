import asyncio
import uvicorn
from fastapi import FastAPI
from discord_bot import run_discord_bot
from routes import router

app = FastAPI()
app.include_router(router)

async def main():
    loop = asyncio.get_event_loop()
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    bot_task = loop.create_task(run_discord_bot())
    api_task = loop.create_task(server.serve())
    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    asyncio.run(main())
