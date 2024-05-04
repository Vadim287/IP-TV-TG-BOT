from pyrogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, Message
import os, pyrogram, json
from pyrogram import Client, filters
from requests import get

# conifg
with open('config.json', 'r') as f: CONFIGDATA = json.load(f)

# app
TOKEN = os.environ.get("TOKEN") or CONFIGDATA.get("TOKEN", "")
HASH = os.environ.get("HASH") or CONFIGDATA.get("HASH", "")
ID = os.environ.get("ID") or CONFIGDATA.get("ID", "")
app: Client = Client("my_bot", api_id=ID, api_hash=HASH, bot_token=TOKEN)

# channles
CHANNELS = get("https://iptvonline.ucoz.net/channels.json").json()
print("Total Channels:", len(CHANNELS))
CHANNELS_BY_ID = {channel.get("id", "None"): channel for channel in CHANNELS}


# refresh
def refresh():
    streams = get("https://iptvonline.ucoz.net/streams.json").json()
    online = []
    for stream in streams:
        if stream.get("status", "online") == "online" and stream.get("channel", None) is not None:
            channel_id = stream["channel"]
            if channel_id in CHANNELS_BY_ID.keys():
                channel = CHANNELS_BY_ID[channel_id]
                stream["name"] = channel["name"]
            online.append(stream)
    print("Total Streams:", len(online))
    return online


# streams
STREAM_LINK = "https://iptvonline.ucoz.net/"  # Измененная строка
STREAMS = refresh()

# settings
COLMS = 2
ROWS = 15

@app.on_message(filters.command('start'))
def start_handler(client: Client, message: Message):
  message.reply_text('Привет! Я пользовательский бот, больше подробностей -  -, IP-TV Telegram напиши любой канал ПРИМЕР: ТНТ Music.')

@app.on_message(filters.command('help'))
def start_handler(client: Client, message: Message):
  message.reply_text('В базе более 10000 каналов,подпишись для обсуждений 😉😉😉 https://t.me/iptvvtg')

@app.on_message(filters.command('admin'))
def start_handler(client: Client, message: Message):
  message.reply_text('Для связи @Pupsyandiya')

# text
@app.on_message(filters.text)
def tvname(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    search = message.text
    tvs = [InlineKeyboardButton(text=x.get("name", x["channel"]),
                                web_app=WebAppInfo(url=STREAM_LINK + "?url=" + x["url"]))
           for x in STREAMS if search.lower() in x.get("name", x["channel"]).lower()]

    print("Total Results for", search, "is", len(tvs))
    if len(tvs) == 0:
        app.send_message(message.chat.id, "Напишите канал ПРИМЕР: ТНТ Music", reply_to_message_id=message.id)
        return

    main = []
    for i in range(0, len(tvs), COLMS): main.append(tvs[i:i + COLMS])

    app.send_message(message.chat.id, 'Тыкни на любой канал для просмотра IP-TV в ТЕЛЕГРАММЕ',
                     reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(main[:ROWS]))
app.run()
