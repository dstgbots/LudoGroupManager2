import re
from datetime import datetime
from typing import Optional, Tuple

def parse_username_from_mention(text: str) -> Optional[str]:
    """Extract username from @username mention"""
    pattern = r'@(\w+)'
    match = re.search(pattern, text)
    return match.group(1) if match else None

def parse_amount_from_text(text: str) -> Optional[float]:
    """Extract amount (number) from text"""
    pattern = r'(\d+(?:\.\d+)?)'
    match = re.search(pattern, text)
    try:
        return float(match.group(1)) if match else None
    except ValueError:
        return None

def format_currency(amount: float) -> str:
    """Format amount as currency with commas"""
    return f"{amount:,.2f}"

def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def validate_balance_command(text: str) -> Tuple[bool, Optional[str], Optional[float], Optional[str]]:
    """
    Validate and parse /addbalance command
    Returns: (is_valid, username, amount, error_message)
    """
    # Remove extra whitespace
    text = text.strip()
    
    # Check if it starts with /addbalance
    if not text.lower().startswith('/addbalance'):
        return False, None, None, "Command must start with /addbalance"
    
    # Parse the command
    pattern = r'/addbalance\s+@?(\w+)\s+(\d+(?:\.\d+)?)'
    match = re.search(pattern, text, re.IGNORECASE)
    
    if not match:
        return False, None, None, "Invalid format! Use: /addbalance @username amount"
    
    username = match.group(1)
    try:
        amount = float(match.group(2))
    except ValueError:
        return False, None, None, "Invalid amount format!"
    
    if amount <= 0:
        return False, None, None, "Amount must be greater than 0!"
    
    if len(username) < 3:
        return False, None, None, "Username must be at least 3 characters long!"
    
    return True, username, amount, None

def sanitize_username(username: str) -> str:
    """Sanitize username by removing @ and converting to lowercase"""
    return username.replace('@', '').lower()

def generate_transaction_id() -> str:
    """Generate a unique transaction ID"""
    return f"TXN_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{datetime.now().microsecond}"

def is_valid_amount(amount_str: str) -> bool:
    """Check if string is a valid amount"""
    try:
        amount = float(amount_str)
        return amount > 0
    except ValueError:
        return False
