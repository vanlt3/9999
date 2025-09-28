#!/usr/bin/env python3
"""
API Connectivity Improvements for Trading Bot
Cải thiện kết nối API và xử lý lỗi kết nối dựa trên phân tích log
"""

import asyncio
import aiohttp
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json
from dataclasses import dataclass
from enum import Enum
import backoff
from functools import wraps

class APIStatus(Enum):
    """API status enumeration"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"

@dataclass
class APIEndpoint:
    """API endpoint configuration"""
    name: str
    base_url: str
    endpoints: Dict[str, str]
    api_key: Optional[str] = None
    rate_limit: int = 100  # requests per minute
    timeout: int = 30
    retry_count: int = 3
    backoff_factor: float = 2.0

class APIConnectivityManager:
    """Enhanced API connectivity manager với health monitoring"""
    
    def __init__(self):
        self.endpoints = {}
        self.health_status = {}
        self.rate_limiters = {}
        self.circuit_breakers = {}
        self.metrics = {}
        
        # Configuration
        self.config = {
            'health_check_interval': 300,  # 5 minutes
            'circuit_breaker_threshold': 5,
            'circuit_breaker_timeout': 600,  # 10 minutes
            'rate_limit_window': 60,  # 1 minute
            'max_concurrent_requests': 10
        }
        
        # Setup logging
        self.logger = logging.getLogger('APIConnectivity')
        self.logger.setLevel(logging.INFO)
        
        # Initialize default endpoints
        self._initialize_default_endpoints()
    
    def _initialize_default_endpoints(self):
        """Initialize default API endpoints"""
        # Finnhub API
        finnhub = APIEndpoint(
            name="finnhub",
            base_url="https://finnhub.io/api/v1",
            endpoints={
                "quote": "/quote",
                "news": "/company-news",
                "calendar": "/calendar/economic"
            },
            rate_limit=60,
            timeout=30
        )
        self.register_endpoint(finnhub)
        
        # NewsAPI
        newsapi = APIEndpoint(
            name="newsapi",
            base_url="https://newsapi.org/v2",
            endpoints={
                "everything": "/everything",
                "top_headlines": "/top-headlines"
            },
            rate_limit=1000,
            timeout=30
        )
        self.register_endpoint(newsapi)
        
        # Trading Economics
        trading_economics = APIEndpoint(
            name="trading_economics",
            base_url="https://api.tradingeconomics.com",
            endpoints={
                "forecasts": "/markets/forecasts",
                "calendar": "/calendar",
                "indicators": "/indicators"
            },
            rate_limit=120,
            timeout=30
        )
        self.register_endpoint(trading_economics)
        
        # EODHD API
        eodhd = APIEndpoint(
            name="eodhd",
            base_url="https://eodhd.com/api",
            endpoints={
                "real_time": "/real-time",
                "fundamentals": "/fundamentals",
                "news": "/news"
            },
            rate_limit=20,
            timeout=30
        )
        self.register_endpoint(eodhd)
    
    def register_endpoint(self, endpoint: APIEndpoint):
        """Register API endpoint"""
        self.endpoints[endpoint.name] = endpoint
        self.health_status[endpoint.name] = APIStatus.UNKNOWN
        self.rate_limiters[endpoint.name] = RateLimiter(endpoint.rate_limit, self.config['rate_limit_window'])
        self.circuit_breakers[endpoint.name] = CircuitBreaker(
            self.config['circuit_breaker_threshold'],
            self.config['circuit_breaker_timeout']
        )
        self.metrics[endpoint.name] = APIMetrics()
        
        self.logger.info(f"📝 [API] Registered endpoint: {endpoint.name}")
    
    async def test_connectivity(self, endpoint_name: str) -> Tuple[bool, str]:
        """Test API connectivity với comprehensive health check"""
        if endpoint_name not in self.endpoints:
            return False, f"Endpoint {endpoint_name} not registered"
        
        endpoint = self.endpoints[endpoint_name]
        metrics = self.metrics[endpoint_name]
        
        try:
            # Check circuit breaker
            if not self.circuit_breakers[endpoint_name].can_execute():
                self.logger.warning(f"⚠️ [API] {endpoint_name} circuit breaker is OPEN")
                return False, "Circuit breaker is open"
            
            # Check rate limit
            if not self.rate_limiters[endpoint_name].can_make_request():
                self.logger.warning(f"⚠️ [API] {endpoint_name} rate limit exceeded")
                return False, "Rate limit exceeded"
            
            # Perform health check
            start_time = time.time()
            success = await self._perform_health_check(endpoint)
            response_time = time.time() - start_time
            
            # Update metrics
            metrics.record_request(success, response_time)
            
            if success:
                self.health_status[endpoint_name] = APIStatus.HEALTHY
                self.circuit_breakers[endpoint_name].record_success()
                self.logger.info(f"✅ [API] {endpoint_name} health check passed ({response_time:.2f}s)")
                return True, f"Healthy ({response_time:.2f}s)"
            else:
                self.health_status[endpoint_name] = APIStatus.FAILED
                self.circuit_breakers[endpoint_name].record_failure()
                self.logger.warning(f"❌ [API] {endpoint_name} health check failed")
                return False, "Health check failed"
                
        except Exception as e:
            self.health_status[endpoint_name] = APIStatus.FAILED
            self.circuit_breakers[endpoint_name].record_failure()
            metrics.record_request(False, 0)
            self.logger.error(f"❌ [API] {endpoint_name} connectivity test error: {e}")
            return False, str(e)
    
    async def _perform_health_check(self, endpoint: APIEndpoint) -> bool:
        """Perform actual health check for endpoint"""
        try:
            # Use first available endpoint for health check
            health_endpoint = list(endpoint.endpoints.values())[0]
            url = f"{endpoint.base_url}{health_endpoint}"
            
            # Add API key if available
            params = {}
            if endpoint.api_key:
                params['token'] = endpoint.api_key
            
            # Add minimal test parameters
            if endpoint.name == "finnhub":
                params['symbol'] = 'AAPL'
            elif endpoint.name == "newsapi":
                params['q'] = 'bitcoin'
                params['pageSize'] = 1
            elif endpoint.name == "trading_economics":
                params['c'] = 'united states'
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=endpoint.timeout)) as session:
                async with session.get(url, params=params) as response:
                    # Consider 200, 201, 202 as success
                    # 404 might be acceptable for some APIs (endpoint exists but no data)
                    return response.status in [200, 201, 202, 404]
                    
        except Exception as e:
            self.logger.error(f"❌ [HealthCheck] Error for {endpoint.name}: {e}")
            return False
    
    async def make_request(self, endpoint_name: str, endpoint_path: str, params: Dict[str, Any] = None) -> Tuple[bool, Any]:
        """Make API request với error handling và retry logic"""
        if endpoint_name not in self.endpoints:
            return False, f"Endpoint {endpoint_name} not registered"
        
        endpoint = self.endpoints[endpoint_name]
        metrics = self.metrics[endpoint_name]
        
        # Check circuit breaker
        if not self.circuit_breakers[endpoint_name].can_execute():
            return False, "Circuit breaker is open"
        
        # Check rate limit
        if not self.rate_limiters[endpoint_name].can_make_request():
            return False, "Rate limit exceeded"
        
        # Build URL
        if endpoint_path not in endpoint.endpoints:
            return False, f"Endpoint path {endpoint_path} not found"
        
        url = f"{endpoint.base_url}{endpoint.endpoints[endpoint_path]}"
        
        # Add API key
        if params is None:
            params = {}
        if endpoint.api_key:
            params['token'] = endpoint.api_key
        
        # Make request with retry
        for attempt in range(endpoint.retry_count):
            try:
                start_time = time.time()
                
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=endpoint.timeout)) as session:
                    async with session.get(url, params=params) as response:
                        response_time = time.time() - start_time
                        
                        if response.status == 200:
                            data = await response.json()
                            metrics.record_request(True, response_time)
                            self.circuit_breakers[endpoint_name].record_success()
                            self.logger.info(f"✅ [API] {endpoint_name} request successful ({response_time:.2f}s)")
                            return True, data
                        else:
                            self.logger.warning(f"⚠️ [API] {endpoint_name} returned status {response.status}")
                            if response.status in [429, 503, 504]:  # Retryable errors
                                if attempt < endpoint.retry_count - 1:
                                    backoff_time = endpoint.backoff_factor ** attempt
                                    self.logger.info(f"🔄 [API] {endpoint_name} retrying in {backoff_time}s")
                                    await asyncio.sleep(backoff_time)
                                    continue
                            else:
                                metrics.record_request(False, response_time)
                                self.circuit_breakers[endpoint_name].record_failure()
                                return False, f"HTTP {response.status}"
                
            except asyncio.TimeoutError:
                self.logger.warning(f"⚠️ [API] {endpoint_name} timeout on attempt {attempt + 1}")
                if attempt < endpoint.retry_count - 1:
                    await asyncio.sleep(endpoint.backoff_factor ** attempt)
                    continue
                else:
                    metrics.record_request(False, 0)
                    self.circuit_breakers[endpoint_name].record_failure()
                    return False, "Timeout"
                    
            except Exception as e:
                self.logger.error(f"❌ [API] {endpoint_name} request error: {e}")
                if attempt < endpoint.retry_count - 1:
                    await asyncio.sleep(endpoint.backoff_factor ** attempt)
                    continue
                else:
                    metrics.record_request(False, 0)
                    self.circuit_breakers[endpoint_name].record_failure()
                    return False, str(e)
        
        return False, "Max retries exceeded"
    
    def get_health_status(self) -> Dict[str, str]:
        """Get health status of all endpoints"""
        return {name: status.value for name, status in self.health_status.items()}
    
    def get_metrics_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get metrics summary for all endpoints"""
        summary = {}
        for name, metrics in self.metrics.items():
            summary[name] = {
                'success_rate': metrics.get_success_rate(),
                'avg_response_time': metrics.get_avg_response_time(),
                'total_requests': metrics.total_requests,
                'failed_requests': metrics.failed_requests
            }
        return summary
    
    async def health_check_all(self) -> Dict[str, Tuple[bool, str]]:
        """Perform health check on all endpoints"""
        results = {}
        tasks = []
        
        for endpoint_name in self.endpoints.keys():
            task = asyncio.create_task(self.test_connectivity(endpoint_name))
            tasks.append((endpoint_name, task))
        
        for endpoint_name, task in tasks:
            try:
                success, message = await task
                results[endpoint_name] = (success, message)
            except Exception as e:
                results[endpoint_name] = (False, str(e))
        
        return results

class RateLimiter:
    """Rate limiter for API requests"""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
    
    def can_make_request(self) -> bool:
        """Check if request can be made within rate limit"""
        now = time.time()
        
        # Remove old requests outside window
        self.requests = [req_time for req_time in self.requests if now - req_time < self.window_seconds]
        
        # Check if under limit
        return len(self.requests) < self.max_requests
    
    def record_request(self):
        """Record a request"""
        self.requests.append(time.time())

class CircuitBreaker:
    """Circuit breaker pattern for API calls"""
    
    def __init__(self, failure_threshold: int, timeout_seconds: int):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def can_execute(self) -> bool:
        """Check if request can be executed"""
        if self.state == "CLOSED":
            return True
        elif self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout_seconds:
                self.state = "HALF_OPEN"
                return True
            return False
        elif self.state == "HALF_OPEN":
            return True
        return False
    
    def record_success(self):
        """Record successful request"""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def record_failure(self):
        """Record failed request"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

class APIMetrics:
    """Metrics tracking for API performance"""
    
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times = []
        self.last_reset = time.time()
    
    def record_request(self, success: bool, response_time: float):
        """Record API request metrics"""
        self.total_requests += 1
        
        if success:
            self.successful_requests += 1
            self.response_times.append(response_time)
        else:
            self.failed_requests += 1
        
        # Keep only last 100 response times
        if len(self.response_times) > 100:
            self.response_times = self.response_times[-100:]
    
    def get_success_rate(self) -> float:
        """Get success rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    def get_avg_response_time(self) -> float:
        """Get average response time"""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    def reset(self):
        """Reset metrics"""
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times = []
        self.last_reset = time.time()

class APIMonitoringDashboard:
    """Dashboard for monitoring API connectivity"""
    
    def __init__(self, api_manager: APIConnectivityManager):
        self.api_manager = api_manager
    
    def generate_status_report(self) -> str:
        """Generate comprehensive API status report"""
        health_status = self.api_manager.get_health_status()
        metrics = self.api_manager.get_metrics_summary()
        
        report = []
        report.append("=" * 80)
        report.append("🔌 API CONNECTIVITY DASHBOARD")
        report.append("=" * 80)
        
        # Health status
        report.append("📊 Health Status:")
        for endpoint, status in health_status.items():
            status_icon = "✅" if status == "healthy" else "❌" if status == "failed" else "⚠️"
            report.append(f"   - {endpoint}: {status_icon} {status.upper()}")
        
        # Metrics
        report.append("\n📈 Performance Metrics:")
        for endpoint, metric in metrics.items():
            success_rate = metric['success_rate']
            avg_time = metric['avg_response_time']
            total_requests = metric['total_requests']
            
            success_icon = "✅" if success_rate > 95 else "⚠️" if success_rate > 80 else "❌"
            time_icon = "✅" if avg_time < 2 else "⚠️" if avg_time < 5 else "❌"
            
            report.append(f"   - {endpoint}:")
            report.append(f"     • Success Rate: {success_icon} {success_rate:.1f}%")
            report.append(f"     • Avg Response Time: {time_icon} {avg_time:.2f}s")
            report.append(f"     • Total Requests: {total_requests}")
        
        # Circuit breakers
        report.append("\n🔧 Circuit Breakers:")
        for endpoint_name, circuit_breaker in self.api_manager.circuit_breakers.items():
            state_icon = "🟢" if circuit_breaker.state == "CLOSED" else "🔴" if circuit_breaker.state == "OPEN" else "🟡"
            report.append(f"   - {endpoint_name}: {state_icon} {circuit_breaker.state}")
            if circuit_breaker.state == "OPEN":
                time_remaining = circuit_breaker.timeout_seconds - (time.time() - circuit_breaker.last_failure_time)
                report.append(f"     • Time remaining: {max(0, time_remaining):.0f}s")
        
        report.append("=" * 80)
        return "\n".join(report)
    
    async def run_continuous_monitoring(self, interval: int = 300):
        """Run continuous API monitoring"""
        while True:
            try:
                # Perform health checks
                results = await self.api_manager.health_check_all()
                
                # Log results
                for endpoint, (success, message) in results.items():
                    if success:
                        self.api_manager.logger.info(f"✅ [Monitor] {endpoint}: {message}")
                    else:
                        self.api_manager.logger.warning(f"⚠️ [Monitor] {endpoint}: {message}")
                
                # Generate report
                report = self.generate_status_report()
                print(report)
                
                # Wait for next check
                await asyncio.sleep(interval)
                
            except Exception as e:
                self.api_manager.logger.error(f"❌ [Monitor] Error in continuous monitoring: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry

# Usage example
async def main():
    """Example usage of API connectivity improvements"""
    # Initialize API manager
    api_manager = APIConnectivityManager()
    
    # Initialize dashboard
    dashboard = APIMonitoringDashboard(api_manager)
    
    # Test connectivity
    print("🔍 Testing API connectivity...")
    results = await api_manager.health_check_all()
    
    for endpoint, (success, message) in results.items():
        status = "✅" if success else "❌"
        print(f"   {status} {endpoint}: {message}")
    
    # Make test requests
    print("\n📡 Making test requests...")
    
    # Test Finnhub
    success, data = await api_manager.make_request("finnhub", "quote", {"symbol": "AAPL"})
    if success:
        print(f"✅ Finnhub quote: {data}")
    else:
        print(f"❌ Finnhub error: {data}")
    
    # Test NewsAPI
    success, data = await api_manager.make_request("newsapi", "everything", {"q": "bitcoin", "pageSize": 1})
    if success:
        print(f"✅ NewsAPI: {len(data.get('articles', []))} articles")
    else:
        print(f"❌ NewsAPI error: {data}")
    
    # Generate status report
    print("\n" + dashboard.generate_status_report())
    
    # Run continuous monitoring for 1 minute
    print("\n🔄 Running continuous monitoring for 1 minute...")
    try:
        await asyncio.wait_for(dashboard.run_continuous_monitoring(10), timeout=60)
    except asyncio.TimeoutError:
        print("⏰ Monitoring completed")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run example
    asyncio.run(main())