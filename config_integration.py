#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strategy Configuration Integration
File để kết nối strategy_config_updater.py vào bot chính

Tác giả: AI Assistant
Ngày tạo: 2024
Mục đích: Provide easy integration với main bot file
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime

class BotConfigIntegration:
    """Class để integrate config từ strategy updater vào bot chính"""
    
    def __init__(self, bot_file_path: str = "Bot-Trading_Swing (1).py"):
        self.bot_file_path = bot_file_path
        self.config_file_path = "strategy_config.json"
        
    def read_current_config(self) -> Dict[str, Any]:
        """Đọc config hiện tại từ file JSON"""
        try:
            if os.path.exists(self.config_file_path):
                with open(self.config_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"❌ Config file {self.config_file_path} not found")
                return {}
        except Exception as e:
            print(f"❌ Error reading config: {e}")
            return {}
    
    def read_bot_config_section(self, section_name: str = "ENTRY_TP_SL_CONFIG") -> Dict[str, Any]:
        """Đọc phần config từ bot file hiện tại"""
        try:
            with open(self.bot_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find section in bot file
            start_pattern = f"# Enhanced Entry/TP/SL Configuration|{section_name} = {{"
            end_pattern = "}"
            
            # Simple extraction (would need more sophisticated parsing for production)
            start_pos = content.find(f"{section_name} = {{")
            if start_pos == -1:
                print(f"❌ Section {section_name} not found in bot file")
                return {}
            
            # Find matching closing brace
            brace_count = 0
            end_pos = start_pos
            for i, char in enumerate(content[start_pos:]):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = start_pos + i + 1
                        break
            
            section_content = content[start_pos:end_pos]
            print(f"📄 Found {section_name} section (approx {len(section_content)} chars)")
            
            return {"content": section_content, "start": start_pos, "end": end_pos}
            
        except Exception as e:
            print(f"❌ Error reading bot file section: {e}")
            return {}
    
    def generate_updated_entry_config(self, new_config: Dict[str, Dict[str, Any]]) -> str:
        """Generate updated ENTRY_TP_SL_CONFIG section"""
        
        # Template phần đầu
        config_template = '''# Enhanced Entry/TP/SL Configuration for all symbols - UPDATED VERSION
ENTRY_TP_SL_CONFIG = {
    # === COMMODITIES (Global Trading) ===
'''
        
        # Generate config for each symbol
        symbol_order = ["XAUUSD", "USOIL", "DE40", "UK100", "FR40", "JP225", "AU200", 
                       "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "NZDUSD", 
                       "BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "ADAUSD"]
        
        for symbol in symbol_order:
            if symbol in new_config:
                config_data = new_config[symbol]
                config_template += f'''    "{symbol}": {{
        "entry_method": "{config_data.get('entry_method', 'auto_select')}",
        "atr_multiplier_sl": {config_data.get('atr_multiplier_sl', 2.0)},
        "atr_multiplier_tp": {config_data.get('atr_multiplier_tp', 4.0)},
        "min_rr_ratio": {config_data.get('min_rr_ratio', 1.4)},
        "max_rr_ratio": {config_data.get('multiplier_tp', 4.0) / config_data.get('atr_multiplier_sl', 2.0):.1f},
        "support_resistance_weight": {config_data.get('support_resistance_weight', 0.25)},
        "volume_confirmation": {config_data.get('volume_confirmation', True)},
        "session_filter": {config_data.get('session_filter', True)},
        "volatility_adjustment": {config_data.get('volatility_adjustment', True)},
        # Strategy Configuration - Added
        "preferred_strategy": "{config_data.get('preferred_strategy', 'auto')}",
        "trending_threshold": {config_data.get('trending_threshold', 0.02)},
        "ranging_threshold": {config_data.get('ranging_threshold', 0.025)},
        "confidence_threshold": {config_data.get('confidence_threshold', 0.20)},
        "force_strategy": {config_data.get('force_strategy', False)}'''
                
                if config_data.get('explanation'):
                    config_template += f''',
        "explanation": "{config_data.get('explanation', '')}"'''
                
                config_template += '''
    },
'''
        
        config_template += "}"
        return config_template
    
    def generate_updated_global_config(self, global_config: Dict[str, Any]) -> str:
        """Generate updated global configuration"""
        
        config_template = '''# STRATEGY SELECTION_GLOBAL_CONFIG - DYNAMIC UPDATES
STRATEGY_GLOBAL_CONFIG = {
'''
        
        for key, value in global_config.items():
            if isinstance(value, bool):
                config_template += f'    "{key}": {value},\n'
            elif isinstance(value, (int, float)):
                config_template += f'    "{key}": {value},\n'
            elif isinstance(value, str):
                config_template += f'    "{key}": "{value}",\n'
            elif isinstance(value, dict):
                config_template += f'    "{key}": {value},\n'
            elif isinstance(value, list):
                config_template += f'    "{key}": {value},\n'
        
        config_template += "}"
        return config_template
    
    def create_patch_file(self, config_name: str = "balanced") -> str:
        """Tạo patch file để apply config changes"""
        
        from strategy_examples import StrategyExamples
        
        examples = StrategyExamples()
        
        config_mapping = {
            "trending": examples.get_trending_biased_config(),
            "ranging": examples.get_ranging_biased_config(),
            "balanced": examples.get_balanced_config(),
            "aggressive": examples.get_aggressive_config(),
            "conservative": examples.get_conservative_config()
        }
        
        if config_name not in config_mapping:
            print(f"❌ Unknown config: {config_name}")
            return ""
        
        selected_config = config_mapping[config_name]
        
        # Generate update sections
        entry_config_update = self.generate_updated_entry_config(selected_config)
        global_config_update = self.generate_updated_global_config(selected_config)
        
        # Create patch file content
        patch_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STRATEGY CONFIG PATCH FILE
Config Name: {config_name.upper()}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

CRITICAL INSTRUCTIONS TO APPLY THIS PATCH:

1. BACKUP your current Bot-Trading_Swing (1).py file !!!
2. Copy the entries below into the appropriate sections
3. Replace existing ENTRY_TP_SL_CONFIG section with NEW_ENTRY_TP_SL_CONFIG
4. Add STRATEGY_GLOBAL_CONFIG section if not exists
5. Test the bot with small positions first

WARNING: This patch modifies core bot functionality!
"""

print("🚨 STRATEGY CONFIG PATCH - {config_name.upper()} MODE")
print("=" * 60)
print("Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Mode:", config_name.upper())
print("⚠️  BACKUP YOUR BOT BEFORE APPLYING!")
print()

# === NEW ENTRY TB_CONFIG SECTION ===
NEW_ENTRY_TP_SL_CONFIG = {{
    
{entry_config_update}

# === NEW GLOBAL STRATEGY CONFIG SECTION ===
NEW_STRATEGY_GLOBAL_CONFIG = {{
    
{global_config_update}

print("📋 INSTRUCTIONS TO APPLY:")
print("1. Find ENTRY_TP_SL_CONFIG in your Bot-Trading_Swing (1).py")
print("2. Replace entire section with NEW_ENTRY_TP_SL_CONFIG above")
print("3. Add STRATEGY_GLOBAL_CONFIG section with NEW_STRATEGY_GLOBAL_CONFIG")
print("4. Restart the bot")  
print("5. Monitor performance và adjust if needed")
print()
print("🎯 Expected Behavior with {config_name.upper()} config:")
'''
        
        # Add expected behavior description
        behavior_descriptions = {
            "trending": "Bot sẽ prioritize trending strategies với low thresholds",
            "ranging": "Bot sẽ focus on ranging strategies với fibonacci/support-resistance",
            "balanced": "Bot sẽ auto-select based on market conditions với equal thresholds", 
            "aggressive": "Bot sẽ trade more frequently với low confidence requirements",
            "conservative": "Bot sẽ trade less but higher quality signals với strict thresholds"
        }
        
        patch_content += f'print("- {behavior_descriptions[config_name]}")'
        
        # Save patch file
        patch_filename = f"strategy_patch_{config_name}.py"
        with open(patch_filename, 'w', encoding='utf-8') as f:
            f.write(patch_content)
        
        print(f"✅ Patch file created: {patch_filename}")
        return patch_filename
    
    def apply_config_automatically(self, config_name: str = "balanced") -> bool:
        """Auto apply config changes to bot file (with backup)"""
        
        print(f"🚨 AUTOMATIC CONFIG APPLICATION - {config_name.upper()}")
        print("=" * 60)
        
        # Create backup first
        backup_filename = f"Bot_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        
        try:
            # Read original file
            with open(self.bot_file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Create backup
            with open(backup_filename, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            print(f"✅ Backup created: {backup_filename}")
            
            # Generate updated config
            patch_file = self.create_patch_file(config_name)
            
            print(f"✅ Patch ready: {patch_file}")
            print()
            print("⚠️  IMPORTANT: Auto-apply not implemented for safety!")
            print("📋 Please follow manual steps:")
            print("1. Review the config changes trong patch file")
            print("2. Apply changes manually vào bot file")
            print("3. Test thoroughly trước khi live trading")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during auto-apply: {e}")
            return False
    
    def show_integration_status(self) -> Dict[str, Any]:
        """Show current integration status"""
        
        status = {
            "bot_file_exists": os.path.exists(self.bot_file_path),
            "config_file_exists": os.path.exists(self.config_file_path),
            "integration_ready": False
        }
        
        if status["bot_file_exists"]:
            print(f"✅ Bot file found: {self.bot_file_path}")
        else:
            print(f"❌ Bot file not found: {self.bot_file_path}")
        
        if status["config_file_exists"]:
            print(f"✅ Config file found: {self.config_file_path}")
            current_config = self.read_current_config()
            if current_config:
                print(f"✅ Config loaded successfully (version {current_config.get('meta', {}).get('version', 'unknown')})")
        else:
            print(f"❌ Config file not found: {self.config_file_path}")
        
        status["integration_ready"] = status["bot_file_exists"] and status["config_file_exists"]
        
        if status["integration_ready"]:
            print("🚀 Integration ready - có thể apply config changes!")
        else:
            print("⚠️ Integration not ready - missing required files")
        
        return status

def main():
    """Main function để demonstrate integration"""
    
    print("🔧 Strategy Configuration Integration")
    print("=" * 50)
    
    integrator = BotConfigIntegration()
    
    # Show current status
    status = integrator.show_integration_status()
    print()
    
    if status["integration_ready"]:
        print("📋 Available integration options:")
        print("1. Show current config status")
        print("2. Create patch file for specific config")
        print("3. Auto-apply config (with backup)")
        print()
        
        # Create balanced config patch example
        patch_file = integrator.create_patch_file("balanced")
        print(f"📁 Example patch file created: {patch_file}")
        print()
        print("📖 Next steps:")
        print("1. Review patch file content")
        print("2. Apply changes manually vào bot file") 
        print("3. Test với small positions")
        print("4. Monitor performance và refine config if needed")
        
    else:
        print("❌ Cannot proceed - integration not ready")
        print("Make sure both bot file và config file exist")

if __name__ == "__main__":
    main()