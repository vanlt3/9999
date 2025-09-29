#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Symbol Strategy Configuration
File cấu hình đầy đủ cho TẤT CẢ symbols có trong Bot

Tác giả: AI Assistant
Ngày tạo: 2024
Mục đích: Provide complete strategy configuration cho mọi symbol trong bot
"""

import json
import datetime
from typing import Dict, Any, List

class ComprehensiveSymbolConfig:
    """Comprehensive config cho tất cả symbols trong Bot"""
    
    def __init__(self):
        self.config_version = "2.0.0"
        self.last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def get_all_symbols_by_category(self) -> Dict[str, List[str]]:
        """Phân loại tất cả symbols theo asset class"""
        return {
            "CRYPTO": ["BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "ADAUSD"],
            
            "COMMODITIES": ["XAUUSD", "XAGUSD", "USOIL", "UKOIL", "NATGAS"],
            
            "FOREX_MAJORS": ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "NZDUSD", "USDCHF"],
            
            "FOREX_MINORS": ["EURGBP", "EURJPY", "GBPJPY", "AUDJPY", "CADJPY", "CHFJPY", "EURCHF", "GBPCHF"],
            
            "FOREX_EXOTICS": ["AUDNZD"],  # As per config
            
            "EQUITY_MAJORS": ["SPX500", "NAS100", "US30"],
            
            "EQUITY_EUROPEAN": ["DE40", "UK100", "FR40"],
            
            "EQUITY_ASIAN": ["JP225", "AU200"],
            
            "ACTIVE_SYMBOLS": ["BTCUSD", "ETHUSD", "XAUUSD", "USOIL", "SPX500", "DE40", "EURUSD", "AUDUSD", "AUDNZD"]  # As per SYMBOLS list
        }
    
    def get_comprehensive_symbol_config(self) -> Dict[str, Dict[str, Any]]:
        """Comprehensive config cho TẤT CẢ symbols với strategy selection parameters"""
        
        config = {}
        
        # === CRYPTOCURRENCIES (24/7 Trading) ===
        crypto_configs = {
            "BTCUSD": {
                "preferred_strategy": "auto",
                "entry_method": "volatility_breakout",
                "trending_threshold": 0.018,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 3.0,
                "atr_multiplier_tp": 6.0,
                "min_rr_ratio": 1.6,
                "max_rr_ratio": 3.5,
                "support_resistance_weight": 0.25,
                "volume_confirmation": False,
                "session_filter": False,
                "volatility_adjustment": True,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "asset_class": "cryptocurrency",
                "session": "24/7",
                "weight": 0.08,
                "risk_multiplier": 0.9,
                "explanation": "Bitcoin - Main crypto với auto selection"
            },
            
            "ETHUSD": {
                "preferred_strategy": "auto",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.020,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.8,
                "atr_multiplier_tp": 5.5,
                "min_rr_ratio": 1.6,
                "max_rr_ratio": 3.5,
                "support_resistance_weight": 0.25,
                "volume_confirmation": False,
                "session_filter": False,
                "volatility_adjustment": True,
                "confidence_threshold": 0.22,
                "force_strategy": False,
                "asset_class": "cryptocurrency",
                "session": "24/7",
                "weight": 0.07,
                "risk_multiplier": 0.9,
                "explanation": "Ethereum - Second crypto với momentum trending"
            },
            
            "XRPUSD": {
                "preferred_strategy": "ranging",
                "entry_method": "support_resistance",
                "trending_threshold": 0.025,
                "ranging_threshold": 0.018,
                "atr_multiplier_sl": 2.5,
                "atr_multiplier_tp": 4.5,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 3.0,
                "support_resistance_weight": 0.35,
                "volume_confirmation": False,
                "session_filter": False,
                "volatility_adjustment": True,
                "confidence_threshold": 0.24,
                "force_strategy": False,
                "asset_class": "cryptocurrency",
                "session": "24/7",
                "weight": 0.05,
                "risk_multiplier": 0.8,
                "explanation": "Ripple - Ranging strategy với support/resistance"
            },
            
            "LTCUSD": {
                "preferred_strategy": "trending",
                "entry_method": "trend_following",
                "trending threshhold": 0.015,
                "ranging_threshold": 0.028,
                "atr_multiplier_sl": 2.6,
                "atr_multiplier_tp": 5.2,
                "min_rr_ratio": 1.5,
                "max_rr_ratio": 3.2,
                "support_resistance_weight": 0.25,
                "volume_confirmation": False,
                "session_filter": False,
                "volatility_adjustment": True,
                "confidence_threshold": 0.21,
                "force_strategy": False,
                "asset_class": "cryptocurrency",
                "session": "24/7",
                "weight": 0.04,
                "risk_multiplier": 0.8,
                "explanation": "Litecoin - Trending strategy với trend following"
            },
            
            "ADAUSD": {
                "preferred_strategy": "auto",
                "entry_method": "volatility_breakout",
                "trending_threshold": 0.022,
                "ranging_threshold": 0.022,
                "atr_multiplier_sl": 2.8,
                "atr_multiplier_tp": 5.0,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 3.0,
                "support_resistance_weight": 0.25,
                "volume_confirmation": False,
                "session_filter": False,
                "volatility_adjustment": True,
                "confidence_threshold": 0.23,
                "force_strategy": False,
                "asset_class": "cryptocurrency",
                "session": "24/7",
                "weight": 0.03,
                "risk_multiplier": 0.7,
                "explanation": "Cardano - Balanced auto selection"
            }
        }
        
        # === COMMODITIES (Global Trading) ===
        commodities_configs = {
            "XAUUSD": {
                "preferred_strategy": "auto",
                "entry_method": "fibonacci_confluence",
                "trending_threshold": 0.020,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.5,
                "atr_multiplier_tp": 4.0,
                "min_rr_ratio": 1.6,
                "max_rr_ratio": 3.5,
                "support_resistance_weight": 0.4,
                "volume_confirmation": False,
                "session_filter": False,
                "volatility_adjustment": True,
                "fibonacci_levels": [0.236, 0.382, 0.5, 0.618, 0.786],
                "confidence_threshold": 0.19,
                "force_strategy": False,
                "asset_class": "commodity",
                "session": "23/5",
                "weight": 0.10,
                "risk_multiplier": 0.7,
                "explanation": "Gold - Safe haven asset với fibonacci confluence"
            },
            
            "XAGUSD": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.016,
                "ranging_threshold": 0.030,
                "atr_multiplier_sl": 2.8,
                "atr_multiplier_tp": 4.5,
                "min_rr_ratio": 1.5,
                "max_rr_ratio": 3.0,
                "support_resistance_weight": 0.3,
                "volume_confirmation": False,
                "session_filter": False,
                "volatility_adjustment": True,
                "confidence_threshold": 0.21,
                "force_strategy": False,
                "asset_class": "commodity",
                "session": "23/5",
                "weight": 0.03,
                "risk_multiplier": 0.6,
                "explanation": "Silver - Trending strategy với momentum"
            },
            
            "USOIL": {
                "preferred_strategy": "auto",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.018,
                "ranging_threshold": 0.028,
                "atr_multiplier_sl": 2.0,
                "atr_multiplier_tp": 3.5,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.8,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "asset_class": "commodity",
                "session": "23/5",
                "weight": 0.08,
                "risk_multiplier": 0.8,
                "explanation": "Crude Oil - Momentum trending với volume confirmation"
            },
            
            "UKOIL": {
                "preferred_strategy": "trending",
                "entry_method": "tremd_following",
                "trending_threshold": 0.015,
                "ranging_threshold": 0.032,
                "atr_multiplier_sl": 2.2,
                "atr_multiplier_tp": 3.8,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.6,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.22,
                "force_strategy": False,
                "asset_class": "commodity",
                "session": "23/5",
                "weight": 0.05,
                "risk_multiplier": 0.8,
                "explanation": "Brent Oil - Trending với trend following"
            },
            
            "NATGAS": {
                "preferred_strategy": "ranging",
                "entry_method": "support_resistance",
                "trending_threshold": 0.028,
                "ranging_threshold": 0.020,
                "atr_multiplier_sl": 3.0,
                "atr_multiplier_tp": 5.0,
                "min_rr_ratio": 1.6,
                "max_rr_ratio": 3.5,
                "support_resistance_weight": 0.35,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.23,
                "force_strategy": False,
                "asset_class": "commodity",
                "session": "23/5",
                "weight": 0.04,
                "risk_multiplier": 0.7,
                "explanation": "Natural Gas - Ranging với high volatility tolerance"
            }
        }
        
        # === FOREX MAJOR PAIRS ===
        forex_majors_configs = {
            "EURUSD": {
                "preferred_strategy": "auto",
                "entry_method": "trend_following",
                "trending_threshold": 0.018,
                "ranging_threshold": 0.028,
                "atr_multiplier_sl": 1.8,
                "atr_multiplier_tp": 2.8,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.8,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.18,
                "force_strategy": False,
                "asset_class": "forex",
                "session": "24/5",
                "weight": 0.08,
                "risk_multiplier": 0.6,
                "explanation": "EUR/USD - Major pair với trend following"
            },
            
            "GBPUSD": {
                "preferred_strategy": "ranging",
                "entry_method": "support_resistance",
                "trending_threshold": 0.025,
                "ranging_threshold": 0.018,
                "atr_multiplier_sl": 2.0,
                "atr_multiplier_tp": 3.0,
                "min_rr_ratio": 1.3,
                "max_rr_ratio": 2.6,
                "support_resistance_weight": 0.35,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "asset_class": "forex",
                "session": "24/5",
                "weight": 0.06,
                "risk_multiplier": 0.7,
                "explanation": "GBP/USD - Volatile pair với support/resistance"
            },
            
            "USDJPY": {
                "preferred_strategy": "auto",
                "entry_method": "trend_following",
                "trending_threshold": 0.020,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 1.5,
                "atr_multiplier_tp": 2.5,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.6,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.19,
                "force_strategy": False,
                "asset_class": "forex",
                "session": "24/5",
                "weight": 0.05,
                "risk_multiplier": 0.6,
                "explanation": "USD/JPY - Trend following với moderate volatility"
            }
        }
        
        # === FOREX MINOR PAIRS ===
        forex_minors_configs = {
            "AUDUSD": {
                "preferred_strategy": "auto",
                "entry_method": "trend_following",
                "trending_threshold": 0.020,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.0,
                "atr_multiplier_tp": 3.0,
                "min_rr_ratio": 1.3,
                "max_rr_ratio": 2.6,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.18,
                "force_strategy": False,
                "asset_class": "forex",
                "session": "24/5",
                "weight": 0.07,
                "risk_multiplier": 0.6,
                "explanation": "AUD/USD - Commodity currency với trend following"
            },
            
            "USDCAD": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.016,
                "ranging_threshold": 0.030,
                "atr_multiplier_sl": 1.8,
                "atr_multiplier_tp": 3.2,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.8,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "asset_class": "forex",
                "session": "24/5",
                "weight": 0.04,
                "risk_multiplier": 0.6,
                "explanation": "USD/CAD - Momentum trending với oil correlation"
            },
            
            "NZDUSD": {
                "preferred_strategy": "ranging",
                "entry_method": "support_resistance",
                "trending_threshold": 0.025,
                "ranging_threshold": 0.018,
                "atr_multiplier_sl": 2.2,
                "atr_multiplier_tp": 3.5,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 3.0,
                "support_resistance_weight": 0.30,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.22,
                "force_strategy": False,
                "asset_class": "forex",
                "session": "24/5",
                "weight": 0.03,
                "risk_multiplier": 0.7,
                "explanation": "NZD/USD - Volatile pair với support/resistance"
            }
        }
        
        # === FOREX CROSS PAIRS ===
        forex_cross_configs = {
            "EURGBP": {
                "preferred_strategy": "ranging",
                "entry_method": "range_bound",
                "trending_threshold": 0.028,
                "ranging_threshold": 0.015,
                "atr_multiplier_sl": 2.0,
                "atr_multiplier_tp": 3.0,
                "min_rr_ratio": 1.3,
                "max_rr_ratio": 2.6,
                "support_resistance_weight": 0.35,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.24,
                "force_strategy": False,
                "asset_class": "forex_cross",
                "session": "24/5",
                "weight": 0.02,
                "risk_multiplier": 0.5,
                "explanation": "EUR/GBP - Range-bound pair với low volatility"
            },
            
            "EURJPY": {
                "preferred_strategy": "trending",
                "entry_method": "trend_following",
                "trending_threshold": 0.015,
                "ranging_threshold": 0.030,
                "atr_multiplier_sl": 1.8,
                "atr_multiplier_tp": 3.2,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.8,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.18,
                "force_strategy": False,
                "asset_class": "forex_cross",
                "session": "24/5",
                "weight": 0.03,
                "risk_multiplier": 0.6,
                "explanation": "EUR/JPY - Trending với good liquidity"
            },
            
            "GBPJPY": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.012,
                "ranging_threshold": 0.032,
                "atr_multiplier_sl": 2.5,
                "atr_multiplier_tp": 4.0,
                "min_rr_ratio": 1.5,
                "max_rr_ratio": 3.0,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.22,
                "force_strategy": False,
                "asset_class": "forex_cross",
                "session": "24/5",
                "weight": 0.02,
                "risk_multiplier": 0.7,
                "explanation": "GBP/JPY - High volatility trending pair"
            },
            
            "AUDJPY": {
                "preferred_strategy": "auto",
                "entry_method": "trend_following",
                "trending_threshold": 0.020,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.0,
                "atr_multiplier_tp": 3.5,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.8,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "asset_class": "forex_cross",
                "session": "24/5",
                "weight": 0.02,
                "risk_multiplier": 0.6,
                "explanation": "AUD/JPY - Carry trade pair với auto selection"
            },
            
            "CADJPY": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.016,
                "ranging_threshold": 0.028,
                "atr_multiplier_sl": 2.2,
                "atr_multiplier_tp": 3.8,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.8,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.21,
                "force_strategy": False,
                "asset_class": "forex_cross",
                "session": "24/5",
                "weight": 0.015,
                "risk_multiplier": 0.6,
                "explanation": "CAD/JPY - Momentum với oil correlation"
            },
            
            "CHFJPY": {
                "preferred_strategy": "ranging",
                "entry_method": "support_resistance",
                "trending_threshold": 0.025,
                "ranging_threshold": 0.018,
                "atr_multiplier_sl": 1.8,
                "atr_multiplier_tp": 2.8,
                "min_rr_ratio": 1.3,
                "max_rr_ratio": 2.6,
                "support_resistance_weight": 0.35,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.23,
                "force_strategy": False,
                "asset_class": "forex_cross",
                "session": "24/5",
                "weight": 0.01,
                "risk_multiplier": 0.5,
                "explanation": "CHF/JPY - Safe haven ranges"
            },
            
            "EURCHF": {
                "preferred_strategy": "ranging",
                "entry_method": "range_bound",
                "trending_threshold": 0.030,
                "ranging_threshold": 0.015,
                "atr_multiplier_sl": 1.5,
                "atr_multiplier_tp": 2.5,
                "min_rr_ratio": 1.3,
                "max_rr_ratio": 2.6,
                "support_resistance_weight": 0.40,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.25,
                "force_strategy": False,
                "asset_class": "forex_cross",
                "session": "24/5",
                "weight": 0.01,
                "risk_multiplier": 0.4,
                "explanation": "EUR/CHF - Very low volatility ranging"
            },
            
            "GBPCHF": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.015,
                "ranging_threshold": 0.028,
                "atr_multiplier_sl": 2.8,
                "atr_multiplier_tp": 4.2,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 3.0,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.22,
                "force_strategy": False,
                "asset_class": "forex_cross",
                "session": "24/5",
                "weight": 0.01,
                "risk_multiplier": 0.7,
                "explanation": "GBP/CHF - Volatile trending pair"
            },
            
            "AUDNZD": {
                "preferred_strategy": "auto",
                "entry_method": "carry_trade",
                "trending_threshold": 0.020,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.5,
                "atr_multiplier_tp": 4.0,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 3.0,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "asset_class": "forex_exotic",
                "session": "24/5",
                "weight": 0.06,
                "risk_multiplier": 0.7,
                "explanation": "AUD/NZD - Carry trade pair với auto selection"
            },
            
            "USDCHF": {
                "preferred_strategy": "ranging",
                "entry_method": "support_resistance",
                "trending_threshold": 0.025,
                "ranging_threshold": 0.018,
                "atr_multiplier_sl": 1.8,
                "atr_multiplier_tp": 2.8,
                "min_rr_ratio": 1.3,
                "max_rr_ratio": 2.6,
                "support_resistance_weight": 0.35,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.22,
                "force_strategy": False,
                "asset_class": "forex",
                "session": "24/5",
                "weight": 0.03,
                "risk_multiplier": 0.5,
                "explanation": "USD/CHF - Safe haven ranging pair"
            }
        }
        
        # === EQUITY MAJORS (US Indices) ===
        equity_majors_configs = {
            "SPX500": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.016,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.0,
                "atr_multiplier_tp": 3.5,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.8,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.19,
                "force_strategy": False,
                "asset_class": "equity_index",
                "session": "23/5",
                "weight": 0.10,
                "risk_multiplier": 0.7,
                "explanation": "S&P 500 - Major US index với momentum trending"
            },
            
            "NAS100": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.017,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.2,
                "atr_multiplier_tp": 3.5,
                "min_rr_ratio": 1.6,
                "max_rr_ratio": 3.2,
                "support_resistance_weight": 0.32,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "asset_class": "equity_index",
                "session": "23/5",
                "weight": 0.08,
                "risk_multiplier": 0.8,
                "explanation": "Nasdaq 100 - Tech-heavy trending với volatility"
            },
            
            "US30": {
                "preferred_strategy": "auto",
                "entry_method": "trend_following",
                "trending_threshold": 0.018,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 1.8,
                "atr_multiplier_tp": 2.8,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.8,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.18,
                "force_strategy": False,
                "asset_class": "equity_index",
                "session": "23/5",
                "weight": 0.06,
                "risk_multiplier": 0.7,
                "explanation": "Dow Jones - Traditional index với trend following"
            }
        }
        
        # === EQUITY EUROPEAN ===
        equity_european_configs = {
            "DE40": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.016,
                "ranging_threshold": 0.028,
                "atr_multiplier_sl": 2.0,
                "atr_multiplier_tp": 3.2,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.8,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.19,
                "force_strategy": False,
                "asset_class": "equity_index",
                "session": "23/5",
                "weight": 0.07,
                "risk_multiplier": 0.7,
                "explanation": "DAX 40 - German equity trending"
            },
            
            "UK100": {
                "preferred_strategy": "ranging",
                "entry_method": "support_resistance",
                "trending_threshold": 0.025,
                "ranging_threshold": 0.018,
                "atr_multiplier_sl": 2.2,
                "atr_multiplier_tp": 3.5,
                "min_rr_ratio": 1.3,
                "max_rr_ratio": 2.6,
                "support_resistance_weight": 0.35,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.22,
                "force_strategy": False,
                "asset_class": "equity_index",
                "session": "23/5",
                "weight": 0.05,
                "risk_multiplier": 0.6,
                "explanation": "FTSE 100 - UK index với support/resistance"
            },
            
            "FR40": {
                "preferred_strategy": "auto",
                "entry_method": "trend_following",
                "trending_threshold": 0.020,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.0,
                "atr_multiplier_tp": 3.2,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.8,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "asset_class": "equity_index",
                "session": "23/5",
                "weight": 0.04,
                "risk_multiplier": 0.6,
                "explanation": "CAC 40 - French index auto selection"
            }
        }
        
        # === EQUITY ASIAN ===
        equity_asian_configs = {
            "JP225": {
                "preferred_strategy": "trending",
                "entry_method": "momentum_trending",
                "trending_threshold": 0.015,
                "ranging_threshold": 0.030,
                "atr_multiplier_sl": 2.2,
                "atr_multiplier_tp": 3.8,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.6,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.20,
                "force_strategy": False,
                "asset_class": "equity_index",
                "session": "23/5",
                "weight": 0.04,
                "risk_multiplier": 0.6,
                "explanation": "Nikkei 225 - Japanese equity trending"
            },
            
            "AU200": {
                "preferred_strategy": "auto",
                "entry_method": "trend_following",
                "trending_threshold": 0.020,
                "ranging_threshold": 0.025,
                "atr_multiplier_sl": 2.0,
                "atr_multiplier_tp": 3.2,
                "min_rr_ratio": 1.4,
                "max_rr_ratio": 2.8,
                "support_resistance_weight": 0.25,
                "volume_confirmation": True,
                "session_filter": True,
                "volatility_adjustment": True,
                "confidence_threshold": 0.21,
                "force_strategy": False,
                "asset_class": "equity_index",
                "session": "23/5",
                "weight": 0.03,
                "risk_multiplier": 0.6,
                "explanation": "ASX 200 - Australian equity auto selection"
            }
        }
        
        # === MERGE ALL CONFIGS ===
        config.update(crypto_configs)
        config.update(commodities_configs)
        config.update(forex_majors_configs)
        config.update(forex_minors_configs)
        config.update(forex_cross_configs)
        config.update(equity_majors_configs)
        config.update(equity_european_configs)
        config.update(equity_asian_configs)
        
        return config
    
    def generate_summary_report(self) -> str:
        """Generate comprehensive summary report"""
        
        config = self.get_comprehensive_symbol_config()
        categories = self.get_all_symbols_by_category()
        
        # Count strategies per category
        trending_count = sum(1 for c in config.values() if c.get('preferred_strategy') == 'trending')
        ranging_count = sum(1 for c in config.values() if c.get('preferred_strategy') == 'ranging')
        auto_count = sum(1 for c in config.values() if c.get('preferred_strategy') == 'auto')
        
        report = f"""
🎯 COMPREHENSIVE STRATEGY CONFIGURATION REPORT
==============================================
Version: {self.config_version}
Generated: {self.last_updated}
Total Symbols Configured: {len(config)}

📊 STRATEGY DISTRIBUTION:
- Trending Strategy: {trending_count} symbols ({trending_count/len(config)*100:.1f}%)
- Ranging Strategy: {ranging_count} symbols ({ranging_count/len(config)*100:.1f}%)
- Auto Selection: {auto_count} symbols ({auto_count/len(config)*100:.1f}%)

🏷️ SYMBOL CATEGORIES:
"""
        
        for category, symbols in categories.items():
            if category != "ACTIVE_SYMBOLS":
                active_count = sum(1 for s in symbols if s in config)
                report += f"- {category}: {active_count}/{len(symbols)} symbols configured\n"
        
        report += f"\n🔝 TOP ACTIVE SYMBOLS:\n"
        active_symbols = categories["ACTIVE_SYMBOLS"]
        for symbol in active_symbols:
            if symbol in config:
                conf = config[symbol]
                report += f"- {symbol}: {conf['preferred_strategy'].upper()} | {conf['entry_method']} | Weight: {conf['weight']}\n"
        
        report += f"""
⚙️ ENTRY METHODS DISTRIBUTION:
"""
        entry_methods = {}
        for conf in config.values():
            method = conf.get('entry_method', 'unknown')
            entry_methods[method] = entry_methods.get(method, 0) + 1
        
        for method, count in sorted(entry_methods.items()):
            report += f"- {method}: {count} symbols\n"
        
        return report
    
    def save_comprehensive_config(self, filename: str = "comprehensive_symbol_config.json") -> bool:
        """Save comprehensive config to JSON file"""
        try:
            data = {
                "meta": {
                    "version": self.config_version,
                    "created": self.last_updated,
                    "description": "Comprehensive strategy configuration for ALL trading symbols"
                },
                "symbol_categories": self.get_all_symbols_by_category(),
                "comprehensive_symbol_config": self.get_comprehensive_symbol_config(),
                "summary_report": self.generate_summary_report()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Comprehensive config saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False

def main():
    """Main function để demonstrate comprehensive config"""
    
    print("🚀 Comprehensive Symbol Strategy Configuration")
    print("=" * 60)
    
    config_manager = ComprehensiveSymbolConfig()
    
    # Generate và show summary
    print(config_manager.generate_summary_report())
    
    # Save config
    if config_manager.save_comprehensive_config():
        print("\n✅ Comprehensive config ready!")
        print("📁 File: comprehensive_symbol_config.json")
        print("📊 Covers ALL {total_symbols} trading symbols")
        print("\n🎯 Next steps:")
        print("1. Review config trong JSON file")
        print("2. Use integration tools để apply vào bot")
        print("3. Test với different symbol groups")
        print("4. Fine-tune individual symbols if needed")
    
    return config_manager

if __name__ == "__main__":
    main()