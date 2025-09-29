#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strategy Configuration Updater
File riêng để cấu hình và điều chỉnh strategy selection giữa Ranging vs Trending

Tác giả: AI Assistant
Ngày tạo: 2024
Mục đích: Cung cấp file cấu hình độc lập để điều chỉnh Bot strategy
"""

import json
import datetime
from typing import Dict, Any, Optional

class StrategyConfigUpdater:
    """Class để quản lý và cập nhật cấu hình strategy selection"""
    
    def __init__(self):
        self.config_version = "1.0.0"
        self.last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def get_symbol_specific_config(self) -> Dict[str, Dict[str, Any]]:
        """
        Cấu hình riêng cho từng symbol về strategy preference
        """
        return {
            # === CRYPTO SYMBOLS ===
            "BTCUSD": {
                "preferred_strategy": "auto",  # "trending", "ranging", "auto"
                "entry_method": "volatility_breakout",
                "trending_threshold": 0.015,   # Lower = easier to trigger trending
                "ranging_threshold": 0.025,    # Higher = easier to trigger ranging
                "atr_multiplier_sl": 3.0,
                "atr_multiplier_tp": 6.0,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "explanation": "Bitcoin - Volatility breakout strategy với auto selection"
            },
            
            "ETHUSD": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending", 
                "trending_threshold": 0.02,
                "ranging_threshold": 0.03,
                "atr_multiplier_sl": 2.8,
                "atr_multiplier_tp": 5.5,
                "confidence_threshold": 0.22,
                "force_strategy": False,
                "explanation": "Ethereum - Momentum trending với ưu tiên trending"
            },
            
            # === FOREX MAJORS ===
            "EURUSD": {
                "preferred_strategy": "auto",
                "entry_method": "trend_following",
                "trending_threshold": 0.018,
                "ranging_threshold": 0.028,
                "atr_multiplier_sl": 1.8,
                "atr_multiplier_tp": 2.8,
                "confidence_threshold": 0.18,
                "force_strategy": False,
                "explanation": "EUR/USD - Trend following với auto selection"
            },
            
            "GBPUSD": {
                "preferred_strategy": "ranging",
                "entry_method": "support_resistance",
                "trending_threshold": 0.025,
                "ranging_threshold": 0.015,
                "atr_multiplier_sl": 2.0,
                "atr_multiplier_tp": 3.0,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "explanation": "GBP/USD - Support resistance với ưu tiên ranging"
            },
            
            # === COMMODITIES ===
            "XAUUSD": {
                "preferred_strategy": "auto",
                "entry_method": "fibonacci_confluence",
                "trending_threshold": 0.02,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.5,
                "atr_multiplier_tp": 4.0,
                "confidence_threshold": 0.19,
                "force_strategy": False,
                "explanation": "Gold - Fibonacci confluence với auto selection"
            },
            
            "USOIL": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.018,
                "ranging_threshold": 0.03,
                "atr_multiplier_sl": 2.2,
                "atr_multiplier_tp": 4.5,
                "confidence_threshold": 0.21,
                "force_strategy": False,
                "explanation": "Oil - Momentum trending với ưu tiên trending"
            },
            
            # === INDICES ===
            "SPX500": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.016,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.2,
                "atr_multiplier_tp": 3.5,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "explanation": "S&P 500 - Momentum trending với ưu tiên trending"
            },
            
            "NAS100": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.017,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.2,
                "atr_multiplier_tp": 3.5,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "explanation": "Nasdaq - Momentum trending với ưu tiên trending"
            }
        }
    
    def get_global_mode_config(self) -> Dict[str, Any]:
        """
        Cấu hình global mode để điều khiển tổng thể
        """
        return {
            "ENABLE_DYNAMIC_STRATEGY_SELECTION": True,
            "GLOBAL_TREND_PREFERENCE": "auto",  # "trending", "ranging", "auto"
            "MIN_TREND_CONFIDENCE": 0.15,
            "MIN_TREND_STRENGTH": 0.01,
            "MAX_VOLATILITY_TREND": 2.5,
            "STRATEGY_CONSISTENCY_CHECK": True,
            "PERFORMANCE_BASED_SELECTION": True,
            "VOLATILITY_ADJUSTMENT_FACTOR": 1.2,
            "VOLUME_CONFIRMATION_REQUIRED": True,
            "MULTI_TIMEFRAME_ANALYSIS": True,
            "REGIME_DETECTION_WINDOW": 50,
            "ADAPTIVE_THRESHOLDS": True,
            "CONTEXT_EXPLAINED_MODE": True,
            "LOGGING_STRATEGY_DECISIONS": True,
            "STRATEGY_ID_MAP": {
                "trending": ["momentum_trending", "trend_following", "volatility_breakout"],
                "ranging": ["range_bound", "support_resistance", "fibonacci_confluence", "mean_reversion"]
            },
            "STRATEGY_WEIGHT_MULTIPLIERS": {
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
            "MODEL_RETRAIN_THRESHOLDS": {
                "trending_model_min_samples": 1000,
                "ranging_model_min_samples": 800,
                "performance_degradation_threshold": 0.15,
                "retrain_frequency_hours": 24
            }
        }
    
    def get_strategy_selection_rules(self) -> Dict[str, Any]:
        """
        Chi tiết rules cho strategy selection
        """
        return {
            "STRATEGY_RULES": {
                "FORCE_TRENDING_CONDITIONS": [
                    "trend_strength >= trending_threshold",
                    "volatility < max_volatility_trend", 
                    "volume_confirmation == True",
                    "momentum_aligned == True",
                    "sma_alignment_bullish OR sma_alignment_bearish",
                    "confidence >= min_confidence"
                ],
                
                "FORCE_RANGING_CONDITIONS": [
                    "trend_strength < ranging_threshold",
                    "range_size_normalized < 0.015",
                    "sideways_price_action == True",
                    "support_resistance_active == True",
                    "volatility_stable < 2.0",
                    "fibonacci_levels_tested == True"
                ],
                
                "HYBRID_CONDITIONS": [
                    "trend_strength BETWEEN trending_threshold AND ranging_threshold",
                    "high_volatility > 3.0",
                    "mixed_signals == True",
                    "uncertainty_period == True"
                ]
            },
            
            "DECISION_PRIORITY": [
                "1. Force strategy from symbol config",
                "2. Global mode override",
                "3. Market regime detection",
                "4. Technical analysis confluence",
                "5. Volume confirmation",
                "6. Volatility analysis", 
                "7. Timeframe alignment",
                "8. Default ranging strategy"
            ],
            
            "MINIMUM_REQUIREMENTS": {
                "min_data_points": 100,
                "min_signals_count": 3,
                "min_confidence_correlation": 0.15,
                "max_opinion_divergence": 0.4,
                "backup_strategy_timeout": 30  # seconds
            }
        }
    
    def get_interpretation_guide(self) -> Dict[str, str]:
        """
        Hướng dẫn giải thích cách config có ý nghĩa gì
        """
        return {
            "SỬ DỤNG FILE NÀY": """
            File này cho phép bạn điều chỉnh cách Bot quyết định chọn strategy mà KHÔNG CẦN chỉnh sửa file bot chính.
            
            CÁCH SỬ DỤNG:
            1. Chỉnh các giá trị trong get_symbol_specific_config()
            2. Adjust global mode trong get_global_mode_config()
            3. Import và áp dụng vào bot chính
            4. Bot sẽ tự động cập nhật theo config mới
            """,
            
            "Ý NGHĨA CÁC THAM SỐ": {
                "preferred_strategy": """
                - "auto": Bot tự chọn based on market conditions
                - "trending": Force chọn trending strategy  
                - "ranging": Force chọn ranging strategy
                """,
                
                "entry_method": """
                Trending-friendly: momentum_trending, trend_following, volatility_breakout
                Ranging-friendly: range_bound, support_resistance, fibonacci_confluence
                """,

                "trending_threshold": """
                Nhỏ = Dễ trigger trending (Bot sẽ chọn trending nhiều hơn)
                Lớn = Khó trigger trending (Bot sẽ chọn ranging nhiều hơn)
                """,
                
                "ranging_threshold": """
                Nhỏ = Dễ trigger ranging (Bot sẽ chọn ranging nhiều hơn)
                Lớn = Khó trigger ranging (Bot sẽ chọn trending nhiều hơn)  
                """,
                
                "confidence_threshold": """
                Nhỏ = Bot sẽ trade với confidence thấp hơn (nhiều cơ hội hơn)
                Lớn = Bot sẽ trade với confidence cao hơn (ít cơ hội hơn)
                """,
                
                "force_strategy": """
                True = Always chọn strategy được chỉ định, ignore market conditions
                False = Cho phép dynamic selection based on market analysis
                """
            },
            
            "PHONG CÁCH TRADING": {
                "TRENDING BIASED": """
                Để Bot tập trung vào trending:
                1. Set preferred_strategy = "trending" cho main symbols
                2. Giảm trending_threshold xuống 0.01-0.015
                3. Tăng ranging_threshold lên 0.03-0.035
                4. Set entry_method = "momentum_trending"
                5. Set GLOBAL_TREND_PREFERENCE = "trending"
                """,
                
                "RANGING BIASED": """
                Để Bot tập trung vào ranging:
                1. Set preferred_strategy = "ranging" cho main symbols  
                2. Tăng trending_threshold lên 0.025-0.03
                3. Giảm ranging_threshold xuống 0.01-0.015
                4. Set entry_method = "fibonacci_confluence"
                5. Set GLOBAL_TREND_PREFERENCE = "ranging"
                """,
                
                "BALANCED": """
                Để Bot cân bằng và adaptive:
                1. Set preferred_strategy = "auto" cho hầu hết symbols
                2. Maintain thresholds ở khoảng 0.02 +/- 0.005
                3. Enable PERFORMANCE_BASED_SELECTION = True
                4. Set GLOBAL_TREND_PREFERENCE = "auto"
                """
            }
        }
    
    def generate_config_summary(self) -> str:
        """Hiển thị tóm tắt config hiện tại"""
        symbol_config = self.get_symbol_specific_config()
        global_config = self.get_global_mode_config()
        
        trending_count = sum(1 for config in symbol_config.values() 
                           if config.get('preferred_strategy') == 'trending')
        ranging_count = sum(1 for config in symbol_config.values() 
                          if config.get('preferred_strategy') == 'ranging')
        auto_count = sum(1 for config in symbol_config.values() 
                        if config.get('preferred_strategy') == 'auto')
        
        summary = f"""
🔧 STRATEGY CONFIGURATION SUMMARY
================================
Version: {self.config_version}
Last Updated: {self.last_updated}

📊 STRATEGY DISTRIBUTION:
- Trending Biased: {trending_count} symbols
- Ranging Biased: {ranging_count} symbols  
- Auto Selection: {auto_count} symbols

🌍 GLOBAL SETTINGS:
- Dynamic Selection: {'✅ Enabled' if global_config['ENABLE_DYNAMIC_STRATEGY_SELECTION'] else '❌ Disabled'}
- Global Preference: {global_config['GLOBAL_TREND_PREFERENCE'].upper()}
- Performance Based: {'✅ Enabled' if global_config['PERFORMANCE_BASED_SELECTION'] else '❌ Disabled'}
- Adaptive Thresholds: {'✅ Enabled' if global_config['ADAPTIVE_THRESHOLDS'] else '❌ Disabled'}

⚙️ MAJOR SYMBOLS SETTINGS:
"""
        
        for symbol in ['BTCUSD', 'ETHUSD', 'EURUSD', 'XAUUSD', 'SPX500']:
            if symbol in symbol_config:
                config = symbol_config[symbol]
                summary += f"- {symbol}: {config['preferred_strategy'].upper()} | {config['entry_method']} | Thresh: {config['trending_threshold']}/{config['ranging_threshold']}\n"
        
        return summary
    
    def save_config_to_file(self, filename: str = "strategy_config.json") -> bool:
        """Lưu config ra file JSON để backup hoặc chia sẻ"""
        try:
            config_data = {
                "meta": {
                    "version": self.config_version,
                    "created": self.last_updated,
                    "description": "Strategy Configuration for Trading Bot"
                },
                "symbol_specific": self.get_symbol_specific_config(),
                "global_mode": self.get_global_mode_config(), 
                "strategy_rules": self.get_strategy_selection_rules(),
                "interpretation_guide": self.get_interpretation_guide()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuration saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False

def main():
    """Demo function để show cách sử dụng"""
    print("🚀 Strategy Configuration Updater")
    print("=" * 50)
    
    updater = StrategyConfigUpdater()
    
    # Hiển thị summary config hiện tại
    print(updater.generate_config_summary())
    
    print("\n📋 Để điều chỉnh config:")
    print("1. Edit các giá trị trong get_symbol_specific_config()")
    print("2. Adjust global settings trong get_global_mode_config()")
    print("3. Save config: updater.save_config_to_file()")
    print("4. Import vào bot chính để apply changes")
    
    print("\n💡 Examples:")
    print("- Muốn BTCUSD chọn Trending nhiều hơn:")
    print("  Change BTCUSD trending_threshold: 0.015 → 0.01")
    print("  Change BTCUSD preferred_strategy: auto → trending")
    
    print("\n- Muốn toàn bộ Bot ưu tiên Ranging:")
    print("  Change GLOBAL_TREND_PREFERENCE: auto → ranging")
    print("  Tăng all trending_threshold +0.005")
    
    # Save config example
    if updater.save_config_to_file():
        print("\n📁 Config đã được save vào strategy_config.json")
    
    return updater

if __name__ == "__main__":
    main()