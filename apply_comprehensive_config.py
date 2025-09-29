#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apply Comprehensive Symbol Configuration to Bot
Tool để apply comprehensive config vào bot chính

Tác giả: AI Assistant
Ngày tạo: 2024
Mục đích: Easy integration cho comprehensive symbol config
"""

import json
import os
from datetime import datetime
from comprehensive_symbol_config import ComprehensiveSymbolConfig

class ComprehensiveConfigApplicator:
    """Class để apply comprehensive config vào bot"""
    
    def __init__(self, bot_file_path: str = "Bot-Trading_Swing (1).py"):
        self.bot_file_path = bot_file_path
        self.config_loader = ComprehensiveSymbolConfig()
        
    def generate_complete_entry_config(self) -> str:
        """Generate complete ENTRY_TP_SL_CONFIG section với tất cả symbols"""
        
        config = self.config_loader.get_comprehensive_symbol_config()
        
        config_text = '''# Enhanced Entry/TP/SL Configuration for ALL SYMBOLS - COMPREHENSIVE VERSION
ENTRY_TP_SL_CONFIG = {
    # === CRYPTOCURRENCIES (24/7 Trading) ===
'''
        
        # Crypto symbols
        crypto_symbols = ["BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "ADAUSD"]
        for symbol in crypto_symbols:
            if symbol in config:
                conf = config[symbol]
                config_text += self._generate_symbol_config_code(symbol, conf, "Crypto")
        
        config_text += '''
    # === COMMODITIES (Global Trading) ===
'''
        
        # Commodity symbols
        commodity_symbols = ["XAUUSD", "XAGUSD", "USOIL", "UKOIL", "NATGAS"]
        for symbol in commodity_symbols:
            if symbol in config:
                conf = config[symbol]
                config_text += self._generate_symbol_config_code(symbol, conf, "Commodity")
        
        config_text += '''
    # === FOREX MAJOR PAIRS ===
'''
        
        # Forex major symbols
        forex_major_symbols = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "NZDUSD", "USDCHF"]
        for symbol in forex_major_symbols:
            if symbol in config:
                conf = config[symbol]
                config_text += self._generate_symbol_config_code(symbol, conf, "Forex Major")
        
        config_text += '''
    # === FOREX CROSS PAIRS ===
'''
        
        # Forex cross symbols
        forex_cross_symbols = ["EURGBP", "EURJPY", "GBPJPY", "AUDJPY", "CADJPY", "CHFJPY", "EURCHF", "GBPCHF"]
        for symbol in forex_cross_symbols:
            if symbol in config:
                conf = config[symbol]
                config_text += self._generate_symbol_config_code(symbol, conf, "Forex Cross")
        
        config_text += '''
    # === FOREX EXOTIC PAIRS ===
'''
        
        # Forex exotic symbols
        forex_exotic_symbols = ["AUDNZD"]
        for symbol in forex_exotic_symbols:
            if symbol in config:
                conf = config[symbol]
                config_text += self._generate_symbol_config_code(symbol, conf, "Forex Exotic")
        
        config_text += '''
    # === EQUITY MAJOR INDICES (US) ===
'''
        
        # Equity major symbols
        equity_major_symbols = ["SPX500", "NAS100", "US30"]
        for symbol in equity_major_symbols:
            if symbol in config:
                conf = config[symbol]
                config_text += self._generate_symbol_config_code(symbol, conf, "Equity Major")
        
        config_text += '''
    # === EQUITY EUROPEAN INDICES ===
'''
        
        # Equity European symbols
        equity_european_symbols = ["DE40", "UK100", "FR40"]
        for symbol in equity_european_symbols:
            if symbol in config:
                conf = config[symbol]
                config_text += self._generate_symbol_config_code(symbol, conf, "Equity European")
        
        config_text += '''
    # === EQUITY ASIAN INDICES ===
'''
        
        # Equity Asian symbols
        equity_asian_symbols = ["JP225", "AU200"]
        for symbol in equity_asian_symbols:
            if symbol in config:
                conf = config[symbol]
                config_text += self._generate_symbol_config_code(symbol, conf, "Equity Asian")
        
        config_text += '''}
'''
        
        return config_text
    
    def _generate_symbol_config_code(self, symbol: str, conf: dict, category: str) -> str:
        """Generate config code for single symbol"""
        
        code = f'''    "{symbol}": {{
        # {category} - {conf.get('explanation', 'Strategy configuration')}
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
        
        # Add special parameters if available
        if conf.get('fibonacci_levels'):
            fibonacci_str = str(conf['fibonacci_levels']).replace("'", '"')
            code += f''',
        "fibonacci_levels": {fibonacci_str}'''
        
        # Add trailing stop config for some symbols
        if symbol in ['BTCUSD', 'ETHUSD', 'XAUUSD', 'SPX500']:
            code += f''',
        # Master Agent Trailing Stop Configuration
        "min_trailing_profit": {conf.get('min_trailing_profit', 0.012)},
        "trailing_atr_multiplier": {conf.get('trailing_atr_multiplier', 1.5)},
        "trailing_volatility_threshold": {conf.get('trailing_volatility_threshold', 0.6)},
        "trailing_trend_strength_min": {conf.get('trailing_trend_strength_min', 0.7)}'''
        
        code += '''
    },
'''
        
        return code
    
    def generate_strategy_selection_config(self) -> str:
        """Generate strategy selection configuration section"""
        
        config_text = '''# STRATEGY SELECTION CONFIGURATION - COMPREHENSIVE
STRATEGY_SELECTION_CONFIG = {
    "GLOBAL_SETTINGS": {
        "ENABLE_DYNAMIC_STRATEGY_SELECTION": True,
        "GLOBAL_TREND_PREFERENCE": "auto",
        "MIN_TREND_CONFIDENCE": 0.18,
        "MAX_VOLATILITY_TREND": 2.5,
        "PERFORMANCE_BASED_SELECTION": True,
        "VOLATILITY_ADJUSTMENT_FACTOR": 1.2,
        "VOLUME_CONFIRMATION_REQUIRED": True,
        "MULTI_TIMEFRAME_ANALYSIS": True,
        "REGIME_DETECTION_WINDOW": 50,
        "ADAPTIVE_THRESHOLDS": True,
        "CONTEXT_EXPLAINED_MODE": True,
        "LOGGING_STRATEGY_DECISIONS": True
    },
    
    "STRATEGY_MAPPING": {
        "trending_methods": [
            "momentum_trending",
            "trend_following", 
            "volatility_breakout"
        ],
        "ranging_methods": [
            "range_bound",
            "support_resistance",
            "fibonacci_confluence",
            "mean_reversion"
        ],
        "carry_trade_methods": [
            "carry_trade"
        ]
    },
    
    "WEIGHT_MULTIPLIERS": {
        "trending": {
            "trend_strength_weight": 0.35,
            "volatility_weight": 0.25,
            "volume_weight": 0.20,
            "momentum_weight": 0.20
        },
        "ranging": {
            "range_size_weight": 0.30,
            "support_resistance_weight": 0.25,
            "volatility_weight": 0.25,
            "fibonacci_weight": 0.20
        }
    },
    
    "MINIMUM_REQUIREMENTS": {
        "min_data_points": 100,
        "min_signals_count": 3,
        "min_confidence_correlation": 0.15,
        "max_opinion_divergence": 0.4,
        "backup_strategy_timeout": 30
    },
    
    "MODEL_CONFIGURATION": {
        "trending_model_min_samples": 1000,
        "ranging_model_min_samples": 800,
        "performance_degradation_threshold": 0.15,
        "retrain_frequency_hours": 24
    }
}
'''
        
        return config_text
    
    def generate_symbol_metadata_config(self) -> str:
        """Generate symbol metadata configuration"""
        
        config = self.config_loader.get_comprehensive_symbol_config()
        categories = self.config_loader.get_all_symbols_by_category()
        
        config_text = '''# SYMBOL METADATA CONFIGURATION - COMPREHENSIVE
SYMBOL_METADATA_CONFIG = {
'''
        
        for category, symbols in categories.items():
            if category != "ACTIVE_SYMBOLS":
                config_text += f'''    "{category}": {{\n        "symbols": {symbols},\n        "count": {len(symbols)}\n    }},
'''
        
        # Add individual symbol metadata
        config_text += '''
    "individual_symbols": {
'''
        
        for symbol, conf in config.items():
            config_text += f'''        "{symbol}": {{
            "asset_class": "{conf.get('asset_class', 'unknown')}",
            "session": "{conf.get('session', '24/5')}",
            "weight": {conf.get('weight', 0.05)},
            "risk_multiplier": {conf.get('risk_multiplier', 0.7)},
            "strategy_type": "{conf.get('preferred_strategy', 'auto')}",
            "entry_method": "{conf.get('entry_method', 'auto_select')}"
        }},
'''
        
        config_text += '''    }
}'''
        
        return config_text
    
    def create_comprehensive_patch_file(self, patch_type: str = "balanced") -> str:
        """Create comprehensive patch file để apply vào bot"""
        
        patch_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPREHENSIVE BOT CONFIGURATION PATCH
All Symbols Strategy Configuration
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Coverage: 34 symbols across all asset classes

⚠️ CRITICAL INSTRUCTIONS:
1. BACKUP your Bot-Trading_Swing (1).py file!!!
2. Find ENTRY_TP_SL_CONFIG section in bot file
3. Replace entire section with COMPREHENSIVE_ENTRY_TP_SL_CONFIG below
4. Add STRATEGY_SELECTION_CONFIG section if not exists
5. Add SYMBOL_METADATA_CONFIG section if not exists  
6. Test thoroughly trước khi live trading

📊 COVERAGE SUMMARY:
- Total Symbols: 34
- Cryptocurrencies: 5
- Commodities: 5  
- Forex Majors: 7
- Forex Minors/Cross: 9
- Equity Indices: 8
"""

print("🚨 COMPREHENSIVE CONFIGURATION PATCH")
print("=" * 60)
print("Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Total Symbols:", 34)
print("⚠️ BACKUP YOUR BOT BEFORE APPLYING!")
print()

# === COMPREHENSIVE ENTRY CONFIG SECTION ===
COMPREHENSIVE_ENTRY_TP_SL_CONFIG = {{

{self.generate_complete_entry_config()}

# === STRATEGY SELECTION CONFIG SECTION ===  
COMPREHENSIVE_STRATEGY_SELECTION_CONFIG = {{

{self.generate_strategy_selection_config()}

# === SYMBOL METADATA CONFIG SECTION ===
COMPREHENSIVE_SYMBOL_METADATA_CONFIG = {{

{self.generate_symbol_metadata_config()}

print("📋 APPLICATION INSTRUCTIONS:")
print("=" * 50)
print("1. Find ENTRY_TP_SL_CONFIG in Bot-Trading_Swing (1).py")
print("2. Replace with COMPREHENSIVE_ENTRY_TP_SL_CONFIG above")
print("3. Add STRATEGY_SELECTION_CONFIG section")
print("4. Add SYMBOL_METADATA_CONFIG section") 
print("5. Restart bot để apply changes")
print("6. Monitor performance của different symbols")
print()
print("🎯 Expected Benefits:")
print("- Configure strategy selection cho TẤT CẢ symbols")
print("- Optimized thresholds theo asset class")
print("- Better trending/ranging detection")
print("- Enhanced risk management per symbol")
print()
print("⚠️ Testing Recommendations:")
print("- Start với small positions")
print("- Monitor strategy selection logs")
print("- Adjust thresholds if needed")
print("- Backup config trước khi changes")
'''

        update_existing_config = f'''OLD_ENTRY_TP_SL_CONFIG = {{

{self.generate_complete_entry_config()}

NEW_ENTRY_TP_SL_CONFIG = f'''
# Enhanced Entry/TP/SL Configuration for ALL SYMBOLS - UPDATED VERSION  
ENTRY_TP_SL_CONFIG = {{

{self.generate_complete_entry_config()}
'''

        # Save patch file
        patch_filename = f"comprehensive_config_patch.py"
        with open(patch_filename, 'w', encoding='utf-8') as f:
            f.write(patch_content)
        
        print(f"✅ Comprehensive patch created: {patch_filename}")
        
        # Also create simple replacement file
        replacement_filename = f"symbol_config_replacement.py" 
        simple_content = f'''#!/usr/bin/env python3
# Simple Symbol Config Replacement

ENTRY_TP_SL_CONFIG = {{

{self.generate_complete_entry_config()}f'''

print("✅ Symbol config ready for replacement")
'''
        
        with open(replacement_filename, 'w', encoding='utf-8') as f:
            f.write(simple_content)
        
        print(f"✅ Simple replacement created: {replacement_filename}")
        
        return patch_filename

def main():
    """Main function để create comprehensive patch"""
    
    print("🚀 Comprehensive Configuration Applicator")
    print("=" * 50)
    
    applicator = ComprehensiveConfigApplicator()
    
    # Generate comprehensive config
    print("📊 Generating comprehensive configuration...")
    patch_file = applicator.create_comprehensive_patch_file()
    
    print(f"\n✅ Files created:")
    print(f"📁 {patch_file} - Complete patch file")
    print(f"📁 symbol_config_replacement.py - Simple replacement")
    print(f"📁 comprehensive_symbol_config.json - Config data")
    
    print(f"\n📋 SUMMARY:")
    print(f"🎯 Total symbols configured: 34")
    print(f"⚖️ Strategy distribution: Balanced auto selection")
    print(f"🔧 Asset classes covered: Crypto, Forex, Commodities, Equity")
    print(f"📈 Entry methods: 8 different methods optimized per symbol")
    
    print(f"\n🎯 Next Steps:")
    print(f"1. Review comprehensive_symbol_config.json")
    print(f"2. Apply symbol_config_replacement.py vào bot") 
    print(f"3. Test với individual symbols")
    print(f"4. Fine-tune based on performance")
    
    return applicator

if __name__ == "__main__":
    main()