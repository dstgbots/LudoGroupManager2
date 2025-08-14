from datetime import datetime
from typing import Optional

class User:
    def __init__(self, user_id: int, username: str, balance: float = 0.0):
        self.user_id = user_id
        self.username = username
        self.balance = balance
        self.last_updated = datetime.now()
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "balance": self.balance,
            "last_updated": self.last_updated
        }

class Transaction:
    def __init__(self, user_id: int, username: str, amount: float, 
                 transaction_type: str, admin_id: int, 
                 previous_balance: float = 0.0):
        self.user_id = user_id
        self.username = username
        self.amount = amount
        self.transaction_type = transaction_type
        self.admin_id = admin_id
        self.previous_balance = previous_balance
        self.new_balance = previous_balance + amount
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "admin_id": self.admin_id,
            "previous_balance": self.previous_balance,
            "new_balance": self.new_balance,
            "created_at": self.created_at
        }

class Game:
    def __init__(self, message_id: int, players: list, amount: float):
        self.message_id = message_id
        self.players = players
        self.amount = amount
        self.created_at = datetime.now()
        self.winner = None
        self.status = "active"  # active, completed, cancelled
    
    def to_dict(self):
        return {
            "message_id": self.message_id,
            "players": self.players,
            "amount": self.amount,
            "created_at": self.created_at,
            "winner": self.winner,
            "status": self.status
        }
