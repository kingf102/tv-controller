#!/bin/bash
pkg update && pkg install python nmap android-tools -y
pip install requests google-generativeai
echo "✅ Ready! python3 tv_ultimate.py"
