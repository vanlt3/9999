# 🎯 Strategy Configuration Files

## 📁 Các Files Đã Tạo:

### 1. **`strategy_config_updater.py`** - File cấu hình chính
- Chứa tất cả config để điều chỉnh strategy selection
- Có thể chỉnh sửa thresholds, entry methods, confidence levels
- Generate config summary và save ra JSON

### 2. **`strategy_examples.py`** - Các ví dụ config sẵn
- **TRENDING BIASED**: Bot chọn trending nhiều nhất
- **RANGING BIASED**: Bot chọn ranging nhiều nhất  
- **BALANCED**: Bot tự động cân bằng
- **AGGRESSIVE**: Nhiều trading opportunities
- **CONSERVATIVE**: Ít trading nhưng chất lượng cao

### 3. **`config_integration.py`** - Tool để kết nối với bot chính
- Tạo patch files để apply vào bot
- Auto backup trước khi thay đổi
- Status checking

### 4. **`strategy_patch_[mode].py`** - Patch files để apply
- Copy-paste ready configurations
- Detailed instructions để integrate

---

## 🚀 Cách Sử Dụng:

### **Bước 1: Chọn Strategy Mode**
```bash
# Xem tất cả examples
python3 strategy_examples.py

# Apply balanced mode (recommended)
python3 -c "from strategy_examples import apply_config_example; apply_config_example('balanced')"
```

### **Bước 2: Tạo Patch File**
```bash
# Chạy integration tool
python3 config_integration.py

# Hoặc tạo patch cụ thể
python3 -c "from config_integration import BotConfigIntegration; BotConfigIntegration().create_patch_file('trending')"
```

### **Bước 3: Apply vào Bot**
1. **BACKUP** file `Bot-Trading_Swing (1).py` trước!
2. Mở patch file (ví dụ: `strategy_patch_trending.py`)
3. Copy config mới vào bot file
4. Restart bot

---

## ⚙️ **Các Tham Số Chính:**

### **Strategy Selection Parameters:**
```python
"BTCUSD": {
    "preferred_strategy": "auto",        # "trending"/"ranging"/"auto"
    "trending_threshold": 0.018,        # Nhỏ = dễ trending hơn
    "ranging_threshold": 0.025,         # Lớn = khó ranging hơn
    "confidence_threshold": 0.19,       # Min confidence để trade
    "force_strategy": False             # Force strategy hay không
}
```

### **Entry Method Mapping:**
```python
TRENDING_METHODS = [
    "momentum_trending",      # Trending biased
    "trend_following",        # Trending biased  
    "volatility_breakout"     # Trending biased
]

RANGING_METHODS = [
    "fibonacci_confluence",   # Ranging biased
    "support_resistance",     # Ranging biased
    "range_bound"             # Ranging biased
]
```

### **Global Settings:**
```python
GLOBAL_CONFIG = {
    "GLOBAL_TREND_PREFERENCE": "auto",      # "trending"/"ranging"/"auto"
    "MIN_TREND_CONFIDENCE": 0.18,          # Global confidence threshold
    "MAX_VOLATILITY_TREND": 2.5,           # Max volatility cho trending
    "PERFORMANCE_BASED_SELECTION": True    # Auto-adjust based on performance
}
```

---

## 📊 **Quy Tắc Quyết Định:**

### **Bot chọn TRENDING khi:**
- `trend_strength >= trending_threshold`
- `volatility < max_volatility_trend`
- `volume_confirmation == True`
- SMA alignment: `Price > SMA20 > SMA50` (bullish) hoặc ngược lại (bearish)
- `confidence >= min_confidence`

### **Bot chọn RANGING khi:**
- `trend_strength < ranging_threshold`
- `range_size_normalized < 0.015`
- Sideways price action detected
- Support/resistance levels active
- Fibonacci levels being tested

### **Bot chọn AUTO (Balanced) khi:**
- Performance-based selection enabled
- Market conditions uncertain
- No clear trending or ranging signals
- Fallback strategy

---

## 💡 **Tips Điều Chỉnh:**

### **Muốn Bot chọn Trending nhiều hơn:**
- Giảm `trending_threshold` xuống 0.01-0.015
- Tăng `ranging_threshold` lên 0.03-0.035
- Set `GLOBAL_TREND_PREFERENCE = "trending"`
- Set `entry_method = "momentum_trending"`

### **Muốn Bot chọn Ranging nhiều hơn:**
- Tăng `trending_threshold` lên 0.025-0.03
- Giảm `ranging_threshold` xuống 0.01-0.015
- Set `GLOBAL_TREND_PREFERENCE = "ranging"`
- Set `entry_method = "fibonacci_confluence"`

### **Muốn Bot cân bằng và adaptive:**
- Set `preferred_strategy = "auto"` cho hầu hết symbols
- Enable `PERFORMANCE_BASED_SELECTION = True`
- Maintain thresholds ở khoảng 0.02 ± 0.005
- Set `GLOBAL_TREND_PREFERENCE = "auto"`

---

## 🎯 **Ví Dụ Cụ Thể:**

### **BTCUSD - Trendinb Biased:**
```python
"BTCUSD": {
    "preferred_strategy": "trending",
    "entry_method": "volatility_breakout",
    "trending_threshold": 0.008,     # Very low = easy trending
    "ranging_threshold": 0.035,      # High = hard ranging
    "atr_multiplier_sl": 3.5,       # Larger SL for trending moves
    "atr_multiplier_tp": 7.0,       # Larger TP for trending moves
    "confidence_threshold": 0.15,    # Lower confidence needed
    "force_strategy": False
}
```

### **ETHUSD - Ranging Biased:**
```python
"ETHUSD": {
    "preferred_strategy": "ranging",
    "entry_method": "fibonacci_confluence",
    "trending_threshold": 0.035,     # High = rarely trending
    "ranging_threshold": 0.008,      # Very low = easy ranging
    "atr_multiplier_sl": 1.8,       # Smaller SL for ranging
    "atr_multiplier_tp": 3.0,        # Smaller TP for ranging
    "confidence_threshold": 0.25,    # Higher confidence required
    "force_strategy": False
}
```

---

## ⚠️ **Lưu Ý Quan Trọng:**

1. **Always backup** bot file trước khi thay đổi
2. **Test với small positions** trước khi live trading
3. **Monitor performance** và adjust config if needed
4. **Force strategy** chỉ nên dùng khi chắc chắn về market direction
5. **Auto selection** là recommended cho hầu hết cases
6. **Threshold tuning** có thể cần fine-tuning theo từng market cycle

---

## 📞 **Support:**

Nếu có vấn đề gì, check:
1. Config file format đúng không
2. Bot có recognize được new config không  
3. Logs có show strategy selection decisions không
4. Performance có improve không sau khi apply

**Happy Trading! 🚀**