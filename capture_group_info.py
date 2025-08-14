#!/usr/bin/env python3
"""
Script to capture forwarded messages and extract group information
"""

from pyrogram import Client, filters
import config
import asyncio

app = Client(
    name="group_info_capture",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

@app.on_message(filters.forwarded)
async def capture_forwarded_message(client, message):
    """Capture forwarded messages and extract group info"""
    print("\n" + "="*60)
    print("📨 FORWARDED MESSAGE CAPTURED!")
    print("="*60)
    
    # Current chat info (where message was forwarded to)
    print(f"📍 **Current Chat (where you sent this):**")
    print(f"   • Chat ID: {message.chat.id}")
    print(f"   • Chat Type: {message.chat.type}")
    print(f"   • Chat Title: {getattr(message.chat, 'title', 'DM/Private')}")
    
    # Forwarded from info
    if message.forward_from_chat:
        print(f"\n🎯 **ORIGINAL GROUP INFO:**")
        print(f"   • Group ID: {message.forward_from_chat.id}")
        print(f"   • Group Type: {message.forward_from_chat.type}")
        print(f"   • Group Title: {message.forward_from_chat.title}")
        print(f"   • Group Username: @{message.forward_from_chat.username or 'No username'}")
        
        print(f"\n📋 **For your config.py:**")
        print(f"   GROUP_ID = {message.forward_from_chat.id}")
        
        # Reply to user with the info
        await message.reply(
            f"✅ **Group Information Captured!**\n\n"
            f"🎯 **Original Group:**\n"
            f"• **Group ID:** `{message.forward_from_chat.id}`\n"
            f"• **Group Name:** {message.forward_from_chat.title}\n"
            f"• **Group Type:** {message.forward_from_chat.type}\n"
            f"• **Username:** @{message.forward_from_chat.username or 'None'}\n\n"
            f"📝 **Update your config.py:**\n"
            f"```python\n"
            f"GROUP_ID = {message.forward_from_chat.id}\n"
            f"```\n\n"
            f"💡 Make sure to add the bot @{(await client.get_me()).username} to this group and make it admin!"
        )
        
    elif message.forward_from:
        print(f"\n👤 **Forwarded from User:**")
        print(f"   • User ID: {message.forward_from.id}")
        print(f"   • Username: @{message.forward_from.username or 'No username'}")
        print(f"   • Name: {message.forward_from.first_name}")
        
        await message.reply(
            f"ℹ️ This message was forwarded from a user, not a group.\n"
            f"Please forward a message directly from your group."
        )
    else:
        print(f"\n⚠️ **Unknown forward source**")
        await message.reply(
            f"⚠️ Could not determine the source of this forwarded message.\n"
            f"Please try forwarding a regular message from your group."
        )
    
    print("="*60)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    """Start command with instructions"""
    me = await client.get_me()
    await message.reply(
        f"👋 **Group Info Capture Bot**\n\n"
        f"🎯 **Instructions:**\n"
        f"1. Go to your Telegram group\n"
        f"2. Find any message in the group\n"
        f"3. Forward that message to this bot\n"
        f"4. I'll extract the group information for you!\n\n"
        f"🤖 **Bot:** @{me.username}\n"
        f"📨 **Just forward any message from your group now!**"
    )

@app.on_message(filters.text & ~filters.forwarded & ~filters.command("start"))
async def regular_message(client, message):
    """Handle regular messages"""
    await message.reply(
        f"📨 **Please forward a message from your group**\n\n"
        f"I need a forwarded message to extract the group information.\n"
        f"Go to your group → Select any message → Forward it here!"
    )

async def main():
    """Main function"""
    print("🚀 Starting Group Info Capture Bot...")
    print("="*50)
    
    try:
        await app.start()
        me = await app.get_me()
        print(f"✅ Bot started: @{me.username}")
        print(f"🆔 Bot ID: {me.id}")
        
        print(f"\n📋 Instructions:")
        print(f"1. Start a chat with @{me.username}")
        print(f"2. Forward any message from your group to the bot")
        print(f"3. The bot will show you the correct GROUP_ID")
        print(f"4. Update your config.py with the correct GROUP_ID")
        
        print(f"\n🎯 Bot is ready! Waiting for forwarded messages...")
        print(f"Press Ctrl+C to stop")
        
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        print(f"\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
