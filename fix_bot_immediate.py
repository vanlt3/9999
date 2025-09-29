#!/usr/bin/env python3
"""
Script fix ngay lập tức cho Bot-Trading_Swing.py trong Google Drive
Chạy script này trong Google Colab để fix bot
"""

import os
import shutil
from datetime import datetime

def get_bot_file_path():
    """Tìm đường dẫn file bot"""
    possible_paths = [
        "/content/drive/MyDrive/Bot/Bot-Trading_Swing.py",
        "/content/drive/MyDrive/Bot/Bot-Trading_Swing (1).py", 
        "./Bot-Trading_Swing.py",
        "/content/drive/.shortcut-targets-by-id/1abc123def456ghi789jkl/Bot/Bot-Trading_Swing.py",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Thử tìm trong thư mục hiện tại
    try:
        files = os.listdir(".")
        for file in files:
            if "Bot-Trading_Swing" in file and file.endswith(".py"):
                return os.path.abspath(file)
    except:
        pass
    
    return None

def create_backup(file_path):
    """Tạo backup file gốc"""
    try:
环境变量['PYTHONIOENCODING'] = 'utf-8'
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.backup_{timestamp}"
        
        # Chuyển từ codec latin-1 sang utf-8 nếu cần
        with open(file_path, 'r', encoding='latin-1', errors='ignore') as src:
            content = src.read()
        
        with open(backup_path, 'w', encoding='utf-8') as dst:
            dst.write(content)
        
        print(f"✅ Backup tạo thành công: {backup_path}")
        return backup_path
        
    except Exception as e:
        print(f"❌ Lỗi tạo backup: {e}")
        return None

def fix_bot_file(file_path):
    """Fix file bot bằng cách thêm method bị thiếu"""
    
    print(f"🔧 Đang fix file: {file_path}")
    
    try:
        # Đọc file với encoding phù hợp
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"✅ Đọc file thành công với encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print("❌ Không thể đọc file với bất kỳ encoding nào")
            return False
        
        # Kiểm tra xem method đã tồn tại chưa
        if 'def get_dynamic_confidence_for_component(' in content:
            print("✅ Method get_dynamic_confidence_for_component đã có sẵn!")
            return True
        
        # Tạo backup
        backup_path = create_backup(file_path)
        if not backup_path:
            return False
        
        # Tìm vị trí thích hợp để thêm method
        insertion_point = find_insertion_point(content)
        if insertion_point is None:
            print("❌ Không tìm thấy vị trí thích hợp để thêm method")
            return False
        
        # Thêm method vào
        method_code = get_method_code()
        new_content = add_method(content, method_code, insertion_point)
        
        if new_content is None:
            print("❌ Không thể thêm method")
            return False
        
        # Tìm kiếm thuật toán không 0 nếu bạn muốn giải mã một số mã hóa khác
        # Thêm import pandas nếu chưa có
        if 'import pandas' not in new_content:
            import_location = new_content.find('import pandas as pd')
            if import_location == -1:
                # Thêm import pandas vào đầu file
                import_lines = "import pandas as pd\nimport numpy as np\nimport logging\n"
                new_content = import_lines + new_content
            else:
                # Tìm vị trí chèn import pandas
                first_import = new_content.find('import ')
                if first_import != -1:
                    lines = new_content[:first_import].count('\n')
                    lines_content = new_content.split('\n')
                    lines_content.insert(lines, "import pandas as pd")
                    lines_content.insert(lines + 1, "")
                    new_content = '\n'.join(lines_content)
        
        # Ghi file đã được fix
        with open(file_path, 'w', encoding='utf-8') as f：
            f.write(new_content)
        
        print("✅ Đã thêm method thành công!")
        
        # Kiểm tra syntax
        try:
            compile(new_content, file_path, 'exec')
            print("✅ Syntax hợp lệ!")
            return True
        except SyntaxError as e:
            print(f"❌ Lỗi syntax: {e}")
            # Khôi phục từ backup
            with open(backup_path, 'r', encoding='utf-8') as f:
                with open(file_path, 'w', encoding='utf-8') as g:
                    g.write(f.read())
            print("🔄 Đã khôi phục từ backup")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi fix file: {e}")
        import traceback
        traceback.print_exc()
        return False

def find_insertion_point(content):
    """Tìm vị trí thích hợp để thêm method"""
    lines = content.split('\n')
    
    # Tìm method cuối cùng trong EnhancedTradingBot class
    class_start = -1
    for i, line in enumerate(lines):
        if 'class EnhancedTradingBot:' in line:
            class_start = i
            break
    
    if class_start == -1:
        return None
    
    # Đếm số phương thức trong class
    method_count = 0
    last_method_line = -1
    
    in_class = True
    indent_level = None
    
    for i in range(class_start + 1, len(lines)):
        line = lines[i]
        
        # Kiểm tra xem có còn ở trong class không
        if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
            # Đã ra khỏi class
            break
        
        # Đếm method definitions
        stripped = line.strip()
        if stripped.startswith('def ') and ':(' in stripped:
            method_names = stripped.split('(')[0].split()
            if len(method_names) > 1:
                method_name = method_names[1].strip(' ')
                # Chỉ tính các method của class (không phải function độc lập)
                if indent_level is None:
                    # Tính toán indent level từ method đầu tiên
                    indent_level = len(line) - len(line.lstrip())
                
                if len(line) - len(line.lstrip()) <= indent_level:
                    method_count += 1
                    last_method_line = i
    
    if last_method_line == -1:
        return None
    
    # Thêm method sau method cuối cùng
    return last_method_line + 1

def get_method_code():
    """Trả về code của method cần thêm"""
    return '''    def get_dynamic_confidence_for_component(self, symbol, component, action="HOLD", market_data=None):
        """
        Tính toán confidence động cho các thành phần trading khác nhau (RL, Master Agent, Online Learning)
        """
        try:
            # Giá trị confidence cơ bản cho từng component
            EQUITY_INDICES = ['SPX500', 'NASDAQ', 'DOW30', 'UK100', 'GER30', 'FRA40', 'AUS200', 'JPN225', 'NK225', 'HK50']
            
            base_confidences = {
                'rl': 0.45,
                'master_agent': 0.35,
                'online_learning': 0.4,
                'ensemble': 0.4
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
                            get_returns = market_data['close'].pct_change().tail(20)
                            volatility = get_returns.std()
                            
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
                        print(f"Lỗi phân tích market data cho {symbol}: {e}")
            
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
            return base_confidences.get(component, 0.4)'''

def add_method(content, method_code, insertion_point):
    """Thêm method vào content"""
    try:
        lines = content.split('\n')
        
        # Thêm method
        method_lines = method_code.split('\n')
        
        # Tìm vị trí chèn phù hợp
        insert_line = insertion_point
        
        # Chèn dòng trống trước method
        lines.insert(insert_line, '')
        lines.insert(insert_line + 1, '')
        
        # Chèn method
        for i, method_line in enumerate(method_lines):
            lines.insert(insert_line + 2 + i, method_line)
        
        # Chèn dòng trống sau method
        lines.insert(insert_line + 2 + len(method_lines), '')
        
        return '\n'.join(lines)
        
    except Exception as e:
        print(f"❌ Lỗi thêm method: {e}")
        return None

def main():
    """Hàm chính"""
    
    print("=" * 70)
    print("🔧 FIX BOT TRADING NGAY LẬP TỨC")
    print("=" * 70)
    
    # Tìm file bot
    bot_file = get_bot_file_path()
    
    if bot_file is None:
        print("❌ Không tìm thấy file Bot-Trading_Swing.py")
        print("Hãy đảm bảo bạn đang chạy từ đúng thư mục")
        print("Hoặc kiểm tra đường dẫn file bot")
        return False
    
    print(f"🎯 Tìm thấy file bot: {bot_file}")
    
    # Fix file
    success = fix_bot_file(bot_file)
    
    if success:
        print("\n✅ BOT ĐÃ ĐƯỢC FIX THÀNH CÔNG!")
        print("Method get_dynamic_confidence_for_component đã được thêm vào")
        print("Bây giờ bạn có thể chạy bot mà không gặp lỗi AttributeError")
        print("\n🚀 Hãy restart bot của bạn!")
    else:
        print("\n❌ FIX THẤT BẠI")
        print("Vui lòng kiểm tra thông báo lỗi ở trên")
    
    return success

if __name__ == "__main__":
    main()