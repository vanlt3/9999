# Copy code này vào Google Colab và chạy để fix bot của bạn
# ==========================================================

print("🔧 BẮT ĐẦU FIX BOT TRADING...")
print("=" * 50)

import os
import shutil
from datetime import datetime

# 1. Tìm file bot
bot_path = "/content/drive/MyDrive/Bot/Bot-Trading_Swing.py"

if not os.path.exists(bot_path):
    print("❌ Không tìm thấy file bot tại:", bot_path)
    print("Hãy kiểm tra đường dẫn chính xác")
    exit()

print(f"✅ Tìm thấy file bot: {bot_path}")

# 2. Đọc và kiểm tra file
print("📖 Đang đọc file bot...")
try:
    with open(bot_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print("✅ Đọc file thành công!")
except Exception as e:
    print(f"❌ Lỗi đọc file: {e}")
    exit()

# 3. Kiểm tra xem method đã tồn tại chưa
if 'def get_dynamic_confidence_for_component(' in content:
    print("✅ Method get_dynamic_confidence_for_component đã có sẵn!")
    print("🎉 Bot của bạn đã được fix rồi!")
    exit()

print("🔧 Cần thêm method vào bot...")

# 4. Tạo backup
backup_path = bot_path + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
try:
    shutil.copy2(bot_path, backup_path)
    print(f"✅ Backup thành công: {backup_path}")
except Exception as e:
    print(f"❌ Lỗi tạo backup: {e}")
    exit()

# 5. Code method cần thêm
method_code = '''
    def get_dynamic_confidence_for_component(self, symbol, component, action="HOLD", market_data=None):
        """Tính toán confidence động cho các thành phần trading khác nhau"""
        try:
            EQUITY_INDICES = ['SPX500', 'NASDAQ', 'DOW30', 'UK100', 'GER30', 'FRA40', 'AUS200', 'JPN225']
            
            base_confidences = {
                'rl': 0.45,
                'master_agent': 0.35,
                'online_learning': 0.4,
                'ensemble': 0.4
            }
            
            base_confidence = base_confidences.get(component, 0.4)
            
            if symbol in ['BTCUSD', 'ETHUSD']:
                multipliers = {
                    'rl': 1.0,
                    'master_agent': 0.85,
                    'online_learning': 0.95,
                    'ensemble': 0.9
                }
            elif symbol in ['XAUUSD']:
                multipliers = {
                    'rl': 0.95,
                    'master_agent': 0.9,
                    'online_learning': 0.9,
                    'ensemble': 0.9
                }
            elif symbol in EQUITY_INDICES:
                multipliers = {
                    'rl': 0.9,
                    'master_agent': 0.8,
                    'online_learning': 0.85,
                    'ensemble': 0.85
                }
            else:
                multipliers = {
                    'rl': 0.95,
                    'master_agent': 0.85,
                    'online_learning': 0.9,
                    'ensemble': 0.9
                }
            
            confidence = base_confidence * multipliers.get(component, 0.9)
            
            if market_data is not None:
                try:
                    if hasattr(market_data, 'empty') and not market_data.empty and 'close' in market_data.columns:
                        if len(market_data) >= 20:
                            returns = market_data['close'].pct_change().tail(20)
                            vol = returns.std()
                            if vol > 0.03:
                                confidence *= 0.9
                            elif vol < 0.01:
                                confidence *= 1.05
                        
                        if len(market_data) >= 10:
                            closes = market_data['close'].tail(10)
                            if len(closes) >= 10:
                                trend = abs(closes.iloc[-1] - closes.iloc[0]) / closes.iloc[0]
                                if trend > 0.02:
                                    confidence *= 1.05
                                elif trend < 0.005:
                                    confidence *= 0.95
                except:
                    pass
            
            if action in ['BUY', 'SELL']:
                confidence *= 1.02
            
            return max(0.15, min(0.75, confidence))
            
        except Exception as e:
            return base_confidences.get(component, 0.4)
'''

# 6. Tìm vị trí chèn method
lines = content.split('\n')
insertion_point = -1
class_found = False

for i, line in enumerate(lines):
    if 'class EnhancedTradingBot:' in line:
        class_found = True
        print("✅ Tìm thấy class EnhancedTradingBot")
        
        # Tìm method cuối cùng trong class
        class_indent = len(line) - len(line.lstrip())
        
        # Tìm method cuối cùng
        last_method_line = -1
        for j in range(i+1, len(lines)):
            current_line = lines[j]
            if current_line.strip():  # Không phải dòng trống
                current_indent = len(current_line) - len(current_line.lstrip())
                
                # Nếu indent <= class_indent và không phải 'def'
                if current_indent <= class_indent and not current_line.strip().startswith('def '):
                    insertion_point = j  # Chèn trước dòng này
                    break
                
                # Tìm method definition
                if current_line.strip().startswith('def '):
                    last_method_line = j
        
        # Nếu không tìm thấy điểm kết thúc class, chèn ở cuối file
        if insertion_point == -1:
            insertion_point = len(lines)
        
        break

if not class_found:
    print("❌ Không tìm thấy class EnhancedTradingBot")
    exit()

if insertion_point == -1:
    print("❌ Không tìm được vị trí chèn method")
    exit()

print(f"✅ Sẽ chèn method tại dòng {insertion_point}")

# 7. Chèn method
method_lines = method_code.strip().split('\n')

# Thêm dòng trống trước method
lines.insert(insertion_point, '')
insertion_point += 1

# Chèn method
for i, method_line in enumerate(method_lines):
    lines.insert(insertion_point + i, method_line)

# Thêm dòng trống sau method
lines.insert(insertion_point + len(method_lines), '')

print("✅ Đã chuẩn bị nội dung để chèn")

# 8. Ghi file mới
try:
    new_content = '\n'.join(lines)
    print("✅ Đã tạo nội dung mới")
    
    with open(bot_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Đã ghi file mới thành công!")
    
except Exception as e:
    print(f"❌ Lỗi ghi file: {e}")
    exit()

# 9. Kiểm tra syntax
print("🔍 Kiểm tra syntax...")
try:
    compile(new_content, bot_path, 'exec')
    print("✅ Syntax hợp lệ!")
except SyntaxError as e:
    print(f"❌ Lỗi syntax: {e}")
    print("🔄 Đang khôi phục từ backup...")
    
    try:
        with open(backup_path, 'r', encoding='utf-8') as f:
            with open(bot_path, 'w', encoding='utf-8') as g:
                g.write(f.read())
        print("✅ Đã khôi phục từ backup")
    except Exception as restore_e:
        print(f"❌ Lỗi khôi phục: {restore_e}")
    
    exit()

# 10. Kiểm tra lại method đã được thêm chưa
print("🔍 Kiểm tra method đã được thêm...")
try:
    with open(bot_path, 'r', encoding='utf-8') as f:
        final_content = f.read()
    
    if 'def get_dynamic_confidence_for_component(' in final_content:
        print("✅ Method đã được thêm thành công!")
    else:
        print("❌ Method không được thêm vào")
        exit()

except Exception as e:
    print(f"❌ Lỗi kiểm tra cuối: {e}")
    exit()

# 11. Hoàn thành
print("\n" + "=" * 50)
print("🎉 FIX HOÀN THÀNH THÀNH CÔNG!")
print("=" * 50)
print("✅ Method get_dynamic_confidence_for_component đã được thêm vào")
print("✅ Backup file được tạo:", backup_path)
print("✅ Syntax đã được kiểm tra và hợp lệ")
print("\n🚀 BỐ BÂY GIỜ CÓ THỂ:")
print("1. Restart bot trading của bạn")
print("2. Chạy lại quá trình RL strategy")
print("3. Sẽ không còn lỗi AttributeError nữa!")
print("\n💡 Tips:")
print("- Nếu có lỗi gì, file backup sẽ giúp bạn restore")
print("- Method này tính confidence cho RL, Master Agent, Online Learning")
print("- Confidence được điều chỉnh theo symbol và market conditions")

print("\n🔧 HOÀN TẤT FIX BOT!")