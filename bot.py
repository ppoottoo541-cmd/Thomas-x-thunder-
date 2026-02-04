# ==============================
# FILE SHARING BOT (ONE FILE)
# Library: pyTelegramBotAPI
# ==============================

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3, random, string, threading

# ========= CONFIG =========
MAIN_BOT_TOKEN = "8580329271:AAE8SlxlyggTLW0YSR0YZVGgAtjOYGpoRvI"
ADMIN_BOT_TOKEN = "8553759431:AAHKDR2BZ1C550sTe749WaizG9jUCncOm18"
ADMIN_ID = 7417241499   # apna telegram user id
# ==========================

# ========= DATABASE =========
DB = "data.db"

def db_connect():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    db = db_connect()
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS files
        (code TEXT PRIMARY KEY, file_id TEXT, file_name TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS channels
        (channel_id INTEGER PRIMARY KEY, link TEXT, active INTEGER DEFAULT 1)""")
    c.execute("""CREATE TABLE IF NOT EXISTS verified
        (user_id INTEGER, code TEXT, PRIMARY KEY(user_id, code))""")
    db.commit()
    db.close()

init_db()

# ========= HELPERS =========
def gen_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# ========= BOTS =========
main_bot = telebot.TeleBot(MAIN_BOT_TOKEN, parse_mode="HTML")
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN, parse_mode="HTML")

# ==========================
# ADMIN BOT
# ==========================

@admin_bot.message_handler(content_types=["document", "video"])
def admin_upload(msg):
    if msg.from_user.id != ADMIN_ID:
        return

    file = msg.document or msg.video
    code = gen_code()

    db = db_connect()
    db.execute("INSERT INTO files VALUES (?,?,?)",
               (code, file.file_id, file.file_name or "file"))
    db.commit()
    db.close()

    link = f"https://t.me/{main_bot.get_me().username}?start={code}"
    admin_bot.reply_to(
        msg,
        f"✅ <b>File Uploaded</b>\n\n🔗 <code>{link}</code>"
    )

@admin_bot.message_handler(commands=["add_channel"])
def add_channel(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        _, cid, link = msg.text.split(maxsplit=2)
        db = db_connect()
        db.execute("INSERT OR REPLACE INTO channels VALUES (?,?,1)",
                   (int(cid), link))
        db.commit()
        db.close()
        admin_bot.reply_to(msg, "✅ Channel added")
    except:
        admin_bot.reply_to(msg, "❌ Usage:\n/add_channel <channel_id> <link>")

@admin_bot.message_handler(commands=["remove_channel"])
def remove_channel(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        _, cid = msg.text.split(maxsplit=1)
        db = db_connect()
        db.execute("UPDATE channels SET active=0 WHERE channel_id=?",
                   (int(cid),))
        db.commit()
        db.close()
        admin_bot.reply_to(msg, "❌ Channel removed")
    except:
        admin_bot.reply_to(msg, "Usage:\n/remove_channel <channel_id>")

# ==========================
# MAIN BOT
# ==========================

@main_bot.message_handler(commands=["start"])
def start(msg):
    args = msg.text.split()
    if len(args) == 1:
        main_bot.reply_to(msg, "📁 File link bhejo")
        return

    code = args[1]
    db = db_connect()
    cur = db.execute("SELECT file_id, file_name FROM files WHERE code=?", (code,))
    file = cur.fetchone()
    db.close()

    if not file:
        main_bot.reply_to(msg, "❌ Invalid link")
        return

    db = db_connect()
    cur = db.execute("SELECT 1 FROM verified WHERE user_id=? AND code=?",
                     (msg.from_user.id, code))
    if cur.fetchone():
        db.close()
        main_bot.send_document(msg.chat.id, file[0], caption=file[1])
        return
    db.close()

    db = db_connect()
    channels = db.execute(
        "SELECT channel_id, link FROM channels WHERE active=1"
    ).fetchall()
    db.close()

    kb = InlineKeyboardMarkup()
    for _, link in channels:
        kb.add(InlineKeyboardButton("🔔 Join Channel", url=link))
    kb.add(InlineKeyboardButton("✅ I Joined", callback_data=f"check_{code}"))

    main_bot.send_message(
        msg.chat.id,
        "📢 <b>Pehle sab channels join karo:</b>",
        reply_markup=kb
    )

@main_bot.callback_query_handler(func=lambda c: c.data.startswith("check_"))
def verify(call):
    code = call.data.split("_")[1]
    uid = call.from_user.id

    db = db_connect()
    channels = db.execute(
        "SELECT channel_id FROM channels WHERE active=1"
    ).fetchall()
    db.close()

    for (cid,) in channels:
        try:
            m = main_bot.get_chat_member(cid, uid)
            if m.status not in ["member", "administrator", "creator"]:
                raise Exception
        except:
            main_bot.answer_callback_query(
                call.id,
                "❌ Sab channels join nahi kiye",
                show_alert=True
            )
            return

    db = db_connect()
    db.execute("INSERT OR IGNORE INTO verified VALUES (?,?)", (uid, code))
    cur = db.execute("SELECT file_id, file_name FROM files WHERE code=?", (code,))
    file = cur.fetchone()
    db.commit()
    db.close()

    main_bot.send_document(call.message.chat.id, file[0], caption=file[1])
    main_bot.answer_callback_query(call.id, "✅ Verified")

# ==========================
# RUN BOTH BOTS
# ==========================

print("🚀 MAIN BOT + ADMIN BOT RUNNING")

threading.Thread(target=admin_bot.infinity_polling).start()
main_bot.infinity_polling()
