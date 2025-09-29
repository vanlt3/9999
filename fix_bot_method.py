#!/usr/bin/env python3
"""
Fix script for Bot-Trading_Swing.py
Adds the missing get_dynamic_confidence_for_component method to EnhancedTradingBot class
"""

import os
import shutil
from datetime import datetime

def backup_original_file(file_path):
    """Create a backup of the original file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    shutil.copy2(file_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    return backup_path

def find_insertion_point(content):
    """Find where to insert the method in the EnhancedTradingBot class"""
    lines = content.split('\n')
    
    # Look for the end of a method that should come before get_dynamic_confidence_for_component
    insertion_line = None
    
    for i, line in enumerate(lines):
        # Look for a method that typically comes before get_dynamic_confidence_for_component
        if 'return False' in line and i > 0:
            # Check if this looks like the end of schedule_symbol_processing method
            check_start = max(0, i-50)
            prev_lines = lines[check_start:i+1]
            if any('def schedule_symbol_processing' in l for l in prev_lines):
                # Look for the next method after return False
                for j in range(i+1, min(i+20, len(lines))):
                    if lines[j].strip() and not lines[j].startswith('#'):
                        insertion_line = j
                        break
                break
    
    # Alternative: look for where get_highest_scoring_component_for_symbol should be
    if insertion_line is None:
        for i, line in enumerate(lines):
            if 'def get_highest_scoring_component_for_symbol' in line:
                insertion_line = i
                break
    
    return insertion_line

def add_method_to_class(content):
    """Add the get_dynamic_confidence_for_component method to the class"""
    
    method_code = '''    def get_dynamic_confidence_for_component(self, symbol, component, action="HOLD", market_data=None):
        """
        Get dynamic confidence for specific components (RL, Master Agent, Online Learning)
        """
        try:
            # Base confidence values by component
            base_confidences = {
                'rl': 0.45,
                'master_agent': 0.35,
                'online_learning': 0.4,
                'ensemble': 0.4
            }
            
            base_confidence = base_confidences.get(component, 0.4)
            
            # Apply symbol-specific adjustments
            EQUITY_INDICES = ['SPX500', 'NASDAQ', 'DOW30', 'UK100', 'GER30', 'FRA40', 'AUS200', 'JPN225']
            
            if symbol in ['BTCUSD', 'ETHUSD']:
                # Major crypto pairs get higher confidence
                multipliers = {
                    'rl': 1.0,          # Keep RL as is for major crypto
                    'master_agent': 0.85, # Reduce master agent slightly
                    'online_learning': 0.95, # Keep online learning high
                    'ensemble': 0.9
                }
            elif symbol in ['XAUUSD']:
                # Gold gets moderate confidence
                multipliers = {
                    'rl': 0.95,
                    'master_agent': 0.9,
                    'online_learning': 0.9,
                    'ensemble': 0.9
                }
            elif symbol in EQUITY_INDICES:
                # Equity indices get lower confidence due to volatility
                multipliers = {
                    'rl': 0.9,
                    'master_agent': 0.8,
                    'online_learning': 0.85,
                    'ensemble': 0.85
                }
            else:
                # Other symbols get standard confidence
                multipliers = {
                    'rl': 0.95,
                    'master_agent': 0.85,
                    'online_learning': 0.9,
                    'ensemble': 0.9
                }
            
            # Apply component-specific multiplier
            confidence = base_confidence * multipliers.get(component, 0.9)
            
            # Market data adjustments
            if market_data is not None and hasattr(market_data, 'empty') and not market_data.empty:
                try:
                    import pandas as pd
                    # Check recent volatility
                    if len(market_data) >= 20:
                        recent_returns = market_data['close'].pct_change().tail(20)
                        volatility = recent_returns.std()
                        
                        if volatility > 0.03:  # High volatility
                            confidence *= 0.9
                        elif volatility < 0.01:  # Low volatility
                            confidence *= 1.05
                    
                    # Check trend strength
                    if len(market_data) >= 10:
                        recent_closes = market_data['close'].tail(10)
                        trend_strength = abs(recent_closes.iloc[-1] - recent_closes.iloc[0]) / recent_closes.iloc[0]
                        
                        if trend_strength > 0.02:  # Strong trend
                            confidence *= 1.05
                        elif trend_strength < 0.005:  # Weak trend
                            confidence *= 0.95
                            
                except Exception as e:
                    try:
                        logger.debug(f"Error in market data adjustments for {symbol}: {e}")
                    except:
                        pass  # Logger might not be available
            
            # Action-specific adjustments
            if action in ['BUY', 'SELL']:
                confidence *= 1.02  # Slight boost for directional actions
            
            # Clamp between reasonable bounds
            return max(0.15, min(0.75, confidence))
            
        except Exception as e:
            try:
                logger.error(f"Error calculating dynamic confidence for {component} on {symbol}: {e}")
            except:
                print(f"Error calculating dynamic confidence for {component} on {symbol}: {e}")
            return base_confidences.get(component, 0.4)

'''
    
    lines = content.split('\n')
    
    # Find insertion point
    insertion_line = find_insertion_point(content)
    
    if insertion_line is None:
        print("❌ Could not find suitable insertion point in EnhancedTradingBot class")
        return None, False
    
    # Insert the method
    method_lines = method_code.strip().split('\n')
    lines.insert(insertion_line, '')  # Add empty line before method
    while method_lines:
        lines.insert(insertion_line + 1, method_lines.pop(0))
    
    # Add empty line after method
    lines.insert(insertion_line + len(method_lines) + 1, '')
    
    return '\n'.join(lines), True

def check_method_exists(content):
    """Check if the method already exists"""
    return 'def get_dynamic_confidence_for_component(' in content

def fix_bot_file(file_path):
    """Main function to fix the bot file"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🔧 Fixing: {file_path}")
    
    # Read the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Check if method already exists
    if check_method_exists(content):
        print("✅ Method get_dynamic_confidence_for_component already exists!")
        return True
    
    print("🔍 Adding missing method...")
    
    # Create backup
    backup_path = backup_original_file(file_path)
    
    # Add method
    new_content, success = add_method_to_class(content)
    
    if not success:
        print("❌ Failed to add method")
        return False
    
    # Write the fixed content
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Method added successfully!")
        
        # Verify syntax
        try:
            import py_compile
            py_compile.compile(file_path, doraise=True)
            print("✅ Syntax validation passed!")
        except py_compile.PyCompileError as e:
            print(f"❌ Syntax error after modification: {e}")
            # Restore backup
            shutil.copy2(backup_path, file_path)
            print("🔄 Restored from backup")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("🔧 BOT TRADING METHOD FIX")
    print("=" * 60)
    
    # Default file paths to check
    possible_paths = [
        "/content/drive/MyDrive/Bot/Bot-Trading_Swing.py",  # Google Colab path
        "./Bot-Trading_Swing.py",  # Current directory
        "./Bot-Trading_Swing (1).py",  # Alternative name
    ]
    
    file_path = None
    
    # Find the actual bot file
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
    
    if file_path is None:
        print("� no Bot-Trading_Swing.py file found")
        print("Please specify the correct path:")
        print("python main()  # Edit this script to set the correct path")
        return False
    
    print(f"🎯 Found bot file: {file_path}")
    
    # Fix the file
    success = fix_bot_file(file_path)
    
    if success:
        print("\n✅ BOT FIXED SUCCESSFULLY!")
        print("The missing get_dynamic_confidence_for_component method has been added.")
        print("You can now run your bot without errors.")
    else:
        print("\n❌ FIX FAILED")
        print("Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main()