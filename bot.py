import telebot
from telebot import types
import json
import os
import random
import string
import threading

# ================= CONFIG =================
MAIN_BOT_TOKEN = "8423822085:AAFRfhkeq0ffD4XNlH9mFyzgFJff6pAZWAI"
ADMIN_BOT_TOKEN = "8247524950:AAEOcbPack3onrCgOqPndOC_ha-fuvf8q2k"
ADMIN_ID = 8381053240

# IMPORTANT: Yeh channel storage ke liye hai (files save hogi yaha)
# Dono bots ko is channel mein admin banana ZARURI hai
STORAGE_CHANNEL = "-1003855834042"

CHANNEL_DB = "channels.json"
FILE_DB = "files.json"

# Initialize both bots
main_bot = telebot.TeleBot(MAIN_BOT_TOKEN, parse_mode="HTML")
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN, parse_mode="HTML")

# ================= INIT FILES =================
if not os.path.exists(CHANNEL_DB):
    with open(CHANNEL_DB, "w") as f:
        json.dump({}, f)

if not os.path.exists(FILE_DB):
    with open(FILE_DB, "w") as f:
        json.dump({}, f)

def load_channels():
    with open(CHANNEL_DB) as f:
        return json.load(f)

def save_channels(data):
    with open(CHANNEL_DB, "w") as f:
        json.dump(data, f, indent=2)

def load_files():
    with open(FILE_DB) as f:
        return json.load(f)

def save_files(data):
    with open(FILE_DB, "w") as f:
        json.dump(data, f, indent=2)

def gen_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# ================= JOIN CHECK (for main bot) =================
def joined_all(user_id):
    channels = load_channels()
    if not channels:
        return True
    
    for ch_id in channels:
        # Skip storage channel from force subscribe check
        if ch_id == STORAGE_CHANNEL:
            continue
            
        try:
            status = main_bot.get_chat_member(int(ch_id), user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            print(f"Error checking membership for {ch_id}: {e}")
            return False
    return True

# ================= ADMIN BOT COMMANDS =================
@admin_bot.message_handler(commands=["start"])
def admin_start(m):
    if m.from_user.id != ADMIN_ID:
        admin_bot.reply_to(m, "❌ You are not authorized!")
        return
    
    admin_bot.send_message(
        m.chat.id,
        "<b>🤖 Admin Bot Panel</b>\n\n"
        "<b>📢 Channel Management:</b>\n"
        "/addchannel -100xxxxxxxx\n"
        "/removechannel -100xxxxxxxx\n"
        "/channels - List all channels\n\n"
        "<b>📤 File Management:</b>\n"
        "/upload - Upload file and get link\n"
        "/files - List all uploaded files\n"
        "/deletefile CODE - Delete a file\n\n"
        "/help - Show this message"
    )

@admin_bot.message_handler(commands=["help"])
def admin_help(m):
    if m.from_user.id != ADMIN_ID:
        admin_bot.reply_to(m, "❌ You are not authorized!")
        return
    
    help_text = f"""
<b>🤖 Admin Bot Commands:</b>

<b>Channel Management:</b>
/addchannel -100xxxxxxxx - Add force subscribe channel
/removechannel -100xxxxxxxx - Remove channel
/channels - List all channels

<b>File Management:</b>
/upload - Upload file and get shareable link
/files - List all uploaded files
/deletefile CODE - Delete a file

<b>📝 Setup Instructions:</b>
1. Storage Channel: <code>{STORAGE_CHANNEL}</code>
2. <b>DONO BOTS</b> ko is channel mein admin banao
3. Force subscribe channels alag se add karo

<b>📝 How to get Channel ID:</b>
Forward message from channel to @userinfobot
"""
    admin_bot.send_message(m.chat.id, help_text)

@admin_bot.message_handler(commands=["addchannel"])
def add_channel(m):
    if m.from_user.id != ADMIN_ID:
        admin_bot.reply_to(m, "❌ You are not authorized!")
        return
    try:
        ch_id = m.text.split()[1]
        
        if not ch_id.startswith("-100"):
            admin_bot.reply_to(m, "❌ Channel ID must start with -100")
            return
        
        data = load_channels()
        data[ch_id] = "added"
        save_channels(data)
        
        admin_bot.reply_to(
            m, 
            f"✅ Channel added: <code>{ch_id}</code>\n\n"
            f"⚠️ Main Bot ko is channel mein admin banao!"
        )
    except IndexError:
        admin_bot.reply_to(m, "❌ Use: /addchannel -100xxxxxxxx")
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(commands=["removechannel"])
def remove_channel(m):
    if m.from_user.id != ADMIN_ID:
        admin_bot.reply_to(m, "❌ You are not authorized!")
        return
    try:
        ch_id = m.text.split()[1]
        data = load_channels()
        if ch_id in data:
            data.pop(ch_id)
            save_channels(data)
            admin_bot.reply_to(m, f"🗑 Channel removed: <code>{ch_id}</code>")
        else:
            admin_bot.reply_to(m, "❌ Channel not found")
    except IndexError:
        admin_bot.reply_to(m, "❌ Use: /removechannel -100xxxxxxxx")
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(commands=["channels"])
def list_channels(m):
    if m.from_user.id != ADMIN_ID:
        admin_bot.reply_to(m, "❌ You are not authorized!")
        return
    data = load_channels()
    if not data:
        admin_bot.reply_to(m, "📭 No channels\n\nUse: /addchannel -100xxxxxxxx")
        return
    txt = "<b>📢 Force Subscribe Channels:</b>\n\n"
    for i, ch in enumerate(data, 1):
        if ch == STORAGE_CHANNEL:
            txt += f"{i}. <code>{ch}</code> ⚙️ (Storage)\n"
        else:
            txt += f"{i}. <code>{ch}</code>\n"
    txt += f"\n<b>Storage:</b> <code>{STORAGE_CHANNEL}</code>"
    admin_bot.send_message(m.chat.id, txt)

@admin_bot.message_handler(commands=["upload"])
def upload(m):
    if m.from_user.id == ADMIN_ID:
        admin_bot.reply_to(m, "📤 Send file (document/video/photo/audio)")
    else:
        admin_bot.reply_to(m, "❌ Not authorized!")

@admin_bot.message_handler(commands=["files"])
def list_files(m):
    if m.from_user.id != ADMIN_ID:
        admin_bot.reply_to(m, "❌ Not authorized!")
        return
    
    files = load_files()
    if not files:
        admin_bot.reply_to(m, "📭 No files\n\nUse: /upload")
        return
    
    try:
        main_bot_username = main_bot.get_me().username
        txt = "<b>📁 Files:</b>\n\n"
        for i, (code, data) in enumerate(files.items(), 1):
            link = f"https://t.me/{main_bot_username}?start=get_{code}"
            txt += f"{i}. <code>{code}</code> - {data['type']}\n{link}\n\n"
        admin_bot.send_message(m.chat.id, txt)
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(commands=["deletefile"])
def delete_file(m):
    if m.from_user.id != ADMIN_ID:
        admin_bot.reply_to(m, "❌ Not authorized!")
        return
    
    try:
        code = m.text.split()[1]
        files = load_files()
        
        if code in files:
            files.pop(code)
            save_files(files)
            admin_bot.reply_to(m, f"🗑 Deleted: <code>{code}</code>")
        else:
            admin_bot.reply_to(m, "❌ Not found")
    except IndexError:
        admin_bot.reply_to(m, "❌ Use: /deletefile CODE")
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(content_types=["document", "video", "photo", "audio"])
def save_file(m):
    if m.from_user.id != ADMIN_ID:
        return

    try:
        files = load_files()
        code = gen_code()

        # Forward to storage channel
        forwarded = admin_bot.forward_message(STORAGE_CHANNEL, m.chat.id, m.message_id)

        files[code] = {
            "message_id": forwarded.message_id,
            "type": m.content_type
        }

        save_files(files)

        main_bot_username = main_bot.get_me().username
        link = f"https://t.me/{main_bot_username}?start=get_{code}"

        admin_bot.reply_to(
            m,
            f"✅ <b>Saved!</b>\n\n"
            f"📋 <code>{code}</code>\n"
            f"📦 {m.content_type}\n"
            f"🔗 <code>{link}</code>"
        )
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}\n\nDono bots admin hain storage channel mein?")
        print(f"Save error: {e}")

# ================= MAIN BOT =================
@main_bot.message_handler(commands=["start"])
def main_start(m):
    args = m.text.split()

    if len(args) < 2 or not args[1].startswith("get_"):
        main_bot.send_message(
            m.chat.id,
            "👋 <b>Welcome!</b>\n\n"
            "📎 Use valid file link\n"
            "🔗 Format: /start get_xxxxx"
        )
        return

    code = args[1].replace("get_", "")
    files = load_files()

    if code not in files:
        main_bot.send_message(m.chat.id, "❌ Invalid link!")
        return

    if not joined_all(m.from_user.id):
        btn = types.InlineKeyboardMarkup()
        channels = load_channels()
        
        if not channels:
            send_file_to_user(m.chat.id, files[code])
            return
        
        channel_added = False
        for ch in channels:
            if ch == STORAGE_CHANNEL:
                continue
                
            try:
                chat_info = main_bot.get_chat(int(ch))
                channel_name = chat_info.title if hasattr(chat_info, 'title') else "Join"
                
                if hasattr(chat_info, 'username') and chat_info.username:
                    link = f"https://t.me/{chat_info.username}"
                else:
                    channel_id_clean = str(ch).replace('-100', '')
                    link = f"https://t.me/c/{channel_id_clean}/1"
                
                btn.add(types.InlineKeyboardButton(f"📢 {channel_name}", url=link))
                channel_added = True
                
            except Exception as e:
                print(f"Channel error {ch}: {e}")
                try:
                    channel_id_clean = str(ch).replace('-100', '')
                    link = f"https://t.me/c/{channel_id_clean}/1"
                    btn.add(types.InlineKeyboardButton("📢 Join", url=link))
                    channel_added = True
                except:
                    pass
        
        if not channel_added:
            send_file_to_user(m.chat.id, files[code])
            return
        
        btn.add(types.InlineKeyboardButton("✅ Verify", callback_data=f"verify_{code}"))
        
        main_bot.send_message(
            m.chat.id,
            "🔒 <b>Join channels first!</b>\n\n"
            "👇 Click and join\n"
            "✅ Then verify",
            reply_markup=btn
        )
        return

    send_file_to_user(m.chat.id, files[code])

def send_file_to_user(chat_id, file_data):
    try:
        main_bot.forward_message(chat_id, STORAGE_CHANNEL, file_data["message_id"])
        print(f"✅ Sent to {chat_id}")
    except Exception as e:
        main_bot.send_message(chat_id, f"❌ Error: {e}\n\nContact admin!")
        print(f"Send error: {e}")

@main_bot.callback_query_handler(func=lambda call: call.data.startswith("verify_"))
def verify_callback(call):
    code = call.data.replace("verify_", "")
    files = load_files()
    
    if code not in files:
        main_bot.answer_callback_query(call.id, "❌ Invalid!", show_alert=True)
        return
    
    if joined_all(call.from_user.id):
        main_bot.answer_callback_query(call.id, "✅ Verified!")
        try:
            main_bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        send_file_to_user(call.message.chat.id, files[code])
    else:
        main_bot.answer_callback_query(call.id, "❌ Join first!", show_alert=True)

# ================= RUN =================
def run_main_bot():
    print("🤖 Main Bot Started!")
    try:
        main_bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Main error: {e}")

def run_admin_bot():
    print("👨‍💼 Admin Bot Started!")
    try:
        admin_bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Admin error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Starting...")
    print("=" * 50)
    print(f"📱 Admin: {ADMIN_ID}")
    print(f"📦 Storage: {STORAGE_CHANNEL}")
    print("=" * 50)
    
    main_thread = threading.Thread(target=run_main_bot, daemon=True)
    admin_thread = threading.Thread(target=run_admin_bot, daemon=True)
    
    main_thread.start()
    admin_thread.start()
    
    print("✅ Running!")
    print("⚠️  Dono bots admin hone chahiye storage channel mein!")
    print("Ctrl+C to stop")
    
    try:
        main_thread.join()
        admin_thread.join()
    except KeyboardInterrupt:
        print("\n🛑 Stopped")
