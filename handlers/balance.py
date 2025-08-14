from pyrogram import Client, filters
from pyrogram.types import Message
import re
import config
from database.mongodb import db
from utils.decorators import admin_only

@admin_only
async def add_balance_command(client: Client, message: Message):
    """Handle /addbalance @username amount command"""
    try:
        # Parse the command
        text = message.text.strip()
        
        # Regex to match /addbalance @username amount or /addbalance username amount
        pattern = r'/addbalance\s+@?(\w+)\s+(\d+(?:\.\d+)?)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if not match:
            await message.reply(
                "❌ Invalid format!\nUse: `/addbalance @username amount`\nExample: `/addbalance @john123 100`"
            )
            return
        
        username = match.group(1)
        amount = float(match.group(2))
        
        if amount <= 0:
            await message.reply("❌ Amount must be greater than 0!")
            return
        
        # Try to get user info from the mentioned user
        user_id = None
        
        # Check if there are entities (mentions) in the message
        if message.entities:
            for entity in message.entities:
                if entity.type.name == "MENTION":
                    # Get the mentioned user
                    mentioned_text = text[entity.offset:entity.offset + entity.length]
                    if mentioned_text.replace('@', '').lower() == username.lower():
                        # Try to get user from the group
                        try:
                            chat_member = await client.get_chat_member(config.GROUP_ID, mentioned_text)
                            user_id = chat_member.user.id
                            username = chat_member.user.username or chat_member.user.first_name
                            break
                        except:
                            pass
                elif entity.type.name == "TEXT_MENTION":
                    # Direct user mention
                    if entity.user.username and entity.user.username.lower() == username.lower():
                        user_id = entity.user.id
                        username = entity.user.username or entity.user.first_name
                        break
        
        # If we couldn't get user_id from mentions, we'll use a placeholder
        # In a real scenario, you might want to search your database or ask for clarification
        if user_id is None:
            # For now, we'll create a record with username only
            # You can enhance this to search existing users by username
            user_id = hash(username) % (10**10)  # Generate a pseudo user_id
        
        # Add balance to database
        success, new_balance = db.add_balance(
            user_id=user_id,
            username=username,
            amount=amount,
            admin_id=message.from_user.id
        )
        
        if success:
            # Reply with success message
            await message.reply(
                f"✅ **Balance Added Successfully!**\n\n"
                f"👤 **User:** @{username}\n"
                f"💰 **Amount Added:** {amount:,.2f}\n"
                f"💵 **New Balance:** {new_balance:,.2f}\n"
                f"🔧 **Added by:** @{message.from_user.username}"
            )
        else:
            await message.reply(
                f"❌ **Failed to add balance!**\n"
                f"Please try again or contact support."
            )
            
    except ValueError:
        await message.reply("❌ Invalid amount! Please use a valid number.")
    except Exception as e:
        print(f"Error in add_balance_command: {e}")
        await message.reply("❌ An error occurred while processing the command.")

@admin_only
async def check_balance_command(client: Client, message: Message):
    """Handle /balance @username command"""
    try:
        text = message.text.strip()
        
        # Parse username from command
        pattern = r'/balance\s+@?(\w+)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if not match:
            await message.reply(
                "❌ Invalid format!\nUse: `/balance @username`\nExample: `/balance @john123`"
            )
            return
        
        username = match.group(1)
        
        # Search for user in database by username
        user = db.users.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
        
        if user:
            balance = user.get("balance", 0)
            last_updated = user.get("last_updated", "Unknown")
            
            await message.reply(
                f"💰 **Balance Information**\n\n"
                f"👤 **User:** @{user['username']}\n"
                f"💵 **Current Balance:** {balance:,.2f}\n"
                f"📅 **Last Updated:** {last_updated.strftime('%Y-%m-%d %H:%M:%S') if hasattr(last_updated, 'strftime') else last_updated}"
            )
        else:
            await message.reply(f"❌ User @{username} not found in database!")
            
    except Exception as e:
        print(f"Error in check_balance_command: {e}")
        await message.reply("❌ An error occurred while checking balance.")

@admin_only
async def list_balances_command(client: Client, message: Message):
    """Handle /listbalances command"""
    try:
        users_with_balance = db.get_all_users_with_balance()
        
        if not users_with_balance:
            await message.reply("📊 No users with balance found in database!")
            return
        
        # Sort by balance (highest first)
        users_with_balance.sort(key=lambda x: x.get("balance", 0), reverse=True)
        
        balance_text = "💰 **All User Balances:**\n\n"
        
        for i, user in enumerate(users_with_balance[:20], 1):  # Limit to top 20
            username = user.get("username", "Unknown")
            balance = user.get("balance", 0)
            balance_text += f"{i}. @{username}: {balance:,.2f}\n"
        
        if len(users_with_balance) > 20:
            balance_text += f"\n... and {len(users_with_balance) - 20} more users"
        
        await message.reply(balance_text)
        
    except Exception as e:
        print(f"Error in list_balances_command: {e}")
        await message.reply("❌ An error occurred while fetching balances.")
