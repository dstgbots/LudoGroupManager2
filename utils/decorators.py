from functools import wraps
from pyrogram.types import Message
import config

def admin_only(func):
    """Decorator to ensure only authorized admins can use commands"""
    @wraps(func)
    async def wrapper(client, message: Message):
        # Check if user is authorized admin
        if message.from_user.id not in config.ADMIN_IDS:
            await message.reply(
                "❌ **Access Denied!**\n"
                "You are not authorized to use this command.\n"
                "Only authorized admins can use bot commands."
            )
            return
        
        # Check if message is from the configured group
        if message.chat.id != config.GROUP_ID:
            await message.reply(
                "❌ **Wrong Group!**\n"
                "This command can only be used in the authorized group."
            )
            return
        
        # Execute the original function
        return await func(client, message)
    
    return wrapper

def group_only(func):
    """Decorator to ensure commands are only used in the configured group"""
    @wraps(func)
    async def wrapper(client, message: Message):
        if message.chat.id != config.GROUP_ID:
            await message.reply(
                "❌ **Wrong Group!**\n"
                "This command can only be used in the authorized group."
            )
            return
        
        return await func(client, message)
    
    return wrapper
