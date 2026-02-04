import os
import sqlite3
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ============================================
# CONFIGURATION
# ============================================
MAIN_BOT_TOKEN = '8580329271:AAE8SlxlyggTLW0YSR0YZVGgAtjOYGpoRvI'
ADMIN_BOT_TOKEN = '8553759431:AAHKDR2BZ1C550sTe749WaizG9jUCncOm18'
ADMIN_CHAT_ID = 7417241499
MAIN_BOT_USERNAME = os.getenv('MAIN_BOT_USERNAME', 'YourMainBotUsername')  # Railway pe set karna hai
DATABASE = 'bot_database.db'

# ============================================
# DATABASE INITIALIZATION
# ============================================
def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Files table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            file_id TEXT PRIMARY KEY,
            file_unique_id TEXT,
            file_type TEXT,
            caption TEXT,
            file_name TEXT
        )
    ''')
    
    # Channels table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY,
            channel_username TEXT,
            channel_link TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

# ============================================
# MAIN BOT FUNCTIONS
# ============================================

async def check_user_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Check if user is member of all required channels"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT channel_id FROM channels')
    channels = cursor.fetchall()
    conn.close()
    
    if not channels:
        return True, None
    
    not_joined = []
    for channel in channels:
        channel_id = channel[0]
        try:
            member = await context.bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status in ['left', 'kicked']:
                not_joined.append(channel_id)
        except Exception as e:
            print(f"❌ Error checking membership for {channel_id}: {e}")
            not_joined.append(channel_id)
    
    return len(not_joined) == 0, not_joined if not_joined else None

def get_channel_buttons():
    """Get inline keyboard with channel join buttons"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT channel_link, channel_username FROM channels')
    channels = cursor.fetchall()
    conn.close()
    
    keyboard = []
    for channel in channels:
        link = channel[0] if channel[0] else f"https://t.me/{channel[1]}"
        name = channel[1] if channel[1] else "Join Channel"
        keyboard.append([InlineKeyboardButton(f"📢 {name}", url=link)])
    
    keyboard.append([InlineKeyboardButton("✅ Verify Membership", callback_data="verify")])
    return InlineKeyboardMarkup(keyboard)

async def main_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main bot start command handler"""
    user = update.effective_user
    args = context.args
    
    # Check if it's a file request
    if args and args[0].startswith('file_'):
        file_id = args[0].replace('file_', '')
        
        # Check membership
        is_member, not_joined = await check_user_membership(user.id, context)
        
        if not is_member:
            await update.message.reply_text(
                f"👋 Hello {user.first_name}!\n\n"
                "🔒 To access this file, you need to join our channels first:\n\n"
                "Click the buttons below to join, then click 'Verify Membership'",
                reply_markup=get_channel_buttons()
            )
            # Store file_id in user_data for later
            context.user_data['pending_file'] = file_id
        else:
            # Send file directly
            await send_file(update, context, file_id)
    else:
        await update.message.reply_text(
            f"👋 Welcome {user.first_name}!\n\n"
            "🤖 I'm a file sharing bot.\n\n"
            "📎 To get files, use the links provided by admin.\n\n"
            "✨ Enjoy!"
        )

async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle verify membership button callback"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    is_member, not_joined = await check_user_membership(user.id, context)
    
    if is_member:
        await query.message.edit_text("✅ Verification successful! Sending your file...")
        
        # Get pending file from user_data
        file_id = context.user_data.get('pending_file')
        if file_id:
            await send_file_to_user(query.message, context, file_id, user.id)
            context.user_data.pop('pending_file', None)
        else:
            await query.message.reply_text("❌ File not found. Please use the link again.")
    else:
        await query.message.reply_text(
            "❌ You haven't joined all channels yet!\n\n"
            "Please join all channels and click 'Verify Membership' again.",
            reply_markup=get_channel_buttons()
        )

async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE, file_id: str):
    """Send file to user after verification"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files WHERE file_id = ?', (file_id,))
    file_data = cursor.fetchone()
    conn.close()
    
    if file_data:
        file_unique_id, file_type, caption, file_name = file_data[1], file_data[2], file_data[3], file_data[4]
        
        try:
            if file_type == 'document':
                await update.message.reply_document(
                    document=file_id,
                    caption=caption if caption else f"📁 {file_name}"
                )
            elif file_type == 'video':
                await update.message.reply_video(
                    video=file_id,
                    caption=caption if caption else f"🎬 {file_name}"
                )
            elif file_type == 'audio':
                await update.message.reply_audio(
                    audio=file_id,
                    caption=caption if caption else f"🎵 {file_name}"
                )
            elif file_type == 'photo':
                await update.message.reply_photo(
                    photo=file_id,
                    caption=caption if caption else "🖼️ Photo"
                )
        except Exception as e:
            await update.message.reply_text(f"❌ Error sending file: {str(e)}")
    else:
        await update.message.reply_text("❌ File not found!")

async def send_file_to_user(message, context: ContextTypes.DEFAULT_TYPE, file_id: str, user_id: int):
    """Send file directly to user (for callback)"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files WHERE file_id = ?', (file_id,))
    file_data = cursor.fetchone()
    conn.close()
    
    if file_data:
        file_unique_id, file_type, caption, file_name = file_data[1], file_data[2], file_data[3], file_data[4]
        
        try:
            if file_type == 'document':
                await context.bot.send_document(
                    chat_id=user_id,
                    document=file_id,
                    caption=caption if caption else f"📁 {file_name}"
                )
            elif file_type == 'video':
                await context.bot.send_video(
                    chat_id=user_id,
                    video=file_id,
                    caption=caption if caption else f"🎬 {file_name}"
                )
            elif file_type == 'audio':
                await context.bot.send_audio(
                    chat_id=user_id,
                    audio=file_id,
                    caption=caption if caption else f"🎵 {file_name}"
                )
            elif file_type == 'photo':
                await context.bot.send_photo(
                    chat_id=user_id,
                    photo=file_id,
                    caption=caption if caption else "🖼️ Photo"
                )
        except Exception as e:
            await message.reply_text(f"❌ Error sending file: {str(e)}")
    else:
        await message.reply_text("❌ File not found!")

# ============================================
# ADMIN BOT FUNCTIONS
# ============================================

def is_admin(user_id: int):
    """Check if user is admin"""
    return user_id == ADMIN_CHAT_ID

async def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin bot start command handler"""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ You are not authorized to use this bot!")
        return
    
    await update.message.reply_text(
        "👨‍💼 *Admin Bot Control Panel*\n\n"
        "📎 *File Management:*\n"
        "• Send any file to get a shareable link\n\n"
        "📢 *Channel Management:*\n"
        "• `/addchannel <channel_id> <link>` - Add forced channel\n"
        "• `/removechannel <channel_id>` - Remove channel\n"
        "• `/listchannels` - List all channels\n\n"
        "💡 *Example:*\n"
        "`/addchannel -1001234567890 https://t.me/yourchannel`",
        parse_mode='Markdown'
    )

async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add forced subscription channel"""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ You are not authorized!")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage: `/addchannel <channel_id> <link>`\n\n"
            "Example: `/addchannel -1001234567890 https://t.me/yourchannel`",
            parse_mode='Markdown'
        )
        return
    
    channel_id = context.args[0]
    channel_link = context.args[1]
    
    # Try to get channel username
    channel_username = None
    try:
        chat = await context.bot.get_chat(channel_id)
        channel_username = chat.username
    except Exception as e:
        print(f"Could not get channel info: {e}")
    
    # Add to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT OR REPLACE INTO channels (channel_id, channel_username, channel_link) VALUES (?, ?, ?)',
            (channel_id, channel_username, channel_link)
        )
        conn.commit()
        await update.message.reply_text(
            f"✅ Channel added successfully!\n\n"
            f"🆔 ID: `{channel_id}`\n"
            f"🔗 Link: {channel_link}",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        conn.close()

async def remove_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove forced subscription channel"""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ You are not authorized!")
        return
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "❌ Usage: `/removechannel <channel_id>`\n\n"
            "Example: `/removechannel -1001234567890`",
            parse_mode='Markdown'
        )
        return
    
    channel_id = context.args[0]
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM channels WHERE channel_id = ?', (channel_id,))
    conn.commit()
    
    if cursor.rowcount > 0:
        await update.message.reply_text(f"✅ Channel `{channel_id}` removed successfully!", parse_mode='Markdown')
    else:
        await update.message.reply_text(f"❌ Channel `{channel_id}` not found!", parse_mode='Markdown')
    
    conn.close()

async def list_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all forced subscription channels"""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ You are not authorized!")
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM channels')
    channels = cursor.fetchall()
    conn.close()
    
    if not channels:
        await update.message.reply_text("📢 No forced channels added yet!")
        return
    
    message = "📢 *Forced Channels List:*\n\n"
    for idx, channel in enumerate(channels, 1):
        channel_id, username, link = channel
        message += f"{idx}. 🆔 `{channel_id}`\n"
        if username:
            message += f"   👤 @{username}\n"
        if link:
            message += f"   🔗 {link}\n"
        message += "\n"
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file uploads from admin"""
    user = update.effective_user
    
    if not is_admin(user.id):
        await update.message.reply_text("❌ You are not authorized!")
        return
    
    message = update.message
    file_id = None
    file_unique_id = None
    file_type = None
    file_name = "Unknown"
    caption = message.caption
    
    # Determine file type and get file_id
    if message.document:
        file_id = message.document.file_id
        file_unique_id = message.document.file_unique_id
        file_type = 'document'
        file_name = message.document.file_name
    elif message.video:
        file_id = message.video.file_id
        file_unique_id = message.video.file_unique_id
        file_type = 'video'
        file_name = message.video.file_name or "Video"
    elif message.audio:
        file_id = message.audio.file_id
        file_unique_id = message.audio.file_unique_id
        file_type = 'audio'
        file_name = message.audio.file_name or "Audio"
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        file_type = 'photo'
        file_name = "Photo"
    
    if not file_id:
        await update.message.reply_text("❌ No valid file found!")
        return
    
    # Save to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT OR REPLACE INTO files (file_id, file_unique_id, file_type, caption, file_name) VALUES (?, ?, ?, ?, ?)',
            (file_id, file_unique_id, file_type, caption, file_name)
        )
        conn.commit()
        
        # Generate shareable link
        share_link = f"https://t.me/{MAIN_BOT_USERNAME}?start=file_{file_id}"
        
        await update.message.reply_text(
            f"✅ *File Uploaded Successfully!*\n\n"
            f"📁 Name: `{file_name}`\n"
            f"📎 Type: `{file_type}`\n"
            f"🆔 File ID: `{file_id}`\n\n"
            f"🔗 *Share Link:*\n`{share_link}`\n\n"
            f"💡 Users will need to join forced channels before accessing the file.",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error saving file: {str(e)}")
    finally:
        conn.close()

# ============================================
# BOT RUNNERS
# ============================================

async def run_main_bot():
    """Run main bot (user-facing)"""
    print("🚀 Starting Main Bot...")
    application = Application.builder().token(MAIN_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", main_start))
    application.add_handler(CallbackQueryHandler(verify_callback, pattern="^verify$"))
    
    print("✅ Main Bot started successfully!")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

async def run_admin_bot():
    """Run admin bot (file upload & management)"""
    print("🚀 Starting Admin Bot...")
    application = Application.builder().token(ADMIN_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", admin_start))
    application.add_handler(CommandHandler("addchannel", add_channel))
    application.add_handler(CommandHandler("removechannel", remove_channel))
    application.add_handler(CommandHandler("listchannels", list_channels))
    
    # Handle all file types
    application.add_handler(MessageHandler(
        filters.Document.ALL | filters.VIDEO | filters.AUDIO | filters.PHOTO,
        handle_file
    ))
    
    print("✅ Admin Bot started successfully!")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

async def main():
    """Run both bots concurrently"""
    print("=" * 50)
    print("🤖 TELEGRAM FILE SHARING BOT SYSTEM")
    print("=" * 50)
    
    # Initialize database
    init_db()
    
    print(f"\n📋 Configuration:")
    print(f"   Main Bot Token: {MAIN_BOT_TOKEN[:10]}...")
    print(f"   Admin Bot Token: {ADMIN_BOT_TOKEN[:10]}...")
    print(f"   Admin Chat ID: {ADMIN_CHAT_ID}")
    print(f"   Main Bot Username: @{MAIN_BOT_USERNAME}")
    print(f"   Database: {DATABASE}")
    print("\n" + "=" * 50 + "\n")
    
    # Create tasks for both bots
    main_bot_task = asyncio.create_task(run_main_bot())
    admin_bot_task = asyncio.create_task(run_admin_bot())
    
    # Wait for both tasks
    await asyncio.gather(main_bot_task, admin_bot_task)

# ============================================
# ENTRY POINT
# ============================================

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Bots stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
