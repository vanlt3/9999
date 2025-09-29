#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample Symbol Configuration
Demo config với một vài symbols chính
"""

def show_sample_config():
    """Show sample configuration"""
    
    sample_config = '''
ENTRY_TP_SL_CONFIG = {
    # === CRYPTOCURRENCIES (24/7 Trading) ===
    "BTCUSD": {
        "entry_method": "volatility_breakout",
        "atr_multiplier_sl": 3.0,
        "atr_multiplier_tp": 6.0,
        "min_rr_ratio": 1.6,
        "max_rr_ratio": 3.5,
        "support_resistance_weight": 0.25,
        "volume_confirmation": False,
        "session_filter": False,
        "volatility_adjustment": True,
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "auto",
        "trending_threshold": 0.018,
        "ranging_threshold": 0.025,
        "confidence_threshold": 0.20,
        "force_strategy": False,
        "asset_class": "cryptocurrency",
        "session": "24/7",
        "weight": 0.08,
        "risk_multiplier": 0.9
    },
    
    "ETHUSD": {
        "entry_method": "momentum_trending",
        "atr_multiplier_sl": 2.8,
        "atr_multiplier_tp": 5.5,
        "min_rr_ratio": 1.6,
        "max_rr_ratio": 3.5,
        "support_resistance_weight": 0.25,
        "volume_confirmation": False,
        "session_filter": False,
        "volatility_adjustment": True,
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "auto",
        "trending_threshold": 0.020,
        "ranging_threshold": 0.025,
        "confidence_threshold": 0.22,
        "force_strategy": False,
        "asset_class": "cryptocurrency",
        "session": "24/7",
        "weight": 0.07,
        "risk_multiplier": 0.9
    },
    
    # === COMMODITIES (Global Trading) ===
    "XAUUSD": {
        "entry_method": "fibonacci_confluence",
        "atr_multiplier_sl": 2.5,
        "atr_multiplier_tp": 4.0,
        "min_rr_ratio": 1.6,
        "max_rr_ratio": 3.5,
        "support_resistance_weight": 0.4,
        "volume_confirmation": False,
        "session_filter": False,
        "volatility_adjustment": True,
        "fibonacci_levels": [0.236, 0.382, 0.5, 0.618, 0.786],
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "auto",
        "trending_threshold": 0.020,
        "ranging_threshold": 0.025,
        "confidence_threshold": 0.19,
        "force_strategy": False,
        "asset_class": "commodity",
        "session": "23/5",
        "weight": 0.10,
        "risk_multiplier": 0.7
    },
    
    # === FOREX MAJOR PAIRS ===
    "EURUSD": {
        "entry_method": "trend_following",
        "atr_multiplier_sl": 1.8,
        "atr_multiplier_tp": 2.8,
        "min_rr_ratio": 1.4,
        "max_rr_ratio": 2.8,
        "support_resistance_weight": 0.25,
        "volume_confirmation": True,
        "session_filter": True,
        "volatility_adjustment": True,
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "auto",
        "trending_threshold": 0.018,
        "ranging_threshold": 0.028,
        "confidence_threshold": 0.18,
        "force_strategy": False,
        "asset_class": "forex",
        "session": "24/5",
        "weight": 0.08,
        "risk_multiplier": 0.6
    },
    
    # === EQUITY MAJOR INDICES (US) ===
    "SPX500": {
        "entry://method": "momentum_trending",
        "atr_multiplier_sl": 2.0,
        "atr_multiplier_tp": 3.5,
        "min_rr_ratio": 1.4,
        "max_rr_ratio": 2.8,
        "support_resistance_weight": 0.25,
        "volume_confirmation": True,
        "session_filter": True,
        "volatility_adjustment": True,
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "trending",
        "trending_threshold": 0.016,
        "ranging_threshold": 0.025,
        "confidence_threshold": 0.19,
        "force_strategy": False,
        "asset_class": "equity_index",
        "session": "23/5",
        "weight": 0.10,
        "risk_multiplier": 0.7
    }
}
'''
    
    print(sample_config)
    
    return sample_config

def show_comprehensive_example():
    """Show comprehensive example cho tất cả symbols"""
    
    comprehensive = '''
# Đây là cách Bot sẽ quyết định chọn strategy cho TẤT CẢ symbols:

# 1. CRYPTO SYMBOLS (5 symbols):
# - BTCUSD: AUTO strategy với volatility_breakout (trending threshold: 0.018)
# - ETHUSD: AUTO strategy với momentum_trending (trending threshold: 0.020)
# - XRPUSD: RANGING strategy với support_resistance (trending threshold: 0.025)
# - LTCUSD: TRENDING strategy với trend_following (trending threshold: 0.015)
# - ADAUSD: AUTO strategy với volatility_breakout (trending threshold: 0.022)

# 2. COMMODITY SYMBOLS (5 symbols):
# - XAUUSD: AUTO strategy với fibonacci_confluence (equal thresholds: 0.020/0.025)
# - XAGUSD: TRENDING strategy với momentum_trending (trending threshold: 0.016)
# - USOIL: AUTO strategy với momentum_trending (trending threshold: 0.018)
# - UKOIL: TRENDING strategy với trend_following (trending threshold: 0.015)
# - NATGAS: RANGING strategy với support_resistance (trending threshold: 0.028)

# 3. FOREX MAJORS (7 symbols):
# - EURUSD: AUTO strategy với trend_following (trending threshold: 0.018)
# - GBPUSD: RANGING strategy với support_resistance (trending threshold: 0.025)
# - USDJPY: AUTO strategy với trend_following (trending threshold: 0.020)
# - AUDUSD: AUTO strategy với trend_following (trending threshold: 0.020)
# - USDCAD: TRENDING strategy với momentum_trending (trending threshold: 0.016)
# - NZDUSD: RANGING strategy với support_resistance (trending threshold: 0.025)
# - USDCHF: RANGING strategy với support_resistance (trending threshold: 0.025)

# 4. FOREX CROSS PAIRS (8 symbols):
# - EURGBP: RANGING strategy với range_bound (trending threshold: 0.028)
# - EURJPY: TRENDING strategy với trend_following (trending threshold: 0.015)
# - GBPJPY: TRENDING strategy với momentum_trending (trending threshold: 0.012)
# - AUDJPY: AUTO strategy với trend_following (trending threshold: 0.020)
# - CADJPY: TRENDING strategy với momentum_trending (trending threshold: 0.016)
# - CHFJPY: RANGING strategy với support_resistance (trending threshold: 0.025)
# - EURCHF: RANGING strategy với range_bound (trending threshold: 0.030)
# - GBPCHF: TRENDING strategy với momentum_trending (trending threshold: 0.015)

# 5. FOREX EXOTIC (1 symbol):
# - AUDNZD: AUTO strategy với carry_trade (trending threshold: 0.020)

# 6. EQUITY MAJORS (3 symbols):
# - SPX500: TRENDING strategy với momentum_trending (trending threshold: 0.016)
# - NAS100: TRENDING strategy với momentum_trending (trending threshold: 0.017)
# - US30: AUTO strategy với trend_following (trending threshold: 0.018)

# 7. EQUITY EUROPEAN (3 symbols):
# - DE40: TRENDING strategy với momentum_trending (trending threshold: 0.016)
# - UK100: RANGING strategy với support_resistance (trending threshold: 0.025)
# - FR40: AUTO strategy với trend_following (trending threshold: 0.020)

# 8. EQUITY ASIAN (2 symbols):
# - JP225: TRENDING strategy với momentum_trending (trending threshold: 0.015)
# - AU200: AUTO strategy với trend_following (trending threshold: 0.020)

# 📊 SUMMARY:
# - Total Symbols: 34
# - Auto Selection: 12 symbols (35.3%)
# - Trending Strategy: 12 symbols (35.3%)  
# - Ranging Strategy: 10 symbols (29.4%)

# 🎯 DECISION LOGIC:
# 1. Bot sẽ check trending_threshold để quyết định trending
# 2. Bot sẽ check ranging_threshold để quyết định ranging  
# 3. Bot sẽ sử dụng entry_method phù hợp với strategy được chọn
# 4. Bot sẽ adjust confidence_threshold theo từng symbol
# 5. Bot sẽ force_strategy nếu được set True
'''
    
    print(comprehensive)

if __name__ == "__main__":
    print("🚀 Sample Symbol Configuration")
    print("=" * 50)
    
    print("📋 SAMPLE CONFIG (Copy to Bot):")
    print("-" * 30)
    sample_config = show_sample_config()
    
    print("\n📊 COMPREHENSIVE STRATEGY OVERVIEW:")
    print("-" * 40)
    comprehensive_overview = show_comprehensive_example()
    
    print("\n✅ HOW TO APPLY:")
    print("1. Copy sample config above")
    print("2. Replace ENTRY_TP_SL_CONFIG section in Bot-Trading_Swing (1).py")
    print("3. Add strategy selection parameters cho từng symbol")
    print("4. Restart bot để apply changes")
    print("5. Monitor logs để see strategy selection decisions")
    
    # Save sample to file
    with open("sample_config_for_bot.txt", "w") as f:
        f.write(sample_config)
    
    print(f"\n📁 Sample config saved to: sample_config_for_bot.txt")