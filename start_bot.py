#!/usr/bin/env python3
"""
Startup script for the Group Manager Bot
Provides easy way to start the enhanced bot with proper error handling
"""

import sys
import os
import asyncio
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['pyrogram', 'pymongo']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install dependencies with: pip install -r requirements.txt")
        return False
    
    return True

def check_config():
    """Check if configuration is properly set"""
    try:
        import config
        
        # Check required configuration
        required_config = ['API_ID', 'API_HASH', 'BOT_TOKEN', 'ADMIN_IDS', 'GROUP_ID']
        missing_config = []
        
        for attr in required_config:
            if not hasattr(config, attr) or not getattr(config, attr):
                missing_config.append(attr)
        
        if missing_config:
            print("❌ Missing configuration values:")
            for item in missing_config:
                print(f"   - {item}")
            print("\n⚙️ Please update config.py with your bot credentials")
            return False
        
        return True
        
    except ImportError:
        print("❌ config.py file not found!")
        print("⚙️ Please create config.py with your bot credentials")
        return False

def main():
    """Main startup function"""
    print("🚀 Group Manager Bot Startup Script")
    print("=" * 50)
    
    # Check dependencies
    print("📋 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ Dependencies OK")
    
    # Check configuration
    print("⚙️ Checking configuration...")
    if not check_config():
        sys.exit(1)
    print("✅ Configuration OK")
    
    # Start the bot
    print("🤖 Starting Group Manager Bot...")
    print("=" * 50)
    
    try:
        # Import and run the bot
        from bot import main as bot_main
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("\n📋 Troubleshooting:")
        print("1. Check MongoDB is running")
        print("2. Verify bot token and permissions")
        print("3. Ensure group ID is correct")
        sys.exit(1)

if __name__ == "__main__":
    main()
