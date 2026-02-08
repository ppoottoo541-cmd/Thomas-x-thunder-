"""
🔥 HACKER STYLE WEB APP 🔥
Number Info + Call Bomber
Full Admin Control
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_cors import CORS
import json
import os
import requests
import asyncio
import aiohttp
from datetime import datetime, timedelta
import hashlib
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# ==================== CONFIGURATION ====================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "thomas123"  # Change this!

OWNER_USERNAME = "@TGxTHOMASx"
CHANNEL_LINK = "https://t.me/thomasXstoreee"
DM_LINK = "https://t.me/TGxTHOMASx"

# API Configuration
API_URL = "https://xfdhftftjuytdyjtfuitydr5ddyyfgkuylhtydry.onrender.com/api/india/number/{number}?token={token}"
API_TOKEN = "8458169644:13b9efd99198"

# Credit Prices
CREDIT_PRICES = {
    "25": 2,
    "50": 5,
    "100": 12,
    "200": 25
}

# Files
USERS_FILE = "web_users.json"
SETTINGS_FILE = "web_settings.json"
BOMBER_APIS_FILE = "bomber_apis.json"

# ==================== FILE OPERATIONS ====================
def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({
                "site_name": "THOMAS HACKER TOOLS",
                "maintenance": False,
                "bomber_enabled": True,
                "number_info_enabled": True,
                "credits_per_search": 1,
                "credits_per_bomb": 1,
                "signup_credits": 5,
                "owner_username": OWNER_USERNAME,
                "channel_link": CHANNEL_LINK,
                "dm_link": DM_LINK
            }, f)
    
    if not os.path.exists(BOMBER_APIS_FILE):
        # Load from uploaded bot file
        bomber_apis = [
            {"name": "Tata Capital", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "type": "call"},
            {"name": "1MG Call", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "type": "call"},
            {"name": "Swiggy Call", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "type": "call"},
            {"name": "KPN WhatsApp", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate", "method": "POST", "type": "whatsapp"},
            {"name": "Hungama SMS", "url": "https://communication.api.hungama.com/v1/communication/otp", "method": "POST", "type": "sms"},
            {"name": "NoBroker SMS", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "type": "sms"},
        ]
        with open(BOMBER_APIS_FILE, "w") as f:
            json.dump(bomber_apis, f)

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
bomber_apis = load_json(BOMBER_APIS_FILE)

# ==================== AUTH DECORATORS ====================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session or not session['admin']:
            flash('Admin access required!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== HELPER FUNCTIONS ====================
def get_user(user_id):
    global users
    users = load_json(USERS_FILE)
    return users.get(str(user_id), None)

def create_user(username, password, email=""):
    user_id = hashlib.md5(f"{username}{datetime.now()}".encode()).hexdigest()[:12]
    users[user_id] = {
        "username": username,
        "password": hashlib.sha256(password.encode()).hexdigest(),
        "email": email,
        "credits": settings.get("signup_credits", 5),
        "created_at": datetime.now().isoformat(),
        "total_searches": 0,
        "total_bombs": 0
    }
    save_json(USERS_FILE, users)
    return user_id

def verify_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    for uid, user in users.items():
        if user["username"] == username and user["password"] == password_hash:
            return uid
    return None

def make_number_info_request(number):
    try:
        url = API_URL.format(number=number, token=API_TOKEN)
        response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

# ==================== ROUTES ====================

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html', settings=settings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check admin
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            session['user_id'] = 'admin'
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_panel'))
        
        # Check user
        user_id = verify_user(username, password)
        if user_id:
            session['user_id'] = user_id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Invalid credentials!', 'error')
    
    return render_template('login.html', settings=settings)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email', '')
        
        # Check if username exists
        for user in users.values():
            if user['username'] == username:
                flash('Username already exists!', 'error')
                return render_template('register.html', settings=settings)
        
        user_id = create_user(username, password, email)
        session['user_id'] = user_id
        flash(f'Account created! You got {settings.get("signup_credits", 5)} free credits!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html', settings=settings)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = get_user(session['user_id'])
    if not user:
        return redirect(url_for('logout'))
    
    return render_template('dashboard.html', user=user, settings=settings)

@app.route('/number-info', methods=['GET', 'POST'])
@login_required
def number_info():
    user = get_user(session['user_id'])
    
    if request.method == 'POST':
        number = request.form.get('number', '').strip()
        
        if not number or len(number) != 10 or not number.isdigit():
            flash('Invalid phone number! Enter 10 digits.', 'error')
            return render_template('number_info.html', user=user, settings=settings)
        
        # Check credits
        if user['credits'] < settings.get('credits_per_search', 1):
            flash('Insufficient credits! Buy more credits.', 'error')
            return render_template('number_info.html', user=user, settings=settings)
        
        # Make API request
        result = make_number_info_request(number)
        
        if result:
            # Deduct credit
            users[session['user_id']]['credits'] -= settings.get('credits_per_search', 1)
            users[session['user_id']]['total_searches'] += 1
            save_json(USERS_FILE, users)
            
            return render_template('number_info.html', user=get_user(session['user_id']), result=result, number=number, settings=settings)
        else:
            flash('Failed to fetch data! Try again.', 'error')
    
    return render_template('number_info.html', user=user, settings=settings)

@app.route('/call-bomber', methods=['GET', 'POST'])
@login_required
def call_bomber():
    user = get_user(session['user_id'])
    
    if request.method == 'POST':
        number = request.form.get('number', '').strip()
        duration = int(request.form.get('duration', 5))
        
        if not number or len(number) != 10 or not number.isdigit():
            flash('Invalid phone number!', 'error')
            return render_template('call_bomber.html', user=user, settings=settings)
        
        # Check credits
        if user['credits'] < settings.get('credits_per_bomb', 1):
            flash('Insufficient credits!', 'error')
            return render_template('call_bomber.html', user=user, settings=settings)
        
        # Deduct credit
        users[session['user_id']]['credits'] -= settings.get('credits_per_bomb', 1)
        users[session['user_id']]['total_bombs'] += 1
        save_json(USERS_FILE, users)
        
        flash(f'Bombing started on {number} for {duration} minutes!', 'success')
        
        # TODO: Implement actual bombing (background task)
        
        return render_template('call_bomber.html', user=get_user(session['user_id']), settings=settings, bombing=True, number=number, duration=duration)
    
    return render_template('call_bomber.html', user=user, settings=settings)

@app.route('/buy-credits')
@login_required
def buy_credits():
    user = get_user(session['user_id'])
    return render_template('buy_credits.html', user=user, prices=CREDIT_PRICES, settings=settings)

@app.route('/contact')
def contact():
    return render_template('contact.html', settings=settings)

# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@admin_required
def admin_panel():
    total_users = len(users)
    total_credits = sum(u.get('credits', 0) for u in users.values())
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_credits=total_credits,
                         settings=settings)

@app.route('/admin/users')
@admin_required
def admin_users():
    return render_template('admin/users.html', users=users, settings=settings)

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    if request.method == 'POST':
        settings['site_name'] = request.form.get('site_name', settings['site_name'])
        settings['maintenance'] = request.form.get('maintenance') == 'on'
        settings['bomber_enabled'] = request.form.get('bomber_enabled') == 'on'
        settings['number_info_enabled'] = request.form.get('number_info_enabled') == 'on'
        settings['credits_per_search'] = int(request.form.get('credits_per_search', 1))
        settings['credits_per_bomb'] = int(request.form.get('credits_per_bomb', 1))
        settings['signup_credits'] = int(request.form.get('signup_credits', 5))
        settings['owner_username'] = request.form.get('owner_username', OWNER_USERNAME)
        settings['channel_link'] = request.form.get('channel_link', CHANNEL_LINK)
        settings['dm_link'] = request.form.get('dm_link', DM_LINK)
        
        save_json(SETTINGS_FILE, settings)
        flash('Settings updated!', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html', settings=settings)

@app.route('/admin/add-credits', methods=['POST'])
@admin_required
def admin_add_credits():
    user_id = request.form.get('user_id')
    amount = int(request.form.get('amount', 0))
    
    if user_id in users:
        users[user_id]['credits'] = users[user_id].get('credits', 0) + amount
        save_json(USERS_FILE, users)
        flash(f'Added {amount} credits to user!', 'success')
    else:
        flash('User not found!', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/delete-user/<user_id>')
@admin_required
def admin_delete_user(user_id):
    if user_id in users:
        del users[user_id]
        save_json(USERS_FILE, users)
        flash('User deleted!', 'success')
    
    return redirect(url_for('admin_users'))

# ==================== API ENDPOINTS ====================

@app.route('/api/bomber/start', methods=['POST'])
@login_required
def api_bomber_start():
    data = request.json
    number = data.get('number')
    duration = int(data.get('duration', 5))
    
    # TODO: Implement bombing logic
    
    return jsonify({"status": "success", "message": "Bombing started"})

# ==================== RUN ====================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
