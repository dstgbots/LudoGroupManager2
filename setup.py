#!/usr/bin/env python3
"""
Setup script for Group Manager Bot
Helps with initial installation and configuration
"""

import os
import sys
import subprocess
import json

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_mongodb():
    """Check if MongoDB is accessible"""
    print("🗄️ Checking MongoDB connection...")
    try:
        from pymongo import MongoClient
        
        # Try to connect to default MongoDB
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        client.server_info()  # Force connection
        client.close()
        
        print("✅ MongoDB connection successful!")
        return True
    except Exception as e:
        print(f"⚠️ MongoDB connection failed: {e}")
        print("📋 Please ensure MongoDB is installed and running")
        print("   - Install: https://www.mongodb.com/try/download/community")
        print("   - Or use MongoDB Atlas (cloud): https://www.mongodb.com/atlas")
        return False

def create_sample_config():
    """Create a sample configuration file"""
    config_content = '''# Configuration file for the enhanced group management bot

# Bot Configuration (Get these from @BotFather)
API_ID = 12345678  # Your API ID from https://my.telegram.org
API_HASH = "your_api_hash_here"  # Your API Hash from https://my.telegram.org
BOT_TOKEN = "your_bot_token_here"  # Bot token from @BotFather

# Admin and Group Configuration
ADMIN_IDS = [123456789]  # List of admin user IDs (get from @userinfobot)
GROUP_ID = -1001234567890  # Group ID where bot will work (negative for groups)

# MongoDB Configuration
MONGODB_URI = "mongodb://localhost:27017"  # MongoDB connection string
DATABASE_NAME = "telegram_bot_db"
USERS_COLLECTION = "users"
TRANSACTIONS_COLLECTION = "transactions"

# Bot Settings
SESSION_NAME = "group_manager_bot"

# Instructions:
# 1. Replace the placeholder values above with your actual values
# 2. Get API_ID and API_HASH from https://my.telegram.org
# 3. Get BOT_TOKEN from @BotFather on Telegram
# 4. Get your user ID from @userinfobot on Telegram
# 5. Add the bot to your group and get the group ID
# 6. Make sure MongoDB is running (local) or update MONGODB_URI for cloud
'''
    
    if os.path.exists("config.py"):
        print("⚠️ config.py already exists. Skipping creation.")
        return False
    
    try:
        with open("config.py", "w") as f:
            f.write(config_content)
        print("✅ Sample config.py created!")
        print("📝 Please edit config.py with your bot credentials")
        return True
    except Exception as e:
        print(f"❌ Failed to create config.py: {e}")
        return False

def setup_directory_structure():
    """Ensure all required directories exist"""
    directories = ["database", "handlers", "utils"]
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"📁 Created directory: {directory}")
            except Exception as e:
                print(f"❌ Failed to create directory {directory}: {e}")
                return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Group Manager Bot Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Setup directory structure
    print("📁 Setting up directory structure...")
    if not setup_directory_structure():
        print("❌ Failed to setup directories")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed due to dependency installation issues")
        sys.exit(1)
    
    # Check MongoDB
    mongodb_ok = check_mongodb()
    
    # Create sample config
    config_created = create_sample_config()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("=" * 50)
    
    print("\n📋 Next Steps:")
    print("1. Edit config.py with your bot credentials")
    if not mongodb_ok:
        print("2. Install and start MongoDB")
    print("3. Run the bot with: python start_bot.py")
    
    if config_created:
        print("\n⚠️ IMPORTANT: Update config.py before running the bot!")
    
    print("\n📖 For detailed instructions, see README.md")

if __name__ == "__main__":
    main()
