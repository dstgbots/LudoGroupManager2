#!/usr/bin/env python3
"""
Quick script to update config.py with correct GROUP_ID
"""

import re

def update_group_id(new_group_id):
    """Update GROUP_ID in config.py"""
    try:
        # Read current config
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Replace GROUP_ID
        updated_content = re.sub(
            r'GROUP_ID = -?\d+',
            f'GROUP_ID = {new_group_id}',
            content
        )
        
        # Write updated config
        with open('config.py', 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated config.py with GROUP_ID = {new_group_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Config Updater")
    print("=" * 30)
    
    try:
        group_id = input("Enter the correct GROUP_ID: ")
        group_id = int(group_id)
        
        if update_group_id(group_id):
            print("\n✅ Configuration updated successfully!")
            print("🚀 Now you can run: python start_bot.py")
        else:
            print("\n❌ Failed to update configuration")
            
    except ValueError:
        print("❌ Invalid GROUP_ID. Please enter a valid number.")
    except KeyboardInterrupt:
        print("\n🛑 Cancelled by user")
