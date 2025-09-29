# Method này cần được thêm vào class EnhancedTradingBot trong file Google Drive của bạn

def get_dynamic_confidence_for_component(self, symbol, component, action="HOLD", market_data=None):
    """
    Get dynamic confidence for specific components (RL, Master Agent, Online Learning)
    """
    try:
        # Base confidence values by component
        base_confidences = {
            'rl': 0.45,
            'master_agent': 0.35,
            'online_learning': 0.4,
            'ensemble': 0.4
        }
        
        base_confidence = base_confidences.get(component, 0.4)
        
        # Apply symbol-specific adjustments
        if symbol in ['BTCUSD', 'ETHUSD']:
            # Major crypto pairs get higher confidence
            multipliers = {
                'rl': 1.0,          # Keep RL as is for major crypto
                'master_agent': 0.85, # Reduce master agent slightly
                'online_learning': 0.95, # Keep online learning high
                'ensemble': 0.9
            }
        elif symbol in ['XAUUSD']:
            # Gold gets moderate confidence
            multipliers = {
                'rl': 0.95,
                'master_agent': 0.9,
                'online_learning': 0.9,
                'ensemble': 0.9
            }
        elif symbol in EQUITY_INDICES:
            # Equity indices get lower confidence due to volatility
            multipliers = {
                'rl': 0.9,
                'master_agent': 0.8,
                'online_learning': 0.85,
                'ensemble': 0.85
            }
        else:
            # Other symbols get standard confidence
            multipliers = {
                'rl': 0.95,
                'master_agent': 0.85,
                'online_learning': 0.9,
                'ensemble': 0.9
            }
        
        # Apply component-specific multiplier
        confidence = base_confidence * multipliers.get(component, 0.9)
        
        # Market data adjustments
        if market_data is not None and not market_data.empty:
            try:
                # Check recent volatility
                if len(market_data) >= 20:
                    recent_returns = market_data['close'].pct_change().tail(20)
                    volatility = recent_returns.std()
                    
                    if volatility > 0.03:  # High volatility
                        confidence *= 0.9
                    elif volatility < 0.01:  # Low volatility
                        confidence *= 1.05
                
                # Check trend strength
                if len(market_data) >= 10:
                    recent_closes = market_data['close'].tail(10)
                    trend_strength = abs(recent_closes.iloc[-1] - recent_closes.iloc[0]) / recent_closes.iloc[0]
                    
                    if trend_strength > 0.02:  # Strong trend
                        confidence *= 1.05
                    elif trend_strength < 0.005:  # Weak trend
                        confidence *= 0.95
                        
            except Exception as e:
                logger.debug(f"Error in market data adjustments for {symbol}: {e}")
        
        # Action-specific adjustments
        if action in ['BUY', 'SELL']:
            confidence *= 1.02  # Slight boost for directional actions
        
        # Clamp between reasonable bounds
        return max(0.15, min(0.75, confidence))
        
    except Exception as e:
        logger.error(f"Error calculating dynamic confidence for {component} on {symbol}: {e}")
        return base_confidences.get(component, 0.4)