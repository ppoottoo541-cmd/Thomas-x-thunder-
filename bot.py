#!/usr/bin/env python3
"""
COMPLETE FILE SHARING BOT WITH FORCE SUBSCRIBE
- Admin adds channels via link/username/ID
- User must join all channels first
- Then gets file access
"""

import telebot
from telebot import types
import json
import os
import random
import string
import threading
import re

# ============================================
# 🔧 CONFIGURATION - EDIT KARO
# ============================================

MAIN_BOT_TOKEN = "8580329271:AAFPmbJ9JraVIAkHbcZtQ5tohIDwWHvjx3I"
ADMIN_BOT_TOKEN = "8553759431:AAH4BgRJcm1-JI5oBDoYIxR3Vby7oUmJgZQ"
ADMIN_ID = 7417241499  # Your Telegram User ID

# Storage Channel (Files save hongi - Must be private)
# IMPORTANT: Dono bots ko admin banana
STORAGE_CHANNEL = -1001234567890

# ============================================
# INITIALIZATION
# ============================================

CHANNEL_DB = "channels.json"
FILE_DB = "files.json"

main_bot = telebot.TeleBot(MAIN_BOT_TOKEN, parse_mode="HTML")
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN, parse_mode="HTML")

# Initialize databases
if not os.path.exists(CHANNEL_DB):
    with open(CHANNEL_DB, "w") as f:
        json.dump({}, f)

if not os.path.exists(FILE_DB):
    with open(FILE_DB, "w") as f:
        json.dump({}, f)

# ============================================
# DATABASE FUNCTIONS
# ============================================

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
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# ============================================
# CHANNEL MANAGEMENT
# ============================================

def parse_channel_input(text):
    """
    Parse channel from any format:
    - ID: -1001234567890
    - Username: @channel or channelname
    - Public link: https://t.me/channel
    - Private link: https://t.me/+hash or https://t.me/joinchat/hash
    """
    text = text.strip()
    
    # Direct ID format
    if text.startswith("-100"):
        return get_channel_details(text)
    
    # @username format
    if text.startswith("@"):
        return get_channel_details(text)
    
    # Extract username from public link
    public_match = re.search(r't\.me/([a-zA-Z0-9_]+)$', text)
    if public_match:
        username = public_match.group(1)
        return get_channel_details(f"@{username}")
    
    # Private invite link
    if 't.me/+' in text or 't.me/joinchat/' in text:
        return {
            'id': text,  # Use link as ID
            'name': 'Private Channel (Join to see name)',
            'link': text,
            'type': 'private_link'
        }
    
    return None

def get_channel_details(identifier):
    """Get channel details from ID or username"""
    try:
        chat = main_bot.get_chat(identifier)
        
        # Get invite link
        if hasattr(chat, 'username') and chat.username:
            link = f"https://t.me/{chat.username}"
        else:
            try:
                link = main_bot.export_chat_invite_link(chat.id)
            except:
                ch_num = str(chat.id).replace('-100', '')
                link = f"https://t.me/c/{ch_num}/1"
        
        return {
            'id': str(chat.id),
            'name': chat.title if hasattr(chat, 'title') else 'Channel',
            'link': link,
            'type': 'public' if hasattr(chat, 'username') and chat.username else 'private'
        }
    
    except Exception as e:
        print(f"Error getting channel: {e}")
        return None

def is_user_member(user_id, channel_id):
    """Check if user is member"""
    try:
        # Skip check for private links (can't verify without join)
        if channel_id.startswith('http'):
            return False
        
        member = main_bot.get_chat_member(channel_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def check_all_joined(user_id):
    """Check if user joined all channels"""
    channels = load_channels()
    
    if not channels:
        return True  # No channels to join
    
    for ch_id, ch_data in channels.items():
        if not is_user_member(user_id, ch_id):
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
    
    channels = load_channels()
    files = load_files()
    
    admin_bot.send_message(
        msg.chat.id,
        f"🔐 <b>ADMIN PANEL</b>\n\n"
        f"📊 <b>Stats:</b>\n"
        f"📢 Channels: {len(channels)}\n"
        f"📁 Files: {len(files)}\n\n"
        f"<b>📢 Channel Commands:</b>\n"
        f"/addchannel - Add force subscribe channel\n"
        f"/channels - List all channels\n"
        f"/removechannel - Remove channel\n\n"
        f"<b>📁 File Commands:</b>\n"
        f"/upload - Upload file and get link\n"
        f"/files - List all files\n"
        f"/deletefile - Delete file\n\n"
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
        f"<b>Supported Formats:</b>\n"
        f"• ID: <code>-1001234567890</code>\n"
        f"• Username: <code>@channelname</code>\n"
        f"• Public: <code>https://t.me/channel</code>\n"
        f"• Private: <code>https://t.me/+hash</code>\n\n"
        f"<b>2️⃣ Upload File:</b>\n"
        f"<code>/upload</code>\n"
        f"Then send file (document/video/photo/audio)\n"
        f"You'll get shareable link!\n\n"
        f"<b>3️⃣ File Link:</b>\n"
        f"Share link with users\n"
        f"They must join channels first\n"
        f"Then verify to get file\n\n"
        f"<b>⚙️ Setup:</b>\n"
        f"1. Add both bots to storage channel as admin\n"
        f"2. Add force subscribe channels\n"
        f"3. Make Main Bot admin in those channels\n"
        f"4. Upload files and share links!"
    )

@admin_bot.message_handler(commands=['addchannel'])
def add_channel(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    try:
        # Get channel input
        parts = msg.text.split(maxsplit=1)
        if len(parts) < 2:
            admin_bot.reply_to(
                msg,
                "❌ <b>Usage:</b>\n"
                "<code>/addchannel channel_link</code>\n\n"
                "<b>Examples:</b>\n"
                "<code>/addchannel -1001234567890</code>\n"
                "<code>/addchannel @channelname</code>\n"
                "<code>/addchannel https://t.me/channel</code>\n"
                "<code>/addchannel https://t.me/+hash</code>"
            )
            return
        
        channel_input = parts[1].strip()
        
        # Parse channel
        channel_data = parse_channel_input(channel_input)
        
        if not channel_data:
            admin_bot.reply_to(msg, "❌ Invalid channel link/ID/username!")
            return
        
        # Save channel
        channels = load_channels()
        channels[channel_data['id']] = channel_data
        save_channels(channels)
        
        admin_bot.reply_to(
            msg,
            f"✅ <b>Channel Added!</b>\n\n"
            f"📢 <b>Name:</b> {channel_data['name']}\n"
            f"🆔 <b>ID:</b> <code>{channel_data['id']}</code>\n"
            f"🔗 <b>Link:</b> {channel_data['link']}\n"
            f"📊 <b>Type:</b> {channel_data['type']}\n\n"
            f"⚠️ <b>Important:</b>\n"
            f"Make Main Bot admin in this channel!"
        )
    
    except Exception as e:
        admin_bot.reply_to(msg, f"❌ Error: {str(e)}")

@admin_bot.message_handler(commands=['channels'])
def list_channels(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    channels = load_channels()
    
    if not channels:
        admin_bot.send_message(
            msg.chat.id,
            "📭 <b>No channels added!</b>\n\n"
            "Add channel:\n"
            "<code>/addchannel @channelname</code>"
        )
        return
    
    text = f"📢 <b>FORCE SUBSCRIBE CHANNELS ({len(channels)})</b>\n\n"
    
    for i, (ch_id, ch_data) in enumerate(channels.items(), 1):
        text += (
            f"{i}. <b>{ch_data['name']}</b>\n"
            f"   🆔 <code>{ch_id}</code>\n"
            f"   🔗 {ch_data['link']}\n"
            f"   📊 Type: {ch_data['type']}\n\n"
        )
    
    text += (
        f"<b>Commands:</b>\n"
        f"/removechannel <code>channel_id</code>"
    )
    
    admin_bot.send_message(msg.chat.id, text, disable_web_page_preview=True)

@admin_bot.message_handler(commands=['removechannel'])
def remove_channel(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = msg.text.split(maxsplit=1)
        if len(parts) < 2:
            admin_bot.reply_to(
                msg,
                "❌ <b>Usage:</b>\n"
                "<code>/removechannel channel_id</code>\n\n"
                "Get ID from /channels"
            )
            return
        
        ch_id = parts[1].strip()
        channels = load_channels()
        
        if ch_id in channels:
            ch_name = channels[ch_id]['name']
            del channels[ch_id]
            save_channels(channels)
            
            admin_bot.reply_to(
                msg,
                f"🗑️ <b>Channel Removed!</b>\n\n"
                f"📢 {ch_name}\n"
                f"🆔 <code>{ch_id}</code>"
            )
        else:
            admin_bot.reply_to(msg, "❌ Channel not found!")
    
    except Exception as e:
        admin_bot.reply_to(msg, f"❌ Error: {str(e)}")

@admin_bot.message_handler(commands=['upload'])
def upload_cmd(msg):
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
def handle_file(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    try:
        # Generate unique code
        code = gen_code()
        
        # Get file info
        if msg.content_type == 'document':
            file_id = msg.document.file_id
            file_name = msg.document.file_name or "Document"
        elif msg.content_type == 'video':
            file_id = msg.video.file_id
            file_name = "Video"
        elif msg.content_type == 'photo':
            file_id = msg.photo[-1].file_id
            file_name = "Photo"
        else:  # audio
            file_id = msg.audio.file_id
            file_name = msg.audio.title or "Audio"
        
        # Send to storage channel
        sent_msg = admin_bot.copy_message(
            chat_id=STORAGE_CHANNEL,
            from_chat_id=msg.chat.id,
            message_id=msg.message_id
        )
        
        # Save to database
        files = load_files()
        files[code] = {
            'message_id': sent_msg.message_id,
            'type': msg.content_type,
            'name': file_name
        }
        save_files(files)
        
        # Generate link
        bot_username = main_bot.get_me().username
        file_link = f"https://t.me/{bot_username}?start={code}"
        
        # Send confirmation
        admin_bot.reply_to(
            msg,
            f"✅ <b>File Uploaded!</b>\n\n"
            f"📁 <b>Name:</b> {file_name}\n"
            f"📋 <b>Code:</b> <code>{code}</code>\n"
            f"📦 <b>Type:</b> {msg.content_type}\n\n"
            f"🔗 <b>Share Link:</b>\n"
            f"<code>{file_link}</code>\n\n"
            f"Users must join channels to access!",
            disable_web_page_preview=True
        )
    
    except Exception as e:
        admin_bot.reply_to(msg, f"❌ Error uploading file: {str(e)}\n\nCheck: Both bots are admin in storage channel?")

@admin_bot.message_handler(commands=['files'])
def list_files(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    files = load_files()
    
    if not files:
        admin_bot.send_message(
            msg.chat.id,
            "📭 <b>No files uploaded!</b>\n\n"
            "Upload file:\n"
            "<code>/upload</code>"
        )
        return
    
    bot_username = main_bot.get_me().username
    text = f"📁 <b>UPLOADED FILES ({len(files)})</b>\n\n"
    
    for i, (code, data) in enumerate(files.items(), 1):
        link = f"https://t.me/{bot_username}?start={code}"
        text += (
            f"{i}. <b>{data['name']}</b>\n"
            f"   📋 Code: <code>{code}</code>\n"
            f"   📦 Type: {data['type']}\n"
            f"   🔗 <code>{link}</code>\n\n"
        )
        
        # Split if too long
        if len(text) > 3500:
            admin_bot.send_message(msg.chat.id, text, disable_web_page_preview=True)
            text = ""
    
    if text:
        admin_bot.send_message(msg.chat.id, text, disable_web_page_preview=True)

@admin_bot.message_handler(commands=['deletefile'])
def delete_file(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    try:
        parts = msg.text.split(maxsplit=1)
        if len(parts) < 2:
            admin_bot.reply_to(
                msg,
                "❌ <b>Usage:</b>\n"
                "<code>/deletefile file_code</code>\n\n"
                "Get code from /files"
            )
            return
        
        code = parts[1].strip()
        files = load_files()
        
        if code in files:
            file_name = files[code]['name']
            del files[code]
            save_files(files)
            
            admin_bot.reply_to(
                msg,
                f"🗑️ <b>File Deleted!</b>\n\n"
                f"📁 {file_name}\n"
                f"📋 <code>{code}</code>"
            )
        else:
            admin_bot.reply_to(msg, "❌ File not found!")
    
    except Exception as e:
        admin_bot.reply_to(msg, f"❌ Error: {str(e)}")

# ============================================
# MAIN BOT (USER-FACING)
# ============================================

@main_bot.message_handler(commands=['start'])
def main_start(msg):
    # Check if file code provided
    args = msg.text.split()
    
    if len(args) == 1:
        # No file code - just welcome
        main_bot.send_message(
            msg.chat.id,
            "👋 <b>Welcome!</b>\n\n"
            "📎 To access files, use valid link\n\n"
            "Example:\n"
            "<code>/start ABC123</code>"
        )
        return
    
    # Get file code
    code = args[1].strip()
    files = load_files()
    
    if code not in files:
        main_bot.send_message(msg.chat.id, "❌ <b>Invalid or expired link!</b>")
        return
    
    file_data = files[code]
    
    # Check if user joined all channels
    if check_all_joined(msg.from_user.id):
        # User joined all - send file
        send_file(msg.chat.id, file_data)
    else:
        # Show join channels prompt
        show_join_prompt(msg, code, file_data)

def show_join_prompt(msg, code, file_data):
    """Show channels user needs to join"""
    channels = load_channels()
    
    if not channels:
        # No channels - directly send file
        send_file(msg.chat.id, file_data)
        return
    
    # Create buttons for each channel
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for ch_id, ch_data in channels.items():
        btn = types.InlineKeyboardButton(
            text=f"📢 Join {ch_data['name']}",
            url=ch_data['link']
        )
        markup.add(btn)
    
    # Add verify button
    verify_btn = types.InlineKeyboardButton(
        text="✅ Joined, Verify Now!",
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
    """Verify if user joined all channels"""
    code = call.data.replace('verify_', '')
    files = load_files()
    
    if code not in files:
        main_bot.answer_callback_query(call.id, "❌ Invalid link!", show_alert=True)
        return
    
    # Check if joined all
    if check_all_joined(call.from_user.id):
        main_bot.answer_callback_query(call.id, "✅ Verified! Sending file...", show_alert=False)
        
        # Delete join message
        try:
            main_bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        
        # Send file
        send_file(call.message.chat.id, files[code])
    else:
        main_bot.answer_callback_query(
            call.id,
            "❌ Please join ALL channels first!\n\nClick buttons above to join.",
            show_alert=True
        )

def send_file(chat_id, file_data):
    """Send file from storage to user"""
    try:
        main_bot.copy_message(
            chat_id=chat_id,
            from_chat_id=STORAGE_CHANNEL,
            message_id=file_data['message_id'],
            caption=f"✅ <b>Here's your file!</b>\n\n📁 {file_data['name']}"
        )
        print(f"✅ File sent to {chat_id}: {file_data['name']}")
    except Exception as e:
        main_bot.send_message(
            chat_id,
            "❌ <b>Error sending file!</b>\n\n"
            "Contact admin for help."
        )
        print(f"❌ Error sending file: {e}")

# ============================================
# RUN BOTH BOTS
# ============================================

def run_main():
    print("🤖 Main Bot running...")
    try:
        main_bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"❌ Main Bot error: {e}")

def run_admin():
    print("👨‍💼 Admin Bot running...")
    try:
        admin_bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"❌ Admin Bot error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 STARTING FILE SHARING BOT")
    print("=" * 60)
    print(f"👤 Admin ID: {ADMIN_ID}")
    print(f"📦 Storage: {STORAGE_CHANNEL}")
    print("=" * 60)
    
    # Start both bots in separate threads
    main_thread = threading.Thread(target=run_main, daemon=True)
    admin_thread = threading.Thread(target=run_admin, daemon=True)
    
    main_thread.start()
    admin_thread.start()
    
    print("✅ Both bots running!\n")
    print("⚠️  SETUP CHECKLIST:")
    print("1. ✅ Add both bots to storage channel as admin")
    print("2. ✅ Add force subscribe channels: /addchannel")
    print("3. ✅ Make Main Bot admin in force channels")
    print("4. ✅ Upload files: /upload")
    print("5. ✅ Share links with users\n")
    print("💡 Press Ctrl+C to stop\n")
    
    try:
        main_thread.join()
        admin_thread.join()
    except KeyboardInterrupt:
        print("\n🛑 Bots stopped!\n")
