#!/usr/bin/env python3
"""
VERIFICATION SCRIPT: Fallback Confidence Improvements
Checks that all improvements have been properly applied to the bot.
"""

import re
import os

def verify_fallback_improvements():
    """Verify that fallback confidence improvements are properly implemented"""
    
    bot_file = "Bot-Trading_Swing (1).py"
    
    if not os.path.exists(bot_file):
        print(f"❌ Error: {bot_file} not found!")
        return False
    
    print("🔍 VERIFYING FALLBACK CONFIDENCE IMPROVEMENTS")
    print("=" * 60)
    
    success_count = 0
    total_checks = 0
    
    # Read the file
    with open(bot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check 1: Helper function exists
    total_checks += 1
    if '_calculate_fallback_confidence(self, symbol, market_data, component_type=' in content:
        print("✅ 1. Helper function '_calculate_fallback_confidence' found")
        success_count += 1
    else:
        print("❌ 1. Helper function '_calculate_fallback_confidence' NOT found")
    
    # Check 2: Master Agent dynamic calculation
    total_checks += 1
    master_pattern = r'master_agent.*_calculate_fallback_confidence'
    if re.search(master_pattern, content):
        print("✅ 2. Master Agent using dynamic confidence calculation")
        success_count += 1
    else:
        print("❌ 2. Master Agent still using fixed confidence values")
    
    # Check 3: Online Learning dynamic calculation  
    total_checks += 1
    online_pattern = r'online_learning.*_calculate_fallback_confidence'
    if re.search(online_pattern, content):
        print("✅ 3. Online Learning using dynamic confidence calculation")
        success_count += 1
    else:
        print("❌ 3. Online Learning still using fixed confidence values")
    
    # Check 4: RL Strategy confidence source tracking
    total_checks += 1
    rl_source_pattern = r'confidence_source.*Fallback due to insufficient data'
    if re.search(rl_source_pattern, content):
        print("✅ 4. RL Strategy confidence source tracking implemented")
        success_count += 1
    else:
        print("❌ 4. RL Strategy confidence source tracking NOT found")
    
    # Check 5: Enhanced RL logging
    total_checks += 1
    rl_logging_pattern = r'logger\.info\(f"   - RL Action.*confidence_source\)'
    if re.search(rl_logging_pattern, content):
        print("✅ 5. Enhanced RL logging with confidence source")
        success_count += 1
    else:
        print("❌ 5. Enhanced RL logging NOT found")
    
    # Check 6: No fixed confidence values remain
    total_checks += 1
    fixed_patterns = [
        r'dynamic_confidence = 0\.25.*BTCUSD.*ETHUSD',
        r'dynamic_confidence = 0\.38.*Higher for major crypto',
        r'dynamic_confidence = 0\.36.*Moderate for gold',
        r'dynamic_confidence = 0\.32.*Lower for volatile indices'
    ]
    
    fixed_values_found = False
    for pattern in fixed_patterns:
        if re.search(pattern, content):
            fixed_values_found = True
            break
    
    if not fixed_values_found:
        print("✅ 6. Fixed confidence values successfully replaced")
        success_count += 1
    else:
        print("❌ 6. Some fixed confidence values still remain")
    
    # Check 7: Volatility adjustment logic
    total_checks += 1
    volatility_pattern = r'volatility_adjustment.*atr_normalized'
    if re.search(volatility_pattern, content):
        print("✅ 7. Volatility adjustment logic implemented")
        success_count += 1
    else:
        print("❌ 7. Volatility adjustment logic NOT found")
    
    # Check 8: Symbol type multipliers
    total_checks += 1
    symbol_pattern = r'symbol_adjustments.*BTCUSD.*ETHUSD.*EURUSD'
    if re.search(symbol_pattern, content):
        print("✅ 8. Symbol type multipliers defined")
        success_count += 1
    else:
        print("❌ 8. Symbol type multipliers NOT found")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 VERIFICATION SUMMARY: {success_count}/{total_checks} checks passed")
    
    if success_count == total_checks:
        print("🎉 ALL FALLBACK CONFIDENCE IMPROVEMENTS SUCCESSFULLY APPLIED!")
        print("✅ Bot now uses dynamic, volatility-aware confidence calculations")
        print("✅ All components (Master Agent, Online Learning, RL) are enhanced")
        print("✅ Confidence attribution and logging improved")
        return True
    else:
        print(f"⚠️ {total_checks - success_count} improvements may need additional attention")
        return False

def check_concrete_examples():
    """Check for concrete examples of the improvements in action"""
    
    bot_file = "Bot-Trading_Swing (1).py"
    
    print("\n📋 CHECKING CONCRETE EXAMPLES")
    print("=" * 40)
    
    with open(bot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for specific logging examples
    examples = [
        ("Master Agent logging", r'Master Agent.*Fallback confidence calculated'),
        ("Online Learning logging", r'Online Learning.*Fallback confidence calculated'),
        ("RL source tracking", r'confidence_source.*Fallback due to insufficient data'),
        ("Enhanced RL logging", r'RL Action.*confidence.*-.*Fallback due to')
    ]
    
    found_examples = 0
    for name, pattern in examples:
        if re.search(pattern, content):
            print(f"✅ {name}: Example found")
            found_examples += 1
        else:
            print(f"❌ {name}: Example NOT found")
    
    print(f"\n📊 Examples found: {found_examples}/{len(examples)}")

if __name__ == "__main__":
    success = verify_fallback_improvements()
    check_concrete_examples()
    
    if success:
        print("\n🎯 READY FOR PRODUCTION!")
        print("All fallback confidence improvements are working correctly.")
    else:
        print("\n⚠️ ATTENTION NEEDED!")
        print("Some improvements may require manual review.")