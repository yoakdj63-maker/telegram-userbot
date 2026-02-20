import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ENV VARIABLES
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION")

client = TelegramClient(StringSession(session_string), api_id, api_hash)

groups = []
message_text = ""
pm_text = ""
interval = 60
running = False


# START
@client.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    global running
    running = True
    await event.reply("Bot started.")


# STOP
@client.on(events.NewMessage(pattern="/stop"))
async def stop_handler(event):
    global running
    running = False
    await event.reply("Bot stopped.")


# ADD GROUP
@client.on(events.NewMessage(pattern=r"/add (.+)"))
async def add_group(event):
    global groups
    group = event.pattern_match.group(1)
    if group not in groups:
        groups.append(group)
        await event.reply(f"Added: {group}")
    else:
        await event.reply("Already in list.")


# REMOVE GROUP
@client.on(events.NewMessage(pattern=r"/remove (.+)"))
async def remove_group(event):
    global groups
    group = event.pattern_match.group(1)
    if group in groups:
        groups.remove(group)
        await event.reply(f"Removed: {group}")
    else:
        await event.reply("Not found.")


# LIST GROUPS
@client.on(events.NewMessage(pattern="/liste"))
async def list_groups(event):
    if groups:
        await event.reply("Groups:\n" + "\n".join(groups))
    else:
        await event.reply("Group list empty.")


# SET MESSAGE
@client.on(events.NewMessage(pattern=r"/mesaj (.+)"))
async def set_message(event):
    global message_text
    message_text = event.pattern_match.group(1)
    await event.reply("Message saved.")


# SET PM AUTO REPLY
@client.on(events.NewMessage(pattern=r"/pm (.+)"))
async def set_pm(event):
    global pm_text
    pm_text = event.pattern_match.group(1)
    await event.reply("PM auto-reply set.")


# SET INTERVAL
@client.on(events.NewMessage(pattern=r"/ping (\d+)"))
async def set_interval(event):
    global interval
    interval = int(event.pattern_match.group(1))
    await event.reply(f"Interval set to {interval} seconds.")


# AUTO PM REPLY
@client.on(events.NewMessage(incoming=True))
async def auto_pm(event):
    global pm_text
    if event.is_private and not event.out:
        if pm_text:
            await event.reply(pm_text)


# MESSAGE LOOP
async def send_loop():
    global running
    while True:
        if running and groups and message_text:
            for group in groups:
                try:
                    await client.send_message(group, message_text)
                except Exception as e:
                    print(f"Error sending to {group}: {e}")
            await asyncio.sleep(interval)
        else:
            await asyncio.sleep(5)


async def main():
    await client.start()
    print("Userbot is running...")
    asyncio.create_task(send_loop())
    await client.run_until_disconnected()


client.start()
print("Userbot is running...")
client.loop.create_task(send_loop())
client.run_until_disconnected()
