#!/usr/bin/env python3
"""
CRITICAL SAFETY FIX: RL Model Dimension Mismatch
This script patches the bot to prevent silent dimension adjustments in RL predictions.
"""

import re
import sys
import os

def patch_rl_dimensions():
    """Patch RL prediction logic to enforce strict dimension matching"""
    
    bot_file = "Bot-Trading_Swing (1).py"
    
    if not os.path.exists(bot_file):
        print(f"Error: {bot_file} not found!")
        return False
    
    # Read the file
    with open(bot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Replace silent dimension adjustment with assertion error
    rt_strategy_pattern = r'(# So snh v fix l i shape if needs\s*if final_live_observation\.shape != expected_shape:.*?)final_live_observation = np\.nan_to_num\(final_live_observation\)'
    
    def replace_rt_adjustment(match):
        return '''# CRITICAL SAFETY CHECK: Assert exact shape match before model prediction
            if final_live_observation.shape != expected_shape:
                error_msg = f"CRITICAL ERROR: Observation shape mismatch! Expected {expected_shape}, but got {final_live_observation.shape}. The RL model trained with {expected_shape[0]} features but production is generating {final_live_observation.shape[0]} features. This indicates environment mismatch between training and production. STOPPING to prevent invalid predictions."
                logging.critical(error_msg)
                print(f"[RL Strategy] {error_msg}")
                
                # Instead of silently adjusting, throw an error to prevent invalid trading decisions
                raise AssertionError(f"Shape mismatch: Expected {expected_shape}, got {final_live_observation.shape}. Retrain model or fix feature generation.")
            
            final_live_observation = np.nan_to_num(final_live_observation)'''
    
    content = re.sub(rt_strategy_pattern, replace_rt_adjustment, content, flags=re.DOTALL)
    
    # Fix 2: Replace training environment adjustment with assertion  
    train_env_pattern = r'(# Final validation\s*if len\(final_obs\) != self\.observation_space\.shape\[0\]:.*?)return final_obs'
    
    def replace_train_adjustment(match):
        return '''# CRITICAL SAFETY CHECK: Assert exact shape match for training environment consistency
            if len(final_obs) != self.observation_space.shape[0]:
                error_msg = f"CRITICAL ERROR in RL Environment: Observation shape mismatch! Environment expected {(self.observation_space.shape[0],)} but generated ({len(final_obs)},). This indicates inconsistency in feature generation. STOPPING training to prevent model corruption."
                logging.critical(error_msg)
                raise AssertionError(f"Environment shape mismatch: Expected {(self.observation_space.shape[0],)}, got ({len(final_obs)},). Check feature generation consistency.")

            return final_obs'''
    
    content = re.sub(train_env_pattern, replace_train_adjustment, content, flags=re.DOTALL)
    
    # Fix 3: Add dimension debugging info
    dimension_debug = '''
        print(f"   [Environment] ⚠️ EXPECTED MODEL SHAPE: ({total_obs_size},) - This MUST match trained model!")
        print(f"   [Environment] 🔍 Dimension Formula: {self.n_symbols} symbols × {single_symbol_market_features_dim + 3} features/symbol + 4 global = {total_obs_size}")
        '''
    
    content = re.sub(
        r'(print\(f"\[Environment\] Total symbols: \{self\.n_symbols\}"\))',
        r'\1' + dimension_debug,
        content
    )
    
    # Write the patched content
    backup_file = f"{bot_file}.rl_backup" 
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(open(bot_file, 'r', encoding='utf-8').read())
    
    with open(bot_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ CRITICAL FIX APPLIED: RL dimension strict checking")
    print(f"📁 Backup created: {backup_file}")
    print(f"🚨 Bot now throws errors on RL dimension mismatches instead of silently adjusting")
    
    return True

if __name__ == "__main__":
    patch_rl_dimensions()