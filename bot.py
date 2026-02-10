#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ADVANCED AI CHATBOT
Powered by WORMgpt API
Clean & Professional Replies
"""

import telebot
from telebot import types
import requests
import json
import os
import time
from datetime import datetime
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== CONFIGURATION ====================
MAIN_BOT_TOKEN = "8532068765:AAHxGgjltPhimYAGIjeHwZpP_Pkn-bbLBoQ"
ADMIN_BOT_TOKEN = "8586819943:AAG6w5gMAfmY8TR8I4ZS4VJqrV3NwvlSLNs"
OWNER_ID = 7417241499

# AI API Configuration
AI_API_URL = "https://usesir.vercel.app/api/WORMgpt"
AI_API_KEY = "bday"

# Bot Settings
BOT_NAME = "AI Assistant"
BOT_USERNAME = "@YourBotUsername"  # Update after creation

# Files
USERS_FILE = "ai_users.json"
SETTINGS_FILE = "ai_settings.json"
CHAT_HISTORY_FILE = "chat_history.json"

# ==================== FILE OPERATIONS ====================
def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({
                "bot_active": True,
                "maintenance_msg": "Bot is under maintenance.",
                "chat_mode_users": [],
                "banned_users": [],
                "total_requests": 0
            }, f)
    
    if not os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump({}, f)

def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

init_files()

users = load_json(USERS_FILE)
settings = load_json(SETTINGS_FILE)
chat_history = load_json(CHAT_HISTORY_FILE)

bot = telebot.TeleBot(MAIN_BOT_TOKEN, parse_mode="HTML")
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN, parse_mode="HTML")

logger.info(f"✅ Main Bot: @{bot.get_me().username}")
logger.info(f"✅ Admin Bot: @{admin_bot.get_me().username}")

# ==================== HELPER FUNCTIONS ====================

def is_owner(uid):
    return uid == OWNER_ID

def is_banned(uid):
    return uid in settings.get("banned_users", [])

def get_user(uid):
    uid_str = str(uid)
    if uid_str not in users:
        users[uid_str] = {
            "user_id": uid,
            "name": "",
            "username": "",
            "joined": datetime.now().isoformat(),
            "total_requests": 0,
            "chat_mode": False,
            "last_active": datetime.now().isoformat()
        }
        save_json(USERS_FILE, users)
    return users[uid_str]

def update_user_activity(uid, name, username):
    uid_str = str(uid)
    if uid_str in users:
        users[uid_str]["name"] = name
        users[uid_str]["username"] = username
        users[uid_str]["last_active"] = datetime.now().isoformat()
        save_json(USERS_FILE, users)

def make_ai_request(text):
    """Make request to WORMgpt API"""
    try:
        params = {
            "key": AI_API_KEY,
            "text": text
        }
        response = requests.get(AI_API_URL, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract reply from different possible response formats
            if isinstance(data, dict):
                reply = data.get("reply") or data.get("response") or data.get("answer") or data.get("result")
                if reply:
                    return reply
            elif isinstance(data, str):
                return data
            
            return response.text
        else:
            return None
    except Exception as e:
        logger.error(f"AI API Error: {e}")
        return None

def format_ai_reply(question, answer):
    """Format AI reply in clean style"""
    reply = f"<b>🤖 AI Assistant</b>\n\n"
    
    # Question
    reply += f"<b>❓ Question:</b>\n<i>{question}</i>\n\n"
    
    # Answer
    reply += f"<b>💡 Answer:</b>\n{answer}\n\n"
    
    # Footer
    reply += f"<code>───────────────────</code>\n"
    reply += f"<i>Powered by WORMgpt</i>"
    
    return reply

def save_chat_history(uid, question, answer):
    """Save chat history"""
    uid_str = str(uid)
    if uid_str not in chat_history:
        chat_history[uid_str] = []
    
    chat_history[uid_str].append({
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 50 messages
    if len(chat_history[uid_str]) > 50:
        chat_history[uid_str] = chat_history[uid_str][-50:]
    
    save_json(CHAT_HISTORY_FILE, chat_history)

# ==================== MAIN BOT HANDLERS ====================

@bot.message_handler(commands=['start'])
def cmd_start(m):
    if is_banned(m.from_user.id):
        return bot.reply_to(m, "❌ You are banned from using this bot.")
    
    user = get_user(m.from_user.id)
    update_user_activity(m.from_user.id, m.from_user.first_name or "", m.from_user.username or "")
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🤖 Ask AI", "💬 Chat Mode")
    kb.row("📊 My Stats", "❓ Help")
    
    welcome = f"""
╔════════════════════════════════╗
║     <b>🤖 AI ASSISTANT BOT</b>      ║
╚════════════════════════════════╝

👋 <b>Welcome, {m.from_user.first_name}!</b>

I'm an advanced AI assistant powered by WORMgpt. 
I can answer your questions intelligently!

<b>━━━━━ QUICK START ━━━━━</b>

🔹 <b>/ai [question]</b> - Ask anything
🔹 <b>/ask [question]</b> - Alternative command
🔹 <b>/chat</b> - Enable chat mode (auto-reply)
🔹 <b>/history</b> - View chat history
🔹 <b>/clear</b> - Clear your history

<b>━━━━━ FEATURES ━━━━━</b>

✅ Smart AI responses
✅ Clean formatted replies
✅ Chat mode for conversations
✅ Unlimited questions
✅ Fast response time

<b>━━━━━━━━━━━━━━━━━━━━━</b>

💡 <b>Just send me any question!</b>
"""
    
    bot.send_message(m.chat.id, welcome, reply_markup=kb)

@bot.message_handler(commands=['ai', 'ask'])
def cmd_ai(m):
    if is_banned(m.from_user.id):
        return
    
    if not settings.get("bot_active", True):
        return bot.reply_to(m, settings.get("maintenance_msg"))
    
    # Extract question
    question = m.text.replace('/ai', '').replace('/ask', '').strip()
    
    if not question:
        return bot.reply_to(
            m,
            "❓ <b>Please provide a question!</b>\n\n"
            "<b>Usage:</b>\n"
            "<code>/ai What is AI?</code>\n"
            "<code>/ask How does gravity work?</code>"
        )
    
    # Send processing message
    processing = bot.reply_to(m, "🤔 <i>Thinking...</i>")
    
    # Get AI response
    answer = make_ai_request(question)
    
    if answer:
        # Update stats
        uid_str = str(m.from_user.id)
        users[uid_str]["total_requests"] += 1
        settings["total_requests"] += 1
        save_json(USERS_FILE, users)
        save_json(SETTINGS_FILE, settings)
        
        # Save history
        save_chat_history(m.from_user.id, question, answer)
        
        # Format and send reply
        reply = format_ai_reply(question, answer)
        
        try:
            bot.edit_message_text(reply, m.chat.id, processing.message_id)
        except:
            bot.delete_message(m.chat.id, processing.message_id)
            bot.send_message(m.chat.id, reply)
    else:
        bot.edit_message_text(
            "❌ <b>Sorry, couldn't get a response.</b>\n\n"
            "Please try again later!",
            m.chat.id,
            processing.message_id
        )

@bot.message_handler(commands=['chat'])
def cmd_chat_mode(m):
    if is_banned(m.from_user.id):
        return
    
    uid_str = str(m.from_user.id)
    user = get_user(m.from_user.id)
    
    # Toggle chat mode
    current_mode = users[uid_str].get("chat_mode", False)
    users[uid_str]["chat_mode"] = not current_mode
    save_json(USERS_FILE, users)
    
    if users[uid_str]["chat_mode"]:
        msg = """
✅ <b>CHAT MODE ENABLED</b>

Now I'll respond to all your messages automatically!

💬 Just type anything and I'll reply.

🔹 <b>/chat</b> - Disable chat mode
🔹 <b>/clear</b> - Clear history
"""
    else:
        msg = """
❌ <b>CHAT MODE DISABLED</b>

Use <b>/ai</b> or <b>/ask</b> to get responses.

💡 <b>/chat</b> - Enable chat mode again
"""
    
    bot.reply_to(m, msg)

@bot.message_handler(commands=['history'])
def cmd_history(m):
    if is_banned(m.from_user.id):
        return
    
    uid_str = str(m.from_user.id)
    
    if uid_str not in chat_history or not chat_history[uid_str]:
        return bot.reply_to(m, "📭 <b>No chat history yet!</b>\n\nStart asking questions to build history.")
    
    history = chat_history[uid_str][-10:]  # Last 10
    
    msg = "<b>📜 YOUR CHAT HISTORY</b>\n\n"
    
    for i, item in enumerate(reversed(history), 1):
        timestamp = item.get("timestamp", "")[:10]
        question = item.get("question", "")[:50]
        
        msg += f"<b>{i}.</b> {question}...\n"
        msg += f"   <i>{timestamp}</i>\n\n"
    
    msg += f"<code>───────────────────</code>\n"
    msg += f"<b>Total:</b> {len(chat_history[uid_str])} conversations\n\n"
    msg += f"💡 Use <b>/clear</b> to clear history"
    
    bot.send_message(m.chat.id, msg)

@bot.message_handler(commands=['clear'])
def cmd_clear(m):
    if is_banned(m.from_user.id):
        return
    
    uid_str = str(m.from_user.id)
    
    if uid_str in chat_history:
        chat_history[uid_str] = []
        save_json(CHAT_HISTORY_FILE, chat_history)
    
    bot.reply_to(m, "✅ <b>History cleared!</b>\n\nStart fresh conversations now.")

@bot.message_handler(commands=['stats'])
def cmd_stats(m):
    if is_banned(m.from_user.id):
        return
    
    user = get_user(m.from_user.id)
    uid_str = str(m.from_user.id)
    
    total_chats = len(chat_history.get(uid_str, []))
    
    msg = f"""
<b>📊 YOUR STATISTICS</b>

<b>━━━━━ USAGE ━━━━━</b>

🤖 <b>Total Requests:</b> {user.get('total_requests', 0)}
💬 <b>Chat History:</b> {total_chats}
📅 <b>Joined:</b> {user.get('joined', '')[:10]}
⚡ <b>Chat Mode:</b> {'ON' if user.get('chat_mode') else 'OFF'}

<b>━━━━━ ACCOUNT ━━━━━</b>

👤 <b>Name:</b> {user.get('name', 'N/A')}
🆔 <b>User ID:</b> <code>{m.from_user.id}</code>

<b>━━━━━━━━━━━━━━━━━━━━━</b>

💡 Keep chatting to increase stats!
"""
    
    bot.send_message(m.chat.id, msg)

@bot.message_handler(commands=['help'])
def cmd_help(m):
    help_msg = """
<b>❓ HELP & COMMANDS</b>

<b>━━━━━ BASIC COMMANDS ━━━━━</b>

🔹 <b>/start</b> - Start the bot
🔹 <b>/ai [question]</b> - Ask AI
🔹 <b>/ask [question]</b> - Alternative
🔹 <b>/chat</b> - Toggle chat mode
🔹 <b>/history</b> - View history
🔹 <b>/clear</b> - Clear history
🔹 <b>/stats</b> - Your statistics
🔹 <b>/help</b> - This message

<b>━━━━━ HOW TO USE ━━━━━</b>

<b>Method 1: Commands</b>
<code>/ai What is quantum physics?</code>
<code>/ask Explain blockchain</code>

<b>Method 2: Chat Mode</b>
<code>/chat</code> (enable)
Then just type normally!

<b>━━━━━ FEATURES ━━━━━</b>

✅ Smart AI responses
✅ Clean formatting
✅ Fast replies
✅ Chat history
✅ Unlimited questions

<b>━━━━━━━━━━━━━━━━━━━━━</b>

💡 <b>Just ask anything!</b>
"""
    
    bot.send_message(m.chat.id, help_msg)

@bot.message_handler(func=lambda m: m.text and m.text.startswith(('🤖', '💬', '📊', '❓')))
def btn_handler(m):
    if m.text == "🤖 Ask AI":
        bot.send_message(
            m.chat.id,
            "💬 <b>Send your question!</b>\n\n"
            "Or use: <code>/ai your question</code>"
        )
    elif m.text == "💬 Chat Mode":
        cmd_chat_mode(m)
    elif m.text == "📊 My Stats":
        cmd_stats(m)
    elif m.text == "❓ Help":
        cmd_help(m)

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(m):
    if is_banned(m.from_user.id):
        return
    
    if not settings.get("bot_active", True):
        return
    
    uid_str = str(m.from_user.id)
    user = get_user(m.from_user.id)
    
    # Check if chat mode is enabled
    if not users[uid_str].get("chat_mode", False):
        return bot.reply_to(
            m,
            "💡 <b>Use commands to interact!</b>\n\n"
            "<b>Quick start:</b>\n"
            "🔹 <code>/ai your question</code>\n"
            "🔹 <code>/chat</code> - Enable auto-reply"
        )
    
    # Chat mode active - process message
    question = m.text.strip()
    
    if not question or len(question) < 2:
        return
    
    processing = bot.reply_to(m, "💭 <i>Processing...</i>")
    
    answer = make_ai_request(question)
    
    if answer:
        # Update stats
        users[uid_str]["total_requests"] += 1
        settings["total_requests"] += 1
        save_json(USERS_FILE, users)
        save_json(SETTINGS_FILE, settings)
        
        # Save history
        save_chat_history(m.from_user.id, question, answer)
        
        # Format reply
        reply = format_ai_reply(question, answer)
        
        try:
            bot.edit_message_text(reply, m.chat.id, processing.message_id)
        except:
            bot.delete_message(m.chat.id, processing.message_id)
            bot.send_message(m.chat.id, reply)
    else:
        bot.edit_message_text(
            "❌ <b>Error getting response.</b>\n\nPlease try again!",
            m.chat.id,
            processing.message_id
        )

# ==================== ADMIN BOT ====================

@admin_bot.message_handler(commands=['start'])
def admin_start(m):
    if not is_owner(m.from_user.id):
        return admin_bot.send_message(m.chat.id, "❌ Unauthorized!")
    
    total_users = len(users)
    total_requests = settings.get("total_requests", 0)
    active_chats = sum(1 for u in users.values() if u.get("chat_mode"))
    
    msg = f"""
<b>🔐 ADMIN PANEL</b>

<b>━━━━━ STATISTICS ━━━━━</b>

👥 <b>Total Users:</b> {total_users}
🤖 <b>Total Requests:</b> {total_requests}
💬 <b>Active Chats:</b> {active_chats}
🤖 <b>Bot Status:</b> {'🟢 Active' if settings.get('bot_active') else '🔴 Maintenance'}

<b>━━━━━ COMMANDS ━━━━━</b>

<b>/stats</b> - Detailed statistics
<b>/users</b> - List all users
<b>/broadcast</b> - Send message to all
<b>/ban [id]</b> - Ban user
<b>/unban [id]</b> - Unban user
<b>/maintenance</b> - Toggle maintenance
<b>/clearall</b> - Clear all history

<b>━━━━━━━━━━━━━━━━━━━━━</b>

🔑 Owner: {OWNER_ID}
"""
    
    admin_bot.send_message(m.chat.id, msg)

@admin_bot.message_handler(commands=['stats'])
def admin_stats(m):
    if not is_owner(m.from_user.id):
        return
    
    total_users = len(users)
    total_requests = settings.get("total_requests", 0)
    total_history = sum(len(h) for h in chat_history.values())
    active_chats = sum(1 for u in users.values() if u.get("chat_mode"))
    banned = len(settings.get("banned_users", []))
    
    # Recent users (last 24h)
    from datetime import datetime, timedelta
    now = datetime.now()
    recent = sum(
        1 for u in users.values()
        if (now - datetime.fromisoformat(u.get("last_active", "2000-01-01"))).days < 1
    )
    
    msg = f"""
<b>📊 DETAILED STATISTICS</b>

<b>━━━━━ USERS ━━━━━</b>

👥 <b>Total Users:</b> {total_users}
⚡ <b>Active (24h):</b> {recent}
💬 <b>Chat Mode ON:</b> {active_chats}
🚫 <b>Banned:</b> {banned}

<b>━━━━━ ACTIVITY ━━━━━</b>

🤖 <b>Total Requests:</b> {total_requests}
📜 <b>Total History:</b> {total_history}
📈 <b>Avg per User:</b> {total_requests // total_users if total_users > 0 else 0}

<b>━━━━━ STATUS ━━━━━</b>

🔘 <b>Bot:</b> {'🟢 Active' if settings.get('bot_active') else '🔴 Maintenance'}
📅 <b>Date:</b> {datetime.now().strftime('%d %b %Y')}

<b>━━━━━━━━━━━━━━━━━━━━━</b>
"""
    
    admin_bot.send_message(m.chat.id, msg)

@admin_bot.message_handler(commands=['users'])
def admin_users(m):
    if not is_owner(m.from_user.id):
        return
    
    if not users:
        return admin_bot.send_message(m.chat.id, "📭 No users yet!")
    
    msg = "<b>👥 USER LIST</b>\n\n"
    
    sorted_users = sorted(
        users.items(),
        key=lambda x: x[1].get("total_requests", 0),
        reverse=True
    )
    
    for i, (uid, user) in enumerate(sorted_users[:20], 1):
        name = user.get("name", "Unknown")
        username = user.get("username", "N/A")
        requests = user.get("total_requests", 0)
        chat_mode = "💬" if user.get("chat_mode") else ""
        
        msg += f"<b>{i}.</b> {name} (@{username})\n"
        msg += f"   🆔 <code>{uid}</code> {chat_mode}\n"
        msg += f"   📊 {requests} requests\n\n"
    
    if len(users) > 20:
        msg += f"\n<i>... and {len(users) - 20} more</i>"
    
    admin_bot.send_message(m.chat.id, msg)

@admin_bot.message_handler(commands=['broadcast'])
def admin_broadcast(m):
    if not is_owner(m.from_user.id):
        return
    
    msg = admin_bot.send_message(
        m.chat.id,
        "📢 <b>BROADCAST MESSAGE</b>\n\n"
        "Send the message to broadcast to all users:\n\n"
        "Or /cancel"
    )
    
    admin_bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(m):
    if m.text == '/cancel':
        return admin_bot.send_message(m.chat.id, "❌ Cancelled!")
    
    message = m.text
    
    progress = admin_bot.send_message(m.chat.id, "📤 Broadcasting...")
    
    success = 0
    failed = 0
    
    for uid in users:
        try:
            bot.send_message(
                int(uid),
                f"📢 <b>ANNOUNCEMENT</b>\n\n{message}"
            )
            success += 1
        except:
            failed += 1
        time.sleep(0.05)
    
    admin_bot.edit_message_text(
        f"✅ <b>Broadcast Complete!</b>\n\n"
        f"📤 Sent: {success}\n"
        f"❌ Failed: {failed}",
        m.chat.id,
        progress.message_id
    )

@admin_bot.message_handler(commands=['ban'])
def admin_ban(m):
    if not is_owner(m.from_user.id):
        return
    
    try:
        uid = int(m.text.split()[1])
        
        if uid in settings.get("banned_users", []):
            return admin_bot.reply_to(m, "⚠️ Already banned!")
        
        settings.setdefault("banned_users", []).append(uid)
        save_json(SETTINGS_FILE, settings)
        
        admin_bot.reply_to(m, f"✅ Banned user: <code>{uid}</code>")
        
        try:
            bot.send_message(uid, "❌ You have been banned from using this bot.")
        except:
            pass
    except:
        admin_bot.reply_to(m, "❌ Usage: /ban user_id")

@admin_bot.message_handler(commands=['unban'])
def admin_unban(m):
    if not is_owner(m.from_user.id):
        return
    
    try:
        uid = int(m.text.split()[1])
        
        if uid not in settings.get("banned_users", []):
            return admin_bot.reply_to(m, "⚠️ User not banned!")
        
        settings["banned_users"].remove(uid)
        save_json(SETTINGS_FILE, settings)
        
        admin_bot.reply_to(m, f"✅ Unbanned user: <code>{uid}</code>")
    except:
        admin_bot.reply_to(m, "❌ Usage: /unban user_id")

@admin_bot.message_handler(commands=['maintenance'])
def admin_maintenance(m):
    if not is_owner(m.from_user.id):
        return
    
    current = settings.get("bot_active", True)
    settings["bot_active"] = not current
    save_json(SETTINGS_FILE, settings)
    
    status = "🟢 ACTIVE" if settings["bot_active"] else "🔴 MAINTENANCE"
    admin_bot.reply_to(m, f"✅ Bot status: {status}")

# ==================== RUN BOTS ====================

def run_main_bot():
    while True:
        try:
            logger.info("🤖 Main bot starting...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Main bot error: {e}")
            time.sleep(5)

def run_admin_bot():
    while True:
        try:
            logger.info("⚙️ Admin bot starting...")
            admin_bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Admin bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("╔════════════════════════════════════════════════════╗")
    print("║                                                    ║")
    print("║          🤖 AI CHATBOT - WORMGPT POWERED          ║")
    print("║                                                    ║")
    print("║        Smart Replies | Clean Format | Fast        ║")
    print("║                                                    ║")
    print("╚════════════════════════════════════════════════════╝")
    print("="*60)
    
    logger.info(f"👑 Owner: {OWNER_ID}")
    logger.info(f"👥 Users: {len(users)}")
    logger.info(f"🤖 Total Requests: {settings.get('total_requests', 0)}")
    
    print("\n" + "="*60)
    print("✅ BOTS STARTING!")
    print("🛑 Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    main_thread = threading.Thread(target=run_main_bot, daemon=True)
    admin_thread = threading.Thread(target=run_admin_bot, daemon=True)
    
    main_thread.start()
    admin_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Stopping bots...")
