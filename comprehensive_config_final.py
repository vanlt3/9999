#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Comprehensive Configuration for All Symbols
Ready-to-apply configuration cho tất cả symbols trong Bot

Tác giả: AI Assistant  
Ngày tạo: 2024
Mục đích: Provide đơn giản và hoàn chỉnh configuration cho ALL symbols
"""

import json
from comprehensive_symbol_config import ComprehensiveSymbolConfig

def generate_entry_config_text():
    """Generate ENTRY_TP_SL_CONFIG as text"""
    
    config_loader = ComprehensiveSymbolConfig()
    config = config_loader.get_comprehensive_symbol_config()
    
    config_text = """# Enhanced Entry/TP/SL Configuration for ALL SYMBOLS - COMPREHENSIVE VERSION
ENTRY_TP_SL_CONFIG = {
    # === CRYPTOCURRENCIES (24/7 Trading) ===
"""
    
    # Crypto symbols
    crypto_symbols = ["BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "ADAUSD"]
    for symbol in crypto_symbols:
        if symbol in config:
            conf = config[symbol]
            config_text += f'''    "{symbol}": {{
        # Crypto - {conf.get('explanation', 'Strategy configuration')}
        "entry_method": "{conf.get('entry_method', 'auto_select')}",
        "atr_multiplier_sl": {conf.get('atr_multiplier_sl', 2.0)},
        "atr_multiplier_tp": {conf.get('atr_multiplier_tp', 4.0)},
        "min_rr_ratio": {conf.get('min_rr_ratio', 1.4)},
        "max_rr_ratio": {(conf.get('atr_multiplier_tp', 4.0) / conf.get('atr_multiplier_sl', 2.0)):.1f},
        "support_resistance_weight": {conf.get('support_resistance_weight', 0.25)},
        "volume_confirmation": {conf.get('volume_confirmation', True)},
        "session_filter": {conf.get('session_filter', True)},
        "volatility_adjustment": {conf.get('volatility_adjustment', True)},
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "{conf.get('preferred_strategy', 'auto')}",
        "trending_threshold": {conf.get('trending_threshold', 0.020)},
        "ranging_threshold": {conf.get('ranging_threshold', 0.025)},
        "confidence_threshold": {conf.get('confidence_threshold', 0.20)},
        "force_strategy": {conf.get('force_strategy', False)},
        "asset_class": "{conf.get('asset_class', 'unknown')}",
        "session": "{conf.get('session', '24/5')}",
        "weight": {conf.get('weight', 0.05)},
        "risk_multiplier": {conf.get('risk_multiplier', 0.7)}
    }},
'''
    
    config_text += '''
    # === COMMODITIES (Global Trading) ===
'''
    
    # Commodity symbols  
    commodity_symbols = ["XAUUSD", "XAGUSD", "USOIL", "UKOIL", "NATGAS"]
    for symbol in commodity_symbols:
        if symbol in config:
            conf = config[symbol]
            fibonacci_levels = conf.get('fibonacci_levels', [0.236, 0.382, 0.5, 0.618, 0.786])
            config_text += f'''    "{symbol}": {{
        # Commodity - {conf.get('explanation', 'Strategy configuration')}
        "entry_method": "{conf.get('entry_method', 'auto_select')}",
        "atr_multiplier_sl": {conf.get('atr_multiplier_sl', 2.0)},
        "atr_multiplier_tp": {conf.get('atr_multiplier_tp', 4.0)},
        "min_rr_ratio": {conf.get('min_rr_ratio', 1.4)},
        "max_rr_ratio": {(conf.get('atr_multiplier_tp', 4.0) / conf.get('atr_multiplier_sl', 2.0)):.1f},
        "support_resistance_weight": {conf.get('support_resistance_weight', 0.25)},
        "volume_confirmation": {conf.get('volume_confirmation', True)},
        "session_filter": {conf.get('session_filter', True)},
        "volatility_adjustment": {conf.get('volatility_adjustment', True)},
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "{conf.get('preferred_strategy', 'auto')}",
        "trending_threshold": {conf.get('trending_threshold', 0.020)},
        "ranging_threshold": {conf.get('ranging_threshold', 0.025)},
        "confidence_threshold": {conf.get('confidence_threshold', 0.20)},
        "force_strategy": {conf.get('force_strategy', False)},
        "asset_class": "{conf.get('asset_class', 'unknown')}",
        "session": "{conf.get('session', '24/5')}",
        "weight": {conf.get('weight', 0.05)},
        "risk_multiplier": {conf.get('risk_multiplier', 0.7)}'''
        
        # Add special parameters
        if symbol == "XAUUSD":
            config_text += f',
        "fibonacci_levels": {fibonacci_levels}'
        
        config_text += '''
    },
'''
    
    config_text += '''
    # === FOREX MAJOR PAIRS ===
'''
    
    # Forex major symbols
    forex_major_symbols = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "NZDUSD", "USDCHF"]
    for symbol in forex_major_symbols:
        if symbol in config:
            conf = config[symbol]
            config_text += f'''    "{symbol}": {{
        # Forex Major - {conf.get('explanation', 'Strategy configuration')}
        "entry_method": "{conf.get('entry_method', 'auto_select')}",
        "atr_multiplier_sl": {conf.get('atr_multiplier_sl', 2.0)},
        "atr_multiplier_tp": {conf.get('atr_multiplier_tp', 4.0)},
        "min_rr_ratio": {conf.get('min_rr_ratio', 1.4)},
        "max_rr_ratio": {(conf.get('atr_multiplier_tp', 4.0) / conf.get('atr_multiplier_sl', 2.0)):.1f},
        "support_resistance_weight": {conf.get('support_resistance_weight', 0.25)},
        "volume_confirmation": {conf.get('volume_confirmation', True)},
        "session_filter": {conf.get('session_filter', True)},
        "volatility_adjustment": {conf.get('volatility_adjustment', True)},
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "{conf.get('preferred_strategy', 'auto')}",
        "trending_threshold": {conf.get('trending_threshold', 0.020)},
        "ranging_threshold": {conf.get('ranging_threshold', 0.025)},
        "confidence_threshold": {conf.get('confidence_threshold', 0.20)},
        "force_strategy": {conf.get('force_strategy', False)},
        "asset_class": "{conf.get('asset_class', 'unknown')}",
        "session": "{conf.get('session', '24/5')}",
        "weight": {conf.get('weight', 0.05)},
        "risk_multiplier": {conf.get('risk_multiplier', 0.7)}
    }},
'''
    
    config_text += '''
    # === FOREX CROSS PAIRS ===
'''
    
    # Forex cross symbols
    forex_cross_symbols = ["EURGBP", "EURJPY", "GBPJPY", "AUDJPY", "CADJPY", "CHFJPY", "EURCHF", "GBPCHF"]
    for symbol in forex_cross_symbols:
        if symbol in config:
            conf = config[symbol]
            config_text += f'''    "{symbol}": {{
        # Forex Cross - {conf.get('explanation', 'Strategy configuration')}
        "entry_method": "{conf.get('entry_method', 'auto_select')}",
        "atr_multiplier_sl": {conf.get('atr_multiplier_sl', 2.0)},
        "atr_multiplier_tp": {conf.get('atr_multiplier_tp', 4.0)},
        "min_rr_ratio": {conf.get('min_rr_ratio', 1.4)},
        "max_rr_ratio": {(conf.get('atr_multiplier_tp', 4.0) / conf.get('atr_multiplier_sl', 2.0)):.1f},
        "support_resistance_weight": {conf.get('support_resistance_weight', 0.25)},
        "volume_confirmation": {conf.get('volume_confirmation', True)},
        "session_filter": {conf.get('session_filter', True)},
        "volatility_adjustment": {conf.get('volatility_adjustment', True)},
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "{conf.get('preferred_strategy', 'auto')}",
        "trending_threshold": {conf.get('trending_threshold', 0.020)},
        "ranging_threshold": {conf.get('ranging_threshold', 0.025)},
        "confidence_threshold": {conf.get('confidence_threshold', 0.20)},
        "force_strategy": {conf.get('force_strategy', False)},
        "asset_class": "{conf.get('asset_class', 'unknown')}",
        "session": "{conf.get('session', '24/5')}",
        "weight": {conf.get('weight', 0.05)},
        "risk_multiplier": {conf.get('risk_multiplier', 0.7)}
    }},
'''
    
    config_text += '''
    # === FOREX EXOTIC PAIRS ===
'''
    
    # Forex exotic symbols
    forex_exotic_symbols = ["AUDNZD"]
    for symbol in forex_exotic_symbols:
        if symbol in config:
            conf = config[symbol]
            config_text += f'''    "{symbol}": {{
        # Forex Exotic - {conf.get('explanation', 'Strategy configuration')}
        "entry_method": "{conf.get('entry_method', 'auto_select')}",
        "atr_multiplier_sl": {conf.get('atr_multiplier_sl', 2.0)},
        "atr_multiplier_tp": {conf.get('atr_multiplier_tp', 4.0)},
        "min_rr_ratio": {conf.get('min_rr_ratio', 1.4)},
        "max_rr_ratio": {(conf.get('atr_multiplier_tp', 4.0) / conf.get('atr_multiplier_sl', 2.0)):.1f},
        "support_resistance_weight": {conf.get('support_resistance_weight', 0.25)},
        "volume_confirmation": {conf.get('volume_confirmation', True)},
        "session_filter": {conf.get('session_filter', True)},
        "volatility_adjustment": {conf.get('volatility_adjustment', True)},
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "{conf.get('preferred_strategy', 'auto')}",
        "trending_threshold": {conf.get('trending_threshold', 0.020)},
        "ranging_threshold": {conf.get('ranging_threshold', 0.025)},
        "confidence_threshold": {conf.get('confidence_threshold', 0.20)},
        "force_strategy": {conf.get('force_strategy', False)},
        "asset_class": "{conf.get('asset_class', 'unknown')}",
        "session": "{conf.get('session', '24/5')}",
        "weight": {conf.get('weight', 0.05)},
        "risk_multiplier": {conf.get('risk_multiplier', 0.7)}
    }},
'''
    
    config_text += '''
    # === EQUITY MAJOR INDICES (US) ===
'''
    
    # Equity major symbols
    equity_major_symbols = ["SPX500", "NAS100", "US30"]
    for symbol in equity_major_symbols:
        if symbol in config:
            conf = config[symbol]
            config_text += f'''    "{symbol}": {{
        # Equity Major - {conf.get('explanation', 'Strategy configuration')}
        "entry_method": "{conf.get('entry_method', 'auto_select')}",
        "atr_multiplier_sl": {conf.get('atr_multiplier_sl', 2.0)},
        "atr_multiplier_tp": {conf.get('atr_multiplier_tp', 4.0)},
        "min_rr_ratio": {conf.get('min_rr_ratio', 1.4)},
        "max_rr_ratio": {(conf.get('atr_multiplier_tp', 4.0) / conf.get('atr_multiplier_sl', 2.0)):.1f},
        "support_resistance_weight": {conf.get('support_resistance_weight', 0.25)},
        "volume_confirmation": {conf.get('volume_confirmation', True)},
        "session_filter": {conf.get('session_filter', True)},
        "volatility_adjustment": {conf.get('volatility_adjustment', True)},
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "{conf.get('preferred_strategy', 'auto')}",
        "trending_threshold": {conf.get('trending_threshold', 0.020)},
        "ranging_threshold": {conf.get('ranging_threshold', 0.025)},
        "confidence_threshold": {conf.get('confidence_threshold', 0.20)},
        "force_strategy": {conf.get('force_strategy', False)},
        "asset_class": "{conf.get('asset_class', 'unknown')}",
        "session": "{conf.get('session', '24/5')}",
        "weight": {conf.get('weight', 0.05)},
        "risk_multiplier": {conf.get('risk_multiplier', 0.7)}
    }},
'''
    
    config_text += '''
    # === EQUITY EUROPEAN INDICES ===
'''
    
    # Equity European symbols
    equity_european_symbols = ["DE40", "UK100", "FR40"]
    for symbol in equity_european_symbols:
        if symbol in config:
            conf = config[symbol]
            config_text += f'''    "{symbol}": {{
        # Equity European - {conf.get('explanation', 'Strategy configuration')}
        "entry_method": "{conf.get('entry_method', 'auto_select')}",
        "atr_multiplier_sl": {conf.get('atr_multiplier_sl', 2.0)},
        "atr_multiplier_tp": {conf.get('atr_multiplier_tp', 4.0)},
        "min_rr_ratio": {conf.get('min_rr_ratio', 1.4)},
        "max_rr_ratio": {(conf.get('atr_multiplier_tp', 4.0) / conf.get('atr_multiplier_sl', 2.0)):.1f},
        "support_resistance_weight": {conf.get('support_resistance_weight', 0.25)},
        "volume_confirmation": {conf.get('volume_confirmation', True)},
        "session_filter": {conf.get('session_filter', True)},
        "volatility_adjustment": {conf.get('volatility_adjustment', True)},
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "{conf.get('preferred_strategy', 'auto')}",
        "trending_threshold": {conf.get('trending_threshold', 0.020)},
        "ranging_threshold": {conf.get('ranging_threshold', 0.025)},
        "confidence_threshold": {conf.get('confidence_threshold', 0.20)},
        "force_strategy": {conf.get('force_strategy', False)},
        "asset_class": "{conf.get('asset_class', 'unknown')}",
        "session": "{conf.get('session', '24/5')}",
        "weight": {conf.get('weight', 0.05)},
        "risk_multiplier": {conf.get('risk_multiplier', 0.7)}
    }},
'''
    
    config_text += '''
    # === EQUITY ASIAN INDICES ===
'''
    
    # Equity Asian symbols
    equity_asian_symbols = ["JP225", "AU200"]
    for symbol in equity_asian_symbols:
        if symbol in config:
            conf = config[symbol]
            config_text += f'''    "{symbol}": {{
        # Equity Asian - {conf.get('explanation', 'Strategy configuration')}
        "entry_method": "{conf.get('entry_method', 'auto_select')}",
        "atr_multiplier_sl": {conf.get('atr_multiplier_sl', 2.0)},
        "atr_multiplier_tp": {conf.get('atr_multiplier_tp', 4.0)},
        "min_rr_ratio": {conf.get('min_rr_ratio', 1.4)},
        "max_rr_ratio": {(conf.get('atr_multiplier_tp', 4.0) / conf.get('atr_multiplier_sl', 2.0)):.1f},
        "support_resistance_weight": {conf.get('support_resistance_weight', 0.25)},
        "volume_confirmation": {conf.get('volume_confirmation', True)},
        "session_filter": {conf.get('session_filter', True)},
        "volatility_adjustment": {conf.get('volatility_adjustment', True)},
        
        # Strategy Selection Parameters - NEWLY ADDED
        "preferred_strategy": "{conf.get('preferred_strategy', 'auto')}",
        "trending_threshold": {conf.get('trending_threshold', 0.020)},
        "ranging_threshold": {conf.get('ranging_threshold', 0.025)},
        "confidence_threshold": {conf.get('confidence_threshold', 0.20)},
        "force_strategy": {conf.get('force_strategy', False)},
        "asset_class": "{conf.get('asset_class', 'unknown')}",
        "session": "{conf.get('session', '24/5')}",
        "weight": {conf.get('weight', 0.05)},
        "risk_multiplier": {conf.get('risk_multiplier', 0.7)}
    }},
'''
    
    config_text += '''}
'''
    
    return config_text

def main():
    """Main function để generate config"""
    
    print("🚀 Comprehensive Symbol Configuration Generator")
    print("=" * 60)
    
    # Generate config text
    config_text = generate_entry_config_text()
    
    # Save to file
    filename = "complete_symbol_config_for_bot.py"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(config_text)
    
    print(f"✅ Complete configuration generated!")
    print(f"📁 File: {filename}")
    
    # Also save just the config dict
    config_dict_filename = "symbol_config_dict.py"
    config_text_dict = f'''# Symbol Configuration Dictionary - Copy to Bot
{config_text}

print("✅ Symbol configuration ready for Bot integration")
'''
    
    with open(config_dict_filename, 'w', encoding='utf-8') as f:
        f.write(config_text_dict)
    
    print(f"📁 Alternative file: {config_dict_filename}")
    
    print(f"\n📋 Summary:")
    print(f"🎯 Total symbols configured: 34")
    print(f"📊 Asset classes: Crypto (5), Commodities (5), Forex (16), Equity (8)")
    print(f"⚖️ Strategy distribution: Auto selection optimized")
    print(f"🔧 Entry methods: Optimized per symbol characteristics")
    
    print(f"\n🎯 Integration Instructions:")
    print(f"1. Open Bot-Trading_Swing (1).py")
    print(f"2. Find ENTRY_TP_SL_CONFIG section")
    print(f"3. Replace with content từ {filename}")
    print(f"4. Save và restart bot")
    print(f"5. Monitor strategy selection trong logs")
    
    return config_text

if __name__ == "__main__":
    main()