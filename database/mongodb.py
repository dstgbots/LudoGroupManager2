from pymongo import MongoClient
from datetime import datetime
import config

class MongoDB:
    def __init__(self):
        self.client = MongoClient(config.MONGODB_URI)
        self.db = self.client[config.DATABASE_NAME]
        self.users = self.db[config.USERS_COLLECTION]
        self.transactions = self.db[config.TRANSACTIONS_COLLECTION]
        
        # Create indexes for better performance
        self.users.create_index("user_id", unique=True)
        self.transactions.create_index("user_id")
        self.transactions.create_index("created_at")
    
    def get_user_balance(self, user_id):
        """Get user's current balance"""
        user = self.users.find_one({"user_id": user_id})
        return user["balance"] if user else 0
    
    def add_balance(self, user_id, username, amount, admin_id):
        """Add balance to a user"""
        try:
            # Update or create user record
            current_balance = self.get_user_balance(user_id)
            new_balance = current_balance + amount
            
            # Update user balance
            self.users.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "user_id": user_id,
                        "username": username,
                        "balance": new_balance,
                        "last_updated": datetime.now()
                    }
                },
                upsert=True
            )
            
            # Record transaction
            self.transactions.insert_one({
                "user_id": user_id,
                "username": username,
                "amount": amount,
                "transaction_type": "add_balance",
                "admin_id": admin_id,
                "created_at": datetime.now(),
                "previous_balance": current_balance,
                "new_balance": new_balance
            })
            
            return True, new_balance
        except Exception as e:
            print(f"Error adding balance: {e}")
            return False, 0
    
    def get_user_info(self, user_id):
        """Get complete user information"""
        return self.users.find_one({"user_id": user_id})
    
    def get_transaction_history(self, user_id, limit=10):
        """Get user's transaction history"""
        return list(self.transactions.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(limit))
    
    def get_all_users_with_balance(self):
        """Get all users who have balance"""
        return list(self.users.find({"balance": {"$gt": 0}}))

# Create a global instance
db = MongoDB()
