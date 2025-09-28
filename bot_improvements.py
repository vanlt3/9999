#!/usr/bin/env python3
"""
Bot Trading Improvements - Khắc phục các vấn đề từ log analysis
Các cải tiến chính:
1. Tối ưu hóa hiệu suất - giảm thời gian xử lý
2. Cải thiện xử lý dữ liệu - loại bỏ dummy data
3. Tăng cường API connectivity
4. Cải thiện error handling
5. Tối ưu hóa model loading
"""

import os
import sys
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import numpy as np
from functools import lru_cache
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

class BotPerformanceOptimizer:
    """Tối ưu hóa hiệu suất Bot Trading"""
    
    def __init__(self):
        self.model_cache = {}
        self.feature_cache = {}
        self.data_cache = {}
        self.api_cache = {}
        self.cache_ttl = 300  # 5 minutes
        
    def optimize_model_loading(self, symbol: str, model_type: str) -> Any:
        """Tối ưu hóa việc load model - cache models để tránh load lại"""
        cache_key = f"{symbol}_{model_type}"
        
        # Check cache first
        if cache_key in self.model_cache:
            cached_model, timestamp = self.model_cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                logging.info(f"🚀 [Cache] Using cached model for {symbol} {model_type}")
                return cached_model
        
        # Load model if not in cache
        try:
            # Simulate model loading
            model = self._load_model_from_disk(symbol, model_type)
            self.model_cache[cache_key] = (model, time.time())
            logging.info(f"📦 [Cache] Cached model for {symbol} {model_type}")
            return model
        except Exception as e:
            logging.error(f"❌ [Model] Failed to load {symbol} {model_type}: {e}")
            return None
    
    def _load_model_from_disk(self, symbol: str, model_type: str) -> Any:
        """Load model từ disk với error handling"""
        # Implementation would load actual model
        return f"model_{symbol}_{model_type}"
    
    def optimize_feature_engineering(self, df: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """Tối ưu hóa feature engineering - cache features"""
        cache_key = f"features_{symbol}_{hash(str(df.index[-1]))}"
        
        # Check cache
        if cache_key in self.feature_cache:
            cached_features, timestamp = self.feature_cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                logging.info(f"🚀 [Cache] Using cached features for {symbol}")
                return cached_features
        
        # Generate features
        try:
            features_df = self._generate_features(df, symbol)
            self.feature_cache[cache_key] = (features_df, time.time())
            logging.info(f"📦 [Cache] Cached features for {symbol}")
            return features_df
        except Exception as e:
            logging.error(f"❌ [Features] Failed to generate features for {symbol}: {e}")
            return df
    
    def _generate_features(self, df: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """Generate features với tối ưu hóa"""
        # Optimized feature generation
        if len(df) < 20:
            logging.warning(f"⚠️ [Features] Insufficient data for {symbol}: {len(df)} candles")
            return df
        
        # Add essential features only
        df = self._add_technical_indicators(df)
        df = self._add_market_state_features(df)
        
        return df
    
    def _add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add technical indicators efficiently"""
        try:
            # Simple moving averages
            df['sma_20'] = df['close'].rolling(20).mean()
            df['sma_50'] = df['close'].rolling(50).mean()
            
            # RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # ATR
            high_low = df['high'] - df['low']
            high_close = np.abs(df['high'] - df['close'].shift())
            low_close = np.abs(df['low'] - df['close'].shift())
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = np.max(ranges, axis=1)
            df['atr'] = true_range.rolling(14).mean()
            
        except Exception as e:
            logging.warning(f"⚠️ [Indicators] Error adding technical indicators: {e}")
        
        return df
    
    def _add_market_state_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add market state features efficiently"""
        try:
            # Trend detection
            df['trend'] = np.where(df['sma_20'] > df['sma_50'], 1, 
                                 np.where(df['sma_20'] < df['sma_50'], -1, 0))
            
            # Volatility
            df['volatility'] = df['atr'] / df['close']
            
            # Market regime
            df['market_regime'] = np.where(df['volatility'] > df['volatility'].rolling(20).quantile(0.8), 2,
                                         np.where(df['volatility'] < df['volatility'].rolling(20).quantile(0.2), 0, 1))
            
        except Exception as e:
            logging.warning(f"⚠️ [MarketState] Error adding market state features: {e}")
        
        return df

class DataQualityManager:
    """Quản lý chất lượng dữ liệu - loại bỏ dummy data"""
    
    def __init__(self):
        self.min_candles = 50
        self.data_sources = ['oanda', 'finnhub', 'backup']
    
    def validate_market_data(self, df: pd.DataFrame, symbol: str) -> Tuple[bool, str]:
        """Validate market data quality"""
        if df is None or df.empty:
            return False, "Empty dataframe"
        
        if len(df) < self.min_candles:
            return False, f"Insufficient data: {len(df)} < {self.min_candles}"
        
        # Check for required columns
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return False, f"Missing columns: {missing_cols}"
        
        # Check for data quality
        if df['close'].isna().sum() > len(df) * 0.1:  # More than 10% NaN
            return False, "Too many NaN values in close price"
        
        # Check for unrealistic values
        if (df['close'] <= 0).any():
            return False, "Invalid close prices (<= 0)"
        
        # Check for duplicate timestamps
        if df.index.duplicated().any():
            return False, "Duplicate timestamps found"
        
        return True, "Valid data"
    
    def get_reliable_data(self, symbol: str, timeframe: str = 'H1', count: int = 1000) -> Optional[pd.DataFrame]:
        """Lấy dữ liệu đáng tin cậy từ multiple sources"""
        for source in self.data_sources:
            try:
                df = self._fetch_from_source(symbol, timeframe, count, source)
                is_valid, message = self.validate_market_data(df, symbol)
                
                if is_valid:
                    logging.info(f"✅ [Data] Got valid data for {symbol} from {source}: {len(df)} candles")
                    return df
                else:
                    logging.warning(f"⚠️ [Data] {source} data invalid for {symbol}: {message}")
                    
            except Exception as e:
                logging.error(f"❌ [Data] Error fetching from {source} for {symbol}: {e}")
                continue
        
        logging.error(f"❌ [Data] All sources failed for {symbol}")
        return None
    
    def _fetch_from_source(self, symbol: str, timeframe: str, count: int, source: str) -> pd.DataFrame:
        """Fetch data from specific source"""
        # Implementation would connect to actual data source
        # For now, return None to indicate no data available
        return None

class APIConnectivityManager:
    """Quản lý kết nối API và xử lý lỗi"""
    
    def __init__(self):
        self.api_status = {}
        self.retry_config = {
            'max_retries': 3,
            'backoff_factor': 2,
            'timeout': 30
        }
    
    async def test_api_connectivity(self, api_name: str, test_url: str) -> bool:
        """Test API connectivity với retry logic"""
        if api_name in self.api_status:
            status, timestamp = self.api_status[api_name]
            if time.time() - timestamp < 300:  # 5 minutes cache
                return status
        
        for attempt in range(self.retry_config['max_retries']):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.retry_config['timeout'])) as session:
                    async with session.get(test_url) as response:
                        if response.status == 200:
                            self.api_status[api_name] = (True, time.time())
                            logging.info(f"✅ [API] {api_name} connected successfully")
                            return True
                        else:
                            logging.warning(f"⚠️ [API] {api_name} returned status {response.status}")
                            
            except Exception as e:
                logging.warning(f"⚠️ [API] {api_name} attempt {attempt + 1} failed: {e}")
                if attempt < self.retry_config['max_retries'] - 1:
                    await asyncio.sleep(self.retry_config['backoff_factor'] ** attempt)
        
        self.api_status[api_name] = (False, time.time())
        logging.error(f"❌ [API] {api_name} failed after {self.retry_config['max_retries']} attempts")
        return False
    
    def get_api_status(self, api_name: str) -> bool:
        """Get current API status"""
        if api_name in self.api_status:
            return self.api_status[api_name][0]
        return False

class ErrorHandlingManager:
    """Cải thiện xử lý lỗi và logging"""
    
    def __init__(self):
        self.error_counts = {}
        self.error_thresholds = {
            'data_fetch': 5,
            'model_loading': 3,
            'api_call': 10
        }
    
    def handle_data_error(self, symbol: str, error: Exception) -> bool:
        """Handle data fetching errors"""
        error_key = f"data_{symbol}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        if self.error_counts[error_key] > self.error_thresholds['data_fetch']:
            logging.error(f"❌ [Error] Too many data errors for {symbol}, disabling")
            return False
        
        logging.warning(f"⚠️ [Error] Data error for {symbol}: {error}")
        return True
    
    def handle_model_error(self, symbol: str, model_type: str, error: Exception) -> bool:
        """Handle model loading errors"""
        error_key = f"model_{symbol}_{model_type}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        if self.error_counts[error_key] > self.error_thresholds['model_loading']:
            logging.error(f"❌ [Error] Too many model errors for {symbol} {model_type}, disabling")
            return False
        
        logging.warning(f"⚠️ [Error] Model error for {symbol} {model_type}: {error}")
        return True
    
    def reset_error_count(self, error_key: str):
        """Reset error count for specific key"""
        if error_key in self.error_counts:
            del self.error_counts[error_key]

class BotOptimizer:
    """Main optimizer class combining all improvements"""
    
    def __init__(self):
        self.performance_optimizer = BotPerformanceOptimizer()
        self.data_manager = DataQualityManager()
        self.api_manager = APIConnectivityManager()
        self.error_manager = ErrorHandlingManager()
        
        # Configuration
        self.config = {
            'enable_caching': True,
            'enable_parallel_processing': True,
            'max_workers': 4,
            'cache_ttl': 300,
            'min_data_quality': 0.8
        }
    
    async def optimize_bot_startup(self) -> Dict[str, Any]:
        """Tối ưu hóa quá trình khởi động Bot"""
        start_time = time.time()
        results = {
            'success': True,
            'errors': [],
            'warnings': [],
            'optimizations': []
        }
        
        try:
            # 1. Test API connectivity
            logging.info("🔍 [Startup] Testing API connectivity...")
            api_tests = await self._test_all_apis()
            results['api_tests'] = api_tests
            
            # 2. Validate data sources
            logging.info("🔍 [Startup] Validating data sources...")
            data_validation = await self._validate_data_sources()
            results['data_validation'] = data_validation
            
            # 3. Pre-load critical models
            logging.info("🔍 [Startup] Pre-loading critical models...")
            model_loading = await self._preload_models()
            results['model_loading'] = model_loading
            
            # 4. Initialize caches
            logging.info("🔍 [Startup] Initializing caches...")
            self._initialize_caches()
            results['optimizations'].append("Caches initialized")
            
        except Exception as e:
            results['success'] = False
            results['errors'].append(f"Startup optimization failed: {e}")
            logging.error(f"❌ [Startup] Optimization failed: {e}")
        
        end_time = time.time()
        results['startup_time'] = end_time - start_time
        logging.info(f"✅ [Startup] Bot optimization completed in {results['startup_time']:.2f}s")
        
        return results
    
    async def _test_all_apis(self) -> Dict[str, bool]:
        """Test all API connections"""
        apis = {
            'finnhub': 'https://finnhub.io/api/v1/quote?symbol=AAPL&token=test',
            'newsapi': 'https://newsapi.org/v2/everything?q=bitcoin&apiKey=test',
            'trading_economics': 'https://api.tradingeconomics.com/markets/forecasts?c=test'
        }
        
        results = {}
        for api_name, test_url in apis.items():
            results[api_name] = await self.api_manager.test_api_connectivity(api_name, test_url)
        
        return results
    
    async def _validate_data_sources(self) -> Dict[str, Any]:
        """Validate data sources"""
        symbols = ['BTCUSD', 'ETHUSD', 'XAUUSD', 'USOIL', 'SPX500']
        results = {}
        
        for symbol in symbols:
            try:
                df = self.data_manager.get_reliable_data(symbol)
                if df is not None:
                    is_valid, message = self.data_manager.validate_market_data(df, symbol)
                    results[symbol] = {'valid': is_valid, 'message': message, 'candles': len(df)}
                else:
                    results[symbol] = {'valid': False, 'message': 'No data available', 'candles': 0}
            except Exception as e:
                results[symbol] = {'valid': False, 'message': str(e), 'candles': 0}
        
        return results
    
    async def _preload_models(self) -> Dict[str, Any]:
        """Pre-load critical models"""
        symbols = ['BTCUSD', 'ETHUSD']
        model_types = ['ensemble_trending', 'ensemble_ranging']
        results = {}
        
        for symbol in symbols:
            results[symbol] = {}
            for model_type in model_types:
                try:
                    model = self.performance_optimizer.optimize_model_loading(symbol, model_type)
                    results[symbol][model_type] = model is not None
                except Exception as e:
                    results[symbol][model_type] = False
                    logging.error(f"❌ [Model] Failed to preload {symbol} {model_type}: {e}")
        
        return results
    
    def _initialize_caches(self):
        """Initialize all caches"""
        if self.config['enable_caching']:
            # Initialize performance caches
            self.performance_optimizer.model_cache = {}
            self.performance_optimizer.feature_cache = {}
            self.performance_optimizer.data_cache = {}
            
            logging.info("✅ [Cache] All caches initialized")
    
    def get_optimization_report(self) -> str:
        """Generate optimization report"""
        report = []
        report.append("=" * 60)
        report.append("🤖 BOT OPTIMIZATION REPORT")
        report.append("=" * 60)
        
        # Performance metrics
        report.append(f"📊 Performance Optimizations:")
        report.append(f"   - Model caching: {'✅ Enabled' if self.config['enable_caching'] else '❌ Disabled'}")
        report.append(f"   - Parallel processing: {'✅ Enabled' if self.config['enable_parallel_processing'] else '❌ Disabled'}")
        report.append(f"   - Cache TTL: {self.config['cache_ttl']}s")
        
        # Data quality
        report.append(f"\n📈 Data Quality:")
        report.append(f"   - Min candles required: {self.data_manager.min_candles}")
        report.append(f"   - Data sources: {len(self.data_manager.data_sources)}")
        
        # API status
        report.append(f"\n🔌 API Connectivity:")
        for api_name, (status, timestamp) in self.api_manager.api_status.items():
            status_icon = "✅" if status else "❌"
            report.append(f"   - {api_name}: {status_icon}")
        
        # Error handling
        report.append(f"\n⚠️ Error Handling:")
        report.append(f"   - Active error counts: {len(self.error_manager.error_counts)}")
        
        report.append("=" * 60)
        return "\n".join(report)

# Usage example
async def main():
    """Main function to run optimizations"""
    optimizer = BotOptimizer()
    
    # Run startup optimization
    results = await optimizer.optimize_bot_startup()
    
    # Print results
    print(optimizer.get_optimization_report())
    
    # Print detailed results
    print(f"\n📋 Detailed Results:")
    print(f"   - Success: {results['success']}")
    print(f"   - Startup time: {results['startup_time']:.2f}s")
    print(f"   - Errors: {len(results['errors'])}")
    print(f"   - Warnings: {len(results['warnings'])}")
    print(f"   - Optimizations: {len(results['optimizations'])}")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Run optimization
    asyncio.run(main())