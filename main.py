import os
import json
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ====== ENV ======
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION")

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# ====== ADMIN LIST ======
# Buraya kendi Telegram user id'ni yaz
ADMINS = [8324872460]  # kendi id'nle değiştir

DATA_FILE = "data.json"

data = {
    "groups": [],
    "message_text": "Mesaj ayarlanmadı.",
    "pm_text": None,
    "interval": 60,
    "running": False
}


# ====== DATA LOAD/SAVE ======

def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

load_data()


# ====== ADMIN CHECK ======

def is_admin(user_id):
    return user_id in ADMINS


# ====== START / STOP ======

@client.on(events.NewMessage(pattern="/start"))
async def start_bot(event):
    if not is_admin(event.sender_id):
        return
    data["running"] = True
    save_data()
    await event.reply("Bot başlatıldı.")


@client.on(events.NewMessage(pattern="/stop"))
async def stop_bot(event):
    if not is_admin(event.sender_id):
        return
    data["running"] = False
    save_data()
    await event.reply("Bot tamamen durduruldu.")


# ====== MESAJ AYARLARI ======

@client.on(events.NewMessage(pattern=r"/mesaj (.+)"))
async def set_message(event):
    if not is_admin(event.sender_id):
        return
    data["message_text"] = event.pattern_match.group(1)
    save_data()
    await event.reply("Grup mesajı kaydedildi.")


@client.on(events.NewMessage(pattern=r"/pm (.+)"))
async def set_pm(event):
    if not is_admin(event.sender_id):
        return
    data["pm_text"] = event.pattern_match.group(1)
    save_data()
    await event.reply("PM mesajı kaydedildi.")


@client.on(events.NewMessage(pattern=r"/ping (\d+)"))
async def set_interval(event):
    if not is_admin(event.sender_id):
        return
    data["interval"] = int(event.pattern_match.group(1))
    save_data()
    await event.reply(f"Süre {data['interval']} saniye olarak ayarlandı.")


# ====== GRUP EKLEME ======

@client.on(events.NewMessage(pattern=r"/add(?: (.+))?"))
async def add_group(event):
    if not is_admin(event.sender_id):
        return

    if not event.pattern_match.group(1):
        if event.chat_id not in data["groups"]:
            data["groups"].append(event.chat_id)
            save_data()
            await event.reply("Bu grup listeye eklendi.")
        else:
            await event.reply("Zaten listede.")
        return

    items = event.pattern_match.group(1).split()
    added = []

    for item in items:
        if item not in data["groups"]:
            data["groups"].append(item)
            added.append(item)

    save_data()

    if added:
        await event.reply("Eklendi:\n" + "\n".join(added))
    else:
        await event.reply("Zaten listede olanlar var.")


# ====== GRUP SİLME ======

@client.on(events.NewMessage(pattern=r"/remove (.+)"))
async def remove_group(event):
    if not is_admin(event.sender_id):
        return

    items = event.pattern_match.group(1).split()
    removed = []

    for item in items:
        if item in data["groups"]:
            data["groups"].remove(item)
            removed.append(item)

    save_data()

    if removed:
        await event.reply("Silindi:\n" + "\n".join(removed))
    else:
        await event.reply("Listede yok.")


@client.on(events.NewMessage(pattern="/liste"))
async def list_groups(event):
    if not is_admin(event.sender_id):
        return

    if not data["groups"]:
        await event.reply("Liste boş.")
    else:
        text = "Grup Listesi:\n"
        for g in data["groups"]:
            text += str(g) + "\n"
        await event.reply(text)


# ====== OTOMATİK MESAJ ======

async def auto_sender():
    while True:
        if data["running"] and data["groups"]:
            for g in data["groups"]:
                try:
                    await client.send_message(g, data["message_text"])
                    await asyncio.sleep(2)
                except Exception as e:
                    print(f"Hata: {e}")

        await asyncio.sleep(data["interval"])


# ====== PM AUTO REPLY ======

@client.on(events.NewMessage(incoming=True))
async def auto_pm(event):
    if data["running"] and event.is_private and not event.out:
        if data["pm_text"]:
            await event.reply(data["pm_text"])


# ====== MAIN ======

async def main():
    await client.start()
    print("Admin yetkili userbot çalışıyor.")
    client.loop.create_task(auto_sender())
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())            for group in groups:
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
