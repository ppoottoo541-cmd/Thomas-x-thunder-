#!/usr/bin/env python3
"""
FILE SHARING BOT - COMPLETE SYSTEM
Admin uploads file → Gets link
User joins channels → Gets file
"""

import telebot
from telebot import types
import json
import os
import random
import string
import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================
# CONFIGURATION - YOUR TOKENS
# ============================================

MAIN_BOT_TOKEN = "8580329271:AAFPmbJ9JraVIAkHbcZtQ5tohIDwWHvjx3I"
ADMIN_BOT_TOKEN = "8553759431:AAH4BgRJcm1-JI5oBDoYIxR3Vby7oUmJgZQ"
ADMIN_ID = 7417241499

# Storage channel (Create private channel, add both bots as admin)
# Get channel ID by forwarding message to @username_to_id_bot
STORAGE_CHANNEL = -1001234567890  # EDIT THIS - Your storage channel ID

# ============================================
# INITIALIZATION
# ============================================

CHANNELS_FILE = "channels.json"
FILES_FILE = "files.json"

main_bot = telebot.TeleBot(MAIN_BOT_TOKEN, parse_mode="HTML")
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN, parse_mode="HTML")

# Create files if not exist
for file in [CHANNELS_FILE, FILES_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)

# ============================================
# DATABASE FUNCTIONS
# ============================================

def load_json(file):
    with open(file) as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def gen_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# ============================================
# CHANNEL MANAGEMENT
# ============================================

def parse_channel(text):
    """Parse channel from any format"""
    text = text.strip()
    
    # Direct ID
    if text.startswith("-100"):
        try:
            chat = main_bot.get_chat(text)
            return {
                'id': str(chat.id),
                'name': chat.title if hasattr(chat, 'title') else 'Channel',
                'username': chat.username if hasattr(chat, 'username') else None,
                'type': 'id'
            }
        except:
            return None
    
    # @username
    if text.startswith("@"):
        try:
            chat = main_bot.get_chat(text)
            return {
                'id': str(chat.id),
                'name': chat.title if hasattr(chat, 'title') else text,
                'username': text[1:],
                'type': 'username'
            }
        except:
            return None
    
    # Link: https://t.me/username
    if 't.me/' in text and '+' not in text and 'joinchat' not in text:
        username = text.split('t.me/')[-1].strip('/')
        try:
            chat = main_bot.get_chat(f"@{username}")
            return {
                'id': str(chat.id),
                'name': chat.title if hasattr(chat, 'title') else username,
                'username': username,
                'type': 'public_link'
            }
        except:
            return None
    
    # Private link
    if 't.me/+' in text or 't.me/joinchat/' in text:
        return {
            'id': text,  # Use link as ID
            'name': 'Private Channel',
            'username': None,
            'type': 'private_link'
        }
    
    return None

def get_channel_link(channel_data):
    """Get join link"""
    if channel_data['type'] == 'private_link':
        return channel_data['id']
    
    if channel_data.get('username'):
        return f"https://t.me/{channel_data['username']}"
    
    try:
        link = main_bot.export_chat_invite_link(channel_data['id'])
        return link
    except:
        ch_id = channel_data['id'].replace('-100', '')
        return f"https://t.me/c/{ch_id}/1"

def check_membership(user_id, channel_id):
    """Check if user is member"""
    try:
        if channel_id.startswith('http'):
            return False
        
        member = main_bot.get_chat_member(channel_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def all_channels_joined(user_id):
    """Check all channels"""
    channels = load_json(CHANNELS_FILE)
    
    if not channels:
        return True
    
    for ch_id in channels:
        if not check_membership(user_id, ch_id):
            return False
    
    return True

# ============================================
# ADMIN BOT COMMANDS
# ============================================

@admin_bot.message_handler(commands=['start'])
def admin_start(msg):
    if msg.from_user.id != ADMIN_ID:
        admin_bot.reply_to(msg, "❌ Unauthorized!")
        return
    
    channels = load_json(CHANNELS_FILE)
    files = load_json(FILES_FILE)
    
    admin_bot.send_message(
        msg.chat.id,
        f"🔐 <b>ADMIN PANEL</b>\n\n"
        f"📊 <b>Statistics:</b>\n"
        f"📢 Channels: {len(channels)}\n"
        f"📁 Files: {len(files)}\n\n"
        f"<b>Commands:</b>\n\n"
        f"<b>📢 Channels:</b>\n"
        f"/addchannel - Add force subscribe\n"
        f"/channels - List all\n"
        f"/delchannel - Remove channel\n\n"
        f"<b>📁 Files:</b>\n"
        f"/upload - Upload file\n"
        f"/files - List files\n"
        f"/delfile - Delete file\n\n"
        f"❓ /help - Detailed help"
    )

@admin_bot.message_handler(commands=['help'])
def admin_help(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    admin_bot.send_message(
        msg.chat.id,
        f"📚 <b>HELP GUIDE</b>\n\n"
        f"<b>1️⃣ Add Channel:</b>\n"
        f"<code>/addchannel channel_link</code>\n\n"
        f"<b>Examples:</b>\n"
        f"• <code>/addchannel -1001234567890</code>\n"
        f"• <code>/addchannel @channelname</code>\n"
        f"• <code>/addchannel https://t.me/channel</code>\n"
        f"• <code>/addchannel https://t.me/+hash</code>\n\n"
        f"<b>2️⃣ Upload File:</b>\n"
        f"<code>/upload</code>\n"
        f"Send any file → Get link!\n\n"
        f"<b>3️⃣ Share Link:</b>\n"
        f"Users must join channels → Verify → Get file!\n\n"
        f"<b>⚙️ Setup:</b>\n"
        f"1. Create private channel\n"
        f"2. Add both bots as admin\n"
        f"3. Get channel ID: @username_to_id_bot\n"
        f"4. Edit STORAGE_CHANNEL in code\n"
        f"5. Add force channels\n"
        f"6. Upload files!"
    )

@admin_bot.message_handler(commands=['addchannel'])
def add_channel(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = msg.text.split(maxsplit=1)
        
        if len(parts) < 2:
            admin_bot.reply_to(
                msg,
                "❌ <b>Usage:</b>\n"
                "<code>/addchannel channel_link</code>\n\n"
                "<b>Examples:</b>\n"
                "• <code>/addchannel -1001234567890</code>\n"
                "• <code>/addchannel @channel</code>\n"
                "• <code>/addchannel https://t.me/channel</code>"
            )
            return
        
        channel_input = parts[1].strip()
        channel_data = parse_channel(channel_input)
        
        if not channel_data:
            admin_bot.reply_to(msg, "❌ Invalid channel! Check format.")
            return
        
        # Save
        channels = load_json(CHANNELS_FILE)
        channels[channel_data['id']] = channel_data
        save_json(CHANNELS_FILE, channels)
        
        link = get_channel_link(channel_data)
        
        admin_bot.reply_to(
            msg,
            f"✅ <b>Channel Added!</b>\n\n"
            f"📢 <b>Name:</b> {channel_data['name']}\n"
            f"🆔 <b>ID:</b> <code>{channel_data['id']}</code>\n"
            f"🔗 <b>Link:</b> {link}\n"
            f"📊 <b>Type:</b> {channel_data['type']}\n\n"
            f"⚠️ Make Main Bot admin in this channel!"
        )
        
        logger.info(f"Channel added: {channel_data['name']}")
    
    except Exception as e:
        admin_bot.reply_to(msg, f"❌ Error: {str(e)}")
        logger.error(f"Add channel error: {e}")

@admin_bot.message_handler(commands=['channels'])
def list_channels(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    channels = load_json(CHANNELS_FILE)
    
    if not channels:
        admin_bot.send_message(
            msg.chat.id,
            "📭 <b>No channels!</b>\n\n"
            "Add channel:\n"
            "<code>/addchannel @channel</code>"
        )
        return
    
    text = f"📢 <b>FORCE SUBSCRIBE CHANNELS</b>\n\n"
    text += f"Total: {len(channels)}\n\n"
    
    for i, (ch_id, ch_data) in enumerate(channels.items(), 1):
        link = get_channel_link(ch_data)
        text += (
            f"{i}. <b>{ch_data['name']}</b>\n"
            f"   🆔 <code>{ch_id}</code>\n"
            f"   🔗 {link}\n\n"
        )
    
    text += f"<b>Remove:</b> <code>/delchannel channel_id</code>"
    
    admin_bot.send_message(msg.chat.id, text, disable_web_page_preview=True)

@admin_bot.message_handler(commands=['delchannel'])
def del_channel(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = msg.text.split(maxsplit=1)
        
        if len(parts) < 2:
            admin_bot.reply_to(
                msg,
                "❌ <b>Usage:</b>\n"
                "<code>/delchannel channel_id</code>\n\n"
                "Get ID from /channels"
            )
            return
        
        ch_id = parts[1].strip()
        channels = load_json(CHANNELS_FILE)
        
        if ch_id in channels:
            ch_name = channels[ch_id]['name']
            del channels[ch_id]
            save_json(CHANNELS_FILE, channels)
            
            admin_bot.reply_to(
                msg,
                f"🗑️ <b>Removed!</b>\n\n"
                f"📢 {ch_name}\n"
                f"🆔 <code>{ch_id}</code>"
            )
            logger.info(f"Channel removed: {ch_name}")
        else:
            admin_bot.reply_to(msg, "❌ Channel not found!")
    
    except Exception as e:
        admin_bot.reply_to(msg, f"❌ Error: {str(e)}")

@admin_bot.message_handler(commands=['upload'])
def upload_prompt(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    admin_bot.send_message(
        msg.chat.id,
        "📤 <b>Upload File</b>\n\n"
        "Send file now:\n"
        "• Document\n"
        "• Video\n"
        "• Photo\n"
        "• Audio\n\n"
        "You'll get shareable link!"
    )

@admin_bot.message_handler(content_types=['document', 'video', 'photo', 'audio'])
def handle_file_upload(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    try:
        code = gen_code()
        
        # Get file info
        if msg.content_type == 'document':
            file_name = msg.document.file_name or "Document"
        elif msg.content_type == 'video':
            file_name = "Video File"
        elif msg.content_type == 'photo':
            file_name = "Photo"
        else:
            file_name = "Audio File"
        
        # Copy to storage
        sent = admin_bot.copy_message(
            chat_id=STORAGE_CHANNEL,
            from_chat_id=msg.chat.id,
            message_id=msg.message_id
        )
        
        # Save to database
        files = load_json(FILES_FILE)
        files[code] = {
            'message_id': sent.message_id,
            'type': msg.content_type,
            'name': file_name
        }
        save_json(FILES_FILE, files)
        
        # Generate link
        bot_username = main_bot.get_me().username
        file_link = f"https://t.me/{bot_username}?start={code}"
        
        admin_bot.reply_to(
            msg,
            f"✅ <b>File Uploaded!</b>\n\n"
            f"📁 <b>Name:</b> {file_name}\n"
            f"📋 <b>Code:</b> <code>{code}</code>\n"
            f"📦 <b>Type:</b> {msg.content_type}\n\n"
            f"🔗 <b>Share Link:</b>\n"
            f"<code>{file_link}</code>",
            disable_web_page_preview=True
        )
        
        logger.info(f"File uploaded: {file_name} [{code}]")
    
    except Exception as e:
        admin_bot.reply_to(
            msg,
            f"❌ Error uploading!\n\n"
            f"Details: {str(e)}\n\n"
            f"Check:\n"
            f"• Both bots admin in storage channel?\n"
            f"• Storage channel ID correct?"
        )
        logger.error(f"Upload error: {e}")

@admin_bot.message_handler(commands=['files'])
def list_files(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    files = load_json(FILES_FILE)
    
    if not files:
        admin_bot.send_message(
            msg.chat.id,
            "📭 <b>No files!</b>\n\n"
            "Upload file:\n"
            "<code>/upload</code>"
        )
        return
    
    bot_username = main_bot.get_me().username
    text = f"📁 <b>FILES ({len(files)})</b>\n\n"
    
    for i, (code, data) in enumerate(files.items(), 1):
        link = f"https://t.me/{bot_username}?start={code}"
        text += (
            f"{i}. <b>{data['name']}</b>\n"
            f"   📋 <code>{code}</code>\n"
            f"   📦 {data['type']}\n"
            f"   🔗 <code>{link}</code>\n\n"
        )
        
        if len(text) > 3500:
            admin_bot.send_message(msg.chat.id, text, disable_web_page_preview=True)
            text = ""
    
    if text:
        admin_bot.send_message(msg.chat.id, text, disable_web_page_preview=True)

@admin_bot.message_handler(commands=['delfile'])
def del_file(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = msg.text.split(maxsplit=1)
        
        if len(parts) < 2:
            admin_bot.reply_to(
                msg,
                "❌ <b>Usage:</b>\n"
                "<code>/delfile file_code</code>\n\n"
                "Get code from /files"
            )
            return
        
        code = parts[1].strip()
        files = load_json(FILES_FILE)
        
        if code in files:
            file_name = files[code]['name']
            del files[code]
            save_json(FILES_FILE, files)
            
            admin_bot.reply_to(
                msg,
                f"🗑️ <b>Deleted!</b>\n\n"
                f"📁 {file_name}\n"
                f"📋 <code>{code}</code>"
            )
            logger.info(f"File deleted: {file_name}")
        else:
            admin_bot.reply_to(msg, "❌ File not found!")
    
    except Exception as e:
        admin_bot.reply_to(msg, f"❌ Error: {str(e)}")

@admin_bot.message_handler(commands=['stats'])
def admin_stats(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    channels = load_json(CHANNELS_FILE)
    files = load_json(FILES_FILE)
    
    admin_bot.send_message(
        msg.chat.id,
        f"📊 <b>BOT STATISTICS</b>\n\n"
        f"📢 Force Channels: {len(channels)}\n"
        f"📁 Uploaded Files: {len(files)}\n"
        f"🤖 Status: Running\n\n"
        f"<b>Commands:</b>\n"
        f"/channels - View channels\n"
        f"/files - View files"
    )

# ============================================
# MAIN BOT (USER-FACING)
# ============================================

@main_bot.message_handler(commands=['start'])
def main_start(msg):
    args = msg.text.split()
    
    # No file code
    if len(args) == 1:
        main_bot.send_message(
            msg.chat.id,
            "👋 <b>Welcome!</b>\n\n"
            "📎 To access files, use valid link\n\n"
            "Format:\n"
            "<code>/start FILE_CODE</code>"
        )
        return
    
    code = args[1].strip()
    files = load_json(FILES_FILE)
    
    if code not in files:
        main_bot.send_message(msg.chat.id, "❌ <b>Invalid or expired link!</b>")
        return
    
    file_data = files[code]
    
    # Check membership
    if all_channels_joined(msg.from_user.id):
        send_file(msg.chat.id, file_data)
    else:
        show_join_screen(msg, code, file_data)

def show_join_screen(msg, code, file_data):
    """Show channels to join"""
    channels = load_json(CHANNELS_FILE)
    
    if not channels:
        send_file(msg.chat.id, file_data)
        return
    
    # Create buttons
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for ch_id, ch_data in channels.items():
        link = get_channel_link(ch_data)
        btn = types.InlineKeyboardButton(
            text=f"📢 Join {ch_data['name']}",
            url=link
        )
        markup.add(btn)
    
    # Verify button
    verify_btn = types.InlineKeyboardButton(
        text="✅ Joined All, Verify Now!",
        callback_data=f"verify_{code}"
    )
    markup.add(verify_btn)
    
    main_bot.send_message(
        msg.chat.id,
        f"🔒 <b>Access Restricted!</b>\n\n"
        f"📁 <b>File:</b> {file_data['name']}\n\n"
        f"<b>To get this file:</b>\n"
        f"1️⃣ Join ALL channels below\n"
        f"2️⃣ Click 'Verify' button\n"
        f"3️⃣ Get your file!\n\n"
        f"👇 <b>Join these channels:</b>",
        reply_markup=markup
    )

@main_bot.callback_query_handler(func=lambda call: call.data.startswith('verify_'))
def verify_join(call):
    """Verify membership"""
    code = call.data.replace('verify_', '')
    files = load_json(FILES_FILE)
    
    if code not in files:
        main_bot.answer_callback_query(call.id, "❌ Invalid link!", show_alert=True)
        return
    
    if all_channels_joined(call.from_user.id):
        main_bot.answer_callback_query(call.id, "✅ Verified! Sending...", show_alert=False)
        
        # Delete join message
        try:
            main_bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        
        send_file(call.message.chat.id, files[code])
    else:
        main_bot.answer_callback_query(
            call.id,
            "❌ Please join ALL channels!\n\nClick buttons above.",
            show_alert=True
        )

def send_file(chat_id, file_data):
    """Send file to user"""
    try:
        main_bot.copy_message(
            chat_id=chat_id,
            from_chat_id=STORAGE_CHANNEL,
            message_id=file_data['message_id'],
            caption=f"✅ <b>Here's your file!</b>\n\n📁 {file_data['name']}"
        )
        logger.info(f"File sent to {chat_id}: {file_data['name']}")
    except Exception as e:
        main_bot.send_message(
            chat_id,
            "❌ <b>Error sending file!</b>\n\nContact admin."
        )
        logger.error(f"Send file error: {e}")

# ============================================
# RUN BOTS
# ============================================

def run_main():
    logger.info("🤖 Main Bot starting...")
    while True:
        try:
            main_bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Main Bot error: {e}")
            time.sleep(5)

def run_admin():
    logger.info("⚙️ Admin Bot starting...")
    while True:
        try:
            admin_bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Admin Bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 FILE SHARING BOT")
    print("=" * 60)
    print(f"👤 Admin ID: {ADMIN_ID}")
    print(f"📦 Storage: {STORAGE_CHANNEL}")
    print("=" * 60)
    
    main_thread = threading.Thread(target=run_main, daemon=True)
    admin_thread = threading.Thread(target=run_admin, daemon=True)
    
    main_thread.start()
    admin_thread.start()
    
    print("✅ Bots running!\n")
    print("📋 SETUP CHECKLIST:")
    print("1. ✅ Create private channel")
    print("2. ✅ Add both bots as admin")
    print("3. ✅ Edit STORAGE_CHANNEL in code")
    print("4. ✅ Add force channels: /addchannel")
    print("5. ✅ Upload files: /upload\n")
    print("💡 Ctrl+C to stop\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Bots stopped!\n")
