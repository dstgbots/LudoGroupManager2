#!/usr/bin/env python3
"""
Script to help find the correct GROUP_ID and test bot access
"""

from pyrogram import Client
import config
import asyncio

app = Client(
    name="group_id_finder",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

async def get_group_info():
    """Get information about groups the bot has access to"""
    print("🔍 Finding groups and checking access...")
    print("=" * 50)
    
    try:
        await app.start()
        me = await app.get_me()
        print(f"✅ Bot: @{me.username} (ID: {me.id})")
        print()
        
        # Try to get info about the configured group
        try:
            chat = await app.get_chat(config.GROUP_ID)
            print(f"✅ Current GROUP_ID ({config.GROUP_ID}) is accessible:")
            print(f"   📱 Name: {chat.title}")
            print(f"   👥 Type: {chat.type}")
            print(f"   👤 Members: {chat.members_count if hasattr(chat, 'members_count') else 'Unknown'}")
            
            # Check if bot is admin
            try:
                member = await app.get_chat_member(config.GROUP_ID, me.id)
                print(f"   🔧 Bot Status: {member.status}")
                if member.status in ["administrator", "creator"]:
                    print("   ✅ Bot has admin permissions")
                else:
                    print("   ⚠️ Bot is NOT an admin - this might cause issues!")
            except Exception as e:
                print(f"   ❌ Cannot check bot permissions: {e}")
                
        except Exception as e:
            print(f"❌ Cannot access GROUP_ID {config.GROUP_ID}: {e}")
            print("   This means the bot is not added to this group or GROUP_ID is wrong")
        
        print("\n" + "=" * 50)
        print("📋 To find the correct GROUP_ID:")
        print("1. Add the bot to your group")
        print("2. Make the bot an admin")
        print("3. Send any message in the group")
        print("4. The bot will print the GROUP_ID in the console")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await app.stop()

# Handler to capture group messages and show GROUP_ID
@app.on_message()
async def show_group_id(client, message):
    """Show GROUP_ID for any message received"""
    if message.chat.type.name in ["GROUP", "SUPERGROUP"]:
        print(f"\n📨 Message received from GROUP:")
        print(f"   GROUP_ID: {message.chat.id}")
        print(f"   Group Name: {message.chat.title}")
        print(f"   Message: {message.text[:50]}...")
        print(f"   From User: {message.from_user.id if message.from_user else 'Unknown'}")
        print(f"   ✅ Use this GROUP_ID in your config.py: {message.chat.id}")

async def main():
    """Main function"""
    await get_group_info()
    
    print("\n🎯 Starting message listener...")
    print("Send any message in your group to see the GROUP_ID")
    print("Press Ctrl+C to stop")
    
    try:
        await app.start()
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
