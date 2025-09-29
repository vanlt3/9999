# Bot Trading Method Fix

## Problem
The `EnhancedTradingBot` class is missing the `get_dynamic_confidence_for_component` method, causing the following error:

```
AttributeError: 'EnhancedTradingBot' object has no attribute 'get_dynamic_confidence_for_component'
```

## Solution
Run the fix script to automatically add the missing method to your bot file.

### Option 1: Automatic Fix (Recommended)
```bash
python fix_bot_method.py
```

### Option 2: Manual Fix
If the automatic fix doesn't work, manually add this method to your `EnhancedTradingBot` class:

1. Open your `Bot-Trading_Swing.py` file
2. Find the `EnhancedTradingBot` class
3. Add the `get_dynamic_confidence_for_component` method (see method code below)

## Method Code
```python
def get_dynamic_confidence_for_component(self, symbol, component, action="HOLD", market_data=None):
    """
    Get dynamic confidence for specific components<｜tool▁calls▁end｜>RL, Master Agent, Online Learning)
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
        EQUITY_INDICES = ['SPX500', 'NASDAQ', 'DOW30', 'UK100', 'GER30', 'FRA40', 'AUS200', 'JPN225']
        
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
        if market_data is not None and hasattr(market_data, 'empty') and not market_data.empty:
            try:
                import pandas as pd
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
                try:
                    logger.debug(f"Error in market data adjustments for {symbol}: {e}")
                except:
                    pass  # Logger might not be available
        
        # Action-specific adjustments
        if action in ['BUY', 'SELL']:
            confidence *= 1.02  # Slight boost for directional actions
        
        # Clamp between reasonable bounds
        return max(0.15, min(0.75, confidence))
        
    except Exception as e:
        try:
            logger.error(f"Error calculating dynamic confidence for {component} on {symbol}: {e}")
        except:
            print(f"Error calculating dynamic confidence for {component} on {symbol}: {e}")
        return base_confidences.get(component, 0.4)
```

## What This Method Does
This method calculates dynamic confidence scores for different trading components:

- **RL Strategy**: Reinforcement learning confidence
- **Master Agent**: Master agent confidence  
- **Online Learning**: Online learning confidence
- **Ensemble**: Combined approach confidence

It adjusts confidence based on:
- Symbol type (crypto, gold, indices)
- Market volatility
- Trend strength
- Action type (BUY/SELL vs HOLD)

## Files
- `fix_bot_method.py` - Automatic fix script
- `Bot-Trading_Swing.py` - Fixed working version (if needed)
- `missing_method_fix.py` - Original method definition

After applying the fix, your bot should run without the AttributeError.