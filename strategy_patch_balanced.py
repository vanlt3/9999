#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STRATEGY CONFIG PATCH FILE
Config Name: BALANCED
Generated: 2025-09-29 06:41:17

CRITICAL INSTRUCTIONS TO APPLY THIS PATCH:

1. BACKUP your current Bot-Trading_Swing (1).py file !!!
2. Copy the entries below into the appropriate sections
3. Replace existing ENTRY_TP_SL_CONFIG section with NEW_ENTRY_TP_SL_CONFIG
4. Add STRATEGY_GLOBAL_CONFIG section if not exists
5. Test the bot with small positions first

WARNING: This patch modifies core bot functionality!
"""

print("🚨 STRATEGY CONFIG PATCH - BALANCED MODE")
print("=" * 60)
print("Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Mode:", config_name.upper())
print("⚠️  BACKUP YOUR BOT BEFORE APPLYING!")
print()

# === NEW ENTRY TB_CONFIG SECTION ===
NEW_ENTRY_TP_SL_CONFIG = {
    
# Enhanced Entry/TP/SL Configuration for all symbols - UPDATED VERSION
ENTRY_TP_SL_CONFIG = {
    # === COMMODITIES (Global Trading) ===
    "XAUUSD": {
        "entry_method": "fibonacci_confluence",
        "atr_multiplier_sl": 2.3,
        "atr_multiplier_tp": 4.2,
        "min_rr_ratio": 1.4,
        "max_rr_ratio": 1.7,
        "support_resistance_weight": 0.25,
        "volume_confirmation": True,
        "session_filter": True,
        "volatility_adjustment": True,
        # Strategy Configuration - Added
        "preferred_strategy": "auto",
        "trending_threshold": 0.022,
        "ranging_threshold": 0.022,
        "confidence_threshold": 0.2,
        "force_strategy": False,
        "explanation": "Gold - Balanced với fibonacci và equal thresholds"
    },
    "BTCUSD": {
        "entry_method": "volatility_breakout",
        "atr_multiplier_sl": 2.8,
        "atr_multiplier_tp": 5.2,
        "min_rr_ratio": 1.4,
        "max_rr_ratio": 1.4,
        "support_resistance_weight": 0.25,
        "volume_confirmation": True,
        "session_filter": True,
        "volatility_adjustment": True,
        # Strategy Configuration - Added
        "preferred_strategy": "auto",
        "trending_threshold": 0.018,
        "ranging_threshold": 0.025,
        "confidence_threshold": 0.19,
        "force_strategy": False,
        "explanation": "Bitcoin - Balanced auto selection with moderate thresholds"
    },
    "ETHUSD": {
        "entry_method": "momentum_trending",
        "atr_multiplier_sl": 2.6,
        "atr_multiplier_tp": 4.8,
        "min_rr_ratio": 1.4,
        "max_rr_ratio": 1.5,
        "support_resistance_weight": 0.25,
        "volume_confirmation": True,
        "session_filter": True,
        "volatility_adjustment": True,
        # Strategy Configuration - Added
        "preferred_strategy": "auto",
        "trending_threshold": 0.02,
        "ranging_threshold": 0.025,
        "confidence_threshold": 0.2,
        "force_strategy": False,
        "explanation": "Ethereum - Balanced trending với moderate settings"
    },
}

# === NEW GLOBAL STRATEGY CONFIG SECTION ===
NEW_STRATEGY_GLOBAL_CONFIG = {
    
# STRATEGY SELECTION_GLOBAL_CONFIG - DYNAMIC UPDATES
STRATEGY_GLOBAL_CONFIG = {
    "GLOBAL_TREND_PREFERENCE": "auto",
    "MIN_TREND_CONFIDENCE": 0.18,
    "MAX_VOLATILITY_TREND": 2.5,
    "PERFORMANCE_BASED_SELECTION": True,
    "BTCUSD": {'preferred_strategy': 'auto', 'entry_method': 'volatility_breakout', 'trending_threshold': 0.018, 'ranging_threshold': 0.025, 'atr_multiplier_sl': 2.8, 'atr_multiplier_tp': 5.2, 'confidence_threshold': 0.19, 'force_strategy': False, 'explanation': 'Bitcoin - Balanced auto selection with moderate thresholds'},
    "ETHUSD": {'preferred_strategy': 'auto', 'entry_method': 'momentum_trending', 'trending_threshold': 0.02, 'ranging_threshold': 0.025, 'atr_multiplier_sl': 2.6, 'atr_multiplier_tp': 4.8, 'confidence_threshold': 0.2, 'force_strategy': False, 'explanation': 'Ethereum - Balanced trending với moderate settings'},
    "XAUUSD": {'preferred_strategy': 'auto', 'entry_method': 'fibonacci_confluence', 'trending_threshold': 0.022, 'ranging_threshold': 0.022, 'atr_multiplier_sl': 2.3, 'atr_multiplier_tp': 4.2, 'confidence_threshold': 0.2, 'force_strategy': False, 'explanation': 'Gold - Balanced với fibonacci và equal thresholds'},
}

print("📋 INSTRUCTIONS TO APPLY:")
print("1. Find ENTRY_TP_SL_CONFIG in your Bot-Trading_Swing (1).py")
print("2. Replace entire section with NEW_ENTRY_TP_SL_CONFIG above")
print("3. Add STRATEGY_GLOBAL_CONFIG section with NEW_STRATEGY_GLOBAL_CONFIG")
print("4. Restart the bot")  
print("5. Monitor performance và adjust if needed")
print()
print("🎯 Expected Behavior with BALANCED config:")
print("- Bot sẽ auto-select based on market conditions với equal thresholds")