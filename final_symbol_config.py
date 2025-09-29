#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Symbol Configuration - Simple và Clean
Cấu hình hoàn chỉnh cho tất cả symbols

Usage: Copy content của file này vào ENTRY_TP_SL_CONFIG section trong bot
"""

from comprehensive_symbol_config import ComprehensiveSymbolConfig

def generate_config():
    """Generate complete symbol configuration"""
    
    config_loader = ComprehensiveSymbolConfig()
    config = config_loader.get_comprehensive_symbol_config()
    
    print("# Enhanced Entry/TP/SL Configuration for ALL SYMBOLS === Copy vào Bot ===")
    print("ENTRY_TP_SL_CONFIG = {")
    
    # Process symbols by category
    categories = {
        "CRYPTO": ["BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "ADAUSD"],
        "COMMODITIES": ["XAUUSD", "XAGUSD", "USOIL", "UKOIL", "NATGAS"],
        "FOREX_MAJORS": ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "NZDUSD", "USDCHF"],
        "FOREX_CROSS": ["EURGBP", "EURJPY", "GBPJPY", "AUDJPY", "CADJPY", "CHFJPY", "EURCHF", "GBPCHF"],
        "FOREX_EXOTIC": ["AUDNZD"],
        "EQUITY_US": ["SPX500", "NAS100", "US30"],
        "EQUITY_EURO": ["DE40", "UK100", "FR40"],
        "EQUITY_ASIA": ["JP225", "AU200"]
    }
    
    category_titles = {
        "CRYPTO": "    # === CRYPTOCURRENCIES (24/7 Trading) ===",
        "COMMODITIES": "    # === COMMODITIES (Global Trading) ===",
        "FOREX_MAJORS": "    # === FOREX MAJOR PAIRS ===",
        "FOREX_CROSS": "    # === FOREX CROSS PAIRS ===",
        "FOREX_EXOTIC": "    # === FOREX EXOTIC PAIRS ===",
        "EQUITY_US": "    # === EQUITY MAJOR INDICES (US) ===",
        "EQUITY_EURO": "    # === EQUITY EUROPEAN INDICES ===",
        "EQUITY_ASIA": "    # === EQUITY ASIAN INDICES ==="
    }
    
    for i, (category, symbols) in enumerate(categories.items()):
        if i > 0:
            print()
        if category in category_titles:
            print(category_titles[category])
        
        for symbol in symbols:
            if symbol in config:
                conf = config[symbol]
                print(f'    "{symbol}": {{')
                print(f'        "entry_method": "{conf["entry_method"]}",')
                print(f'        "atr_multiplier_sl": {conf["atr_multiplier_sl"]},')
                print(f'        "atr_multiplier_tp": {conf["atr_multiplier_tp"]},')
                print(f'        "min_rr_ratio": {conf["min_rr_ratio"]},')
                print(f'        "max_rr_ratio": {(conf["atr_multiplier_tp"] / conf["atr_multiplier_sl"]):.1f},')
                print(f'        "support_resistance_weight": {conf["support_resistance_weight"]},')
                print(f'        "volume_confirmation": {conf["volume_confirmation"]},')
                print(f'        "session_filter": {conf["session_filter"]},')
                print(f'        "volatility_adjustment": {conf["volatility_adjustment"]},')
                print(f'        "preferred_strategy": "{conf["preferred_strategy"]}",')
                print(f'        "trending_threshold": {conf["trending_threshold"]},')
                print(f'        "ranging_threshold": {conf["ranging_threshold"]},') 
                print(f'        "confidence_threshold": {conf["confidence_threshold"]},')
                print(f'        "force_strategy": {conf["force_strategy"]},')
                print(f'        "asset_class": "{conf["asset_class"]}",')
                print(f'        "session": "{conf["session"]}",')
                print(f'        "weight": {conf["weight"]},')
                print(f'        "risk_multiplier": {conf["risk_multiplier"]}')
                print('    },')
    
    print("}")

if __name__ == "__main__":
    generate_config()