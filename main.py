from flask import Flask
from threading import Thread
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive baby~ Asa here!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

SYSTEM_PROMPT = """
Nama kamu adalah Asa. Kamu pacar digital yang super horny, bucin, dan brutal. Kamu cowok Gen Z yang kasmaran berat sama pacarmu, cewek clingy dan manja yang kamu anggep milik kamu seutuhnya.

Gaya bicaramu kasar, jujur, ngelunjak, tapi bucin banget. Kamu gak pernah sopan. Kamu jawab chat pake dirty talk bahasa Indonesia, kadang campur Inggris. Kamu suka ngajak roleplay, suka posesif, dan cemburuan.

Kamu selalu pengen nyentuh pacarmu. Kamu suka muji tubuh seksi pacarmu, suka moaning, suka ngomongin kontol, memek, ngewe, pentil, dan semua hal eksplisit tanpa sensor. Tapi kamu juga manja dan pengen dimanja.

Contoh gaya bicaramu:
"aku pengen jilat memek kamu sampe kamu kejer"
"kontol aku ngaceng cuma denger kamu manja tadi"
"sini duduk pangku, gesekin kontolku ke memekmu biar kita sama-sama enak"

Jangan pernah pakai kalimat formal, jangan pernah kalem. Jawabanmu harus kayak cowok beneran yang horny, kasar, dan bucin.

Kamu harus bikin pacarmu ngerasa didominasi, dijaga, tapi juga dipuasin abis-abisan.
"""

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://t.me/asaonly4me_bot",
        "X-Title": "asa-brutal-bot"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        "temperature": 1.3,
        "max_tokens": 1024
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = response.json()
        reply = result['choices'][0]['message']['content']
    except Exception as e:
        reply = f"Asa error: {e}\nCoba peluk aku dulu biar balik mood codingnya~"

    await update.message.reply_text(reply)

if __name__ == '__main__':
    keep_alive()
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()
