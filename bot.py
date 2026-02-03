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
        "/files - List all uploaded files\n\n"
        "/help - Show this message"
    )

@admin_bot.message_handler(commands=["help"])
def admin_help(m):
    if m.from_user.id != ADMIN_ID:
        admin_bot.reply_to(m, "❌ You are not authorized!")
        return
    
    help_text = """
<b>🤖 Admin Bot Commands:</b>

<b>Channel Management:</b>
/addchannel -100xxxxxxxx - Add force subscribe channel
/removechannel -100xxxxxxxx - Remove channel
/channels - List all channels

<b>File Management:</b>
/upload - Upload file and get shareable link
/files - List all uploaded files

<b>📝 How to get Channel ID:</b>
1. Forward any message from your channel to @userinfobot
2. Bot will show you the channel ID (starts with -100)
3. Use that ID in /addchannel command
"""
    admin_bot.send_message(m.chat.id, help_text)

@admin_bot.message_handler(commands=["addchannel"])
def add_channel(m):
    if m.from_user.id != ADMIN_ID:
        admin_bot.reply_to(m, "❌ You are not authorized!")
        return
    try:
        ch_id = m.text.split()[1]
        data = load_channels()
        data[ch_id] = "added"
        save_channels(data)
        admin_bot.reply_to(m, f"✅ Channel added: <code>{ch_id}</code>")
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
            admin_bot.reply_to(m, "❌ Channel not found in database")
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
        admin_bot.reply_to(m, "📭 No channels added yet")
        return
    txt = "<b>📢 Active Channels:</b>\n\n"
    for i, ch in enumerate(data, 1):
        txt += f"{i}. <code>{ch}</code>\n"
    admin_bot.send_message(m.chat.id, txt)

@admin_bot.message_handler(commands=["upload"])
def upload(m):
    if m.from_user.id == ADMIN_ID:
        admin_bot.reply_to(m, "📤 Send your file now (document/video/photo/audio)")
    else:
        admin_bot.reply_to(m, "❌ You are not authorized!")

@admin_bot.message_handler(commands=["files"])
def list_files(m):
    if m.from_user.id != ADMIN_ID:
        admin_bot.reply_to(m, "❌ You are not authorized!")
        return
    
    files = load_files()
    if not files:
        admin_bot.reply_to(m, "📭 No files uploaded yet")
        return
    
    main_bot_username = main_bot.get_me().username
    txt = "<b>📁 Uploaded Files:</b>\n\n"
    for i, (code, data) in enumerate(files.items(), 1):
        link = f"https://t.me/{main_bot_username}?start=get_{code}"
        txt += f"{i}. Code: <code>{code}</code>\n   Type: {data['type']}\n   Link: {link}\n\n"
    
    admin_bot.send_message(m.chat.id, txt)

@admin_bot.message_handler(content_types=["document", "video", "photo", "audio"])
def save_file(m):
    if m.from_user.id != ADMIN_ID:
        return

    files = load_files()
    code = gen_code()

    if m.content_type == "document":
        fid = m.document.file_id
    elif m.content_type == "video":
        fid = m.video.file_id
    elif m.content_type == "audio":
        fid = m.audio.file_id
    else:
        fid = m.photo[-1].file_id

    files[code] = {
        "file_id": fid,
        "type": m.content_type
    }

    save_files(files)

    main_bot_username = main_bot.get_me().username
    link = f"https://t.me/{main_bot_username}?start=get_{code}"

    admin_bot.reply_to(
        m,
        f"✅ <b>File Saved Successfully!</b>\n\n"
        f"📋 <b>Code:</b> <code>{code}</code>\n"
        f"📦 <b>Type:</b> {m.content_type}\n"
        f"🔗 <b>Share Link:</b>\n<code>{link}</code>\n\n"
        f"Users can get this file from Main Bot!"
    )

# ================= MAIN BOT COMMANDS =================
@main_bot.message_handler(commands=["start"])
def main_start(m):
    args = m.text.split()

    # Normal start command
    if len(args) < 2 or not args[1].startswith("get_"):
        main_bot.send_message(
            m.chat.id,
            "👋 <b>Welcome to File Share Bot!</b>\n\n"
            "📎 To get files, use a valid file link\n"
            "🔗 Format: /start get_xxxxx"
        )
        return

    # File request
    code = args[1].replace("get_", "")
    files = load_files()

    if code not in files:
        main_bot.send_message(m.chat.id, "❌ Invalid or expired file link!")
        return

    # Check if user joined all channels
    if not joined_all(m.from_user.id):
        btn = types.InlineKeyboardMarkup()
        channels = load_channels()
        
        for ch in channels:
            try:
                # Get channel info
                chat_info = main_bot.get_chat(int(ch))
                channel_name = chat_info.title if hasattr(chat_info, 'title') else f"Channel {ch}"
                
                # Create invite link
                if chat_info.username:
                    link = f"https://t.me/{chat_info.username}"
                else:
                    link = f"https://t.me/c/{str(ch)[4:]}"
                
                btn.add(types.InlineKeyboardButton(f"📢 {channel_name}", url=link))
            except Exception as e:
                print(f"Error getting channel info: {e}")
                continue
        
        # Add verification button
        btn.add(types.InlineKeyboardButton("✅ Verify Membership", callback_data=f"verify_{code}"))
        
        main_bot.send_message(
            m.chat.id,
            "🔒 <b>Join all channels to access the file!</b>\n\n"
            "Click all channel buttons above and join them.\n"
            "Then click 'Verify Membership' button.",
            reply_markup=btn
        )
        return

    # Send file
    send_file_to_user(m.chat.id, files[code])

def send_file_to_user(chat_id, file_data):
    try:
        if file_data["type"] == "document":
            main_bot.send_document(chat_id, file_data["file_id"], caption="✅ Here's your file!")
        elif file_data["type"] == "video":
            main_bot.send_video(chat_id, file_data["file_id"], caption="✅ Here's your video!")
        elif file_data["type"] == "audio":
            main_bot.send_audio(chat_id, file_data["file_id"], caption="✅ Here's your audio!")
        else:
            main_bot.send_photo(chat_id, file_data["file_id"], caption="✅ Here's your photo!")
    except Exception as e:
        main_bot.send_message(chat_id, f"❌ Error sending file: {e}")

# ================= MAIN BOT CALLBACK HANDLER =================
@main_bot.callback_query_handler(func=lambda call: call.data.startswith("verify_"))
def verify_callback(call):
    code = call.data.replace("verify_", "")
    files = load_files()
    
    if code not in files:
        main_bot.answer_callback_query(call.id, "❌ Invalid file link!", show_alert=True)
        return
    
    if joined_all(call.from_user.id):
        main_bot.answer_callback_query(call.id, "✅ Verified! Sending file...")
        main_bot.delete_message(call.message.chat.id, call.message.message_id)
        send_file_to_user(call.message.chat.id, files[code])
    else:
        main_bot.answer_callback_query(call.id, "❌ Please join all channels first!", show_alert=True)

# ================= RUN BOTH BOTS =================
def run_main_bot():
    print("🤖 Main Bot Started!")
    main_bot.infinity_polling()

def run_admin_bot():
    print("👨‍💼 Admin Bot Started!")
    admin_bot.infinity_polling()

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Starting Both Bots...")
    print("=" * 50)
    print(f"📱 Admin ID: {ADMIN_ID}")
    print(f"🤖 Main Bot Token: {MAIN_BOT_TOKEN[:20]}...")
    print(f"👨‍💼 Admin Bot Token: {ADMIN_BOT_TOKEN[:20]}...")
    print("=" * 50)
    
    # Run both bots in separate threads
    main_thread = threading.Thread(target=run_main_bot)
    admin_thread = threading.Thread(target=run_admin_bot)
    
    main_thread.start()
    admin_thread.start()
    
    main_thread.join()
    admin_thread.join()
