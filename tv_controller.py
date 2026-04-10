#!/usr/bin/env python3
"""
LG TV Controller v6.5 - PHONE ADB → TV Wireless Bridge
Created by Fazil Abdulwahab
Your PHONE (USB debugging) → TV (Wireless/Network)
No TV USB needed!
"""

class LGTVController:
    def phone_tv_bridge(self):
        """📱 Phone USB → TV Wireless Bridge"""
        print("\n🔗 PHONE→TV Bridge Mode")
        print("1. Phone USB debugging ON")
        print("2. Find TV IP (hunt below)")
        
        # Auto-detect phone
        devices = self.run_cmd(["adb", "devices"])
        phone_match = re.search(r'([a-f0-9]{8,16})\s+device', devices)
        if not phone_match:
            print("❌ No phone detected - enable USB debugging")
            return
        
        phone_id = phone_match.group(1)
        print(f"📱 Phone found: {phone_id}")
        
        # Bridge to TV wireless
        tv_ip = input("TV IP: ").strip()
        print(f"🔌 Bridging phone → TV {tv_ip}:5555...")
        
        # Phone forwards ADB to TV
        self.run_cmd(["adb", "-s", phone_id, "tcpip", "5555"])
        self.run_cmd(["adb", "-s", phone_id, "connect", f"{tv_ip}:5555"])
        
        # Now TV accessible via phone bridge
        self.ai_tv_shell(f"{phone_id}!{tv_ip}")

    def ai_tv_shell(self, target: str):
        """🤖 AI Shell for TV via phone bridge"""
        print(f"\n🎯 AI TV Shell: {target}")
        while True:
            cmd = input("TV-AI> ").strip()
            if cmd.lower() in ['exit', 'q']:
                break
            
            parsed = self.parse_ai_adb_command(cmd)
            device_flag = "-s " + target.split('!')[0] if '!' in target else ""
            full_cmd = f"adb {device_flag} {parsed['command']}"
            result = self.run_cmd(full_cmd.split())
            print(result)

    def ssap_exploit(self, ip: str):
        """🌐 LG SSAP RCE Exploits"""
        print(f"\n💥 SSAP Exploits → {ip}:3000")
        
        exploits = {
            "rce_reboot": '{"method":"ssap://system/reboot","params":{}}',
            "rce_poweroff": '{"method":"ssap://system/turnOff","params":{}}',
            "dump_apps": '{"method":"ssap://com.webos.appBroadcast/getAppList","params":{}}',
            "dev_info": '{"method":"ssap://system.getPointerInputSocket","params":{}}',
            "ssrf_test": '{"method":"ssap://network/getSSIDInfo","params":{}}'
        }
        
        for name, payload in exploits.items():
            print(f"\n{name.upper()}:")
            try:
                resp = requests.post(f"http://{ip}:3000/", 
                                   data=payload, 
                                   headers={'Content-Type': 'application/json'},
                                   timeout=3)
                print(f"Status: {resp.status_code}")
                print(resp.text[:200])
            except Exception as e:
                print(f"Failed: {e}")

    def network_pentest(self, ip: str):
        """Full network pentest suite"""
        print(f"\n🛡️ Network Pentest: {ip}")
        
        # Port scan
        ports = self.run_cmd(["nmap", "-p", "3000,8001,8080,5555", ip])
        print("Ports:\n", ports)
        
        # SSAP exploits
        self.ssap_exploit(ip)
        
        # WebOS dev console (port 30829 sometimes)
        try:
            resp = requests.get(f"http://{ip}:30829/", timeout=3)
            print("Dev Console:", resp.text[:100])
        except:
            pass

    def run(self):
        while True:
            choice = input("\n📱1=Phone→TV  5=Network Pentest  h=IP Hunt: ").strip()
            
            if choice == '1':
                self.phone_tv_bridge()
            elif choice == '5':
                ip = input("TV IP: ")
                self.network_pentest(ip)
            elif choice == 'h':
                self.hunt_lg_ip()
            elif choice.lower() in ['q', 'exit']:
                break

# Add to usb_mode for phone-only:
def usb_mode(self):
    print("\n📱 Phone USB detected → Use '1=Phone→TV Bridge'")
    self.phone_tv_bridge()
