#!/usr/bin/env python3
"""
ENHANCED FIX: Stale Data Retry Mechanism  
This script improves stale data handling with retry logic and market hours awareness.
"""

import re
import sys
import os

def patch_stale_data_handling():
    """Patch stale data handling with retry mechanism"""
    
    bot_file = "Bot-Trading_Swing (1).py"
    
    if not os.path.exists(bot_file):
        print(f"Error: {bot_file} not found!")
        return False
    
    # Read the file
    with open(bot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Enhance the stale data warning with market hours check
    stale_pattern = r'(is_fresh = time_diff <= tf_limit\s*if not is_fresh:\s+logging\.warning\(f"\[Data Freshness\] .*?\)\n.*?logging\.info\(f"\[Data Freshness\] Last timestamp.*?return is_fresh)'
    
    def enhance_stale_check(match):
        return '''is_fresh = time_diff <= tf_limit
        if not is_fresh:
            # Check market hours before reporting staleness
            if not is_market_open(symbol):
                logging.info(f"[Data Freshness] {symbol} {primary_tf} data is not recent ({time_diff:.1f} minutes old), but market is currently closed. Skipping symbol as normal.")
                return False  # Safe to skip during market closure
            
            logging.warning(f"[Data Freshness] {symbol} {primary_tf} data is stale: {time_diff:.1f} minutes old (limit: {tf_limit})")
            logging.info(f"[Data Freshness] Last timestamp: {last_timestamp}, Current time: {now}")
            
            # Attempt recovery with retry mechanism
            recovery_success = _attempt_data_recovery_with_retry(symbol, primary_tf, time_diff)
            if not recovery_success:
                logging.error(f"[Data Freshness] CRITICAL - Failed to get recent data for {symbol} after retry attempts while market is open. Symbol will be disabled for this cycle.")
        
        return is_fresh'''
    
    content = re.sub(stale_pattern, enhance_stale_check, content, flags=re.DOTALL)
    
    # Fix 2: Enhance the recovery function with retry mechanism
    recovery_pattern = r'def _attempt_data_recovery\([^}]+\}'
    
    enhanced_recovery = '''def _attempt_data_recovery_with_retry(symbol: str, timeframe: str, stale_minutes: float, max_retries: int = 3) -> bool:
    """Enhanced data recovery with retry mechanism and market hours awareness"""
    try:
        from io_clients import DataRecoveryClient
        import time
        
        # Check market hours first
        if not is_market_open(symbol):
            logging.info(f"[Data Recovery] Market closed for {symbol}. Data staleness normal during closed hours.")
            return False
        
        logging.warning(f"[Data Recovery] {symbol} {timeframe} data is stale ({stale_minutes:.0f} minutes old). Starting retry mechanism...")
        
        retry_success = False
        for attempt in range(max_retries):
            logging.info(f"[Data Recovery] Attempting recovery for {symbol} {timeframe} (Retry {attempt + 1}/{max_retries})")
            
            try:
                recovery_client = DataRecoveryClient(use_async=False)
                success = recovery_client.attempt_data_recovery_sync(symbol, timeframe)
                
                if success:
                    logging.info(f"[Data Recovery] Recovery successful for {symbol} {timeframe} on attempt {attempt + 1}")
                    retry_success = True
                    break
                else:
                    logging.warning(f"[Data Recovery] Recovery failed for {symbol} {timeframe} on attempt {attempt + 1}")
                    
            except Exception as recovery_error:
                logging.error(f"[Data Recovery] Recovery error for {symbol} {timeframe} on attempt {attempt + 1}: {recovery_error}")
            
            # Wait before next retry (except for last attempt)
            if attempt < max_retries - 1:
                wait_time = 60  # 1 minute wait
                logging.info(f"[Data Recovery] Waiting {wait_time} seconds before next retry...")
                time.sleep(wait_time)
        
        # Final assessment
        if not retry_success:
            logging.error(f"[Data Recovery] CRITICAL - Failed to recover {symbol} {timeframe} after {max_retries} attempts while market is open!")
            return False
        
        return retry_success
        
    except Exception as e:
        logging.error(f"[Data Recovery] Recovery system error for {symbol} {timeframe}: {e}")
        return False'''
    
    content = re.sub(recovery_pattern, enhanced_recovery, content, flags=re.DOTALL)
    
    # Write the patched content
    backup_file = f"{bot_file}.stale_backup"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(open(bot_file, 'r', encoding='utf-8').read())
    
    with open(bot_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ ENHANCED FIX APPLIED: Stale data retry mechanism")
    print(f"📁 Backup created: {backup_file}")
    print(f"🔄 Bot now retries data recovery 3 times with 1-minute intervals")
    print(f"⏰ Market hours check prevents false alarms during closed hours")
    
    return True

if __name__ == "__main__":
    patch_stale_data_handling()