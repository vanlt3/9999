# METHOD CẦN THÊM VÀO BOT CỦA BẠN
# Copy method này và thêm vào class EnhancedTradingBot trong bot của bạn

def get_dynamic_confidence_for_component(self, symbol, component, action="HOLD", market_data=None):
    """
    Tính toán confidence động cho các thành phần trading khác nhau (RL, Master Agent, Online Learning)
    """
    try:
        # Định nghĩa các chỉ số chứng khoán
        EQUITY_INDICES = ['SPX500', 'NASDAQ', 'DOW30', 'UK100', 'GER30', 'FRA40', 'AUS200', 'JPN225', 'NK225', 'HK50']
        
        # Giá trị confidence cơ bản cho từng component
        base_confidences = {
            'rl': 0.45,           # Reinforcement Learning
            'master_agent': 0.35, # Master Agent
            'online_learning': 0.4, # Online Learning
            'ensemble': 0.4       # Combined approach
        }
        
        base_confidence = base_confidences.get(component, 0.4)
        
        # Áp dụng điều chỉnh theo symbol cụ thể
        if symbol in ['BTCUSD', 'ETHUSD']:
            # Cặp crypto chính có confidence cao hơn
            multipliers = {
                'rl': 1.0,           # Giữ RL như cũ cho crypto chính
                'master_agent': 0.85, # Giảm master agent một chút
                'online_learning': 0.95, # Giữ online learning cao
                'ensemble': 0.9
            }
        elif symbol in ['XAUUSD']:
            # Vàng có confidence vừa phải
            multipliers = {
                'rl': 0.95,
                'master_agent': 0.9,
                'online_learning': 0.9,
                'ensemble': 0.9
            }
        elif symbol in EQUITY_INDICES:
            # Chỉ số cổ phiếu có confidence thấp hơn do độ biến động cao
            multipliers = {
                'rl': 0.9,
                'master_agent': 0.8,
                'online_learning': 0.85,
                'ensemble': 0.85
            }
        else:
            # Symbol khác có confidence chuẩn
            multipliers = {
                'rl': 0.95,
                'master_agent': 0.85,
                'online_learning': 0.9,
                'ensemble': 0.9
            }
        
        # Áp dụng multiplier theo thành phần
        confidence = base_confidence * multipliers.get(component, 0.9)
        
        # Điều chỉnh theo dữ liệu thị trường
        if market_data is not None:
            try:
                import pandas as pd
                
                # Kiểm tra xem market_data có phải DataFrame không
                if hasattr(market_data, 'empty') and not market_data.empty:
                    # Kiểm tra độ biến động gần đây
                    if len(market_data) >= 20 and 'close' in market_data.columns:
                        recent_returns = market_data['close'].pct_change().tail(20)
                        volatility = recent_returns.std()
                        
                        if volatility > 0.03:  # Biến động cao
                            confidence *= 0.9
                        elif volatility < 0.01:  # Biến động thấp
                            confidence *= 1.05
                    
                    # Kiểm tra sức mạnh xu hướng
                    if len(market_data) >= 10 and 'close' in market_data.columns:
                        recent_closes = market_data['close'].tail(10)
                        if len(recent_closes) >= 10:
                            trend_strength = abs(recent_closes.iloc[-1] - recent_closes.iloc[0]) / recent_closes.iloc[0]
                            
                            if trend_strength > 0.02:  # Xu hướng mạnh
                                confidence *= 1.05
                            elif trend_strength < 0.005:  # Xu hướng yếu
                                confidence *= 0.95
                                
            except Exception as e:
                try:
                    logger = logging.getLogger(__name__)
                    logger.debug(f"Lỗi phân tích market data cho {symbol}: {e}")
                except:
                    pass  # Logger không tìm thấy thì bỏ qua
        
        # Điều chỉnh theo hành động
        if action in ['BUY', 'SELL']:
            confidence *= 1.02  # Tăng nhẹ cho hành động có hướng
        
        # Giới hạn trong khoảng hợp lý
        return max(0.15, min(0.75, confidence))
        
    except Exception as e:
        try:
            logger = logging.getLogger(__name__)
            logger.error(f"Lỗi tính confidence cho {component} trên {symbol}: {e}")
        except:
            print(f"Lỗi tính confidence cho {component} trên {symbol}: {e}")
        return base_confidences.get(component, 0.4)

# HƯỚNG DẪN THÊM METHOD VÀO BOT:
# 1. Mở file Bot-Trading_Swing.py trong Google Drive
# 2. Tìm class EnhancedTradingBot
# 3. Tìm method cuối cùng trong class (trước khi có class khác)
# 4. Thêm method trên vào (không bao gồm dòng comment này)
# 5. Đảm bảo indentation đúng (phải cùng level với các method khác)
# 6. Lưu file và restart bot

print("""
🔧 HƯỚNG DẪN FIX BOT:

1. Copy method get_dynamic_confidence_for_component ở trên
2. Thêm vào class EnhancedTradingBot trong file Bot-Trading_Swing.py
3. Đặt ở cuối class (trước class khác)
4. Đảm bảo indentation đúng
5. Lưu file và restart bot

✅ Method này sẽ fix lỗi AttributeError: 'EnhancedTradingBot' object has no attribute 'get_dynamic_confidence_for_component'
""")