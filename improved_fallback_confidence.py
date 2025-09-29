#!/usr/bin/env python3
"""
IMPROVED FALLBACK CONFIDENCE LOGIC
Fixes Master Agent and Online Learning fallback confidence to be dynamic and context-aware.
"""

import re
import sys
import os

def patch_improved_fallback_confidence():
    """Implement improved fallback confidence logic"""
    
    bot_file = "Bot-Trading_Swing (1).py"
    
    if not os.path.exists(bot_file):
        print(f"Error: {bot_file} not found!")
        return False
    
    # Read the file
    with open(bot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # First, add the helper function for dynamic confidence calculation 
    helper_function = '''
def _calculate_fallback_confidence(self, symbol, market_data, component_type="master_agent"):
    """
    Calculate dynamic fallback confidence based on symbol type and market volatility.
    
    Args:
        symbol: Trading symbol
        market_data: Market data (can be None or empty for fallback)
        component_type: Type of component calling this function
        
    Returns:
        float: Dynamic confidence value between 0.15 and 0.40
    """
    try:
        # Base confidence levels by component type
        base_confidences = {
            "master_agent": 0.30,
            "online_learning": 0.35, 
            "rl_strategy": 0.25
        }
        
        base_confidence = base_confidences.get(component_type, 0.30)
        
        # Symbol type adjustments
        symbol_adjustments = {
            'BTCUSD': 1.15,    # Crypto major - slightly higher confidence
            'ETHUSD': 1.10,    # Crypto major - slightly higher confidence  
            'XAUUSD': 1.05,    # Gold - stable commodity
            'EURUSD': 1.00,    # Major forex - baseline
            'GBPUSD': 0.98,    # Volatile forex
            'USDJPY': 1.00,    # Major forex - baseline
            'SPX500': 0.95,    # Volatile equity index
            'NAS100': 0.92,    # Tech-heavy volatile index
            'US30': 0.96,      # Traditional index
            'DE40': 0.94       # European index
        }
        
        symbol_multiplier = symbol_adjustments.get(symbol, 1.00)
        
        # Volatility adjustment based on market data
        volatility_adjustment = 1.0
        
        if market_data is not None and not market_data.empty and len(market_data) > 0:
            try:
                # Try to get volatility indicators from last available data
                last_row = market_data.iloc[-1]
                
                # Check for ATR normalized if available
                if 'atr_normalized' in market_data.columns:
                    atr_value = last_row.get('atr_normalized', 0.01)
                    if atr_value > 0.015:  # High volatility
                        volatility_adjustment *= 0.70  # Reduce confidence significantly
                        logging.debug(f"[Fallback] {symbol}: High volatility detected (ATR: {atr_value:.4f}), reducing confidence by 30%")
                    elif atr_value < 0.005:  # Low volatility
                        volatility_adjustment *= 1.10  # Increase confidence slightly  
                        logging.debug(f"[Fallback] {symbol}: Low volatility detected (ATR: {atr_value:.4f}), increasing confidence by 10%")
                        
            except Exception as e:
                logging.debug(f"[Fallback] {symbol}: Error analyzing volatility for fallback confidence: {e}")
                # Continue with default confidence if volatility analysis fails
        
        # Calculate final confidence
        final_confidence = base_confidence * symbol_multiplier * volatility_adjustment
        
        # Ensure confidence stays within reasonable bounds (15% to 40%)
        final_confidence = max(0.15, min(0.40, final_confidence))
        
        logging.debug(f"[Fallback Confidence] {symbol} ({component_type}): base={base_confidence:.2%}, symbol_mult={symbol_multiplier:.2f}, volatility_mult={volatility_adjustment:.2f}, final={final_confidence:.2%}")
        
        return final_confidence
        
    except Exception as e:
        logging.error(f"[Fallback Confidence] Error calculating confidence for {symbol}: {e}")
        # Safe fallback to reasonable default
        return 0.20


'''
    
    # Add the helper function before the MasterAgent class
    content = re.sub(
        r'(# === MASTER AGENT FOR TP/SL DECISIONS ===)',
        helper_function + r'\1',
        content
    )
    
    # Fix 1: Replace Master Agent's fixed confidence with dynamic calculation
    master_fallback_pattern = r'(dynamic_confidence = 0\.25 if symbol in.*?return "HOLD", dynamic_confidence)'
    
    master_replacement = '''# Use dynamic confidence calculation instead of fixed value
                dynamic_confidence = self._calculate_fallback_confidence(symbol, market_data, "master_agent")
                logging.info(f"[Master Agent] {symbol}: Fallback confidence calculated as {dynamic_confidence:.2%}")
                return "HOLD", dynamic_confidence'''
    
    content = re.sub(master_fallback_pattern, master_replacement, content)
    
    # Fix 2: Replace Online Learning's multiple fixed confidence values
    online_patterns = [
        (r'(dynamic_confidence = 0\.38.*?# Higher for major crypto)', 'dynamic_confidence = self._calculate_fallback_confidence(symbol, market_data, "online_learning")'),
        (r'(dynamic_confidence = 0\.36.*?# Moderate for gold)', 'dynamic_confidence = self._calculate_fallback_confidence(symbol, market_data, "online_learning")'),
        (r'(dynamic_confidence = 0\.32.*?# Lower for volatile indices)', 'dynamic_confidence = self._calculate_fallback_confidence(symbol, market_data, "online_learning")'),
        (r'(dynamic_confidence = 0\.35.*?# Standard for major forex)', 'dynamic_confidence = self._calculate_fallback_confidence(symbol, market_data, "online_learning")'),
        (r'(dynamic_confidence = 0\.33.*?# Other symbols)', 'dynamic_confidence = self._calculate_fallback_confidence(symbol, market_data, "online_learning")')
    ]
    
    for pattern, replacement in online_patterns:
        content = re.sub(pattern, replacement, content)
        # Add logging for each replacement
        logging_addition = '\n                logging.info(f"[Online Learning] {symbol}: Fallback satisfaction calculated as {dynamic_confidence:.2%}")'
        content = re.sub(replacement, replacement + logging_addition, content)
    
    # Fix 3: Update RL Strategy confidence attribution  
    rl_pattern = r'(# Dynamic confidence based on symbol type and market conditions\s*if symbol in.*?confidence = dynamic_confidence)'
    
    def enhance_rl_confidence(match):
        return '''# Use dynamic confidence calculation for RL fallback
                    confidence = self._calculate_fallback_confidence(symbol_to_act, None, "rl_strategy")
                    logging.info(f"[RL Strategy] {symbol_to_act}: Fallback confidence calculated as {confidence:.2%}")'''
    
    content = re.sub(rl_pattern, enhance_rl_confidence, content, flags=re.DOTALL)
    
    # Fix 4: Enhance RL logging to show confidence source
    rl_logging_pattern = r'(logger\.info\(f"   - RL Action: \{action_name\} \(confidence: \{adjusted_confidence:.2%\}"\))'
    
    rl_logging_replacement = '''logger.info(f"   - RL Action: {action_name} (confidence: {adjusted_confidence:.2%} - {confidence_source})")'''
    
    content = re.sub(rl_logging_pattern, rl_logging_replacement, content)
    
    # Fix 5: Add confidence source tracking before RL logging
    rl_source_pattern = r'(adjusted_confidence = confidence)'
    
    rl_source_replacement = '''adjusted_confidence = confidence
                        
                        # Track confidence source for debugging
                        symbol_data = live_data_cache.get(symbol_to_act, pd.DataFrame())
                        if symbol_data.empty or len(symbol_data) < 10:
                            confidence_source = "Fallback due to insufficient data"
                        else:
                            confidence_source = "Normal calculation"'''
    
    content = re.sub(rl_source_pattern, rl_source_replacement, content)
    
    # Write the patched content
    backup_file = f"{bot_file}.improved_fallback_backup"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(open(bot_file, 'r', encoding='utf-8').read())
    
    with open(bot_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ IMPROVED FALLBACK CONFIDENCE APPLIED:")
    print(f"📁 Backup created: {backup_file}")
    print(f"🧮 Added dynamic fallback confidence calculation")
    print(f"🎯 Master Agent: Now uses volatility-aware confidence (15%-40%)")
    print(f"🔄 Online Learning: Unified dynamic confidence logic")
    print(f"🤖 RL Strategy: Proper confidence attribution with source tracking")
    print(f"📊 Confidence factors: Symbol type + volatility + component type")
    
    return True

if __name__ == "__main__":
    patch_improved_fallback_confidence()