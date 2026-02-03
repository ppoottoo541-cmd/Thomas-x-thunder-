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

# Storage channel - Files yaha save hongi (private rakho, users ko dikhegi nahi)
# Dono bots ko is channel mein ADMIN banana ZARURI hai
STORAGE_CHANNEL = -1003855834042  # Integer format (without quotes)

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

# ================= JOIN CHECK =================
def joined_all(user_id):
    channels = load_channels()
    if not channels:
        return True  # No force subscribe channels
    
    for ch_id in channels:
        try:
            status = main_bot.get_chat_member(int(ch_id), user_id).status
            if status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            print(f"❌ Error checking {ch_id}: {e}")
            return False
    return True

# ================= ADMIN BOT COMMANDS =================
@admin_bot.message_handler(commands=["start"])
def admin_start(m):
    if m.from_user.id != ADMIN_ID:
        admin_bot.reply_to(m, "❌ Not authorized!")
        return
    
    admin_bot.send_message(
        m.chat.id,
        "<b>🤖 Admin Panel</b>\n\n"
        "<b>📢 Channels:</b>\n"
        "/addchannel -100xxxxx\n"
        "/removechannel -100xxxxx\n"
        "/channels\n\n"
        "<b>📤 Files:</b>\n"
        "/upload\n"
        "/files\n"
        "/deletefile CODE\n\n"
        "/help"
    )

@admin_bot.message_handler(commands=["help"])
def admin_help(m):
    if m.from_user.id != ADMIN_ID:
        return
    
    help_text = f"""
<b>🤖 Commands:</b>

<b>Channels:</b>
/addchannel -100xxxxx
/removechannel -100xxxxx
/channels

<b>Files:</b>
/upload
/files
/deletefile CODE

<b>⚙️ Setup:</b>
1. Storage channel: <code>{STORAGE_CHANNEL}</code>
2. Dono bots ko storage channel mein admin banao
3. Force subscribe channels alag se /addchannel se add karo

<b>📝 Channel ID kaise nikale:</b>
Message forward karo channel se @userinfobot ko
"""
    admin_bot.send_message(m.chat.id, help_text)

@admin_bot.message_handler(commands=["addchannel"])
def add_channel(m):
    if m.from_user.id != ADMIN_ID:
        return
    try:
        ch_id = m.text.split()[1]
        
        if not ch_id.startswith("-100"):
            admin_bot.reply_to(m, "❌ ID must start with -100")
            return
        
        data = load_channels()
        data[ch_id] = "force_subscribe"
        save_channels(data)
        
        admin_bot.reply_to(m, f"✅ Added: <code>{ch_id}</code>\n\nMain Bot ko admin banao!")
    except IndexError:
        admin_bot.reply_to(m, "❌ Use: /addchannel -100xxxxx")
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(commands=["removechannel"])
def remove_channel(m):
    if m.from_user.id != ADMIN_ID:
        return
    try:
        ch_id = m.text.split()[1]
        data = load_channels()
        if ch_id in data:
            data.pop(ch_id)
            save_channels(data)
            admin_bot.reply_to(m, f"🗑 Removed: <code>{ch_id}</code>")
        else:
            admin_bot.reply_to(m, "❌ Not found")
    except IndexError:
        admin_bot.reply_to(m, "❌ Use: /removechannel -100xxxxx")
    except Exception as e:
        admin_bot.reply_to(m, f"❌ {e}")

@admin_bot.message_handler(commands=["channels"])
def list_channels(m):
    if m.from_user.id != ADMIN_ID:
        return
    
    data = load_channels()
    txt = f"<b>📢 Force Subscribe Channels:</b>\n\n"
    
    if not data:
        txt += "No channels added\n\n"
    else:
        for i, ch in enumerate(data, 1):
            txt += f"{i}. <code>{ch}</code>\n"
    
    txt += f"\n<b>⚙️ Storage:</b> <code>{STORAGE_CHANNEL}</code>"
    admin_bot.send_message(m.chat.id, txt)

@admin_bot.message_handler(commands=["upload"])
def upload(m):
    if m.from_user.id == ADMIN_ID:
        admin_bot.reply_to(m, "📤 Send file now")
    else:
        admin_bot.reply_to(m, "❌ Not authorized!")

@admin_bot.message_handler(commands=["files"])
def list_files(m):
    if m.from_user.id != ADMIN_ID:
        return
    
    files = load_files()
    if not files:
        admin_bot.reply_to(m, "📭 No files\n\nUse /upload")
        return
    
    try:
        main_bot_username = main_bot.get_me().username
        txt = "<b>📁 Files:</b>\n\n"
        for i, (code, data) in enumerate(files.items(), 1):
            link = f"https://t.me/{main_bot_username}?start=get_{code}"
            txt += f"{i}. <code>{code}</code> ({data['type']})\n{link}\n\n"
        admin_bot.send_message(m.chat.id, txt, disable_web_page_preview=True)
    except Exception as e:
        admin_bot.reply_to(m, f"❌ {e}")

@admin_bot.message_handler(commands=["deletefile"])
def delete_file(m):
    if m.from_user.id != ADMIN_ID:
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
        admin_bot.reply_to(m, f"❌ {e}")

@admin_bot.message_handler(content_types=["document", "video", "photo", "audio"])
def save_file(m):
    if m.from_user.id != ADMIN_ID:
        return

    try:
        files = load_files()
        code = gen_code()

        # Copy file to storage channel (NOT forward, so it won't show in channel)
        if m.content_type == "document":
            sent = admin_bot.send_document(STORAGE_CHANNEL, m.document.file_id)
            msg_id = sent.message_id
        elif m.content_type == "video":
            sent = admin_bot.send_video(STORAGE_CHANNEL, m.video.file_id)
            msg_id = sent.message_id
        elif m.content_type == "audio":
            sent = admin_bot.send_audio(STORAGE_CHANNEL, m.audio.file_id)
            msg_id = sent.message_id
        else:  # photo
            sent = admin_bot.send_photo(STORAGE_CHANNEL, m.photo[-1].file_id)
            msg_id = sent.message_id

        files[code] = {
            "message_id": msg_id,
            "type": m.content_type
        }

        save_files(files)

        main_bot_username = main_bot.get_me().username
        link = f"https://t.me/{main_bot_username}?start=get_{code}"

        admin_bot.reply_to(
            m,
            f"✅ <b>Saved!</b>\n\n"
            f"📋 <code>{code}</code>\n"
            f"📦 {m.content_type}\n\n"
            f"🔗 Link:\n<code>{link}</code>",
            disable_web_page_preview=True
        )
        
        # Delete from storage channel to keep it clean
        try:
            admin_bot.delete_message(STORAGE_CHANNEL, msg_id)
            print(f"✅ File saved and deleted from channel view")
        except:
            print(f"⚠️ Could not delete message from storage channel")
            
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}\n\nCheck: Dono bots admin hain storage channel mein?")
        print(f"❌ Save error: {e}")

# ================= MAIN BOT =================
@main_bot.message_handler(commands=["start"])
def main_start(m):
    args = m.text.split()

    if len(args) < 2 or not args[1].startswith("get_"):
        main_bot.send_message(
            m.chat.id,
            "👋 <b>Welcome!</b>\n\n"
            "📎 Use valid file link\n"
            "🔗 /start get_xxxxx"
        )
        return

    code = args[1].replace("get_", "")
    files = load_files()

    if code not in files:
        main_bot.send_message(m.chat.id, "❌ Invalid or expired link!")
        return

    # Check force subscribe
    if not joined_all(m.from_user.id):
        btn = types.InlineKeyboardMarkup()
        channels = load_channels()
        
        if not channels:
            # No force subscribe, directly send file
            send_file_to_user(m.chat.id, files[code])
            return
        
        # Add channel buttons
        for ch in channels:
            try:
                chat_info = main_bot.get_chat(int(ch))
                ch_name = chat_info.title if hasattr(chat_info, 'title') else "Join Channel"
                
                if hasattr(chat_info, 'username') and chat_info.username:
                    ch_link = f"https://t.me/{chat_info.username}"
                else:
                    ch_link = f"https://t.me/c/{str(ch).replace('-100', '')}/1"
                
                btn.add(types.InlineKeyboardButton(f"📢 {ch_name}", url=ch_link))
                
            except Exception as e:
                print(f"❌ Error with channel {ch}: {e}")
                ch_link = f"https://t.me/c/{str(ch).replace('-100', '')}/1"
                btn.add(types.InlineKeyboardButton("📢 Join Channel", url=ch_link))
        
        # Verify button
        btn.add(types.InlineKeyboardButton("✅ Joined, Verify Now", callback_data=f"verify_{code}"))
        
        main_bot.send_message(
            m.chat.id,
            "🔒 <b>Join all channels first!</b>\n\n"
            "👇 Click buttons below to join\n"
            "✅ Then click verify",
            reply_markup=btn
        )
        return

    # User joined all, send file
    send_file_to_user(m.chat.id, files[code])

def send_file_to_user(chat_id, file_data):
    try:
        # Copy file from storage (not forward, so cleaner)
        main_bot.copy_message(
            chat_id, 
            STORAGE_CHANNEL, 
            file_data["message_id"],
            caption="✅ Here's your file!"
        )
        print(f"✅ File sent to {chat_id}")
    except Exception as e:
        main_bot.send_message(chat_id, f"❌ Error sending file\n\nContact admin!")
        print(f"❌ Send error: {e}")

@main_bot.callback_query_handler(func=lambda call: call.data.startswith("verify_"))
def verify_callback(call):
    code = call.data.replace("verify_", "")
    files = load_files()
    
    if code not in files:
        main_bot.answer_callback_query(call.id, "❌ Invalid link!", show_alert=True)
        return
    
    if joined_all(call.from_user.id):
        main_bot.answer_callback_query(call.id, "✅ Verified! Sending...")
        try:
            main_bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        send_file_to_user(call.message.chat.id, files[code])
    else:
        main_bot.answer_callback_query(call.id, "❌ Please join all channels first!", show_alert=True)

# ================= RUN BOTH BOTS =================
def run_main_bot():
    print("🤖 Main Bot Running")
    try:
        main_bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"❌ Main Bot Error: {e}")

def run_admin_bot():
    print("👨‍💼 Admin Bot Running")
    try:
        admin_bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"❌ Admin Bot Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 STARTING BOTS")
    print("=" * 60)
    print(f"👤 Admin: {ADMIN_ID}")
    print(f"📦 Storage: {STORAGE_CHANNEL}")
    print("=" * 60)
    
    main_thread = threading.Thread(target=run_main_bot, daemon=True)
    admin_thread = threading.Thread(target=run_admin_bot, daemon=True)
    
    main_thread.start()
    admin_thread.start()
    
    print("✅ Bots are running!")
    print("\n⚠️  IMPORTANT:")
    print("1. Dono bots ko storage channel mein admin banao")
    print("2. Force subscribe channels /addchannel se add karo")
    print("3. Main bot ko force subscribe channels mein admin banao")
    print("\n💡 Ctrl+C to stop\n")
    
    try:
        main_thread.join()
        admin_thread.join()
    except KeyboardInterrupt:
        print("\n\n🛑 Bots stopped!\n")
