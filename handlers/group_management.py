from pyrogram import Client, filters
from pyrogram.types import Message
import re
from datetime import datetime
import config
from database.mongodb import db
from utils.decorators import admin_only

# Store active games (from original functionality)
games = {}

def extract_game_data_from_message(message_text):
    """Extract game data from admin messages (original functionality)"""
    lines = message_text.strip().split("\n")
    usernames = []
    amount = None

    for line in lines:
        if "full" in line.lower():
            match = re.search(r"(\d+)\s*[Ff]ull", line)
            if match:
                amount = int(match.group(1))
        else:
            match = re.search(r"@?(\w+)", line)
            if match:
                usernames.append(match.group(1))

    if not usernames or not amount:
        return None

    return {
        "players": usernames,
        "amount": amount,
        "created_at": datetime.now()
    }

def extract_winner_from_edited_message(message_text):
    """Extract winner from edited messages (original functionality)"""
    patterns = [
        r'@(\w+)\s*✅',
        r'(\w+)\s*✅',
        r'✅\s*@(\w+)',
        r'✅\s*(\w+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, message_text)
        if match:
            return match.group(1)
    return None

async def handle_admin_table_message(client: Client, message: Message):
    """Handle admin table messages for game creation (original functionality)"""
    if message.from_user.id not in config.ADMIN_IDS:
        return
        
    game_data = extract_game_data_from_message(message.text)
    if game_data:
        games[message.id] = game_data
        print(f"Game created: {game_data}")

async def handle_admin_edit_message(client: Client, message: Message):
    """Handle admin message edits for winner announcement (original functionality)"""
    if message.from_user.id not in config.ADMIN_IDS:
        return
        
    winner = extract_winner_from_edited_message(message.text)
    if winner and message.id in games:
        game_data = games.pop(message.id)
        print(f"Winner: {winner} for game: {game_data}")
        
        # Send message to the group announcing the winner
        await client.send_message(
            config.GROUP_ID,
            f"🎉 Winner Found: @{winner}\n💰 Prize: {game_data['amount']}"
        )

@admin_only
async def help_command(client: Client, message: Message):
    """Show available commands"""
    help_text = """
🤖 **Group Manager Bot Commands**

**💰 Balance Management:**
• `/addbalance @username amount` - Add balance to user
• `/balance @username` - Check user balance  
• `/listbalances` - Show all users with balance

**🎮 Game Management:**
• Original game functionality still works
• Post player list with amount for game creation
• Edit message with ✅ next to winner name

**👥 Group Commands:**
• `/help` - Show this help message
• `/stats` - Show bot statistics

**⚡ Quick Examples:**
• `/addbalance @john123 500`
• `/balance @john123`

**📋 Note:** Only authorized admins can use these commands.
"""
    await message.reply(help_text)

@admin_only
async def stats_command(client: Client, message: Message):
    """Show bot statistics"""
    try:
        # Get user count
        total_users = db.users.count_documents({})
        users_with_balance = db.users.count_documents({"balance": {"$gt": 0}})
        
        # Get total balance
        pipeline = [
            {"$group": {"_id": None, "total_balance": {"$sum": "$balance"}}}
        ]
        total_balance_result = list(db.users.aggregate(pipeline))
        total_balance = total_balance_result[0]["total_balance"] if total_balance_result else 0
        
        # Get transaction count
        total_transactions = db.transactions.count_documents({})
        
        # Get active games count
        active_games = len(games)
        
        stats_text = f"""
📊 **Bot Statistics**

👥 **Users:**
• Total Users: {total_users:,}
• Users with Balance: {users_with_balance:,}

💰 **Financial:**
• Total Balance: {total_balance:,.2f}
• Total Transactions: {total_transactions:,}

🎮 **Games:**
• Active Games: {active_games}

📅 **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        await message.reply(stats_text)
        
    except Exception as e:
        print(f"Error in stats_command: {e}")
        await message.reply("❌ An error occurred while fetching statistics.")
