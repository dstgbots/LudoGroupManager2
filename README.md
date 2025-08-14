# Group Manager Telegram Bot

An enhanced Telegram bot for group management with MongoDB database integration, featuring balance management and game administration.

## Features

### 💰 Balance Management
- `/addbalance @username amount` - Add balance to users
- `/balance @username` - Check user balance
- `/listbalances` - View all users with balance
- Automatic transaction logging
- Persistent balance storage in MongoDB

### 🎮 Game Management
- Original game functionality preserved from `test.py`
- Automatic game detection from admin messages
- Winner announcements when games are completed
- Prize distribution tracking

### 👥 Group Administration
- Admin-only commands with automatic verification
- Group-specific command execution
- Real-time statistics and monitoring
- `/help` - Show available commands
- `/stats` - Display bot statistics

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. MongoDB Setup
Install and start MongoDB on your system, or use a cloud MongoDB service.

### 3. Configuration
Edit `config.py` with your bot credentials:
```python
API_ID = your_api_id
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
ADMIN_IDS = [your_admin_user_ids]
GROUP_ID = -your_group_id
MONGODB_URI = "your_mongodb_connection_string"
```

### 4. Run the Bot
```bash
# Enhanced bot with all features
python bot.py

# Original basic bot (unchanged)
python test.py
```

## Usage

### Adding Balance
When an admin sends this message in the group:
```
/addbalance @username 500
```

The bot will:
1. Verify the admin is authorized
2. Parse the username and amount
3. Add the amount to user's existing balance
4. Store the transaction in MongoDB
5. Reply with confirmation message

### Example Commands
```bash
/addbalance @john123 1000     # Add 1000 to john123's balance
/balance @john123             # Check john123's balance
/listbalances                 # Show all users with balance
/help                         # Show help message
/stats                        # Show bot statistics
```

## File Structure

```
group_manager_bot/
├── test.py                   # Original bot (unchanged)
├── bot.py                    # Enhanced main bot
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── database/
│   ├── __init__.py
│   ├── mongodb.py           # Database operations
│   └── models.py            # Data models
├── handlers/
│   ├── __init__.py
│   ├── balance.py           # Balance management handlers
│   └── group_management.py  # Group management features
└── utils/
    ├── __init__.py
    ├── decorators.py        # Admin verification decorators
    └── helpers.py           # Utility functions
```

## Database Schema

### Users Collection
```json
{
  "user_id": 123456789,
  "username": "john123",
  "balance": 1500.00,
  "last_updated": "2024-01-15T10:30:00"
}
```

### Transactions Collection
```json
{
  "user_id": 123456789,
  "username": "john123",
  "amount": 500.00,
  "transaction_type": "add_balance",
  "admin_id": 987654321,
  "previous_balance": 1000.00,
  "new_balance": 1500.00,
  "created_at": "2024-01-15T10:30:00"
}
```

## Security Features

- **Admin Verification**: Only authorized users can execute commands
- **Group Restriction**: Commands only work in the configured group
- **Transaction Logging**: All balance changes are logged with admin ID
- **Input Validation**: All user inputs are validated and sanitized

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MongoDB is running
   - Verify MONGODB_URI in config.py
   - Ensure database permissions are correct

2. **Bot Not Responding**
   - Verify bot token is correct
   - Check if bot is admin in the group
   - Ensure GROUP_ID is correct (negative for groups)

3. **Commands Not Working**
   - Verify user ID is in ADMIN_IDS list
   - Check if commands are sent in the correct group
   - Ensure bot has necessary permissions

### Debug Mode
Add print statements to see what's happening:
```python
print(f"Message from user: {message.from_user.id}")
print(f"Message text: {message.text}")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Check the troubleshooting section
- Review the code comments
- Test with the original `test.py` to isolate issues
