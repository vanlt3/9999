#!/usr/bin/env python3
"""
FIX: Active Symbols List Management Conflicts
This script fixes the conflicting logic in active_symbols management.
"""

import re
import sys
import os

def patch_active_symbols_logic():
    """Patch active_symbols management to prevent conflicting logic"""
    
    bot_file = "Bot-Trading_Swing (1).py"
    
    if not os.path.exists(bot_file):
        print(f"Error: {bot_file} not found!")
        return False
    
    # Read the file
    with open(bot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Replace active_symbols.clear() with proper tracking
    clear_pattern = r'self\.active_symbols\.clear\(\)\s*\n\s*print\("Starting to build/update active symbol list\.\.\."\)\s*\n\s*full_data_cache = \{\}'
    
    enhance_init = '''# Create temporary list to track successfully processed symbols
        successfully_processed_symbols = 🎯
        print("Starting to build/update active symbol list...")
        print(f"[Symbol Debug] Initial active_symbols state: {len(self.active_symbols)} symbols")
        full_data_cache = {}'''
    
    content = re.sub(clear_pattern, enhance_init, content)
    
    # Fix 2: Replace active_symbols.add() with tracking logic
    add_pattern = r'self\.active_symbols\.add\(symbol\)\s*\n\s*print\(f"  ✅ Symbol \{symbol\} has been activated\! Active symbols count: \{len\(self\.active_symbols\)\}"\)'
    
    def enhance_symbol_tracking(match):
        return '''# Track successful processing
                    successfully_processed_symbols.add(symbol)
                    print(f"  ✅ Symbol {symbol} has been processed successfully! Tracked count: {len(successfully_processed_symbols)}")'''
    
    content = re.sub(add_pattern, enhance_symbol_tracking, content)
    
    # Fix 3: Remove CRYPTO BACKUP section and replace with clean assignment
    crypto_backup_pattern = r'# --- CRYPTO BACKUP ACTIVATION ---.*?# --- DEBUG: Final active symbols summary ---'
    
    clean_assignment = '''# --- Assign cleaned active_symbols list ---
        print(f"\\n📝 [Symbol Management] Assigning final active_symbols list...")
        print(f"   [Symbol Debug] Successfully processed symbols: {len(successfully_processed_symbols)} symbols")
        print(f"   [Symbol Debug] Successfully processed list: {list(successfully_processed_symbols)}")
        
        # Clear existing and assign the properly tracked list
        self.active_symbols.clear()
        self.active_symbols.update(successfully_processed_symbols)
        
        print(f"   [Symbol Debug] Final active_symbols after assignment: {len(self.active_symbols)} symbols")

        # --- DEBUG: Final active symbols summary ---'''
    
    content = re.sub(crypto_backup_pattern, clean_assignment, content, flags=re.DOTALL)
    
    # Write the patched content
    backup_file = f"{bot_file}.symbols_backup"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(open(bot_file, 'r', encoding='utf-8').read())
    
    with open(bot_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ LOGIC FIX APPLIED: Active symbols management")
    print(f"📁 Backup created: {backup_file}")
    print(f"🎯 Bot now uses clean symbol tracking without conflicts")
    print(f"📝 Debug logging added for symbol processing visibility")
    
    return True

if __name__ == "__main__":
    patch_active_symbols_logic()