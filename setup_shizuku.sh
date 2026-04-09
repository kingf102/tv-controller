### **4. `setup_shizuku.sh`**
```bash
#!/data/data/com.termux/files/usr/bin/bash
echo "🔧 Clean Setup"
pkg update && pkg install python nmap android-tools -y
pip install -r requirements.txt
echo "✅ Ready! Run: python3 tv_shizuku.py"
