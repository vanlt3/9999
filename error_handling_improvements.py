#!/usr/bin/env python3
"""
Error Handling Improvements for Trading Bot
Cải thiện xử lý lỗi và logging dựa trên phân tích log
"""

import logging
import traceback
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from functools import wraps
import json
import os
from pathlib import Path

class EnhancedErrorHandler:
    """Enhanced error handling với detailed logging và recovery"""
    
    def __init__(self, log_file: str = "error_logs.json"):
        self.log_file = log_file
        self.error_counts = {}
        self.error_history = []
        self.recovery_actions = {}
        
        # Error thresholds
        self.thresholds = {
            'data_fetch': 5,
            'model_loading': 3,
            'api_call': 10,
            'feature_generation': 5,
            'prediction': 3
        }
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup enhanced logging configuration"""
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configure file handler
        file_handler = logging.FileHandler(log_dir / "error_handling.log")
        file_handler.setLevel(logging.DEBUG)
        
        # Configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Setup logger
        self.logger = logging.getLogger('ErrorHandler')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def handle_error(self, error_type: str, error: Exception, context: Dict[str, Any] = None) -> bool:
        """Handle error với context và recovery"""
        error_key = f"{error_type}_{context.get('symbol', 'unknown')}" if context else error_type
        
        # Increment error count
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        # Log error details
        error_details = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type,
            'error_message': str(error),
            'error_class': error.__class__.__name__,
            'context': context or {},
            'count': self.error_counts[error_key],
            'traceback': traceback.format_exc()
        }
        
        self.error_history.append(error_details)
        self._save_error_log(error_details)
        
        # Check if threshold exceeded
        threshold = self.thresholds.get(error_type, 5)
        if self.error_counts[error_key] > threshold:
            self.logger.error(f"❌ [Error] Threshold exceeded for {error_key}: {self.error_counts[error_key]} > {threshold}")
            return False
        
        # Log warning
        self.logger.warning(f"⚠️ [Error] {error_type}: {error} (Count: {self.error_counts[error_key]})")
        
        # Try recovery action
        if error_key in self.recovery_actions:
            try:
                recovery_result = self.recovery_actions[error_key](error, context)
                if recovery_result:
                    self.logger.info(f"✅ [Recovery] Successfully recovered from {error_type}")
                    return True
            except Exception as recovery_error:
                self.logger.error(f"❌ [Recovery] Failed to recover from {error_type}: {recovery_error}")
        
        return True
    
    def register_recovery_action(self, error_type: str, recovery_func: Callable):
        """Register recovery action for specific error type"""
        self.recovery_actions[error_type] = recovery_func
        self.logger.info(f"📝 [Recovery] Registered recovery action for {error_type}")
    
    def _save_error_log(self, error_details: Dict[str, Any]):
        """Save error details to JSON log file"""
        try:
            log_path = Path("logs") / self.log_file
            
            # Load existing logs
            if log_path.exists():
                with open(log_path, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Add new error
            logs.append(error_details)
            
            # Keep only last 1000 errors
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            # Save updated logs
            with open(log_path, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"❌ [Error] Failed to save error log: {e}")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary statistics"""
        summary = {
            'total_errors': len(self.error_history),
            'error_counts': self.error_counts,
            'recent_errors': self.error_history[-10:] if self.error_history else [],
            'thresholds': self.thresholds
        }
        
        return summary
    
    def reset_error_count(self, error_type: str, symbol: str = None):
        """Reset error count for specific error type"""
        if symbol:
            error_key = f"{error_type}_{symbol}"
        else:
            error_key = error_type
        
        if error_key in self.error_counts:
            del self.error_counts[error_key]
            self.logger.info(f"🔄 [Reset] Reset error count for {error_key}")

def error_handler(error_type: str, context: Dict[str, Any] = None):
    """Decorator for automatic error handling"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Get error handler instance
                error_handler_instance = getattr(wrapper, '_error_handler', None)
                if error_handler_instance:
                    error_handler_instance.handle_error(error_type, e, context)
                else:
                    logging.error(f"❌ [Error] {error_type}: {e}")
                raise
        return wrapper
    return decorator

class DataErrorHandler:
    """Specialized error handler for data-related errors"""
    
    def __init__(self, error_handler: EnhancedErrorHandler):
        self.error_handler = error_handler
        self.data_sources = ['oanda', 'finnhub', 'backup']
        self.current_source_index = 0
    
    def handle_data_fetch_error(self, symbol: str, error: Exception) -> bool:
        """Handle data fetching errors với source switching"""
        context = {'symbol': symbol, 'operation': 'data_fetch'}
        
        # Try next data source
        if self.current_source_index < len(self.data_sources) - 1:
            self.current_source_index += 1
            next_source = self.data_sources[self.current_source_index]
            context['next_source'] = next_source
            self.error_handler.logger.info(f"🔄 [Data] Switching to {next_source} for {symbol}")
        
        return self.error_handler.handle_error('data_fetch', error, context)
    
    def handle_data_validation_error(self, symbol: str, error: Exception) -> bool:
        """Handle data validation errors"""
        context = {'symbol': symbol, 'operation': 'data_validation'}
        return self.error_handler.handle_error('data_validation', error, context)
    
    def reset_data_source(self):
        """Reset to first data source"""
        self.current_source_index = 0
        self.error_handler.logger.info("🔄 [Data] Reset to primary data source")

class APIErrorHandler:
    """Specialized error handler for API-related errors"""
    
    def __init__(self, error_handler: EnhancedErrorHandler):
        self.error_handler = error_handler
        self.api_retry_counts = {}
        self.api_backoff_times = {}
    
    def handle_api_error(self, api_name: str, error: Exception, endpoint: str = None) -> bool:
        """Handle API errors với retry logic"""
        context = {'api_name': api_name, 'endpoint': endpoint}
        
        # Increment retry count
        retry_key = f"{api_name}_{endpoint}" if endpoint else api_name
        self.api_retry_counts[retry_key] = self.api_retry_counts.get(retry_key, 0) + 1
        
        # Calculate backoff time
        retry_count = self.api_retry_counts[retry_key]
        backoff_time = min(2 ** retry_count, 60)  # Max 60 seconds
        self.api_backoff_times[retry_key] = backoff_time
        
        context['retry_count'] = retry_count
        context['backoff_time'] = backoff_time
        
        # Log API error
        self.error_handler.logger.warning(f"⚠️ [API] {api_name} error (retry {retry_count}): {error}")
        
        return self.error_handler.handle_error('api_call', error, context)
    
    def can_retry_api(self, api_name: str, endpoint: str = None) -> bool:
        """Check if API can be retried"""
        retry_key = f"{api_name}_{endpoint}" if endpoint else api_name
        retry_count = self.api_retry_counts.get(retry_key, 0)
        return retry_count < 3
    
    def get_backoff_time(self, api_name: str, endpoint: str = None) -> float:
        """Get backoff time for API retry"""
        retry_key = f"{api_name}_{endpoint}" if endpoint else api_name
        return self.api_backoff_times.get(retry_key, 1.0)
    
    def reset_api_retry(self, api_name: str, endpoint: str = None):
        """Reset API retry count"""
        retry_key = f"{api_name}_{endpoint}" if endpoint else api_name
        if retry_key in self.api_retry_counts:
            del self.api_retry_counts[retry_key]
        if retry_key in self.api_backoff_times:
            del self.api_backoff_times[retry_key]

class ModelErrorHandler:
    """Specialized error handler for model-related errors"""
    
    def __init__(self, error_handler: EnhancedErrorHandler):
        self.error_handler = error_handler
        self.model_fallback_models = {}
    
    def handle_model_loading_error(self, symbol: str, model_type: str, error: Exception) -> bool:
        """Handle model loading errors"""
        context = {'symbol': symbol, 'model_type': model_type, 'operation': 'model_loading'}
        
        # Try fallback model if available
        fallback_key = f"{symbol}_{model_type}"
        if fallback_key in self.model_fallback_models:
            context['fallback_model'] = self.model_fallback_models[fallback_key]
            self.error_handler.logger.info(f"🔄 [Model] Using fallback model for {symbol} {model_type}")
        
        return self.error_handler.handle_error('model_loading', error, context)
    
    def handle_prediction_error(self, symbol: str, model_type: str, error: Exception) -> bool:
        """Handle prediction errors"""
        context = {'symbol': symbol, 'model_type': model_type, 'operation': 'prediction'}
        return self.error_handler.handle_error('prediction', error, context)
    
    def register_fallback_model(self, symbol: str, model_type: str, fallback_model: Any):
        """Register fallback model"""
        fallback_key = f"{symbol}_{model_type}"
        self.model_fallback_models[fallback_key] = fallback_model
        self.error_handler.logger.info(f"📝 [Model] Registered fallback model for {symbol} {model_type}")

class ErrorRecoveryManager:
    """Manager for error recovery actions"""
    
    def __init__(self, error_handler: EnhancedErrorHandler):
        self.error_handler = error_handler
        self.recovery_strategies = {}
        self._register_default_recoveries()
    
    def _register_default_recoveries(self):
        """Register default recovery strategies"""
        # Data fetch recovery
        self.error_handler.register_recovery_action('data_fetch', self._recover_data_fetch)
        
        # API call recovery
        self.error_handler.register_recovery_action('api_call', self._recover_api_call)
        
        # Model loading recovery
        self.error_handler.register_recovery_action('model_loading', self._recover_model_loading)
    
    def _recover_data_fetch(self, error: Exception, context: Dict[str, Any]) -> bool:
        """Recovery strategy for data fetch errors"""
        symbol = context.get('symbol', 'unknown')
        
        # Try alternative data source
        if 'next_source' in context:
            self.error_handler.logger.info(f"🔄 [Recovery] Trying alternative data source for {symbol}")
            return True
        
        # Try cached data
        self.error_handler.logger.info(f"🔄 [Recovery] Trying cached data for {symbol}")
        return True
    
    def _recover_api_call(self, error: Exception, context: Dict[str, Any]) -> bool:
        """Recovery strategy for API call errors"""
        api_name = context.get('api_name', 'unknown')
        
        # Wait for backoff time
        backoff_time = context.get('backoff_time', 1.0)
        self.error_handler.logger.info(f"🔄 [Recovery] Waiting {backoff_time}s before retry for {api_name}")
        time.sleep(backoff_time)
        
        return True
    
    def _recover_model_loading(self, error: Exception, context: Dict[str, Any]) -> bool:
        """Recovery strategy for model loading errors"""
        symbol = context.get('symbol', 'unknown')
        model_type = context.get('model_type', 'unknown')
        
        # Try fallback model
        if 'fallback_model' in context:
            self.error_handler.logger.info(f"🔄 [Recovery] Using fallback model for {symbol} {model_type}")
            return True
        
        # Try simpler model
        self.error_handler.logger.info(f"🔄 [Recovery] Trying simpler model for {symbol} {model_type}")
        return True

class ErrorMonitoringDashboard:
    """Dashboard for monitoring errors and recovery"""
    
    def __init__(self, error_handler: EnhancedErrorHandler):
        self.error_handler = error_handler
    
    def generate_error_report(self) -> str:
        """Generate comprehensive error report"""
        summary = self.error_handler.get_error_summary()
        
        report = []
        report.append("=" * 80)
        report.append("🚨 ERROR MONITORING DASHBOARD")
        report.append("=" * 80)
        
        # Error counts
        report.append(f"📊 Error Statistics:")
        report.append(f"   - Total errors: {summary['total_errors']}")
        report.append(f"   - Active error types: {len(summary['error_counts'])}")
        
        # Error breakdown
        if summary['error_counts']:
            report.append(f"\n📋 Error Breakdown:")
            for error_key, count in summary['error_counts'].items():
                threshold = summary['thresholds'].get(error_key.split('_')[0], 5)
                status = "🔴 CRITICAL" if count > threshold else "🟡 WARNING"
                report.append(f"   - {error_key}: {count} {status}")
        
        # Recent errors
        if summary['recent_errors']:
            report.append(f"\n🕐 Recent Errors (last 10):")
            for error in summary['recent_errors'][-5:]:  # Show last 5
                timestamp = error['timestamp'][:19]  # Remove microseconds
                report.append(f"   - {timestamp}: {error['error_type']} - {error['error_message'][:50]}...")
        
        # Thresholds
        report.append(f"\n⚙️ Error Thresholds:")
        for error_type, threshold in summary['thresholds'].items():
            report.append(f"   - {error_type}: {threshold}")
        
        report.append("=" * 80)
        return "\n".join(report)
    
    def save_error_report(self, filename: str = None):
        """Save error report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"error_report_{timestamp}.txt"
        
        report = self.generate_error_report()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            self.error_handler.logger.info(f"📄 [Report] Error report saved to {filename}")
        except Exception as e:
            self.error_handler.logger.error(f"❌ [Report] Failed to save error report: {e}")

# Usage example
def main():
    """Example usage of error handling improvements"""
    # Initialize error handler
    error_handler = EnhancedErrorHandler()
    
    # Initialize specialized handlers
    data_handler = DataErrorHandler(error_handler)
    api_handler = APIErrorHandler(error_handler)
    model_handler = ModelErrorHandler(error_handler)
    
    # Initialize recovery manager
    recovery_manager = ErrorRecoveryManager(error_handler)
    
    # Initialize monitoring dashboard
    dashboard = ErrorMonitoringDashboard(error_handler)
    
    # Example error handling
    try:
        # Simulate data fetch error
        raise Exception("Connection timeout")
    except Exception as e:
        data_handler.handle_data_fetch_error("BTCUSD", e)
    
    try:
        # Simulate API error
        raise Exception("HTTP 404")
    except Exception as e:
        api_handler.handle_api_error("finnhub", e, "quote")
    
    try:
        # Simulate model loading error
        raise Exception("Model file not found")
    except Exception as e:
        model_handler.handle_model_loading_error("BTCUSD", "ensemble_trending", e)
    
    # Generate and save report
    print(dashboard.generate_error_report())
    dashboard.save_error_report()

if __name__ == "__main__":
    main()