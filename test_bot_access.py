#!/usr/bin/env python3
"""
Test script to check bot access and functionality
"""

from pyrogram import Client, filters
import config
import asyncio

app = Client(
    name="test_bot_access",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

@app.on_message(filters.command("test"))
async def test_command(client, message):
    """Test command to verify bot is working"""
    await message.reply(
        f"✅ **Bot is working!**\n\n"
        f"💬 **Chat Info:**\n"
        f"• Chat ID: `{message.chat.id}`\n"
        f"• Chat Type: {message.chat.type}\n"
        f"• Chat Title: {getattr(message.chat, 'title', 'N/A')}\n\n"
        f"👤 **User Info:**\n"
        f"• User ID: `{message.from_user.id}`\n"
        f"• Username: @{message.from_user.username or 'No username'}\n"
        f"• Is Admin: {'✅ Yes' if message.from_user.id in config.ADMIN_IDS else '❌ No'}\n\n"
        f"⚙️ **Config Check:**\n"
        f"• Expected Group: `{config.GROUP_ID}`\n"
        f"• Current Group: `{message.chat.id}`\n"
        f"• Match: {'✅ Yes' if message.chat.id == config.GROUP_ID else '❌ No'}"
    )

@app.on_message(filters.command("start"))
async def start_command(client, message):
    """Start command"""
    await message.reply(
        "👋 **Test Bot Started!**\n\n"
        "🧪 **Available test commands:**\n"
        "• `/test` - Check bot functionality\n"
        "• `/id` - Get chat and user IDs\n"
        "• `/ping` - Simple ping test\n\n"
        f"📍 **Current Chat ID:** `{message.chat.id}`\n"
        f"📍 **Your User ID:** `{message.from_user.id}`\n\n"
        "💡 **If this is your group, update config.py with the Chat ID shown above**"
    )

@app.on_message(filters.command("id"))
async def id_command(client, message):
    """Get IDs"""
    await message.reply(
        f"🆔 **ID Information:**\n\n"
        f"**Chat Details:**\n"
        f"• ID: `{message.chat.id}`\n"
        f"• Type: {message.chat.type}\n"
        f"• Title: {getattr(message.chat, 'title', 'N/A')}\n\n"
        f"**Your Details:**\n"
        f"• User ID: `{message.from_user.id}`\n"
        f"• Username: @{message.from_user.username or 'None'}\n"
        f"• First Name: {message.from_user.first_name}\n\n"
        f"**For config.py:**\n"
        f"```\n"
        f"GROUP_ID = {message.chat.id}\n"
        f"ADMIN_IDS = [{message.from_user.id}]\n"
        f"```"
    )

@app.on_message(filters.command("ping"))
async def ping_command(client, message):
    """Ping test"""
    await message.reply("🏓 Pong! Bot is responsive.")

async def main():
    """Main function"""
    print("🧪 Starting Test Bot...")
    print("=" * 50)
    
    try:
        await app.start()
        me = await app.get_me()
        print(f"✅ Bot started: @{me.username}")
        print(f"🆔 Bot ID: {me.id}")
        print(f"📱 Bot Username: @{me.username}")
        
        print("\n📋 Test Instructions:")
        print("1. Add this bot to your group")
        print("2. Make it an admin")
        print("3. Send /test in the group")
        print("4. Check the response for correct IDs")
        print("5. Update config.py if needed")
        
        print("\n🎯 Bot is running... Send /test in your group")
        print("Press Ctrl+C to stop")
        
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Test bot stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
