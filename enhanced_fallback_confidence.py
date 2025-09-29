#!/usr/bin/env python3
"""
ENHANCED FALLBACK CONFIDENCE LOGIC
Creates improved fallback confidence calculation with market volatility awareness
and unified logic for Master Agent and Online Learning systems.
"""

import re
import sys
import os
import numpy as np

def patch_fallback_confidence_logic():
    """Implement enhanced fallback confidence logic with market volatility awareness"""
    
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
    Calculate dynamic fallback confidence based on market volatility and symbol type.
    
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
        
        if market_data is not None and not market_data.empty and hasattr(market_data, '__len__') and len(market_data) > 0:
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
                
                # Check for recent price volatility
                if len(market_data) >= 5 and 'close' in market_data.columns:
                    recent_prices = market_data['close'].tail(5)
                    price_volatility = recent_prices.std() / recent_prices.mean()
                    
                    if price_volatility > 0.02:  # High price volatility (> 2%)
                        volatility_adjustment *= 0.80
                        logging.debug(f"[Fallback] {symbol}: High price volatility detected ({price_volatility:.4f}), reducing confidence by 20%")
                    elif price_volatility < 0.005:  # Low price volatility (< 0.5%)
                        volatility_adjustment *= 1.05
                        logging.debug(f"[Fallback] {symbol}: Low price volatility detected ({price_volatility:.4f}), increasing confidence by 5%")
                        
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
    master_agent_pattern = r'(if market_data is None or .*?dynamic_confidence = 0\.25 if symbol in.*?return "HOLD", dynamic_confidence)'
    
    def enhance_master_agent_fallback(match):
        return '''if market_data is None or (hasattr(market_data, 'empty') and market_data.empty) or len(market_data) < 10:
                logging.warning(f"[Master Agent Coordinator] Insufficient data for {symbol}: {len(market_data) if market_data is not None else 0} rows")
                # Use dynamic confidence calculation instead of fixed value
                dynamic_confidence = self._calculate_fallback_confidence(symbol, market_data, "master_agent")
                logging.info(f"[Master Agent] {symbol}: Fallback confidence calculated as {dynamic_confidence:.2%}")
                return "HOLD", dynamic_confidence'''
    
    content = re.sub(master_agent_pattern, enhance_master_agent_fallback, content, flags=re.DOTALL)
    
    # Fix 2: Replace Online Learning's fixed confidence with dynamic calculation
    online_pattern1 = r'(logging\.warning\(f"\[Online Learning\] Empty market data for.*?dynamic_confidence = 0\.33.*?return "HOLD", dynamic_confidence)'
    online_pattern2 = r'(logging\.warning\(f"\[Online Learning\] All-zero features for.*?dynamic_confidence = 0\.33.*?return "HOLD", dynamic_confidence)'
    
    def enhance_online_fallback(match):
        return '''logging.warning(f"[Online Learning] Empty market data for {symbol}, returning HOLD with dynamic confidence")
                # Use dynamic confidence calculation instead of fixed values
                dynamic_confidence = self._calculate_fallback_confidence(symbol, market_data, "online_learning")
                logging.info(f"[Online Learning] {symbol}: Fallback confidence calculated as {dynamic_confidence:.2%}")
                return "HOLD", dynamic_confidence'''
    
    def enhance_online_fallback_zero(match):
        return '''logging.warning(f"[Online Learning] All-zero features for {symbol}, returning HOLD with dynamic confidence")
                # Use dynamic confidence calculation instead of fixed values  
                dynamic_confidence = self._calculate_fallback_confidence(symbol, market_data, "online_learning")
                logging.info(f"[Online Learning] {symbol}: Fallback confidence calculated as {dynamic_confidence:.2%}")
                return "HOLD", dynamic_confidence'''
    
    content = re.sub(online_pattern1, enhance_online_fallback, content, flags=re.DOTALL)
    content = re.sub(online_pattern2, enhance_online_fallback_zero, content, flags=re.DOTALL)
    
    # Fix 3: Replace RL Strategy confidence attribution with dynamic calculation
    rl_confidence_pattern = r'(# Dynamic confidence based on symbol type and market conditions.*?confidence = dynamic_confidence)'
    
    def enhance_rl_fallback(match):
        return '''# Use dynamic confidence calculation for RL fallback
                    try:
                        symbol_data = live_data_cache.get(symbol_to_act, pd.DataFrame())
                        confidence = self._calculate_fallback_confidence(symbol_to_act, symbol_data, "rl_strategy")
                        logging.info(f"[RL Strategy] {symbol_to_act}: Fallback confidence calculated as {confidence:.2%}")
                    except Exception as conf_error:
                        logging.error(f"[RL Strategy] Error calculating fallback confidence for {symbol_to_act}: {conf_error}")
                        confidence = 0.25  # Safe fallback'''
    
    content = re.sub(rl_confidence_pattern, enhance_rl_fallback, content, flags=re.DOTALL)
    
    # Fix 4: Update RL logging to distinguish between real and fallback confidence
    rl_logging_pattern = r'(logger\.info\(f"   - RL Action: \{action_name\} \(confidence: \{adjusted_confidence:.2%\}"\))'
    
    def enhance_rl_logging(match):
        return '''logger.info(f"   - RL Action: {action_name} (confidence: {adjusted_confidence:.2%} - {confidence_source})")'''
    
    content = re.sub(rl_logging_pattern, enhance_rl_logging, content)
    
    # Update RL action processing to track confidence source
    rl_processing_pattern = r'(adjusted_confidence = confidence)'
    
    def update_rl_processing(match):
        return '''adjusted_confidence = confidence
                        try:
                            # Check if confidence came from fallback calculation
                            symbol_data = live_data_cache.get(symbol_to_act, pd.DataFrame())
                            if symbol_data.empty or len(symbol_data) < 10:
                                confidence_source = "Fallback due to insufficient data"
                            else:
                                confidence_source = "Normal calculation"
                        except:
                            confidence_source = "Fallback due to error"'''
    
    content = re.sub(rl_processing_pattern, update_rl_processing, content)
    
    # Write the patched content
    backup_file = f"{bot_file}.fallback_backup"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(open(bot_file, 'r', encoding='utf-8').read())
    
    with open(bot_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ ENHANCED FALLBACK CONFIDENCE APPLIED:")
    print(f"📁 Backup created: {backup_file}")
    print(f"🧮 Added dynamic confidence calculation with volatility awareness")
    print(f"🎯 Master Agent: Now calculates fallback based on market conditions")
    print(f"🔄 Online Learning: Uses same dynamic logic for consistency")
    print(f"🤖 RL Strategy: Proper confidence attribution with source tracking")
    print(f"📊 Confidence range: 15% - 40% based on volatility and symbol type")
    
    return True

if __name__ == "__main__":
    patch_fallback_confidence_logic()