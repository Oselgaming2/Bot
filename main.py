import httpx

from bs4 import BeautifulSoup

import re

from datetime import datetime

import time

import json

with open("flag.json", "r", encoding="utf-8") as f:
    FLAGS = json.load(f)
    
# ================= CONFIG =================

BASE = "http://159.69.3.189"

LOGIN_URL = f"{BASE}/login"

GET_RANGE_URL = f"{BASE}/portal/sms/received/getsms"

GET_NUMBER_URL = f"{BASE}/portal/sms/received/getsms/number"

GET_SMS_URL = f"{BASE}/portal/sms/received/getsms/number/sms"

USERNAME = "Tanisiramdan22@gmail.com" # Ganti Email Ivas

PASSWORD = "22112002@Dani" # Ganti Password Ivas

BOT_TOKEN = "7841438964:AAH91pCJ4UNTzvJQRcpOMRE9lsE6L8KeQPk" # Pakai Token Bot Mu

CHAT_ID = "-1003933626197" #Wajib Pake - Misal -100000

session = httpx.Client(
    follow_redirects=True,
    timeout=30,
    headers={
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }
)

session.cookies.update({
    "_fbp": "fb.1.1775820034937.154342168959733176", # INI FBP NYA GANTI 
    "XSRF-TOKEN": "eyJpdiI6IlpFTmZsdnpEdjA2MWN1OWFvRDZudHc9PSIsInZhbHVlIjoiVnJJYm5JRGJIWUR1ek4xZDNGcktWWUdtR01xakp5QzVCalRwUlFHcTB4VHpPVEhZMncxS0NMdUtvRzNROU9nZlJjMnlWYWNpNkh1YU5RVVdMUDV0cEpQUDBhS0xiL0hmM3U4ei92OEZGOGJNOEt4b2xOSTdxbWIxVStOQURYdHQiLCJtYWMiOiI4MTMzMmI4NjgwZjRkMWZlODJkOTJmMWI0NWJjNWMxODRiNzczYWE1NGJkNWUzZjU5ODE1YmNhNTBlMDg5YTM3IiwidGFnIjoiIn0%3D",
    "ivas_sms_session": "eyJpdiI6Im11MWtRRnZ6UzVWZ0EzdGpiRG05M1E9PSIsInZhbHVlIjoiTUNOeGdBUWJrTjVxcnZOTjRDSHkvcWNjZEFtdG1JN3pNZ1JSNXd1OHh1N0pidm5UNEt3LzdjenNiT1NCbE9WZ2VzQ1ZDOEhJR1pvYUpTa1JiYVBQUFh5SkpIdnh4V2o3NkRmdHRCQTBEblV0ZHBmdGZpNVRFb3NvMHd6SUVzbW0iLCJtYWMiOiJlZjdhYTMyYjg4ZGEzMDI4YWIwYWMxMGRlYjY1M2FiMTdlYzc2Zjg0Yzc2ODg0OGViMDNhZDU4ODA2YmU2Njk3IiwidGFnIjoiIn0%3D" # GANTI COOKIE XSRF/IVASMS_SESION TOKEN LU
})

sent_cache = set()

csrf_token = session.cookies.get("XSRF-TOKEN")

# ==========================================

def tg_send(msg):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "👤 OWNER", "url": "https://t.me/jackymzxc"} # GANTI USERNAME TELE KAMU
            ]
        ]
    }

    session.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "reply_markup": json.dumps(keyboard)
    })
    
      # ==========================================
def tg_active(msg):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    session.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    })      

# ================= UTILS =================

def escapeHTML(text=""):

    return (text.replace("&", "&amp;")

                .replace("<", "&lt;")

                .replace(">", "&gt;")

                .replace('"', "&quot;")

                .replace("'", "&#39;"))

def extract_otp(text):

    m = re.search(r"\b(\d{3}[- ]?\d{3}|\d{4,6})\b", text)

    return m.group(1) if m else None

def format_phone_number(number):

    if len(number) >= 8:

        return f"{number[:3]}{'*' * (len(number) - 8)}{number[-4:]}"

    return number

def clean_country(rng):

    country = re.sub(r"\s*\(.*?\)", "", rng)

    country = re.sub(r"\d+", "", country)

    return country.strip().upper()

def extract_service(text):

    m = re.search(

        r"(WhatsApp|Telegram|Google|Facebook|Instagram|Shopee|Tokopedia|Grab|Gojek|TikTok)",

        text,

        re.I

    )

    return m.group(1) if m else "Unknown"

# ================= LOGIN =================

def login():

    global csrf_token

    r = session.get(LOGIN_URL)

    soup = BeautifulSoup(r.text, "html.parser")

    csrf_token = soup.find("input", {"name": "_token"})["value"]

    session.post(LOGIN_URL, data={

        "_token": csrf_token,

        "email": USERNAME,

        "password": PASSWORD

    })

    tg_active("✅ <b>BOT OTP AKTIF</b>\nLogin berhasil")

    print("[LOGIN] Berhasil")

# ============ GET SENSOR EMAIL ========
def mask_email(email):
    try:
        name, domain = email.split("@")
        if len(name) <= 2:
            masked = name[0] + "••••"
        else:
            masked = name[0] + "••••" + name[-1]
        return f"{masked}@{domain}"
    except:
        return email
        
# ======= AMBIL FLAGS ========
def get_flag(country):
    return FLAGS.get(country.upper(), "🏴‍☠️")        
        
# ================= GET RANGE =================

def get_ranges():

    today = datetime.now().strftime("%Y-%m-%d")

    r = session.post(GET_RANGE_URL, data={

        "_token": csrf_token,

        "from": today,

        "to": today

    })

    soup = BeautifulSoup(r.text, "html.parser")

    ranges = []

    for div in soup.find_all("div", onclick=True):

        if "toggleRange" in div["onclick"]:

            try:

                ranges.append(div["onclick"].split("'")[1])

            except:

                pass

    return list(set(ranges))

# ================= GET NUMBERS =================

def get_numbers(rng):

    today = datetime.now().strftime("%Y-%m-%d")

    r = session.post(GET_NUMBER_URL, data={

        "_token": csrf_token,

        "start": today,

        "end": today,

        "range": rng

    })

    soup = BeautifulSoup(r.text, "html.parser")

    numbers = []

    for div in soup.find_all("div", onclick=True):

        try:

            val = div["onclick"].split("'")[1]

            if val and val != rng:

                numbers.append(val)

        except:

            pass

    return list(set(numbers))

# ================= GET SMS =================

def get_sms(rng, number):

    today = datetime.now().strftime("%Y-%m-%d")

    r = session.post(GET_SMS_URL, data={

        "_token": csrf_token,

        "start": today,

        "end": today,

        "Number": number,

        "Range": rng

    })

    soup = BeautifulSoup(r.text, "html.parser")

    sms_texts = [p.get_text(strip=True) for p in soup.find_all("p")]

    

    if not sms_texts:

        raw_text = soup.get_text(separator="\n", strip=True)

        if raw_text:

            sms_texts = raw_text.split('\n')

            

    return list(set(sms_texts))

# ================= BOT LOOP =================

def run_bot():

    login()

    while True:

        try:

            ranges = get_ranges()

            for rng in ranges:

                country = clean_country(rng)
                flag = get_flag(country)

                for num in get_numbers(rng):

                    for sms in get_sms(rng, num):

                        

                        # 🔥 FIX BUG HARGA: Abaikan jika teksnya adalah harga (contoh: $0.0120)

                        if "$" in sms and len(sms) < 15:

                            continue

                        otp = extract_otp(sms)

                        if not otp:

                            continue

                        unique_id = f"{num}-{otp}"

                        

                        if unique_id in sent_cache:

                            continue

                        waktu = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                        service = extract_service(sms)
                        email_mask = mask_email(USERNAME)

                        msg = (

                            f"🎉NEW OTP RECEIVED🎉\n"

                            f"🌎 Country: {flag} {country}\n"
                            f"📱 Number: {format_phone_number(num)}\n"
                            f"🚨 Service: {service}\n"
                            f"<pre>{escapeHTML(sms)}</pre>\n"
                            f"<blockquote>🔐 OTP: <code>{otp}\n</code></blockquote>"

                        )

                        tg_send(msg)

                        sent_cache.add(unique_id)

                        print("[SENT]", otp, "ke", num)

            time.sleep(1)

        except Exception as e:

            print("[ERROR]", e)

            time.sleep(1)

# ================= START =================

run_bot()