#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strategy Configuration Examples
Các ví dụ cụ thể để điều chỉnh cách Bot chọn Strategy

Tác giả: AI Assistant  
Ngày tạo: 2024
Mục đích: Provide ready-to-use configuration examples
"""

from strategy_config_updater import StrategyConfigUpdater

class StrategyExamples:
    """Các ví dụ config sẵn để copy-paste"""
    
    @staticmethod
    def get_trending_biased_config():
        """Config để Bot tập trung vào Trending Strategy"""
        config_updater = StrategyConfigUpdater()
        
        trending_config = {
            # Global settings để ưu tiên trending
            "GLOBAL_TREND_PREFERENCE": "trending",
            "MIN_TREND_CONFIDENCE": 0.12,  # Lower threshold = more opportunities
            "MAX_VOLATILITY_TREND": 3.0,   # Allow higher volatility
            
            # Bitcoin - Force trending
            "BTCUSD": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending", 
                "trending_threshold": 0.008,    # Very low = easy trending
                "ranging_threshold": 0.035,     # High = hard ranging
                "atr_multiplier_sl": 3.5,       # Larger SL for trending
                "atr_multiplier_tp": 7.0,       # Larger TP for trending
                "confidence_threshold": 0.15,   # Lower confidence needed
                "force_strategy": False,
                "explanation": "Bitcoin - Maximized for trending with very low threshold"
            },
            
            # Ethereum - Enhanced trending  
            "ETHUSD": {
                "preferred_strategy": "trending",
                "entry_method": "trend_following",
                "trending_threshold": 0.01,
                "ranging_threshold": 0.03,
                "atr_multiplier_sl": 3.2,
                "atr_multiplier_tp": 6.5,
                "confidence_threshold": 0.16,
                "force_strategy": False,
                "explanation": "Ethereum - Enhanced trending with higher tolerance"
            },
            
            # Gold - Trending mode
            "XAUUSD": {
                "preferred_strategy": "trending",
                "entry_method": "volatility_breakout",
                "trending_threshold": 0.012,
                "ranging_threshold": 0.032,
                "atr_multiplier_sl": 2.8,
                "atr_multiplier_tp": 5.5,
                "confidence_threshold": 0.17,
                "force_strategy": False,
                "explanation": "Gold - Switched to trending mode with volatility breakout"
            }
        }
        
        return trending_config
    
    @staticmethod
    def get_ranging_biased_config():
        """Config để Bot tập trung vào Ranging Strategy"""
        ranging_config = {
            # Global settings để ưu tiên ranging
            "GLOBAL_TREND_PREFERENCE": "ranging", 
            "MIN_TREND_CONFIDENCE": 0.25,   # Higher threshold = fewer false signals
            "MAX_VOLATILITY_TREND": 2.0,    # Strict volatility limit
            
            # Bitcoin - Force ranging
            "BTCUSD": {
                "preferred_strategy": "ranging",
                "entry_method": "fibonacci_confluence",
                "trending_threshold": 0.035,     # High = hard trending
                "ranging_threshold": 0.008,      # Very low = easy ranging  
                "atr_multiplier_sl": 1.8,        # Smaller SL for ranging
                "atr_multiplier_tp": 3.0,        # Smaller TP for ranging
                "confidence_threshold": 0.25,    # Higher confidence needed
                "force_strategy": False,
                "explanation": "Bitcoin - Ranging focused with Fibonacci levels"
            },
            
            # Ethereum - Ranging mode
            "ETHUSD": {
                "preferred_strategy": "ranging", 
                "entry_method": "support_resistance",
                "trending_threshold": 0.032,
                "ranging_threshold": 0.01,
                "atr_multiplier_sl": 2.0,
                "atr_multiplier_tp": 3.5,
                "confidence_threshold": 0.24,
                "force_strategy": False,
                "explanation": "Ethereum - Ranging with support/resistance focus"
            },
            
            # Gold - Ranging with Fibonacci
            "XAUUSD": {
                "preferred_strategy": "ranging",
                "entry_method": "fibonacci_confluence", 
                "trending_threshold": 0.03,
                "ranging_threshold": 0.012,
                "atr_multiplier_sl": 2.2,
                "atr_multiplier_tp": 3.8,
                "confidence_threshold": 0.23,
                "force_strategy": False,
                "explanation": "Gold - Ranging optimized with fibonacci tools"
            }
        }
        
        return ranging_config
    
    @staticmethod
    def get_balanced_config():
        """Config cân bằng giữa Trending và Ranging"""
        balanced_config = {
            # Global settings cân bằng
            "GLOBAL_TREND_PREFERENCE": "auto",
            "MIN_TREND_CONFIDENCE": 0.18,
            "MAX_VOLATILITY_TREND": 2.5,
            "PERFORMANCE_BASED_SELECTION": True,  # Key for balanced mode
            
            # Bitcoin - Adaptive auto
            "BTCUSD": {
                "preferred_strategy": "auto", 
                "entry_method": "volatility_breakout",
                "trending_threshold": 0.018,     # Moderate trending
                "ranging_threshold": 0.025,     # Moderate ranging
                "atr_multiplier_sl": 2.8,
                "atr_multiplier_tp": 5.2,
                "confidence_threshold": 0.19,
                "force_strategy": False,
                "explanation": "Bitcoin - Balanced auto selection with moderate thresholds"
            },
            
            # Ethereum - Balanced trending
            "ETHUSD": {
                "preferred_strategy": "auto",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.02,
                "ranging_threshold": 0.025, 
                "atr_multiplier_sl": 2.6,
                "atr_multiplier_tp": 4.8,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "explanation": "Ethereum - Balanced trending với moderate settings"
            },
            
            # Gold - Balanced fibonacci   
            "XAUUSD": {
                "preferred_strategy": "auto",
                "entry_method": "fibonacci_confluence",
                "trending_threshold": 0.022,
                "ranging_threshold": 0.022,    # Equal thresholds
                "atr_multiplier_sl": 2.3,
                "atr_multiplier_tp": 4.2,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "explanation": "Gold - Balanced với fibonacci và equal thresholds"
            }
        }
        
        return balanced_config
    
    @staticmethod
    def get_aggressive_config():
        """Config aggressive - nhiều trading opportunities hơn"""
        aggressive_config = {
            # Global aggressive settings
            "GLOBAL_TREND_PREFERENCE": "auto",
            "MIN_TREND_CONFIDENCE": 0.10,      # Very low = more signals  
            "MAX_VOLATILITY_TREND": 4.0,       # Allow high volatility
            "MIN_TREND_STRENGTH": 0.005,       # Lower strength requirements
            
            # Bitcoin - Aggressive trending
            "BTCUSD": {
                "preferred_strategy": "auto",
                "entry_method": "volatility_breakout",
                "trending_threshold": 0.006,    # Very low trending
                "ranging_threshold": 0.030,     # Still reasonable ranging
                "atr_multiplier_sl": 4.0,       # Larger SL to accommodate volatility
                "atr_multiplier_tp": 8.0,       # Larger TP for trending moves
                "confidence_threshold": 0.12,   # Very low confidence needed
                "force_strategy": False,
                "explanation": "Bitcoin - Aggressive mode với very low thresholds"
            },
            
            # Ethereum - Aggressive auto
            "ETHUSD": {
                "preferred_strategy": "auto",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.008,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 3.5,
                "atr_multiplier_tp": 7.0,
                "confidence_threshold": 0.13,
                "force_strategy": False,
                "explanation": "Ethereum - Aggressive auto với high RR ratios"
            }
        }
        
        return aggressive_config
    
    @staticmethod
    def get_conservative_config():
        """Config conservative - ít trading nhưng chất lượng cao"""
        conservative_config = {
            # Global conservative settings  
            "GLOBAL_TREND_PREFERENCE": "ranging",
            "MIN_TREND_CONFIDENCE": 0.30,      # High confidence required
            "MAX_VOLATILITY_TREND": 1.8,       # Low volatility only
            "MIN_TREND_STRENGTH": 0.025,       # Strong trends only
            
            # Bitcoin - Conservative ranging
            "BTCUSD": {
                "preferred_strategy": "ranging",
                "entry_method": "fibonacci_confluence",
                "trending_threshold": 0.04,     # Very high = rarely trending
                "ranging_threshold": 0.005,    # Very low = easy ranging
                "atr_multiplier_sl": 1.5,      # Tight stops
                "atr_multiplier_tp": 2.8,      # Reasonable TP
                "confidence_threshold": 0.28,   # High confidence required
                "force_strategy": True,         # Force ranging strategy
                "explanation": "Bitcoin - Ultra conservative ranging mode"
            },
            
            # Ethereum - Conservative fibonacci
            "ETHUSD": {
                "preferred_strategy": "ranging",
                "entry_method": "support_resistance", 
                "trending_threshold": 0.038,
                "ranging_threshold": 0.006,
                "atr_multiplier_sl": 1.6,
                "atr_multiplier_tp": 3.0,
                "confidence_threshold": 0.32,
                "force_strategy": True,
                "explanation": "Ethereum - Conservative support/resistance"
            }
        }
        
        return conservative_config

def apply_config_example(config_name: str = "balanced"):
    """
    Apply một config example vào strategy config updater
    
    Args:
        config_name: "trending", "ranging", "balanced", "aggressive", "conservative"
    """
    
    examples = StrategyExamples()
    
    config_mapping = {
        "trending": examples.get_trending_biased_config(),
        "ranging": examples.get_ranging_biased_config(), 
        "balanced": examples.get_balanced_config(),
        "aggressive": examples.get_aggressive_config(),
        "conservative": examples.get_conservative_config()
    }
    
    if config_name not in config_mapping:
        print(f"❌ Unknown config: {config_name}")
        print(f"Available configs: {list(config_mapping.keys())}")
        return None
    
    config = config_mapping[config_name]
    
    print(f"🚀 Applied {config_name.upper()} Configuration")
    print("=" * 50)
    
    if "GLOBAL_TREND_PREFERENCE" in config:
        print(f"🌍 Global Preference: {config['GLOBAL_TREND_PREFERENCE'].upper()}")
        print(f"📊 Min Confidence: {config['MIN_TREND_CONFIDENCE']}")
        print(f"📈 Max Volatility: {config['MAX_VOLATILITY_TREND']}")
        print()
    
    # Show symbol configs
    for symbol, symbol_config in config.items():
        if isinstance(symbol_config, dict) and 'preferred_strategy' in symbol_config:
            print(f"📈 {symbol}:")
            print(f"   Strategy: {symbol_config['preferred_strategy'].upper()}")
            print(f"   Entry Method: {symbol_config['entry_method']}")
            print(f"   Thresholds: Trending {symbol_config['trending_threshold']} | Ranging {symbol_config['ranging_threshold']}")
            print(f"   Confidence: {symbol_config['confidence_threshold']}")
            print(f"   RR Ratio: SL {symbol_config['atr_multiplier_sl']}x | TP {symbol_config['atr_multiplier_tp']}x")
            print()
    
    print("💡 To integrate vào bot:")
    print("1. Copy values từ config example")
    print("2. Update strategy_config_updater.py")  
    print("3. Restart bot để apply changes")
    
    return config

def show_all_examples():
    """Hiển thị summary của tất cả config examples"""
    print("🎯 STRATEGY CONFIG EXAMPLES SUMMARY")
    print("=" * 60)
    
    examples_summary = {
        "TRENDING BIASED": {
            "description": "Bot sẽ chọn trending strategy nhiều nhất",
            "best_for": "Bull/Bear markets, Strong directional moves",
            "characteristics": ["Low trending thresholds", "High RR ratios", "Volatility breakout"]
        },
        
        "RANGING BIASED": {
            "description": "Bot sẽ chọn ranging strategy nhiều nhất", 
            "best_for": "Sideways markets, Consolidation periods",
            "characteristics": ["High ranging thresholds", "Fibonacci tools", "Support/Resistance"]
        },
        
        "BALANCED": {
            "description": "Bot tự động cân bằng giữa trending và ranging",
            "best_for": "Mixed markets, Adaptive trading",
            "characteristics": ["Auto selection", "Equal thresholds", "Performance based"]
        },
        
        "AGGRESSIVE": {
            "description": "Bot sẽ trade với nhiều opportunities nhất",
            "best_for": "Active traders, High frequency strategies", 
            "characteristics": ["Very low thresholds", "High RR ratios", "High volatility tolerance"]
        },
        
        "CONSERVATIVE": {
            "description": "Bot chỉ trade với signals chất lượng cao",
            "best_for": "Risk-averse traders, Quality over quantity",
            "characteristics": ["High confidence required", "Low volatility", "Tight stops"]
        }
    }
    
    for strategy_type, details in examples_summary.items():
        print(f"\n🔧 {strategy_type}:")
        print(f"   📝 {details['description']}")
        print(f"   🎯 Best for: {details['best_for']}")
        print(f"   ⚙️ Key features: {', '.join(details['characteristics'])}")
    
    print(f"\n📋 To apply any config example:")
    print("apply_config_example('trending')  # For trending biased")
    print("apply_config_example('ranging')   # For ranging biased") 
    print("apply_config_example('balanced')  # For balanced mode")
    print("apply_config_example('aggressive') # For aggressive mode")
    print("apply_config_example('conservative') # For conservative mode")

if __name__ == "__main__":
    print("🎯 Strategy Configuration Examples")
    print("=" * 50)
    
    # Show summary of all examples
    show_all_examples()
    
    print("\n🚀 Applying Balanced Example:")
    print("-" * 30)
    
    # Apply balanced example để demo
    balanced_config = apply_config_example("balanced")
    
    if balanced_config:
        print("\n✅ Balanced config ready to use!")
        print("Copy các values này vào strategy_config_updater.py để apply vào bot")