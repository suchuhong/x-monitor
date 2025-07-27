#!/usr/bin/env python3
"""
测试不同浏览器模式配置的行为
"""
import sys
import os
sys.path.append('src')

import config

def test_browser_mode_logic():
    """测试浏览器模式逻辑"""
    print("=" * 80)
    print("浏览器模式配置测试")
    print("=" * 80)
    
    print("当前配置:")
    print(f"  HEADLESS_MODE: {config.HEADLESS_MODE}")
    print(f"  ENABLE_VISUAL_SCRAPING: {config.ENABLE_VISUAL_SCRAPING}")
    print(f"  VISUAL_SCRAPING_SLOW_MO: {config.VISUAL_SCRAPING_SLOW_MO}")
    
    # 模拟main.py中的逻辑
    is_visual_mode = config.ENABLE_VISUAL_SCRAPING
    
    if is_visual_mode:
        headless_mode = False  # 可视化模式强制显示浏览器
        browser_mode = "可视化抓取模式"
        slow_mo = config.VISUAL_SCRAPING_SLOW_MO
    else:
        headless_mode = config.HEADLESS_MODE  # 按照配置决定
        browser_mode = "无头模式" if headless_mode else "普通可视模式"
        slow_mo = 0
    
    print("\n计算结果:")
    print(f"  最终无头模式: {headless_mode}")
    print(f"  浏览器模式: {browser_mode}")
    print(f"  慢动作延迟: {slow_mo} 毫秒")
    
    print("\n行为说明:")
    if is_visual_mode:
        print("  ✅ 启用可视化抓取模式")
        print("  ✅ 浏览器窗口将可见")
        print(f"  ✅ 操作延迟 {slow_mo} 毫秒便于观察")
    else:
        if headless_mode:
            print("  ✅ 使用无头模式")
            print("  ✅ 浏览器窗口不可见")
            print("  ✅ 性能最佳，适合生产环境")
        else:
            print("  ✅ 使用普通可视模式")
            print("  ✅ 浏览器窗口可见但无延迟")
            print("  ✅ 适合调试但不需要慢动作")
    
    print("\n" + "=" * 80)
    print("配置组合说明")
    print("=" * 80)
    
    combinations = [
        ("true", "false", "无头模式 - 浏览器不可见，性能最佳"),
        ("false", "false", "普通可视模式 - 浏览器可见但无延迟"),
        ("true", "true", "可视化抓取模式 - 强制显示浏览器，有延迟"),
        ("false", "true", "可视化抓取模式 - 强制显示浏览器，有延迟"),
    ]
    
    print("HEADLESS_MODE | ENABLE_VISUAL_SCRAPING | 结果")
    print("-" * 80)
    for headless, visual, result in combinations:
        current = "👈 当前" if (headless.lower() == str(config.HEADLESS_MODE).lower() and 
                                visual.lower() == str(config.ENABLE_VISUAL_SCRAPING).lower()) else ""
        print(f"{headless:^13} | {visual:^22} | {result} {current}")
    
    print("\n推荐配置:")
    print("  生产环境: HEADLESS_MODE=true, ENABLE_VISUAL_SCRAPING=false")
    print("  调试环境: HEADLESS_MODE=true, ENABLE_VISUAL_SCRAPING=true")
    print("  快速调试: HEADLESS_MODE=false, ENABLE_VISUAL_SCRAPING=false")

def test_different_configs():
    """测试不同配置的模拟结果"""
    print("\n" + "=" * 80)
    print("模拟不同配置的结果")
    print("=" * 80)
    
    test_cases = [
        {"HEADLESS_MODE": True, "ENABLE_VISUAL_SCRAPING": False},
        {"HEADLESS_MODE": False, "ENABLE_VISUAL_SCRAPING": False},
        {"HEADLESS_MODE": True, "ENABLE_VISUAL_SCRAPING": True},
        {"HEADLESS_MODE": False, "ENABLE_VISUAL_SCRAPING": True},
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试案例 {i}:")
        print(f"  HEADLESS_MODE: {case['HEADLESS_MODE']}")
        print(f"  ENABLE_VISUAL_SCRAPING: {case['ENABLE_VISUAL_SCRAPING']}")
        
        # 模拟逻辑
        is_visual_mode = case['ENABLE_VISUAL_SCRAPING']
        if is_visual_mode:
            headless_mode = False
            result = "可视化抓取模式 - 浏览器可见，有延迟"
        else:
            headless_mode = case['HEADLESS_MODE']
            result = "无头模式 - 浏览器不可见" if headless_mode else "普通可视模式 - 浏览器可见，无延迟"
        
        print(f"  结果: {result}")
        print(f"  实际headless参数: {headless_mode}")

if __name__ == "__main__":
    test_browser_mode_logic()
    test_different_configs()