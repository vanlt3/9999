#!/usr/bin/env python3
"""
Script để copy file bot đã fix vào Google Drive
"""

import os
import shutil

def copy_bot_to_drive():
    """Copy bot đã fix vào Google Drive"""
    
    # File nguồn (đã fix)
    source_file = "/workspace/Bot-Trading_Swing.py"
    
    # Các đường dẫn đích có thể
    target_paths = [
        "/content/drive/MyDrive/Bot/Bot-Trading_Swing.py",
        "/content/drive/.shortcut-targets-by-id/Bot/Bot-Trading_Swing.py",
        "/content/drive/MyDrive/Bot-Trading_Swing.py"
    ]
    
    print("🔧 ĐANG COPY BOT ĐÃ FIX VÀO GOOGLE DRIVE...")
    print("=" * 50)
    
    # Kiểm tra file nguồn
    if not os.path.exists(source_file):
        print(f"❌ File nguồn không tồn tại: {source_file}")
        return False
    
    print(f"✅ File nguồn: {source_file}")
    
    # Thử copy vào các đường dẫn có thể
    copied = False
    for target_path in target_paths:
        if os.path.exists(os.path.dirname(target_path)):
            try:
                # Tạo backup trước khi copy
                if os.path.exists(target_path):
                    backup_path = target_path + ".old_" + str(int(time.time()))
                    shutil.copy2(target_path, backup_path)
                    print(f"✅ Backup: {backup_path}")
                
                # Copy file mới
                shutil.copy2(source_file, target_path)
                print(f"✅ Đã copy vào: {target_path}")
                copied = True
                break
            except Exception as e:
                print(f"❌ Lỗi copy vào {target_path}: {e}")
                continue
        else:
            print(f"⚠️ Thư mục không tồn tại: {os.path.dirname(target_path)}")
    
    if not copied:
        print("❌ Không thể copy vào Google Drive")
        print("💡 Bạn có thể:")
        print("1. Tải file từ workspace về máy")
        print("2. Upload lên Google Drive thủ công")
        print("3. Hoặc chỉ cần lấy code method để thêm vào bot")
        return False
    
    print("\n🎉 COPY THÀNH CÔNG!")
    print("✅ Bot đã fix đã được copy vào Google Drive")
    print("🚀 Bây giờ bạn có thể restart bot!")
    
    return True

if __name__ == "__main__":
    import time
    copy_bot_to_drive()