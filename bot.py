#!/usr/bin/env python3
"""
Enhanced Group Management Telegram Bot
Features:
- Original game management functionality
- MongoDB database integration  
- User balance management
- Admin-only commands
- Group management features
"""

from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from database.mongodb import db
from handlers.balance import (
    add_balance_command, 
    check_balance_command, 
    list_balances_command
)
from handlers.group_management import (
    handle_admin_table_message,
    handle_admin_edit_message,
    help_command,
    stats_command
)

# Initialize the bot client
app = Client(
    name=config.SESSION_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# ============================================================================
# COMMAND HANDLERS
# ============================================================================

@app.on_message(filters.command("addbalance") & filters.chat(config.GROUP_ID))
async def handle_add_balance(client: Client, message: Message):
    """Handle /addbalance command"""
    await add_balance_command(client, message)

@app.on_message(filters.command("balance") & filters.chat(config.GROUP_ID))
async def handle_check_balance(client: Client, message: Message):
    """Handle /balance command"""
    await check_balance_command(client, message)

@app.on_message(filters.command("listbalances") & filters.chat(config.GROUP_ID))
async def handle_list_balances(client: Client, message: Message):
    """Handle /listbalances command"""
    await list_balances_command(client, message)

@app.on_message(filters.command("help") & filters.chat(config.GROUP_ID))
async def handle_help(client: Client, message: Message):
    """Handle /help command"""
    await help_command(client, message)

@app.on_message(filters.command("stats") & filters.chat(config.GROUP_ID))
async def handle_stats(client: Client, message: Message):
    """Handle /stats command"""
    await stats_command(client, message)

# ============================================================================
# ORIGINAL GAME FUNCTIONALITY (from test.py)
# ============================================================================

@app.on_message(filters.chat(config.GROUP_ID) & filters.user(config.ADMIN_IDS) & filters.text)
async def on_admin_table_message(client: Client, message: Message):
    """Handle admin table messages for game creation (original functionality)"""
    # Skip if message starts with a command
    if message.text.startswith('/'):
        return
    
    await handle_admin_table_message(client, message)

@app.on_edited_message(filters.chat(config.GROUP_ID) & filters.user(config.ADMIN_IDS) & filters.text)
async def on_admin_edit_message(client: Client, message: Message):
    """Handle admin message edits for winner announcement (original functionality)"""
    await handle_admin_edit_message(client, message)

# ============================================================================
# BOT STARTUP AND MANAGEMENT
# ============================================================================

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    if message.chat.type.name == "PRIVATE":
        await message.reply(
            "👋 **Welcome to Group Manager Bot!**\n\n"
            "This bot is designed to work in groups for:\n"
            "• 💰 Balance management\n"
            "• 🎮 Game management\n"
            "• 👥 Group administration\n\n"
            "Add me to your group and make me an admin to get started!\n\n"
            "Use /help in the group to see available commands."
        )
    else:
        await message.reply(
            "👋 **Group Manager Bot is active!**\n\n"
            "Use /help to see available commands.\n"
            "Only authorized admins can use bot commands."
        )

async def startup_message():
    """Send startup message to the group"""
    try:
        await app.send_message(
            config.GROUP_ID,
            "🤖 **Group Manager Bot Started!**\n\n"
            "✅ Database connection established\n"
            "✅ All handlers registered\n"
            "✅ Ready to manage your group!\n\n"
            "Use /help to see available commands."
        )
    except Exception as e:
        print(f"Could not send startup message: {e}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Main function to start the bot"""
    print("🚀 Starting Group Manager Bot...")
    
    try:
        # Test database connection
        db.users.find_one()
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your MongoDB connection in config.py")
        return
    
    # Start the bot
    await app.start()
    print(f"✅ Bot started successfully!")
    print(f"📱 Bot username: @{app.me.username}")
    print(f"👥 Monitoring group: {config.GROUP_ID}")
    print(f"👨‍💼 Authorized admins: {config.ADMIN_IDS}")
    
    # Send startup message
    await startup_message()
    
    print("🎯 Bot is running... Press Ctrl+C to stop")
    
    # Keep the bot running
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot crashed: {e}")
        sys.exit(1)
