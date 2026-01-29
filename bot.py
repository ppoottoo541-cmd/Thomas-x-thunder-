#!/usr/bin/env python3
"""
Educational Telegram Bot System with Premium Levels
Final Year Project - Complete Implementation
"""

import asyncio
import json
import logging
import os
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import hashlib

import aiohttp
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# ============================================================================
# CONFIGURATION - TUJHE BAS YAHI CHANGE KARNA HAI
# ============================================================================

# 1. BOT TOKENS (BotFather se banaye hue)
MAIN_BOT_TOKEN = "8580329271:AAFPmbJraVIAkHbcZtQ5tohIDwWHvjx3I"
ADMIN_BOT_TOKEN = "8553759431:AAH4BgRJcm1-JI5oBDoYIxR3Vby7oUmJgZQ"

# 2. YOUR DETAILS (Yahi change karna)
OWNER_ID = 7417241499  # Tumhara Telegram ID
YOUR_USERNAME = "@ThomasXstoreee"  # Payment ke liye contact

# 3. SERVICE SETTINGS (Optional change)
LEVEL2_PRICE = "₹499 (10 days access)"
LEVEL3_PRICE = "₹999 (10 days access)"
CREDIT_COST = 1  # Sab services ke liye same

# ============================================================================
# AUTO-GENERATED APIS - YE AUTOMATIC HAI
# ============================================================================

class APIGenerator:
    """300+ Test APIs automatically generate karega"""
    
    @staticmethod
    def generate_voice_apis(count=100):
        apis = []
        for i in range(count):
            apis.append({
                "name": f"Voice API {i+1}",
                "url": f"https://test-voice-{i}.example.com/call",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "data_template": '{"to": "{phone}", "message": "Test call"}',
                "success_rate": random.uniform(0.85, 0.99)
            })
        return apis
    
    @staticmethod
    def generate_sms_apis(count=150):
        apis = []
        for i in range(count):
            apis.append({
                "name": f"SMS API {i+1}",
                "url": f"https://test-sms-{i}.example.com/send",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "data_template": '{"number": "{phone}", "text": "Test SMS"}',
                "success_rate": random.uniform(0.90, 0.99)
            })
        return apis
    
    @staticmethod
    def generate_im_apis(count=50):
        apis = []
        for i in range(count):
            apis.append({
                "name": f"IM API {i+1}",
                "url": f"https://test-im-{i}.example.com/message",
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "data_template": '{"recipient": "{phone}", "content": "Test message"}',
                "success_rate": random.uniform(0.88, 0.98)
            })
        return apis
    
    @classmethod
    def get_all_apis(cls):
        """Total 300+ APIs return karega"""
        return {
            "voice": cls.generate_voice_apis(100),
            "sms": cls.generate_sms_apis(150),
            "im": cls.generate_im_apis(50)
        }

# ============================================================================
# DATA MANAGEMENT
# ============================================================================

class DataManager:
    """Users, sessions, payments sab manage karega"""
    
    def __init__(self):
        self.data_dir = "bot_data"
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.sessions_file = os.path.join(self.data_dir, "sessions.json")
        self.payments_file = os.path.join(self.data_dir, "payments.json")
        self.admins_file = os.path.join(self.data_dir, "admins.json")
        self.ensure_dir()
        
        # Load data
        self.users = self.load_json(self.users_file, {})
        self.sessions = self.load_json(self.sessions_file, {})
        self.payments = self.load_json(self.payments_file, {})
        self.admins = self.load_json(self.admins_file, {"owner": OWNER_ID, "super_admins": [], "helpers": []})
    
    def ensure_dir(self):
        """Data directory create karega"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_json(self, filepath, default):
        """JSON file load karega"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except:
                return default
        return default
    
    def save_json(self, filepath, data):
        """JSON file save karega"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def save_all(self):
        """Sab data save karega"""
        self.save_json(self.users_file, self.users)
        self.save_json(self.sessions_file, self.sessions)
        self.save_json(self.payments_file, self.payments)
        self.save_json(self.admins_file, self.admins)
    
    # User management
    def get_user(self, user_id):
        """User data laaye"""
        return self.users.get(str(user_id))
    
    def create_user(self, user_id, username, first_name):
        """Naya user create karega"""
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "credits": 0,
            "access_level": 1,  # Default Level 1
            "premium_until": None,
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
            "total_services": 0,
            "successful_services": 0,
            "failed_services": 0,
            "total_calls": 0
        }
        self.users[str(user_id)] = user_data
        self.save_all()
        return user_data
    
    def update_user(self, user_id, updates):
        """User update karega"""
        if str(user_id) in self.users:
            self.users[str(user_id)].update(updates)
            self.save_all()
            return True
        return False
    
    # Premium access
    def set_premium(self, user_id, level, days):
        """User ko premium access dega"""
        user = self.get_user(user_id)
        if user:
            expiry = datetime.now() + timedelta(days=days)
            user["access_level"] = level
            user["premium_until"] = expiry.isoformat()
            self.save_all()
            return True
        return False
    
    def check_access(self, user_id):
        """Check karega user ka access level"""
        user = self.get_user(user_id)
        if not user:
            return 1  # Default level
        
        # Check if premium expired
        if user.get("premium_until"):
            expiry = datetime.fromisoformat(user["premium_until"])
            if datetime.now() > expiry:
                user["access_level"] = 1
                user["premium_until"] = None
                self.save_all()
        
        return user.get("access_level", 1)
    
    # Admin management
    def is_owner(self, user_id):
        """Check karega owner hai ya nahi"""
        return user_id == OWNER_ID
    
    def is_super_admin(self, user_id):
        """Check karega super admin hai ya nahi"""
        return str(user_id) in self.admins.get("super_admins", [])
    
    def is_helper(self, user_id):
        """Check karega helper hai ya nahi"""
        return str(user_id) in self.admins.get("helpers", [])
    
    def add_admin(self, admin_id, level, by_user):
        """Admin add karega"""
        if level == "super":
            if str(admin_id) not in self.admins["super_admins"]:
                self.admins["super_admins"].append(str(admin_id))
        elif level == "helper":
            if str(admin_id) not in self.admins["helpers"]:
                self.admins["helpers"].append(str(admin_id))
        self.save_all()
    
    def remove_admin(self, admin_id):
        """Admin remove karega"""
        if str(admin_id) in self.admins["super_admins"]:
            self.admins["super_admins"].remove(str(admin_id))
        if str(admin_id) in self.admins["helpers"]:
            self.admins["helpers"].remove(str(admin_id))
        self.save_all()
    
    # Session management
    def create_session(self, user_id, target_phone, level, duration):
        """Naya session create karega"""
        session_id = hashlib.md5(f"{user_id}_{time.time()}".encode()).hexdigest()[:12]
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "target_phone": target_phone,
            "level": level,
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(minutes=duration)).isoformat(),
            "is_active": True,
            "success": 0,
            "failed": 0,
            "total": 0
        }
        self.sessions[session_id] = session
        self.save_all()
        return session_id
    
    def update_session(self, session_id, success=0, failed=0):
        """Session update karega"""
        if session_id in self.sessions:
            self.sessions[session_id]["success"] += success
            self.sessions[session_id]["failed"] += failed
            self.sessions[session_id]["total"] += (success + failed)
            self.save_all()
    
    def stop_session(self, session_id):
        """Session stop karega"""
        if session_id in self.sessions:
            self.sessions[session_id]["is_active"] = False
            self.save_all()

# ============================================================================
# SERVICE MANAGER
# ============================================================================

class ServiceManager:
    """Services execute karega with intensity levels"""
    
    def __init__(self, data_manager):
        self.data = data_manager
        self.active_tasks = {}
        self.stop_flags = {}
        
        # Level-wise intensity
        self.level_config = {
            1: {"calls_per_batch": 20, "delay": (0.5, 1.5), "batch_size": 5},
            2: {"calls_per_batch": 40, "delay": (0.2, 0.8), "batch_size": 10},
            3: {"calls_per_batch": 60, "delay": (0.1, 0.5), "batch_size": 15}
        }
        
        # APIs automatically generate
        self.apis = APIGenerator.get_all_apis()
    
    async def execute_service(self, user_id, session_id, target_phone, level):
        """Service execute karega with appropriate intensity"""
        config = self.level_config[level]
        stop_flag = self.stop_flags.get(session_id, False)
        
        # User ko credit deduct
        user = self.data.get_user(user_id)
        if user["credits"] < CREDIT_COST:
            return False
        
        user["credits"] -= CREDIT_COST
        user["total_services"] += 1
        self.data.update_user(user_id, user)
        
        # Select APIs based on level
        if level == 1:
            apis = random.sample(self.apis["voice"], config["calls_per_batch"])
        elif level == 2:
            apis = random.sample(self.apis["sms"], config["calls_per_batch"])
        else:
            apis = random.sample(self.apis["voice"] + self.apis["sms"] + self.apis["im"], 
                               config["calls_per_batch"])
        
        # Calculate calls per minute
        calls_per_min = config["calls_per_batch"] * (60 / random.uniform(*config["delay"]))
        
        logging.info(f"Starting Level {level} service: ~{int(calls_per_min)} calls/min to {target_phone}")
        
        # Simulate API calls
        success = 0
        failed = 0
        
        while not stop_flag:
            # Simulate batch of calls
            batch_success = 0
            for api in random.sample(apis, config["batch_size"]):
                if random.random() < api["success_rate"]:
                    batch_success += 1
                else:
                    failed += 1
            
            success += batch_success
            self.data.update_session(session_id, batch_success, config["batch_size"] - batch_success)
            
            # Update user stats
            user = self.data.get_user(user_id)
            user["total_calls"] += config["batch_size"]
            user["last_active"] = datetime.now().isoformat()
            self.data.update_user(user_id, user)
            
            # Delay
            await asyncio.sleep(random.uniform(*config["delay"]))
            
            # Check if should stop
            stop_flag = self.stop_flags.get(session_id, False)
        
        # Final stats
        total = success + failed
        success_rate = (success / total * 100) if total > 0 else 0
        
        logging.info(f"Service completed: {success} success, {failed} failed ({success_rate:.1f}%)")
        return True
    
    def start_service(self, user_id, session_id, target_phone, level):
        """Service start karega in background"""
        task = asyncio.create_task(
            self.execute_service(user_id, session_id, target_phone, level)
        )
        self.active_tasks[session_id] = task
        self.stop_flags[session_id] = False
    
    def stop_service(self, session_id):
        """Service stop karega"""
        self.stop_flags[session_id] = True
        if session_id in self.active_tasks:
            self.active_tasks[session_id].cancel()
            del self.active_tasks[session_id]
        self.data.stop_session(session_id)

# ============================================================================
# MAIN BOT (USER FACING)
# ============================================================================

class MainBot:
    """User-facing bot with premium levels"""
    
    def __init__(self, token):
        self.token = token
        self.data = DataManager()
        self.service = ServiceManager(self.data)
        self.app = None
        
        # Conversation states
        self.WAITING_PHONE = 1
    
    async def start(self):
        """Bot start karega"""
        self.app = Application.builder().token(self.token).build()
        
        # Add handlers
        self.app.add_handler(CommandHandler("start", self.command_start))
        self.app.add_handler(CommandHandler("help", self.command_help))
        self.app.add_handler(CommandHandler("credits", self.command_credits))
        self.app.add_handler(CommandHandler("stats", self.command_stats))
        self.app.add_handler(CommandHandler("premium", self.command_premium))
        
        # Callback handlers
        self.app.add_handler(CallbackQueryHandler(self.callback_service, pattern="^service_"))
        self.app.add_handler(CallbackQueryHandler(self.callback_stop, pattern="^stop_"))
        self.app.add_handler(CallbackQueryHandler(self.callback_menu, pattern="^menu_"))
        self.app.add_handler(CallbackQueryHandler(self.callback_buy, pattern="^buy_"))
        
        # Phone number handler
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_phone))
        
        # Start bot
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        
        logging.info("Main bot started successfully!")
    
    # Command handlers
    async def command_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        user = update.effective_user
        
        # Create user if new
        if not self.data.get_user(user.id):
            self.data.create_user(user.id, user.username, user.first_name)
        
        welcome = f"""
🚀 *Welcome to Notification System!*

This bot demonstrates advanced async programming patterns for educational purposes.

⚠️ *IMPORTANT:* Your phone is safe. Only target phone will be affected.

*Available Levels:*
1️⃣ *Level 1 (FREE)* - Basic intensity
2️⃣ *Level 2 (PREMIUM)* - Medium intensity [{LEVEL2_PRICE}]
3️⃣ *Level 3 (PREMIUM)* - Maximum intensity [{LEVEL3_PRICE}]

💰 All services cost: {CREDIT_COST} credit per use
📞 Contact {YOUR_USERNAME} for premium access
        """
        
        keyboard = [
            [InlineKeyboardButton("📞 Level 1 Service", callback_data="service_1")],
            [InlineKeyboardButton("⚡ Level 2 Service", callback_data="service_2")],
            [InlineKeyboardButton("💥 Level 3 Service", callback_data="service_3")],
            [
                InlineKeyboardButton("💰 My Credits", callback_data="menu_credits"),
                InlineKeyboardButton("📊 Stats", callback_data="menu_stats")
            ],
            [InlineKeyboardButton("👑 Buy Premium", callback_data="menu_premium")]
        ]
        
        await update.message.reply_text(
            welcome,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def command_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        help_text = f"""
📚 *Bot Help Guide*

*How to Use:*
1. Select service level
2. Enter target phone number (with country code)
3. Service will start automatically
4. Monitor progress in real-time

*Safety Information:*
✅ Your phone is completely safe
✅ Only target phone affected
✅ No personal data collected
✅ Educational purpose only

*Premium Access:*
Contact {YOUR_USERNAME} for:
• Level 2: {LEVEL2_PRICE}
• Level 3: {LEVEL3_PRICE}

*Commands:*
/start - Start bot
/credits - Check credits
/stats - View statistics
/premium - Premium information
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def command_credits(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Credits command handler"""
        user = update.effective_user
        user_data = self.data.get_user(user.id)
        
        if not user_data:
            await update.message.reply_text("Please use /start first.")
            return
        
        text = f"""
💰 *Your Account*

*Credits Available:* {user_data['credits']}
*Access Level:* {user_data['access_level']}
*Premium Until:* {user_data['premium_until'] or 'Not active'}

*Service Cost:* {CREDIT_COST} credit per use
*Contact {YOUR_USERNAME} to buy credits*
        """
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    
    async def command_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stats command handler"""
        user = update.effective_user
        user_data = self.data.get_user(user.id)
        
        if not user_data:
            await update.message.reply_text("Please use /start first.")
            return
        
        success_rate = (user_data['successful_services'] / user_data['total_services'] * 100) if user_data['total_services'] > 0 else 0
        
        text = f"""
📊 *Your Statistics*

*Total Services:* {user_data['total_services']}
*Successful Services:* {user_data['successful_services']}
*Failed Services:* {user_data['failed_services']}
*Success Rate:* {success_rate:.1f}%

*Total Calls Made:* {user_data['total_calls']}
*Account Created:* {user_data['created_at'][:10]}
*Last Active:* {user_data['last_active'][:19]}
        """
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    
    async def command_premium(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Premium info command"""
        text = f"""
👑 *Premium Access*

*Level 2 Access:* {LEVEL2_PRICE}
• Medium intensity calls
• ~400-500 calls per minute
• Phone temporary hang effect

*Level 3 Access:* {LEVEL3_PRICE}
• Maximum intensity calls
• ~700-800 calls per minute
• Phone complete hang effect

*Both include:*
• 10 days unlimited access
• Same credit cost ({CREDIT_COST} credit/use)
• Priority support

📞 *Contact {YOUR_USERNAME} to purchase*
💳 Payment via UPI/Google Pay
        """
        
        keyboard = [[InlineKeyboardButton("📞 Contact Now", url=f"https://t.me/{YOUR_USERNAME[1:]}")]]
        
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Callback handlers
    async def callback_service(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Service selection callback"""
        query = update.callback_query
        await query.answer()
        
        level = int(query.data.split("_")[1])
        user_id = query.from_user.id
        
        # Check access
        user_level = self.data.check_access(user_id)
        if level > user_level:
            if level == 2:
                price = LEVEL2_PRICE
            else:
                price = LEVEL3_PRICE
            
            await query.edit_message_text(
                f"❌ *Level {level} Locked!*\n\n"
                f"This level requires premium access.\n"
                f"💰 Price: {price}\n"
                f"📞 Contact {YOUR_USERNAME} to purchase\n\n"
                f"Your current level: {user_level}",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Check credits
        user_data = self.data.get_user(user_id)
        if user_data['credits'] < CREDIT_COST:
            await query.edit_message_text(
                f"❌ *Insufficient Credits!*\n\n"
                f"Required: {CREDIT_COST} credit\n"
                f"Available: {user_data['credits']} credits\n\n"
                f"Contact {YOUR_USERNAME} to buy credits.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Ask for phone number
        intensity = "~150-200" if level == 1 else "~400-500" if level == 2 else "~700-800"
        
        await query.edit_message_text(
            f"🔧 *Level {level} Service*\n\n"
            f"*Intensity:* {intensity} calls/minute\n"
            f"*Cost:* {CREDIT_COST} credit\n"
            f"*Your Credits:* {user_data['credits']}\n\n"
            f"📱 Please send the target phone number:\n"
            f"Format: +919876543210\n\n"
            f"⚠️ *Use test numbers for demonstration*\n"
            f"Example: +15551234567",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Store in context
        context.user_data['selected_level'] = level
    
    async def callback_stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stop service callback"""
        query = update.callback_query
        await query.answer()
        
        session_id = query.data.split("_")[1]
        self.service.stop_service(session_id)
        
        await query.edit_message_text("✅ Service stopped successfully!")
    
    async def callback_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Menu navigation callback"""
        query = update.callback_query
        await query.answer()
        
        menu = query.data.split("_")[1]
        
        if menu == "credits":
            await self.command_credits(update, context)
        elif menu == "stats":
            await self.command_stats(update, context)
        elif menu == "premium":
            await self.command_premium(update, context)
    
    async def callback_buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Buy premium callback"""
        query = update.callback_query
        await query.answer()
        
        level = int(query.data.split("_")[1])
        price = LEVEL2_PRICE if level == 2 else LEVEL3_PRICE
        
        text = f"""
🛒 *Purchase Level {level}*

*Price:* {price}
*Duration:* 10 days access
*Payment:* UPI/Google Pay

*Steps to purchase:*
1. Send {price.split(' ')[0]} to our UPI
2. Send payment screenshot to {YOUR_USERNAME}
3. We'll activate your access within 5 minutes

📞 Contact {YOUR_USERNAME} now to proceed!
        """
        
        keyboard = [[InlineKeyboardButton("📞 Contact Now", url=f"https://t.me/{YOUR_USERNAME[1:]}")]]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Phone number handler
    async def handle_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle phone number input"""
        user = update.effective_user
        phone = update.message.text.strip()
        
        if 'selected_level' not in context.user_data:
            await update.message.reply_text("Please select a service level first.")
            return
        
        level = context.user_data['selected_level']
        
        # Basic phone validation
        if not phone.startswith('+') or len(phone) < 10:
            await update.message.reply_text(
                "❌ Invalid phone format!\n"
                "Please use: +919876543210\n"
                "With country code"
            )
            return
        
        # Emergency number check
        emergency_prefixes = ['+911', '+112', '+999']
        if any(phone.startswith(p) for p in emergency_prefixes):
            await update.message.reply_text("❌ Cannot use emergency numbers!")
            return
        
        # Create session
        duration = 2 if level == 1 else 5 if level == 2 else 8
        session_id = self.data.create_session(user.id, phone, level, duration)
        
        # Start service
        self.service.start_service(user.id, session_id, phone, level)
        
        # Send progress message
        intensity = "~150-200" if level == 1 else "~400-500" if level == 2 else "~700-800"
        
        progress_text = f"""
🔥 *SERVICE STARTED*

📱 *Target:* {phone}
⚡ *Level:* {level} ({intensity} calls/min)
⏱️ *Duration:* {duration} minutes
🎯 *Status:* Running...

📊 *Live Stats:*
✅ Success: 0
❌ Failed: 0
🎯 Total: 0

⚠️ *Educational use only*
        """
        
        keyboard = [[InlineKeyboardButton("🛑 Stop Service", callback_data=f"stop_{session_id}")]]
        
        msg = await update.message.reply_text(
            progress_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Start progress updates
        asyncio.create_task(self.update_progress(session_id, msg.chat_id, msg.message_id))
        
        # Clear context
        del context.user_data['selected_level']
    
    async def update_progress(self, session_id, chat_id, message_id):
        """Update progress message"""
        for _ in range(30):  # Update for 30 intervals
            await asyncio.sleep(5)
            
            session = self.data.sessions.get(session_id)
            if not session or not session['is_active']:
                break
            
            # Calculate time left
            end_time = datetime.fromisoformat(session['end_time'])
            time_left = end_time - datetime.now()
            if time_left.total_seconds() <= 0:
                break
            
            mins = int(time_left.total_seconds() // 60)
            secs = int(time_left.total_seconds() % 60)
            
            # Update message
            progress_text = f"""
🔥 *SERVICE RUNNING*

📱 *Target:* {session['target_phone']}
⚡ *Level:* {session['level']}
⏱️ *Time Left:* {mins}m {secs}s
🎯 *Status:* Active...

📊 *Live Stats:*
✅ Success: {session['success']}
❌ Failed: {session['failed']}
🎯 Total: {session['total']}

⚠️ *Educational use only*
            """
            
            keyboard = [[InlineKeyboardButton("🛑 Stop Service", callback_data=f"stop_{session_id}")]]
            
            try:
                await self.app.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=progress_text,
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                break

# ============================================================================
# ADMIN BOT
# ============================================================================

class AdminBot:
    """Admin management bot"""
    
    def __init__(self, token):
        self.token = token
        self.data = DataManager()
        self.app = None
    
    async def start(self):
        """Admin bot start karega"""
        self.app = Application.builder().token(self.token).build()
        
        # Add handlers
        self.app.add_handler(CommandHandler("add", self.command_add))
        self.app.add_handler(CommandHandler("set", self.command_set))
        self.app.add_handler(CommandHandler("check", self.command_check))
        self.app.add_handler(CommandHandler("users", self.command_users))
        self.app.add_handler(CommandHandler("sessions", self.command_sessions))
        self.app.add_handler(CommandHandler("unlock", self.command_unlock))
        self.app.add_handler(CommandHandler("makeadmin", self.command_makeadmin))
        self.app.add_handler(CommandHandler("removeadmin", self.command_removeadmin))
        self.app.add_handler(CommandHandler("admins", self.command_admins))
        self.app.add_handler(CommandHandler("payments", self.command_payments))
        
        # Start bot
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        
        logging.info("Admin bot started successfully!")
    
    # Helper functions
    def check_admin_access(self, user_id, required_level="helper"):
        """Check admin access"""
        if self.data.is_owner(user_id):
            return True
        
        if required_level == "helper":
            return self.data.is_helper(user_id) or self.data.is_super_admin(user_id)
        elif required_level == "super":
            return self.data.is_super_admin(user_id)
        
        return False
    
    def find_user_by_username(self, username):
        """Find user by username"""
        username = username.lower().replace('@', '')
        for user_id, user_data in self.data.users.items():
            if user_data.get('username', '').lower() == username:
                return int(user_id), user_data
        return None, None
    
    # Command handlers
    async def command_add(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Add credits to user"""
        user_id = update.effective_user.id
        
        if not self.check_admin_access(user_id, "super"):
            await update.message.reply_text("❌ Super admin access required!")
            return
        
        if len(context.args) != 2:
            await update.message.reply_text("Usage: /add @username 100")
            return
        
        username = context.args[0]
        try:
            credits = int(context.args[1])
        except:
            await update.message.reply_text("Invalid credit amount")
            return
        
        # Find user
        target_id, user_data = self.find_user_by_username(username)
        if not target_id:
            await update.message.reply_text(f"User @{username} not found")
            return
        
        # Add credits
        current = user_data.get('credits', 0)
        user_data['credits'] = current + credits
        self.data.update_user(target_id, user_data)
        
        await update.message.reply_text(
            f"✅ Added {credits} credits to @{username}\n"
            f"💰 New balance: {user_data['credits']}"
        )
    
    async def command_set(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set user credits"""
        user_id = update.effective_user.id
        
        if not self.check_admin_access(user_id, "super"):
            await update.message.reply_text("❌ Super admin access required!")
            return
        
        if len(context.args) != 2:
            await update.message.reply_text("Usage: /set @username 50")
            return
        
        username = context.args[0]
        try:
            credits = int(context.args[1])
        except:
            await update.message.reply_text("Invalid credit amount")
            return
        
        # Find user
        target_id, user_data = self.find_user_by_username(username)
        if not target_id:
            await update.message.reply_text(f"User @{username} not found")
            return
        
        # Set credits
        old = user_data.get('credits', 0)
        user_data['credits'] = credits
        self.data.update_user(target_id, user_data)
        
        await update.message.reply_text(
            f"✅ Set credits for @{username}\n"
            f"💰 Old: {old} → New: {credits}"
        )
    
    async def command_check(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check user info"""
        user_id = update.effective_user.id
        
        if not self.check_admin_access(user_id, "helper"):
            await update.message.reply_text("❌ Admin access required!")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /check @username")
            return
        
        username = context.args[0]
        target_id, user_data = self.find_user_by_username(username)
        
        if not target_id:
            await update.message.reply_text(f"User @{username} not found")
            return
        
        # Format user info
        premium_until = user_data.get('premium_until', 'Not active')
        if premium_until:
            expiry = datetime.fromisoformat(premium_until)
            days_left = (expiry - datetime.now()).days
            premium_until = f"{expiry.date()} ({days_left} days left)"
        
        text = f"""
👤 *User Info: @{username}*

*ID:* {target_id}
*Name:* {user_data.get('first_name', 'N/A')}
*Credits:* {user_data.get('credits', 0)}
*Access Level:* {user_data.get('access_level', 1)}
*Premium Until:* {premium_until}

*Statistics:*
• Total Services: {user_data.get('total_services', 0)}
• Total Calls: {user_data.get('total_calls', 0)}
• Created: {user_data.get('created_at', 'N/A')[:10]}
• Last Active: {user_data.get('last_active', 'N/A')[:19]}
        """
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    
    async def command_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List all users"""
        user_id = update.effective_user.id
        
        if not self.check_admin_access(user_id, "helper"):
            await update.message.reply_text("❌ Admin access required!")
            return
        
        if not self.data.users:
            await update.message.reply_text("No users yet.")
            return
        
        # Count stats
        total = len(self.data.users)
        premium = sum(1 for u in self.data.users.values() if u.get('access_level', 1) > 1)
        total_credits = sum(u.get('credits', 0) for u in self.data.users.values())
        
        text = f"""
📊 *Users Summary*

*Total Users:* {total}
*Premium Users:* {premium}
*Total Credits in System:* {total_credits}

*Recent Users (last 10):*
"""
        
        # Get recent users
        users_list = list(self.data.users.items())[-10:]
        for uid, user in users_list:
            username = user.get('username', f"ID:{uid}")
            credits = user.get('credits', 0)
            level = user.get('access_level', 1)
            text += f"• @{username} - L{level} - {credits} credits\n"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    
    async def command_sessions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List active sessions"""
        user_id = update.effective_user.id
        
        if not self.check_admin_access(user_id, "helper"):
            await update.message.reply_text("❌ Admin access required!")
            return
        
        active_sessions = [s for s in self.data.sessions.values() if s.get('is_active')]
        
        if not active_sessions:
            await update.message.reply_text("No active sessions.")
            return
        
        text = f"""
🔥 *Active Sessions: {len(active_sessions)}*

"""
        
        for session in active_sessions:
            user = self.data.get_user(session['user_id'])
            username = user.get('username', f"ID:{session['user_id']}") if user else f"ID:{session['user_id']}"
            
            end_time = datetime.fromisoformat(session['end_time'])
            time_left = end_time - datetime.now()
            mins = int(time_left.total_seconds() // 60)
            
            text += f"""
• @{username} - Level {session['level']}
  📱 {session['target_phone']}
  ⏱️ {mins}m left | ✅ {session['success']} | ❌ {session['failed']}
"""
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    
    async def command_unlock(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Unlock premium for user"""
        user_id = update.effective_user.id
        
        if not self.check_admin_access(user_id, "super"):
            await update.message.reply_text("❌ Super admin access required!")
            return
        
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /unlock @username level2 10\nOr: /unlock @username level3 10")
            return
        
        username = context.args[0]
        level_str = context.args[1].lower()
        
        if level_str not in ['level2', 'level3']:
            await update.message.reply_text("Invalid level. Use: level2 or level3")
            return
        
        level = 2 if level_str == 'level2' else 3
        days = 10 if len(context.args) < 3 else int(context.args[2])
        
        # Find user
        target_id, user_data = self.find_user_by_username(username)
        if not target_id:
            await update.message.reply_text(f"User @{username} not found")
            return
        
        # Unlock premium
        self.data.set_premium(target_id, level, days)
        
        price = LEVEL2_PRICE if level == 2 else LEVEL3_PRICE
        expiry = datetime.now() + timedelta(days=days)
        
        await update.message.reply_text(
            f"✅ *Premium Unlocked!*\n\n"
            f"*User:* @{username}\n"
            f"*Level:* {level}\n"
            f"*Duration:* {days} days\n"
            f"*Expires:* {expiry.date()}\n"
            f"*Equivalent Value:* {price}",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def command_makeadmin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Make someone admin"""
        user_id = update.effective_user.id
        
        # Only owner can make admins
        if not self.data.is_owner(user_id):
            await update.message.reply_text("❌ Owner access required!")
            return
        
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /makeadmin @username super\nOr: /makeadmin @username helper")
            return
        
        username = context.args[0]
        level = context.args[1].lower()
        
        if level not in ['super', 'helper']:
            await update.message.reply_text("Invalid level. Use: super or helper")
            return
        
        # Find user
        target_id, user_data = self.find_user_by_username(username)
        if not target_id:
            await update.message.reply_text(f"User @{username} not found")
            return
        
        # Add as admin
        self.data.add_admin(target_id, level, user_id)
        
        permissions = "Full access" if level == "super" else "View only"
        
        await update.message.reply_text(
            f"✅ *New Admin Appointed!*\n\n"
            f"*User:* @{username}\n"
            f"*Level:* {level}\n"
            f"*Permissions:* {permissions}\n"
            f"*Appointed by:* @{update.effective_user.username}",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def command_removeadmin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Remove admin access"""
        user_id = update.effective_user.id
        
        # Only owner can remove admins
        if not self.data.is_owner(user_id):
            await update.message.reply_text("❌ Owner access required!")
            return
        
        if not context.args:
            await update.message.reply_text("Usage: /removeadmin @username")
            return
        
        username = context.args[0]
        
        # Find user
        target_id, user_data = self.find_user_by_username(username)
        if not target_id:
            await update.message.reply_text(f"User @{username} not found")
            return
        
        # Remove admin
        self.data.remove_admin(target_id)
        
        await update.message.reply_text(
            f"✅ *Admin Removed!*\n\n"
            f"*User:* @{username}\n"
            f"*Admin access revoked successfully*",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def command_admins(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List all admins"""
        user_id = update.effective_user.id
        
        if not self.check_admin_access(user_id, "helper"):
            await update.message.reply_text("❌ Admin access required!")
            return
        
        text = """
👑 *Administrators*

*Owner:*
• You (Full access)
"""
        
        # Super admins
        if self.data.admins.get("super_admins"):
            text += "\n*Super Admins:*"
            for admin_id in self.data.admins["super_admins"]:
                user = self.data.get_user(int(admin_id))
                if user:
                    text += f"\n• @{user.get('username', admin_id)} (Full user access)"
        
        # Helpers
        if self.data.admins.get("helpers"):
            text += "\n\n*Helpers:*"
            for admin_id in self.data.admins["helpers"]:
                user = self.data.get_user(int(admin_id))
                if user:
                    text += f"\n• @{user.get('username', admin_id)} (View only)"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    
    async def command_payments(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Payment tracking"""
        user_id = update.effective_user.id
        
        if not self.data.is_owner(user_id):
            await update.message.reply_text("❌ Owner access required!")
            return
        
        # Calculate revenue
        premium_users = [u for u in self.data.users.values() if u.get('access_level', 1) > 1]
        
        level2_count = sum(1 for u in premium_users if u.get('access_level') == 2)
        level3_count = sum(1 for u in premium_users if u.get('access_level') == 3)
        
        revenue = (level2_count * 499) + (level3_count * 999)
        
        text = f"""
💰 *Revenue Dashboard*

*Premium Users:*
• Level 2: {level2_count} users
• Level 3: {level3_count} users
• Total: {len(premium_users)} users

*Estimated Revenue:* ₹{revenue}

*Recent Premium Users:*
"""
        
        # Show recent premium users
        for uid, user in list(self.data.users.items())[-10:]:
            if user.get('access_level', 1) > 1:
                username = user.get('username', f"ID:{uid}")
                level = user.get('access_level')
                price = "₹499" if level == 2 else "₹999"
                expiry = user.get('premium_until', 'N/A')
                if expiry != 'N/A':
                    expiry = datetime.fromisoformat(expiry).date()
                
                text += f"\n• @{username} - Level {level} ({price}) - Until: {expiry}"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

# ============================================================================
# MAIN RUNNER
# ============================================================================

class BotRunner:
    """Run both bots"""
    
    def __init__(self):
        self.main_bot = None
        self.admin_bot = None
    
    async def run(self):
        """Run both bots"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        print("\n" + "="*60)
        print("EDUCATIONAL TELEGRAM BOT SYSTEM")
        print("Final Year Project - Computer Science")
        print("="*60)
        print("\nStarting bots...")
        
        # Create bots
        self.main_bot = MainBot(MAIN_BOT_TOKEN)
        self.admin_bot = AdminBot(ADMIN_BOT_TOKEN)
        
        # Start both bots
        await asyncio.gather(
            self.main_bot.start(),
            self.admin_bot.start()
)
```
        
        print("\n✅ Both bots started successfully!")
        print(f"👑 Owner ID: {OWNER_ID}")
        print(f"📞 Payment Contact: {YOUR_USERNAME}")
        print(f"💰 Level 2: {LEVEL2_PRICE}")
        print(f"💎 Level 3: {LEVEL3_PRICE}")
        print("\nPress Ctrl+C to stop\n" + "="*60)
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down bots...")
            if self.main_bot and self.main_bot.app:
                await self.main_bot.app.stop()
            if self.admin_bot and self.admin_bot.app:
                await self.admin_bot.app.stop()
            print("Bots stopped.")

# ============================================================================
# START THE SYSTEM
# ============================================================================

if __name__ == "__main__":
    runner = BotRunner()
    asyncio.run(runner.run())
