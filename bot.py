#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎰 SUPER ADDICTIVE BETTING BOT 🎰
Win Big Money! Daily Rewards! Refer & Earn!
Owner: @TGxTHOMASx
"""

import telebot
from telebot import types
import json
import os
import random
import time
from datetime import datetime, timedelta
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

MAIN_BOT_TOKEN = "8580329271:AAFPmbJ9JraVIAkHbcZtQ5tohIDwWHvjx3I"
ADMIN_BOT_TOKEN = "8553759431:AAH4BgRJcm1-JI5oBDoYIxR3Vby7oUmJgZQ"

OWNER_ID = 7417241499
OWNER_USERNAME = "@TGxTHOMASx"
BOT_USERNAME = "YourBettingBot"  # Your bot username

# UPI Details
UPI_ID = "yourname@paytm"
UPI_QR = "https://i.imgur.com/your-qr.jpg"

# Money Limits
MIN_DEPOSIT = 10
MIN_WITHDRAWAL = 100  # Higher to keep money in system
MIN_BET = 10
MAX_BET = 5000

# Bonuses & Rewards
SIGNUP_BONUS = 50
DAILY_REWARD = 20
STREAK_BONUS = {3: 50, 7: 150, 15: 500, 30: 1500}
REFERRAL_BONUS = 30  # When friend joins
REFERRAL_COMMISSION = 0.1  # 10% of friend's deposits

# Game Payouts
COLOR_PAYOUT = 1.95  # Slightly less than 2x (house edge)
NUMBER_PAYOUT = 8.5  # Slightly less than 9x

# VIP Levels
VIP_LEVELS = {
    0: {"name": "Bronze", "deposit": 0, "cashback": 0},
    1: {"name": "Silver", "deposit": 1000, "cashback": 0.02},
    2: {"name": "Gold", "deposit": 5000, "cashback": 0.05},
    3: {"name": "Platinum", "deposit": 10000, "cashback": 0.08},
    4: {"name": "Diamond", "deposit": 25000, "cashback": 0.12}
}

# Daily Missions
DAILY_MISSIONS = {
    "bet_5": {"name": "Place 5 bets", "reward": 25, "target": 5},
    "win_3": {"name": "Win 3 games", "reward": 40, "target": 3},
    "deposit": {"name": "Deposit ₹50+", "reward": 30, "target": 50},
    "refer_1": {"name": "Refer 1 friend", "reward": 50, "target": 1}
}

# ============================================================================
# FILES
# ============================================================================

FILES = {
    "users": "users.json",
    "deposits": "deposits.json",
    "withdrawals": "withdrawals.json",
    "bets": "bets.json",
    "stats": "stats.json",
    "lottery": "lottery.json"
}

def init_files():
    for file in FILES.values():
        if not os.path.exists(file):
            default = [] if file in ["deposits.json", "withdrawals.json", "bets.json", "lottery.json"] else {}
            if file == "stats.json":
                default = {
                    "total_users": 0,
                    "total_deposits": 0,
                    "total_withdrawals": 0,
                    "total_bets": 0,
                    "total_profit": 0,
                    "today_profit": 0,
                    "last_reset": datetime.now().isoformat()
                }
            with open(file, 'w') as f:
                json.dump(default, f, indent=2)

def load_json(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except:
        return [] if file in ["deposits.json", "withdrawals.json", "bets.json", "lottery.json"] else {}

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2, default=str)

init_files()

users = load_json(FILES["users"])
deposits = load_json(FILES["deposits"])
withdrawals = load_json(FILES["withdrawals"])
bets = load_json(FILES["bets"])
stats = load_json(FILES["stats"])
lottery_entries = load_json(FILES["lottery"])

bot = telebot.TeleBot(MAIN_BOT_TOKEN, parse_mode="HTML")
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN, parse_mode="HTML")

logger.info(f"✅ Main Bot: @{bot.get_me().username}")
logger.info(f"✅ Admin Bot: @{admin_bot.get_me().username}")

temp_data = {}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_owner(uid):
    return uid == OWNER_ID

def generate_id():
    return hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:10].upper()

def get_user(uid):
    uid_str = str(uid)
    if uid_str not in users:
        users[uid_str] = {
            "user_id": uid,
            "name": "",
            "username": "",
            "balance": SIGNUP_BONUS,
            "total_deposit": 0,
            "total_withdrawal": 0,
            "total_bets": 0,
            "total_won": 0,
            "total_lost": 0,
            "win_count": 0,
            "loss_count": 0,
            "joined": datetime.now().isoformat(),
            "last_claim": None,
            "streak": 0,
            "level": 0,
            "vip_level": 0,
            "referrals": [],
            "referred_by": None,
            "daily_missions": {},
            "spin_available": True,
            "lottery_tickets": 0
        }
        save_json(FILES["users"], users)
        stats["total_users"] += 1
        save_json(FILES["stats"], stats)
    return users[uid_str]

def update_balance(uid, amount):
    uid_str = str(uid)
    if uid_str in users:
        users[uid_str]["balance"] += amount
        save_json(FILES["users"], users)
        return users[uid_str]["balance"]
    return 0

def get_vip_level(user):
    """Calculate VIP level based on total deposits"""
    total = user.get("total_deposit", 0)
    level = 0
    for lvl, data in sorted(VIP_LEVELS.items(), reverse=True):
        if total >= data["deposit"]:
            level = lvl
            break
    return level

def get_vip_icon(level):
    icons = {0: "🥉", 1: "🥈", 2: "🥇", 3: "💎", 4: "👑"}
    return icons.get(level, "🥉")

def check_daily_reward(user):
    """Check if user can claim daily reward"""
    last_claim = user.get("last_claim")
    if not last_claim:
        return True
    
    try:
        last_date = datetime.fromisoformat(last_claim).date()
        today = datetime.now().date()
        return today > last_date
    except:
        return True

def update_streak(user):
    """Update login streak"""
    last_claim = user.get("last_claim")
    if not last_claim:
        user["streak"] = 1
        return
    
    try:
        last_date = datetime.fromisoformat(last_claim).date()
        yesterday = (datetime.now() - timedelta(days=1)).date()
        today = datetime.now().date()
        
        if last_date == yesterday:
            user["streak"] += 1
        elif last_date < yesterday:
            user["streak"] = 1
    except:
        user["streak"] = 1

def format_number(num):
    """Format number with commas"""
    return f"{num:,}"

def get_leaderboard(limit=10):
    """Get top earners"""
    sorted_users = sorted(
        users.items(),
        key=lambda x: x[1].get("total_won", 0) - x[1].get("total_lost", 0),
        reverse=True
    )
    return sorted_users[:limit]

# ============================================================================
# MAIN BOT - USER INTERFACE
# ============================================================================

@bot.message_handler(commands=['start'])
def cmd_start(m):
    # Check referral
    if len(m.text.split()) > 1:
        ref_id = m.text.split()[1]
        if ref_id.isdigit() and int(ref_id) != m.from_user.id:
            referrer_id = str(ref_id)
            if referrer_id in users:
                user = get_user(m.from_user.id)
                if not user.get("referred_by"):
                    # New referral
                    user["referred_by"] = int(ref_id)
                    users[referrer_id]["referrals"].append(m.from_user.id)
                    
                    # Give bonus to both
                    update_balance(m.from_user.id, REFERRAL_BONUS)
                    update_balance(int(ref_id), REFERRAL_BONUS)
                    
                    save_json(FILES["users"], users)
                    
                    bot.send_message(
                        m.chat.id,
                        f"🎁 <b>REFERRAL BONUS!</b>\n\n"
                        f"✅ You got ₹{REFERRAL_BONUS} bonus!\n"
                        f"✅ Your friend also got ₹{REFERRAL_BONUS}!\n\n"
                        f"💰 New Balance: ₹{user['balance'] + REFERRAL_BONUS}"
                    )
                    
                    try:
                        bot.send_message(
                            int(ref_id),
                            f"🎉 <b>NEW REFERRAL!</b>\n\n"
                            f"👤 {m.from_user.first_name} joined using your link!\n"
                            f"💰 You earned ₹{REFERRAL_BONUS}!"
                        )
                    except:
                        pass
    
    user = get_user(m.from_user.id)
    
    # Update user info
    uid_str = str(m.from_user.id)
    users[uid_str]["name"] = m.from_user.first_name or ""
    users[uid_str]["username"] = m.from_user.username or ""
    
    # Update VIP level
    users[uid_str]["vip_level"] = get_vip_level(user)
    save_json(FILES["users"], users)
    
    vip_icon = get_vip_icon(user["vip_level"])
    vip_name = VIP_LEVELS[user["vip_level"]]["name"]
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🎨 Color Game", "🔢 Number Game")
    kb.row("💰 Deposit", "💸 Withdraw")
    kb.row("🎁 Daily Bonus", "🎰 Lucky Spin")
    kb.row("👥 Refer & Earn", "🏆 Leaderboard")
    kb.row("👛 Wallet", "📊 Stats", "❓ Help")
    
    welcome = f"""
╔════════════════════════════════╗
║   🎰 <b>WIN MONEY BOT</b> 🎰        ║
╚════════════════════════════════╝

🔥 <b>Welcome {m.from_user.first_name}!</b>

<b>━━━━━ YOUR ACCOUNT ━━━━━</b>

{vip_icon} <b>VIP:</b> {vip_name}
👛 <b>Balance:</b> ₹{format_number(user['balance'])}
🔥 <b>Streak:</b> {user.get('streak', 0)} days
🆔 <b>ID:</b> <code>{m.from_user.id}</code>

<b>━━━━━ PLAY & WIN ━━━━━</b>

🎨 <b>Color Game</b> - Win 2x money!
🔢 <b>Number Game</b> - Win 9x money!

<b>━━━━━ EARN MORE ━━━━━</b>

🎁 Daily login bonus
🎰 Lucky spin (FREE!)
👥 Refer friends = ₹{REFERRAL_BONUS}
🏆 Top players win prizes

<b>━━━━━━━━━━━━━━━━━━━━━</b>

💡 <b>Play Smart, Win Big!</b>
📞 Support: {OWNER_USERNAME}
"""
    
    bot.send_message(m.chat.id, welcome, reply_markup=kb)
    
    # Show daily bonus notification if available
    if check_daily_reward(user):
        bot.send_message(
            m.chat.id,
            "🎁 <b>DAILY BONUS AVAILABLE!</b>\n\n"
            "Click '🎁 Daily Bonus' to claim!"
        )

@bot.message_handler(func=lambda m: m.text == "🎁 Daily Bonus")
def btn_daily_bonus(m):
    user = get_user(m.from_user.id)
    
    if not check_daily_reward(user):
        next_claim = datetime.fromisoformat(user["last_claim"]) + timedelta(days=1)
        hours_left = (next_claim - datetime.now()).total_seconds() / 3600
        return bot.send_message(
            m.chat.id,
            f"⏰ <b>Already claimed today!</b>\n\n"
            f"⏳ Next claim in: {int(hours_left)} hours"
        )
    
    # Update streak
    update_streak(user)
    
    # Base reward
    reward = DAILY_REWARD
    
    # Streak bonus
    streak = user["streak"]
    streak_extra = 0
    for days, bonus in sorted(STREAK_BONUS.items()):
        if streak >= days:
            streak_extra = bonus
    
    total_reward = reward + streak_extra
    
    # Update balance
    update_balance(m.from_user.id, total_reward)
    
    # Update last claim
    uid_str = str(m.from_user.id)
    users[uid_str]["last_claim"] = datetime.now().isoformat()
    save_json(FILES["users"], users)
    
    # Show animation
    msg = bot.send_message(
        m.chat.id,
        "🎁 <b>Opening gift...</b>\n\n"
        "⏳ Please wait..."
    )
    
    time.sleep(1)
    
    reward_msg = f"""
🎉 <b>DAILY BONUS CLAIMED!</b>

<b>━━━━━ REWARDS ━━━━━</b>

💰 <b>Daily Bonus:</b> ₹{reward}
"""
    
    if streak_extra > 0:
        reward_msg += f"🔥 <b>Streak Bonus:</b> ₹{streak_extra}\n"
    
    reward_msg += f"""
✅ <b>Total Earned:</b> ₹{total_reward}

<b>━━━━━ STREAK ━━━━━</b>

🔥 <b>Current Streak:</b> {streak} days

<b>Next Milestones:</b>
"""
    
    for days, bonus in sorted(STREAK_BONUS.items()):
        if days > streak:
            reward_msg += f"• {days} days = ₹{bonus}\n"
            break
    
    reward_msg += f"""
<b>━━━━━━━━━━━━━━━━━━━</b>

👛 <b>New Balance:</b> ₹{format_number(user['balance'])}

💡 <b>Come back tomorrow for more!</b>
"""
    
    bot.edit_message_text(reward_msg, m.chat.id, msg.message_id)

@bot.message_handler(func=lambda m: m.text == "🎰 Lucky Spin")
def btn_lucky_spin(m):
    user = get_user(m.from_user.id)
    
    if not user.get("spin_available", True):
        return bot.send_message(
            m.chat.id,
            "⏰ <b>Spin used today!</b>\n\n"
            "🎰 Come back tomorrow for free spin!"
        )
    
    # Disable spin
    uid_str = str(m.from_user.id)
    users[uid_str]["spin_available"] = False
    save_json(FILES["users"], users)
    
    # Show spinning animation
    prizes = [10, 20, 30, 50, 100, 5, 15, 25, 0, 200]
    
    msg = bot.send_message(
        m.chat.id,
        "🎰 <b>LUCKY SPIN!</b>\n\n"
        "🎲 Spinning...\n\n"
        "⏳ Please wait..."
    )
    
    # Animate
    for i in range(5):
        time.sleep(0.5)
        bot.edit_message_text(
            f"🎰 <b>LUCKY SPIN!</b>\n\n"
            f"{'🎲' * (i+1)}\n\n"
            f"⏳ Spinning...",
            m.chat.id,
            msg.message_id
        )
    
    # Random prize (weighted towards lower)
    weights = [15, 20, 15, 10, 5, 15, 10, 5, 3, 2]
    prize = random.choices(prizes, weights=weights)[0]
    
    if prize > 0:
        update_balance(m.from_user.id, prize)
        result = f"""
🎉 <b>WINNER!</b>

🎰 <b>You won:</b> ₹{prize}

👛 <b>New Balance:</b> ₹{format_number(user['balance'] + prize)}

💡 <b>Free spin tomorrow!</b>
"""
    else:
        result = f"""
😔 <b>Better luck next time!</b>

🎰 <b>Prize:</b> ₹0

💡 <b>Try again tomorrow!</b>
👛 <b>Balance:</b> ₹{format_number(user['balance'])}
"""
    
    bot.edit_message_text(result, m.chat.id, msg.message_id)

@bot.message_handler(func=lambda m: m.text == "👥 Refer & Earn")
def btn_referral(m):
    user = get_user(m.from_user.id)
    
    ref_link = f"https://t.me/{BOT_USERNAME}?start={m.from_user.id}"
    ref_count = len(user.get("referrals", []))
    ref_earnings = ref_count * REFERRAL_BONUS
    
    msg = f"""
👥 <b>REFER & EARN</b>

<b>━━━━━ YOUR STATS ━━━━━</b>

👤 <b>Referrals:</b> {ref_count}
💰 <b>Earned:</b> ₹{format_number(ref_earnings)}

<b>━━━━━ HOW IT WORKS ━━━━━</b>

1️⃣ Share your link
2️⃣ Friend joins & deposits
3️⃣ You get ₹{REFERRAL_BONUS} instantly
4️⃣ + {int(REFERRAL_COMMISSION*100)}% of friend's deposits!

<b>━━━━━ YOUR LINK ━━━━━</b>

<code>{ref_link}</code>

👆 <b>Click to copy</b>

<b>━━━━━━━━━━━━━━━━━━━</b>

💡 <b>More friends = More money!</b>
"""
    
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📤 Share Link", url=f"https://t.me/share/url?url={ref_link}&text=Join this amazing betting bot and get ₹{SIGNUP_BONUS} signup bonus!"))
    
    bot.send_message(m.chat.id, msg, reply_markup=mk)

@bot.message_handler(func=lambda m: m.text == "🏆 Leaderboard")
def btn_leaderboard(m):
    top_users = get_leaderboard(10)
    
    msg = "🏆 <b>TOP EARNERS</b>\n\n"
    msg += "<b>━━━━━━━━━━━━━━━━━━━</b>\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    
    for i, (uid, user_data) in enumerate(top_users, 1):
        name = user_data.get("name", "User")
        profit = user_data.get("total_won", 0) - user_data.get("total_lost", 0)
        
        medal = medals[i-1] if i <= 3 else f"{i}."
        
        msg += f"{medal} <b>{name}</b>\n"
        msg += f"   💰 Profit: ₹{format_number(profit)}\n\n"
    
    msg += "<b>━━━━━━━━━━━━━━━━━━━</b>\n\n"
    msg += "💡 <b>Play more to rank up!</b>"
    
    bot.send_message(m.chat.id, msg)

@bot.message_handler(func=lambda m: m.text == "🎨 Color Game")
def btn_color_game(m):
    user = get_user(m.from_user.id)
    
    if user['balance'] < MIN_BET:
        return bot.send_message(
            m.chat.id,
            f"❌ <b>Insufficient balance!</b>\n\n"
            f"👛 Balance: ₹{user['balance']}\n"
            f"💰 Min bet: ₹{MIN_BET}\n\n"
            f"💸 Please deposit to play!"
        )
    
    mk = types.InlineKeyboardMarkup()
    mk.row(
        types.InlineKeyboardButton("🔴 Red", callback_data="color_red"),
        types.InlineKeyboardButton("🟢 Green", callback_data="color_green")
    )
    mk.add(types.InlineKeyboardButton("🟣 Violet", callback_data="color_violet"))
    
    vip_icon = get_vip_icon(user["vip_level"])
    cashback = VIP_LEVELS[user["vip_level"]]["cashback"]
    
    bot.send_message(
        m.chat.id,
        f"""
🎨 <b>COLOR PREDICTION</b>

<b>━━━━━ HOW TO PLAY ━━━━━</b>

1️⃣ Choose your color
2️⃣ Enter bet amount
3️⃣ Wait for result
4️⃣ <b>WIN 2X MONEY!</b>

<b>━━━━━ YOUR INFO ━━━━━</b>

{vip_icon} <b>VIP:</b> {VIP_LEVELS[user["vip_level"]]["name"]}
👛 <b>Balance:</b> ₹{format_number(user['balance'])}
💰 <b>Min:</b> ₹{MIN_BET} | <b>Max:</b> ₹{format_number(MAX_BET)}
{"💎 <b>Cashback:</b> " + str(int(cashback*100)) + "%" if cashback > 0 else ""}

<b>━━━━━ WIN EXAMPLES ━━━━━</b>

Bet ₹100 → Win ₹195
Bet ₹500 → Win ₹975
Bet ₹1000 → Win ₹1,950

👇 <b>Choose your lucky color:</b>
""",
        reply_markup=mk
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("color_"))
def cb_color_choice(c):
    color = c.data.replace("color_", "")
    
    temp_data[c.from_user.id] = {
        'game': 'color',
        'choice': color
    }
    
    color_emoji = {"red": "🔴", "green": "🟢", "violet": "🟣"}
    color_name = color.title()
    
    bot.answer_callback_query(c.id, f"Selected: {color_emoji[color]} {color_name}")
    
    msg = bot.send_message(
        c.message.chat.id,
        f"✅ <b>Color:</b> {color_emoji[color]} <b>{color_name}</b>\n\n"
        f"💰 <b>Enter bet amount:</b>\n\n"
        f"Min: ₹{MIN_BET} | Max: ₹{format_number(MAX_BET)}\n\n"
        f"Or /cancel to cancel"
    )
    
    bot.register_next_step_handler(msg, process_color_bet)

def process_color_bet(m):
    if m.text == '/cancel':
        if m.from_user.id in temp_data:
            del temp_data[m.from_user.id]
        return bot.send_message(m.chat.id, "❌ <b>Game cancelled!</b>")
    
    try:
        bet_amount = int(m.text.strip())
    except:
        return bot.send_message(m.chat.id, "❌ <b>Invalid!</b> Enter numbers only.")
    
    if bet_amount < MIN_BET:
        return bot.send_message(m.chat.id, f"❌ <b>Minimum bet:</b> ₹{MIN_BET}")
    
    if bet_amount > MAX_BET:
        return bot.send_message(m.chat.id, f"❌ <b>Maximum bet:</b> ₹{format_number(MAX_BET)}")
    
    user = get_user(m.from_user.id)
    
    if bet_amount > user['balance']:
        return bot.send_message(
            m.chat.id,
            f"❌ <b>Insufficient balance!</b>\n\n"
            f"👛 Balance: ₹{format_number(user['balance'])}\n"
            f"💰 Bet: ₹{format_number(bet_amount)}\n\n"
            f"💸 Please deposit!"
        )
    
    data = temp_data.get(m.from_user.id)
    if not data:
        return bot.send_message(m.chat.id, "❌ Session expired!")
    
    user_choice = data['choice']
    color_emoji = {"red": "🔴", "green": "🟢", "violet": "🟣"}
    
    # Deduct bet
    update_balance(m.from_user.id, -bet_amount)
    
    # Animation
    loading = bot.send_message(
        m.chat.id,
        f"🎲 <b>GAME STARTING...</b>\n\n"
        f"🎨 Your choice: {color_emoji[user_choice]}\n"
        f"💰 Bet: ₹{format_number(bet_amount)}\n\n"
        f"⏳ Please wait..."
    )
    
    # Spinning animation
    for i in range(3):
        time.sleep(0.7)
        colors = ["🔴", "🟢", "🟣"]
        spinning = " ".join([random.choice(colors) for _ in range(3)])
        bot.edit_message_text(
            f"🎲 <b>SPINNING...</b>\n\n"
            f"{spinning}\n\n"
            f"💰 Bet: ₹{format_number(bet_amount)}",
            m.chat.id,
            loading.message_id
        )
    
    time.sleep(0.5)
    
    # Result (slightly favor house)
    colors = ["red", "green", "violet"]
    # 32% chance for user's choice, 34% each for others
    if random.random() < 0.32:
        result_color = user_choice
    else:
        other_colors = [c for c in colors if c != user_choice]
        result_color = random.choice(other_colors)
    
    # Check win
    uid_str = str(m.from_user.id)
    
    if result_color == user_choice:
        # WIN!
        win_amount = int(bet_amount * COLOR_PAYOUT)
        update_balance(m.from_user.id, win_amount)
        
        users[uid_str]["total_won"] += win_amount
        users[uid_str]["win_count"] += 1
        users[uid_str]["total_bets"] += 1
        save_json(FILES["users"], users)
        
        profit = win_amount - bet_amount
        
        result = f"""
🎉 <b>WINNER! WINNER!</b>

🎨 <b>Result:</b> {color_emoji[result_color]} {result_color.title()}
✅ <b>Your choice:</b> {color_emoji[user_choice]} {user_choice.title()}

<b>━━━━━ WINNINGS ━━━━━</b>

💰 <b>Bet:</b> ₹{format_number(bet_amount)}
🎁 <b>Won:</b> ₹{format_number(win_amount)}
💚 <b>Profit:</b> +₹{format_number(profit)}

👛 <b>New Balance:</b> ₹{format_number(user['balance'])}

🔥 <b>Keep winning!</b>
"""
        
        # Record bet
        bets.append({
            "user_id": m.from_user.id,
            "game": "color",
            "bet": bet_amount,
            "result": "win",
            "profit": profit,
            "time": datetime.now().isoformat()
        })
        save_json(FILES["bets"], bets)
        
    else:
        # LOSS (but show "almost won" psychology)
        users[uid_str]["total_lost"] += bet_amount
        users[uid_str]["loss_count"] += 1
        users[uid_str]["total_bets"] += 1
        
        # VIP Cashback
        cashback_amount = 0
        vip_level = user["vip_level"]
        cashback_rate = VIP_LEVELS[vip_level]["cashback"]
        
        if cashback_rate > 0:
            cashback_amount = int(bet_amount * cashback_rate)
            update_balance(m.from_user.id, cashback_amount)
        
        save_json(FILES["users"], users)
        
        # Near-miss psychology
        almost_msgs = [
            "🔥 So close! Try again!",
            "💪 Almost there! One more!",
            "⚡ Next one is yours!",
            "🎯 You were so close!"
        ]
        
        result = f"""
😔 <b>OOPS! SO CLOSE!</b>

🎨 <b>Result:</b> {color_emoji[result_color]} {result_color.title()}
❌ <b>Your choice:</b> {color_emoji[user_choice]} {user_choice.title()}

<b>━━━━━━━━━━━━━━━━━━━</b>

💔 <b>Lost:</b> ₹{format_number(bet_amount)}
"""
        
        if cashback_amount > 0:
            result += f"💎 <b>VIP Cashback:</b> +₹{cashback_amount}\n"
        
        result += f"""
👛 <b>Balance:</b> ₹{format_number(user['balance'])}

{random.choice(almost_msgs)}
💡 <b>Double your bet to recover!</b>
"""
        
        # Record bet
        bets.append({
            "user_id": m.from_user.id,
            "game": "color",
            "bet": bet_amount,
            "result": "loss",
            "profit": -bet_amount,
            "time": datetime.now().isoformat()
        })
        save_json(FILES["bets"], bets)
        
        # Update stats
        stats["total_profit"] += bet_amount - cashback_amount
        stats["today_profit"] += bet_amount - cashback_amount
        save_json(FILES["stats"], stats)
    
    bot.edit_message_text(result, m.chat.id, loading.message_id)
    
    # Quick play again button
    mk = types.InlineKeyboardMarkup()
    mk.row(
        types.InlineKeyboardButton("🔴 Red", callback_data="color_red"),
        types.InlineKeyboardButton("🟢 Green", callback_data="color_green")
    )
    mk.add(types.InlineKeyboardButton("🟣 Violet", callback_data="color_violet"))
    
    bot.send_message(
        m.chat.id,
        "🎮 <b>Play Again?</b>",
        reply_markup=mk
    )
    
    # Clean temp
    if m.from_user.id in temp_data:
        del temp_data[m.from_user.id]

@bot.message_handler(func=lambda m: m.text == "🔢 Number Game")
def btn_number_game(m):
    user = get_user(m.from_user.id)
    
    if user['balance'] < MIN_BET:
        return bot.send_message(
            m.chat.id,
            f"❌ <b>Insufficient balance!</b>\n\n"
            f"👛 Balance: ₹{user['balance']}\n"
            f"💰 Min bet: ₹{MIN_BET}\n\n"
            f"💸 Deposit now!"
        )
    
    mk = types.InlineKeyboardMarkup()
    row1 = [types.InlineKeyboardButton(str(i), callback_data=f"num_{i}") for i in range(5)]
    row2 = [types.InlineKeyboardButton(str(i), callback_data=f"num_{i}") for i in range(5, 10)]
    mk.row(*row1)
    mk.row(*row2)
    
    vip_icon = get_vip_icon(user["vip_level"])
    
    bot.send_message(
        m.chat.id,
        f"""
🔢 <b>NUMBER GAME</b>

<b>━━━━━ HOW TO PLAY ━━━━━</b>

1️⃣ Pick a number (0-9)
2️⃣ Enter bet amount
3️⃣ Win = <b>9X MONEY!</b>

<b>━━━━━ YOUR INFO ━━━━━</b>

{vip_icon} <b>VIP:</b> {VIP_LEVELS[user["vip_level"]]["name"]}
👛 <b>Balance:</b> ₹{format_number(user['balance'])}
💰 <b>Min:</b> ₹{MIN_BET} | <b>Max:</b> ₹{format_number(MAX_BET)}

<b>━━━━━ BIG WINS ━━━━━</b>

Bet ₹100 → Win ₹850
Bet ₹500 → Win ₹4,250
Bet ₹1000 → Win ₹8,500

👇 <b>Pick your lucky number:</b>
""",
        reply_markup=mk
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("num_"))
def cb_number_choice(c):
    number = int(c.data.replace("num_", ""))
    
    temp_data[c.from_user.id] = {
        'game': 'number',
        'choice': number
    }
    
    bot.answer_callback_query(c.id, f"Selected: {number}")
    
    msg = bot.send_message(
        c.message.chat.id,
        f"✅ <b>Number:</b> {number}\n\n"
        f"💰 <b>Enter bet amount:</b>\n\n"
        f"Min: ₹{MIN_BET} | Max: ₹{format_number(MAX_BET)}\n\n"
        f"💡 <b>Win 9x your bet!</b>\n\n"
        f"Or /cancel"
    )
    
    bot.register_next_step_handler(msg, process_number_bet)

def process_number_bet(m):
    if m.text == '/cancel':
        if m.from_user.id in temp_data:
            del temp_data[m.from_user.id]
        return bot.send_message(m.chat.id, "❌ Cancelled!")
    
    try:
        bet_amount = int(m.text.strip())
    except:
        return bot.send_message(m.chat.id, "❌ Invalid! Numbers only.")
    
    if bet_amount < MIN_BET or bet_amount > MAX_BET:
        return bot.send_message(
            m.chat.id,
            f"❌ Bet must be between ₹{MIN_BET} - ₹{format_number(MAX_BET)}"
        )
    
    user = get_user(m.from_user.id)
    
    if bet_amount > user['balance']:
        return bot.send_message(
            m.chat.id,
            f"❌ <b>Not enough money!</b>\n\n"
            f"👛 Balance: ₹{format_number(user['balance'])}\n"
            f"💰 Need: ₹{format_number(bet_amount)}"
        )
    
    data = temp_data.get(m.from_user.id)
    if not data:
        return bot.send_message(m.chat.id, "❌ Expired!")
    
    user_number = data['choice']
    
    # Deduct
    update_balance(m.from_user.id, -bet_amount)
    
    # Animation
    loading = bot.send_message(
        m.chat.id,
        f"🎲 <b>ROLLING...</b>\n\n"
        f"🔢 Your number: {user_number}\n"
        f"💰 Bet: ₹{format_number(bet_amount)}\n\n"
        f"⏳ Please wait..."
    )
    
    # Rolling animation
    for i in range(4):
        time.sleep(0.6)
        random_nums = " ".join([str(random.randint(0, 9)) for _ in range(3)])
        bot.edit_message_text(
            f"🎲 <b>ROLLING...</b>\n\n"
            f"{random_nums}\n\n"
            f"💰 Bet: ₹{format_number(bet_amount)}",
            m.chat.id,
            loading.message_id
        )
    
    time.sleep(0.5)
    
    # Result (10% win chance, slightly less for house edge)
    result_number = random.randint(0, 9)
    
    # Slightly favor house (9% actual win rate)
    if random.random() > 0.09:
        # Force loss
        while result_number == user_number:
            result_number = random.randint(0, 9)
    
    uid_str = str(m.from_user.id)
    
    if result_number == user_number:
        # BIG WIN!
        win_amount = int(bet_amount * NUMBER_PAYOUT)
        update_balance(m.from_user.id, win_amount)
        
        users[uid_str]["total_won"] += win_amount
        users[uid_str]["win_count"] += 1
        users[uid_str]["total_bets"] += 1
        save_json(FILES["users"], users)
        
        profit = win_amount - bet_amount
        
        result = f"""
🎊 <b>JACKPOT!!! 🎊</b>

🔢 <b>Result:</b> {result_number}
✅ <b>Your number:</b> {user_number}

<b>━━━━━ BIG WIN ━━━━━</b>

💰 <b>Bet:</b> ₹{format_number(bet_amount)}
🎁 <b>Won:</b> ₹{format_number(win_amount)}
💚 <b>Profit:</b> +₹{format_number(profit)}

👛 <b>New Balance:</b> ₹{format_number(user['balance'])}

🔥🔥🔥 <b>AMAZING!</b> 🔥🔥🔥
"""
        
        bets.append({
            "user_id": m.from_user.id,
            "game": "number",
            "bet": bet_amount,
            "result": "win",
            "profit": profit,
            "time": datetime.now().isoformat()
        })
        save_json(FILES["bets"], bets)
        
    else:
        # Loss
        users[uid_str]["total_lost"] += bet_amount
        users[uid_str]["loss_count"] += 1
        users[uid_str]["total_bets"] += 1
        
        # VIP Cashback
        cashback_amount = 0
        vip_level = user["vip_level"]
        cashback_rate = VIP_LEVELS[vip_level]["cashback"]
        
        if cashback_rate > 0:
            cashback_amount = int(bet_amount * cashback_rate)
            update_balance(m.from_user.id, cashback_amount)
        
        save_json(FILES["users"], users)
        
        # Show near miss if close
        diff = abs(result_number - user_number)
        if diff == 1:
            near_msg = "🔥 SO CLOSE! Just 1 number away!"
        elif diff == 2:
            near_msg = "💪 Almost! Try again!"
        else:
            near_msg = "⚡ Next one is yours!"
        
        result = f"""
😔 <b>NOT THIS TIME!</b>

🔢 <b>Result:</b> {result_number}
❌ <b>Your number:</b> {user_number}

<b>━━━━━━━━━━━━━━━━━━━</b>

💔 <b>Lost:</b> ₹{format_number(bet_amount)}
"""
        
        if cashback_amount > 0:
            result += f"💎 <b>Cashback:</b> +₹{cashback_amount}\n"
        
        result += f"""
👛 <b>Balance:</b> ₹{format_number(user['balance'])}

{near_msg}
💡 <b>Big win coming soon!</b>
"""
        
        bets.append({
            "user_id": m.from_user.id,
            "game": "number",
            "bet": bet_amount,
            "result": "loss",
            "profit": -bet_amount,
            "time": datetime.now().isoformat()
        })
        save_json(FILES["bets"], bets)
        
        stats["total_profit"] += bet_amount - cashback_amount
        stats["today_profit"] += bet_amount - cashback_amount
        save_json(FILES["stats"], stats)
    
    bot.edit_message_text(result, m.chat.id, loading.message_id)
    
    # Quick play
    mk = types.InlineKeyboardMarkup()
    row1 = [types.InlineKeyboardButton(str(i), callback_data=f"num_{i}") for i in range(5)]
    row2 = [types.InlineKeyboardButton(str(i), callback_data=f"num_{i}") for i in range(5, 10)]
    mk.row(*row1)
    mk.row(*row2)
    
    bot.send_message(m.chat.id, "🎮 <b>Try Again?</b>", reply_markup=mk)
    
    if m.from_user.id in temp_data:
        del temp_data[m.from_user.id]

@bot.message_handler(func=lambda m: m.text == "👛 Wallet")
def btn_wallet(m):
    user = get_user(m.from_user.id)
    
    vip_icon = get_vip_icon(user["vip_level"])
    vip_name = VIP_LEVELS[user["vip_level"]]["name"]
    
    # Calculate next VIP
    next_vip = user["vip_level"] + 1
    if next_vip < len(VIP_LEVELS):
        next_deposit = VIP_LEVELS[next_vip]["deposit"]
        need = next_deposit - user["total_deposit"]
    else:
        next_deposit = 0
        need = 0
    
    msg = f"""
👛 <b>YOUR WALLET</b>

<b>━━━━━ BALANCE ━━━━━</b>

💰 <b>Current:</b> ₹{format_number(user['balance'])}

<b>━━━━━ VIP STATUS ━━━━━</b>

{vip_icon} <b>Level:</b> {vip_name}
💎 <b>Cashback:</b> {int(VIP_LEVELS[user['vip_level']]['cashback']*100)}%
"""
    
    if next_vip < len(VIP_LEVELS):
        next_icon = get_vip_icon(next_vip)
        next_name = VIP_LEVELS[next_vip]["name"]
        msg += f"\n🎯 <b>Next:</b> {next_icon} {next_name}\n"
        msg += f"💸 <b>Need:</b> ₹{format_number(need)} more deposits\n"
    
    msg += f"""
<b>━━━━━ LIFETIME STATS ━━━━━</b>

📥 <b>Deposited:</b> ₹{format_number(user['total_deposit'])}
📤 <b>Withdrawn:</b> ₹{format_number(user['total_withdrawal'])}

<b>━━━━━━━━━━━━━━━━━━━</b>

💡 <b>Deposit more to increase VIP!</b>
"""
    
    mk = types.InlineKeyboardMarkup()
    mk.row(
        types.InlineKeyboardButton("💰 Deposit", callback_data="deposit"),
        types.InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")
    )
    
    bot.send_message(m.chat.id, msg, reply_markup=mk)

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def btn_stats(m):
    user = get_user(m.from_user.id)
    
    total_bets = user.get("total_bets", 0)
    wins = user.get("win_count", 0)
    losses = user.get("loss_count", 0)
    win_rate = (wins / total_bets * 100) if total_bets > 0 else 0
    
    profit = user.get("total_won", 0) - user.get("total_lost", 0)
    profit_sign = "+" if profit >= 0 else ""
    
    msg = f"""
📊 <b>YOUR STATISTICS</b>

<b>━━━━━ GAME STATS ━━━━━</b>

🎲 <b>Total Bets:</b> {total_bets}
✅ <b>Wins:</b> {wins}
❌ <b>Losses:</b> {losses}
📈 <b>Win Rate:</b> {win_rate:.1f}%

<b>━━━━━ MONEY STATS ━━━━━</b>

💰 <b>Total Won:</b> ₹{format_number(user.get('total_won', 0))}
💔 <b>Total Lost:</b> ₹{format_number(user.get('total_lost', 0))}
{'💚' if profit >= 0 else '💔'} <b>Net Profit:</b> {profit_sign}₹{format_number(abs(profit))}

<b>━━━━━ ACCOUNT ━━━━━</b>

🔥 <b>Streak:</b> {user.get('streak', 0)} days
👥 <b>Referrals:</b> {len(user.get('referrals', []))}
📅 <b>Joined:</b> {user.get('joined', '')[:10]}

<b>━━━━━━━━━━━━━━━━━━━</b>

💡 <b>Keep playing to improve stats!</b>
"""
    
    bot.send_message(m.chat.id, msg)

@bot.message_handler(func=lambda m: m.text == "💰 Deposit")
@bot.callback_query_handler(func=lambda c: c.data == "deposit")
def show_deposit(m_or_c):
    if isinstance(m_or_c, types.CallbackQuery):
        chat_id = m_or_c.message.chat.id
        bot.answer_callback_query(m_or_c.id)
    else:
        chat_id = m_or_c.chat.id
    
    msg = f"""
💰 <b>DEPOSIT MONEY</b>

<b>━━━━━ UPI PAYMENT ━━━━━</b>

📱 <b>UPI ID:</b> <code>{UPI_ID}</code>

💡 <b>Click to copy UPI ID</b>

<b>OR Scan QR Code:</b>
{UPI_QR if UPI_QR != "https://i.imgur.com/your-qr.jpg" else "Contact admin for QR"}

<b>━━━━━ AFTER PAYMENT ━━━━━</b>

1️⃣ Pay any amount (Min ₹{MIN_DEPOSIT})
2️⃣ Copy UTR/Transaction ID
3️⃣ Click "Submit Proof" below
4️⃣ Send UTR + Screenshot
5️⃣ Get balance in 5-30 min

<b>━━━━━ BONUSES ━━━━━</b>

🎁 First deposit: +10% bonus
💎 ₹500+: +15% bonus
👑 ₹1000+: +20% bonus

<b>━━━━━━━━━━━━━━━━━━━</b>

📞 Support: {OWNER_USERNAME}
"""
    
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📤 Submit Payment Proof", callback_data="submit_deposit"))
    
    bot.send_message(chat_id, msg, reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data == "submit_deposit")
def cb_submit_deposit(c):
    bot.answer_callback_query(c.id)
    
    msg = bot.send_message(
        c.message.chat.id,
        "💳 <b>DEPOSIT PROOF</b>\n\n"
        "📝 <b>Step 1:</b> Send UTR/Transaction ID\n\n"
        "Or /cancel"
    )
    
    bot.register_next_step_handler(msg, process_deposit_utr)

def process_deposit_utr(m):
    if m.text == '/cancel':
        return bot.send_message(m.chat.id, "❌ Cancelled!")
    
    utr = m.text.strip()
    
    if len(utr) < 6:
        return bot.send_message(m.chat.id, "❌ Invalid UTR! Must be 6+ characters.")
    
    temp_data[m.from_user.id] = {
        'type': 'deposit',
        'utr': utr
    }
    
    msg = bot.send_message(
        m.chat.id,
        f"✅ <b>UTR:</b> <code>{utr}</code>\n\n"
        f"📸 <b>Step 2:</b> Send payment screenshot\n\n"
        f"Or /cancel"
    )
    
    bot.register_next_step_handler(msg, process_deposit_screenshot)

def process_deposit_screenshot(m):
    if m.text == '/cancel':
        if m.from_user.id in temp_data:
            del temp_data[m.from_user.id]
        return bot.send_message(m.chat.id, "❌ Cancelled!")
    
    if not m.photo:
        return bot.send_message(m.chat.id, "❌ Please send image!")
    
    data = temp_data.get(m.from_user.id)
    if not data:
        return bot.send_message(m.chat.id, "❌ Expired! Start again.")
    
    deposit_id = generate_id()
    screenshot = m.photo[-1].file_id
    
    user = get_user(m.from_user.id)
    
    # Save deposit request
    deposit_entry = {
        "id": deposit_id,
        "user_id": m.from_user.id,
        "name": user.get("name", "User"),
        "username": user.get("username", "N/A"),
        "utr": data['utr'],
        "screenshot": screenshot,
        "status": "pending",
        "amount": 0,  # Admin will set
        "submitted": datetime.now().isoformat()
    }
    
    deposits.append(deposit_entry)
    save_json(FILES["deposits"], deposits)
    
    del temp_data[m.from_user.id]
    
    # Notify user
    bot.send_message(
        m.chat.id,
        f"✅ <b>DEPOSIT SUBMITTED!</b>\n\n"
        f"🆔 <b>ID:</b> <code>{deposit_id}</code>\n"
        f"💳 <b>UTR:</b> <code>{data['utr']}</code>\n\n"
        f"⏰ <b>Status:</b> Pending\n"
        f"⏱️ <b>Time:</b> 5-30 minutes\n\n"
        f"💡 Save deposit ID for tracking!\n\n"
        f"📞 {OWNER_USERNAME}"
    )
    
    # Notify admin
    try:
        mk = types.InlineKeyboardMarkup()
        mk.row(
            types.InlineKeyboardButton("✅ Approve", callback_data=f"appdep_{deposit_id}"),
            types.InlineKeyboardButton("❌ Reject", callback_data=f"rejdep_{deposit_id}")
        )
        
        admin_bot.send_photo(
            OWNER_ID,
            screenshot,
            caption=f"💰 <b>NEW DEPOSIT REQUEST</b>\n\n"
                    f"🆔 <b>ID:</b> <code>{deposit_id}</code>\n"
                    f"👤 <b>User:</b> {user.get('name')} (@{user.get('username')})\n"
                    f"🔢 <b>User ID:</b> <code>{m.from_user.id}</code>\n"
                    f"💳 <b>UTR:</b> <code>{data['utr']}</code>\n"
                    f"📅 <b>Time:</b> {datetime.now().strftime('%d %b %H:%M')}\n\n"
                    f"💡 Enter amount to approve!",
            reply_markup=mk
        )
    except Exception as e:
        logger.error(f"Failed to notify admin: {e}")

@bot.message_handler(func=lambda m: m.text == "💸 Withdraw")
@bot.callback_query_handler(func=lambda c: c.data == "withdraw")
def show_withdraw(m_or_c):
    if isinstance(m_or_c, types.CallbackQuery):
        chat_id = m_or_c.message.chat.id
        user_id = m_or_c.from_user.id
        bot.answer_callback_query(m_or_c.id)
    else:
        chat_id = m_or_c.chat.id
        user_id = m_or_c.from_user.id
    
    user = get_user(user_id)
    
    if user['balance'] < MIN_WITHDRAWAL:
        return bot.send_message(
            chat_id,
            f"❌ <b>Insufficient balance!</b>\n\n"
            f"👛 Balance: ₹{format_number(user['balance'])}\n"
            f"💸 Minimum: ₹{MIN_WITHDRAWAL}\n\n"
            f"💡 Play more to reach minimum!"
        )
    
    msg = f"""
💸 <b>WITHDRAW MONEY</b>

<b>━━━━━ YOUR BALANCE ━━━━━</b>

👛 <b>Available:</b> ₹{format_number(user['balance'])}
💸 <b>Minimum:</b> ₹{MIN_WITHDRAWAL}

<b>━━━━━ WITHDRAW TO ━━━━━</b>

📱 UPI
💳 Bank Account
📲 Paytm/PhonePe

<b>━━━━━ PROCESS ━━━━━</b>

1️⃣ Click "Request Withdrawal"
2️⃣ Enter amount
3️⃣ Enter UPI ID/Bank details
4️⃣ Get money in 1-24 hours

<b>━━━━━━━━━━━━━━━━━━━</b>

⚠️ <b>Withdrawal charges:</b> ₹5 per transaction
"""
    
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("💸 Request Withdrawal", callback_data="request_withdraw"))
    
    bot.send_message(chat_id, msg, reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data == "request_withdraw")
def cb_request_withdraw(c):
    bot.answer_callback_query(c.id)
    
    user = get_user(c.from_user.id)
    
    msg = bot.send_message(
        c.message.chat.id,
        f"💸 <b>WITHDRAWAL REQUEST</b>\n\n"
        f"👛 Balance: ₹{format_number(user['balance'])}\n\n"
        f"💰 Enter amount to withdraw:\n\n"
        f"Min: ₹{MIN_WITHDRAWAL}\n\n"
        f"Or /cancel"
    )
    
    bot.register_next_step_handler(msg, process_withdraw_amount)

def process_withdraw_amount(m):
    if m.text == '/cancel':
        return bot.send_message(m.chat.id, "❌ Cancelled!")
    
    try:
        amount = int(m.text.strip())
    except:
        return bot.send_message(m.chat.id, "❌ Invalid! Numbers only.")
    
    user = get_user(m.from_user.id)
    
    if amount < MIN_WITHDRAWAL:
        return bot.send_message(m.chat.id, f"❌ Minimum withdrawal: ₹{MIN_WITHDRAWAL}")
    
    if amount > user['balance']:
        return bot.send_message(
            m.chat.id,
            f"❌ Insufficient balance!\n\n"
            f"👛 Balance: ₹{format_number(user['balance'])}\n"
            f"💸 Requested: ₹{format_number(amount)}"
        )
    
    temp_data[m.from_user.id] = {
        'type': 'withdraw',
        'amount': amount
    }
    
    msg = bot.send_message(
        m.chat.id,
        f"✅ Amount: ₹{format_number(amount)}\n\n"
        f"📱 Send your UPI ID:\n\n"
        f"Example: yourname@paytm\n\n"
        f"Or /cancel"
    )
    
    bot.register_next_step_handler(msg, process_withdraw_upi)

def process_withdraw_upi(m):
    if m.text == '/cancel':
        if m.from_user.id in temp_data:
            del temp_data[m.from_user.id]
        return bot.send_message(m.chat.id, "❌ Cancelled!")
    
    upi_id = m.text.strip()
    
    if '@' not in upi_id:
        return bot.send_message(m.chat.id, "❌ Invalid UPI ID! Must contain @")
    
    data = temp_data.get(m.from_user.id)
    if not data:
        return bot.send_message(m.chat.id, "❌ Expired!")
    
    amount = data['amount']
    withdraw_id = generate_id()
    
    user = get_user(m.from_user.id)
    
    # Deduct balance
    update_balance(m.from_user.id, -amount)
    
    # Save withdrawal
    withdraw_entry = {
        "id": withdraw_id,
        "user_id": m.from_user.id,
        "name": user.get("name", "User"),
        "username": user.get("username", "N/A"),
        "amount": amount,
        "upi_id": upi_id,
        "status": "pending",
        "requested": datetime.now().isoformat()
    }
    
    withdrawals.append(withdraw_entry)
    save_json(FILES["withdrawals"], withdrawals)
    
    uid_str = str(m.from_user.id)
    users[uid_str]["total_withdrawal"] += amount
    save_json(FILES["users"], users)
    
    del temp_data[m.from_user.id]
    
    # Notify user
    bot.send_message(
        m.chat.id,
        f"✅ <b>WITHDRAWAL REQUESTED!</b>\n\n"
        f"🆔 <b>ID:</b> <code>{withdraw_id}</code>\n"
        f"💰 <b>Amount:</b> ₹{format_number(amount)}\n"
        f"📱 <b>UPI:</b> <code>{upi_id}</code>\n\n"
        f"⏰ <b>Status:</b> Processing\n"
        f"⏱️ <b>Time:</b> 1-24 hours\n\n"
        f"👛 <b>New Balance:</b> ₹{format_number(user['balance'])}\n\n"
        f"📞 {OWNER_USERNAME}"
    )
    
    # Notify admin
    try:
        mk = types.InlineKeyboardMarkup()
        mk.row(
            types.InlineKeyboardButton("✅ Paid", callback_data=f"appwith_{withdraw_id}"),
            types.InlineKeyboardButton("❌ Reject", callback_data=f"rejwith_{withdraw_id}")
        )
        
        admin_bot.send_message(
            OWNER_ID,
            f"💸 <b>WITHDRAWAL REQUEST</b>\n\n"
            f"🆔 <b>ID:</b> <code>{withdraw_id}</code>\n"
            f"👤 <b>User:</b> {user.get('name')} (@{user.get('username')})\n"
            f"🔢 <b>User ID:</b> <code>{m.from_user.id}</code>\n"
            f"💰 <b>Amount:</b> ₹{format_number(amount)}\n"
            f"📱 <b>UPI:</b> <code>{upi_id}</code>\n"
            f"📅 <b>Time:</b> {datetime.now().strftime('%d %b %H:%M')}",
            reply_markup=mk
        )
    except Exception as e:
        logger.error(f"Failed to notify admin: {e}")

@bot.message_handler(func=lambda m: m.text == "❓ Help")
def btn_help(m):
    msg = """
❓ <b>HOW TO USE BOT</b>

<b>━━━━━ GAMES ━━━━━</b>

🎨 <b>Color Game:</b>
• Choose Red/Green/Violet
• Enter bet amount
• Win = 2x money

🔢 <b>Number Game:</b>
• Pick number 0-9
• Enter bet amount
• Win = 9x money

<b>━━━━━ MONEY ━━━━━</b>

💰 <b>Deposit:</b>
• Pay to UPI
• Submit proof
• Get balance in 5-30 min

💸 <b>Withdraw:</b>
• Min ₹100
• Enter UPI ID
• Get paid in 1-24 hours

<b>━━━━━ BONUSES ━━━━━</b>

🎁 Daily login bonus
🔥 Streak bonuses
🎰 Free daily spin
👥 Referral rewards

<b>━━━━━━━━━━━━━━━━━━━</b>

📞 Support: {OWNER_USERNAME}
"""
    
    bot.send_message(m.chat.id, msg)

# ============================================================================
# ADMIN BOT
# ============================================================================

@admin_bot.message_handler(commands=['start'])
def admin_start(m):
    if not is_owner(m.from_user.id):
        return admin_bot.send_message(m.chat.id, "❌ <b>UNAUTHORIZED!</b>")
    
    pending_deposits = sum(1 for d in deposits if d.get('status') == 'pending')
    pending_withdrawals = sum(1 for w in withdrawals if w.get('status') == 'pending')
    
    admin_bot.send_message(
        m.chat.id,
        f"""
🔐 <b>ADMIN PANEL</b>

<b>━━━━━ QUICK STATS ━━━━━</b>

👥 Users: {len(users)}
💰 Deposits (Pending): {pending_deposits}
💸 Withdrawals (Pending): {pending_withdrawals}
💵 Today's Profit: ₹{format_number(stats.get('today_profit', 0))}

<b>━━━━━ COMMANDS ━━━━━</b>

/deposits - Pending deposits
/withdrawals - Pending withdrawals
/users - All users
/stats - Full statistics
/broadcast - Send to all
/addbalance - Add balance
/setbalance - Set balance

<b>━━━━━━━━━━━━━━━━━━━</b>

👑 Owner: {OWNER_USERNAME}
"""
    )

@admin_bot.message_handler(commands=['deposits'])
def admin_deposits(m):
    if not is_owner(m.from_user.id):
        return
    
    pending = [d for d in deposits if d.get('status') == 'pending']
    
    if not pending:
        return admin_bot.send_message(m.chat.id, "✅ No pending deposits!")
    
    admin_bot.send_message(m.chat.id, f"💰 <b>Pending deposits: {len(pending)}</b>\n\nSending...")
    
    for dep in pending[-10:]:
        mk = types.InlineKeyboardMarkup()
        mk.row(
            types.InlineKeyboardButton("✅ Approve", callback_data=f"appdep_{dep['id']}"),
            types.InlineKeyboardButton("❌ Reject", callback_data=f"rejdep_{dep['id']}")
        )
        
        admin_bot.send_photo(
            m.chat.id,
            dep['screenshot'],
            caption=f"💰 <b>DEPOSIT</b>\n\n"
                    f"🆔 <code>{dep['id']}</code>\n"
                    f"👤 {dep['name']} (@{dep['username']})\n"
                    f"🔢 <code>{dep['user_id']}</code>\n"
                    f"💳 UTR: <code>{dep['utr']}</code>",
            reply_markup=mk
        )

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("appdep_"))
def admin_approve_deposit(c):
    if not is_owner(c.from_user.id):
        return admin_bot.answer_callback_query(c.id, "❌ Unauthorized!")
    
    deposit_id = c.data.replace("appdep_", "")
    
    admin_bot.answer_callback_query(c.id)
    
    msg = admin_bot.send_message(
        c.message.chat.id,
        f"✅ Approving deposit <code>{deposit_id}</code>\n\n"
        f"💰 Enter amount deposited:\n\n"
        f"Or /cancel"
    )
    
    temp_data[c.from_user.id] = {'deposit_id': deposit_id}
    admin_bot.register_next_step_handler(msg, process_deposit_approval)

def process_deposit_approval(m):
    if m.text == '/cancel':
        if m.from_user.id in temp_data:
            del temp_data[m.from_user.id]
        return admin_bot.send_message(m.chat.id, "❌ Cancelled!")
    
    try:
        amount = int(m.text.strip())
    except:
        return admin_bot.send_message(m.chat.id, "❌ Invalid!")
    
    data = temp_data.get(m.from_user.id)
    if not data:
        return admin_bot.send_message(m.chat.id, "❌ Expired!")
    
    deposit_id = data['deposit_id']
    
    # Find deposit
    deposit = None
    for d in deposits:
        if d['id'] == deposit_id:
            deposit = d
            break
    
    if not deposit:
        return admin_bot.send_message(m.chat.id, "❌ Not found!")
    
    # Calculate bonus
    bonus = 0
    if amount >= 1000:
        bonus = int(amount * 0.20)  # 20%
    elif amount >= 500:
        bonus = int(amount * 0.15)  # 15%
    elif deposit.get('user_id') and str(deposit['user_id']) in users:
        if users[str(deposit['user_id'])].get('total_deposit', 0) == 0:
            bonus = int(amount * 0.10)  # 10% first deposit
    
    total_credit = amount + bonus
    
    # Add to user balance
    update_balance(deposit['user_id'], total_credit)
    
    # Update deposit
    deposit['status'] = 'approved'
    deposit['amount'] = amount
    deposit['bonus'] = bonus
    deposit['approved_at'] = datetime.now().isoformat()
    save_json(FILES["deposits"], deposits)
    
    # Update user total deposit
    uid_str = str(deposit['user_id'])
    users[uid_str]['total_deposit'] += amount
    users[uid_str]['vip_level'] = get_vip_level(users[uid_str])
    save_json(FILES["users"], users)
    
    # Update stats
    stats['total_deposits'] += amount
    save_json(FILES["stats"], stats)
    
    del temp_data[m.from_user.id]
    
    admin_bot.send_message(
        m.chat.id,
        f"✅ <b>DEPOSIT APPROVED!</b>\n\n"
        f"🆔 {deposit_id}\n"
        f"💰 Amount: ₹{format_number(amount)}\n"
        f"🎁 Bonus: ₹{bonus}\n"
        f"✅ Total: ₹{format_number(total_credit)}"
    )
    
    # Notify user
    try:
        bot.send_message(
            deposit['user_id'],
            f"✅ <b>DEPOSIT APPROVED!</b>\n\n"
            f"💰 <b>Deposited:</b> ₹{format_number(amount)}\n"
            f"🎁 <b>Bonus:</b> ₹{bonus}\n"
            f"✅ <b>Total Credit:</b> ₹{format_number(total_credit)}\n\n"
            f"👛 <b>New Balance:</b> ₹{format_number(users[uid_str]['balance'])}\n\n"
            f"🎮 <b>Start playing now!</b>"
        )
    except:
        pass

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("rejdep_"))
def admin_reject_deposit(c):
    if not is_owner(c.from_user.id):
        return admin_bot.answer_callback_query(c.id, "❌ Unauthorized!")
    
    deposit_id = c.data.replace("rejdep_", "")
    
    # Find deposit
    deposit = None
    for d in deposits:
        if d['id'] == deposit_id:
            deposit = d
            break
    
    if not deposit:
        return admin_bot.answer_callback_query(c.id, "❌ Not found!")
    
    deposit['status'] = 'rejected'
    deposit['rejected_at'] = datetime.now().isoformat()
    save_json(FILES["deposits"], deposits)
    
    admin_bot.answer_callback_query(c.id, "❌ Deposit rejected!")
    admin_bot.send_message(c.message.chat.id, f"❌ Deposit <code>{deposit_id}</code> rejected!")
    
    # Notify user
    try:
        bot.send_message(
            deposit['user_id'],
            f"❌ <b>DEPOSIT REJECTED!</b>\n\n"
            f"🆔 {deposit_id}\n\n"
            f"💡 If this is a mistake, contact {OWNER_USERNAME}"
        )
    except:
        pass

@admin_bot.message_handler(commands=['withdrawals'])
def admin_withdrawals(m):
    if not is_owner(m.from_user.id):
        return
    
    pending = [w for w in withdrawals if w.get('status') == 'pending']
    
    if not pending:
        return admin_bot.send_message(m.chat.id, "✅ No pending withdrawals!")
    
    msg = f"💸 <b>PENDING WITHDRAWALS ({len(pending)})</b>\n\n"
    
    for w in pending[-10:]:
        msg += f"🆔 <code>{w['id']}</code>\n"
        msg += f"👤 {w['name']} (<code>{w['user_id']}</code>)\n"
        msg += f"💰 ₹{format_number(w['amount'])}\n"
        msg += f"📱 <code>{w['upi_id']}</code>\n\n"
    
    admin_bot.send_message(m.chat.id, msg)
    
    # Send buttons
    for w in pending[-5:]:
        mk = types.InlineKeyboardMarkup()
        mk.row(
            types.InlineKeyboardButton("✅ Paid", callback_data=f"appwith_{w['id']}"),
            types.InlineKeyboardButton("❌ Reject", callback_data=f"rejwith_{w['id']}")
        )
        
        admin_bot.send_message(
            m.chat.id,
            f"💸 <code>{w['id']}</code> - ₹{format_number(w['amount'])}",
            reply_markup=mk
        )

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("appwith_"))
def admin_approve_withdrawal(c):
    if not is_owner(c.from_user.id):
        return admin_bot.answer_callback_query(c.id, "❌ Unauthorized!")
    
    withdraw_id = c.data.replace("appwith_", "")
    
    # Find withdrawal
    withdrawal = None
    for w in withdrawals:
        if w['id'] == withdraw_id:
            withdrawal = w
            break
    
    if not withdrawal:
        return admin_bot.answer_callback_query(c.id, "❌ Not found!")
    
    withdrawal['status'] = 'approved'
    withdrawal['approved_at'] = datetime.now().isoformat()
    save_json(FILES["withdrawals"], withdrawals)
    
    # Update stats
    stats['total_withdrawals'] += withdrawal['amount']
    save_json(FILES["stats"], stats)
    
    admin_bot.answer_callback_query(c.id, "✅ Approved!")
    admin_bot.send_message(
        c.message.chat.id,
        f"✅ Withdrawal <code>{withdraw_id}</code> approved!\n\n"
        f"💰 ₹{format_number(withdrawal['amount'])} paid to {withdrawal['upi_id']}"
    )
    
    # Notify user
    try:
        bot.send_message(
            withdrawal['user_id'],
            f"✅ <b>WITHDRAWAL SUCCESSFUL!</b>\n\n"
            f"🆔 {withdraw_id}\n"
            f"💰 Amount: ₹{format_number(withdrawal['amount'])}\n"
            f"📱 UPI: {withdrawal['upi_id']}\n\n"
            f"💵 <b>Money sent to your account!</b>"
        )
    except:
        pass

@admin_bot.callback_query_handler(func=lambda c: c.data.startswith("rejwith_"))
def admin_reject_withdrawal(c):
    if not is_owner(c.from_user.id):
        return admin_bot.answer_callback_query(c.id, "❌ Unauthorized!")
    
    withdraw_id = c.data.replace("rejwith_", "")
    
    # Find withdrawal
    withdrawal = None
    for w in withdrawals:
        if w['id'] == withdraw_id:
            withdrawal = w
            break
    
    if not withdrawal:
        return admin_bot.answer_callback_query(c.id, "❌ Not found!")
    
    # Refund to user
    update_balance(withdrawal['user_id'], withdrawal['amount'])
    
    withdrawal['status'] = 'rejected'
    withdrawal['rejected_at'] = datetime.now().isoformat()
    save_json(FILES["withdrawals"], withdrawals)
    
    admin_bot.answer_callback_query(c.id, "❌ Rejected & refunded!")
    admin_bot.send_message(c.message.chat.id, f"❌ Withdrawal <code>{withdraw_id}</code> rejected!")
    
    # Notify user
    try:
        bot.send_message(
            withdrawal['user_id'],
            f"❌ <b>WITHDRAWAL REJECTED!</b>\n\n"
            f"🆔 {withdraw_id}\n"
            f"💰 ₹{format_number(withdrawal['amount'])} refunded to balance\n\n"
            f"📞 Contact {OWNER_USERNAME} for details"
        )
    except:
        pass

@admin_bot.message_handler(commands=['stats'])
def admin_stats(m):
    if not is_owner(m.from_user.id):
        return
    
    total_balance = sum(u.get('balance', 0) for u in users.values())
    total_deposits = sum(d.get('amount', 0) for d in deposits if d.get('status') == 'approved')
    total_withdrawals_amount = sum(w.get('amount', 0) for w in withdrawals if w.get('status') == 'approved')
    
    admin_bot.send_message(
        m.chat.id,
        f"""
📊 <b>BOT STATISTICS</b>

<b>━━━━━ USERS ━━━━━</b>

👥 Total: {len(users)}
💰 Total Balance: ₹{format_number(total_balance)}

<b>━━━━━ MONEY ━━━━━</b>

📥 Deposits: ₹{format_number(total_deposits)}
📤 Withdrawals: ₹{format_number(total_withdrawals_amount)}
💵 Profit: ₹{format_number(stats.get('total_profit', 0))}
🔥 Today: ₹{format_number(stats.get('today_profit', 0))}

<b>━━━━━ GAMES ━━━━━</b>

🎲 Total Bets: {len(bets)}

<b>━━━━━━━━━━━━━━━━━━━</b>

📅 {datetime.now().strftime('%d %b %Y')}
"""
    )

@admin_bot.message_handler(commands=['broadcast'])
def admin_broadcast(m):
    if not is_owner(m.from_user.id):
        return
    
    msg = admin_bot.send_message(
        m.chat.id,
        "📢 <b>BROADCAST</b>\n\n"
        "Send message to broadcast:\n\n"
        "Or /cancel"
    )
    
    admin_bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(m):
    if m.text == '/cancel':
        return admin_bot.send_message(m.chat.id, "❌ Cancelled!")
    
    message = m.text or m.caption
    
    progress = admin_bot.send_message(m.chat.id, "📤 Broadcasting...")
    
    success = 0
    for uid in users:
        try:
            bot.send_message(int(uid), f"📢 <b>ANNOUNCEMENT</b>\n\n{message}")
            success += 1
        except:
            pass
        time.sleep(0.05)
    
    admin_bot.edit_message_text(
        f"✅ Broadcast sent!\n\n"
        f"📤 Sent: {success}/{len(users)}",
        m.chat.id,
        progress.message_id
    )

# ============================================================================
# RUN BOTS
# ============================================================================

import threading

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
    print("║      🎰 SUPER ADDICTIVE BETTING BOT 🎰           ║")
    print("║                                                    ║")
    print("║   Color Game | Number Game | Daily Rewards        ║")
    print("║   Referral System | VIP Levels | Leaderboard      ║")
    print("║                                                    ║")
    print("╚════════════════════════════════════════════════════╝")
    print("="*60)
    
    logger.info(f"👑 Owner: {OWNER_ID}")
    logger.info(f"👥 Users: {len(users)}")
    logger.info(f"💰 Total Profit: ₹{format_number(stats.get('total_profit', 0))}")
    
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
