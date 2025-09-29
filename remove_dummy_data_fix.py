#!/usr/bin/env python3
"""
CRITICAL SAFETY FIX: Remove dummy data generation
This script patches the main bot file to eliminate dangerous dummy data generation
and replace it with safe error handling.
"""

import re
import sys
import os

def patch_bot_file():
    """Patch the bot file to remove dummy data generation"""
    
    bot_file = "Bot-Trading_Swing (1).py"
    
    if not os.path.exists(bot_file):
        print(f"Error: {bot_file} not found!")
        return False
    
    # Read the file
    with open(bot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Replace dummy data calls with safe error handling
    pattern1 = r'(.*?)_add_fallback_data\((.*?)\)\s*\n(.*?)(continue|return)'
    
    def replace_fallback(match):
        prefix = match.group(1)
        args = match.group(2) 
        suffix = match.group(3)
        control_flow = match.group(4)
        
        return f'''{prefix}logging.error(f"[Data Safety] CRITICAL - Skipping symbol due to data failure. No dummy data will be created.")
                    print(f"   [Data Safety] CRITICAL - Data unavailable. Symbol completely disabled.")
                    continue'''
    
    content = re.sub(pattern1, replace_fallback, content, flags=re.DOTALL)
    
    # Fix 2: Remove the entire _add_fallback_data function
    pattern2 = r'def _add_fallback_data\([^}]+\}'
    content = re.sub(pattern2, '''def _safe_data_error_handling(self, symbol):
        """
        SAFETY: Handle data errors without dummy data generation
        """
        error_msg = f"CRITICAL - Failed to fetch data for {{symbol}}. Trading disabled for {{symbol}}."
        logging.error(f"[Data Safety] {{error_msg}}")
        print(f"   [Data Safety] {{error_msg}}")
        
        # DO NOT create any fake data - let symbol remain unavailable
        # This ensures trading decisions are never based on artificial data
        pass''', content, flags=re.DOTALL)
    
    # Fix 3: Add emergency stop condition for high failure rates
    emergency_check = '''
        # EMERGENCY STOP: Check if too many symbols failed
        symbols_with_data = len([s for s in all_symbols if s in live_data_cache])
        symbols_failed = len(all_symbols) - symbols_with_data
        failure_rate = symbols_failed / len(all_symbols) if all_symbols else 0
        
        if failure_rate > 0.30:  # Over 30% failure rate
            error_msg = f"🚨 EMERGENCY STOP CONDITION: {symbols_failed}/{len(all_symbols)} symbols ({failure_rate:.1%}) failed data retrieval. Bot disabled for safety."
            logging.critical(error_msg)
            print(f"[EMERGENCY STOP] {error_msg}")
            raise RuntimeError(f"Emergency stop: {failure_rate:.1%} data failure rate exceeds safety threshold.")
            
        elif symbols_failed > 0:
            warning_msg = f"⚠️ DATA WARNING: {symbols_failed}/{len(all_symbols)} symbols failed data retrieval ({failure_rate:.1%}). Continuing with reduced symbol set."
            logging.warning(warning_msg)
            print(f"[Data Warning] {warning_msg}")
        '''
    
    # Add the emergency check before return statement
    content = re.sub(
        r'(\n\s*return live_data_cache)',
        emergency_check + r'\1',
        content
    )
    
    # Write the patched content
    backup_file = f"{bot_file}.backup"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(open(bot_file, 'r', encoding='utf-8').read())
    
    with open(bot_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ CRITICAL FIX APPLIED: Removed dummy data generation")
    print(f"📁 Backup created: {backup_file}")
    print(f"🔒 Bot now safely skips symbols with missing data")
    
    return True

if __name__ == "__main__":
    patch_bot_file()