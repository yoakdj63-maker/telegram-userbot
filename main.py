from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session = os.getenv("SESSION")

client = TelegramClient(StringSession(session), api_id, api_hash)

groups = []
auto_message = ""
pm_message = ""
interval = 60
running = False

async def auto_sender():
    global running
    while running:
        for group in groups:
            try:
                await client.send_message(group, auto_message)
            except:
                pass
        await asyncio.sleep(interval)

@client.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    global running
    running = True
    await event.reply("Bot başlatıldı.")
    client.loop.create_task(auto_sender())

@client.on(events.NewMessage(pattern="/stop"))
async def stop_handler(event):
    global running
    running = False
    await event.reply("Bot durduruldu.")

@client.on(events.NewMessage(incoming=True))
async def auto_pm(event):
    if event.is_private and not event.out:
        if pm_message:
            await event.reply(pm_message)

client.start()
client.run_until_disconnected()
