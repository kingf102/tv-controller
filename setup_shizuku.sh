# Delete broken file
rm setup_shizuku.sh

# Create fresh fixed version
cat > setup_shizuku.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# Shizuku TV Controller Setup - Fixed v5.1

echo "🔧 Installing dependencies..."
pkg update -y -qq
pkg install python nmap android-tools -y -qq

echo "📦 Installing Python packages..."
pip install -r requirements.txt -q

echo ""
echo "✅ Setup complete!"
echo "📱 Next steps:"
echo "1. Install Shizuku app (Play Store/F-Droid)"
echo "2. Enable Developer Options → Wireless debugging"
echo "3. Shizuku app → 'Start via wireless debugging'"
echo "4. Termux: shizuku pair [pairing code]"
echo "5. python3 tv_shizuku.py"
echo ""
echo "🚀 Quick test: shizuku adb connect YOUR_TV_IP"
EOF

# Make executable
chmod +x setup_shizuku.sh
