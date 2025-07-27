#!/usr/bin/env python3
"""
测试浏览器无头模式
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright
from src import browser_config, config

print("=== 浏览器无头模式测试 ===")
print(f"HEADLESS_MODE: {config.HEADLESS_MODE}")
print(f"ENABLE_VISUAL_SCRAPING: {config.ENABLE_VISUAL_SCRAPING}")

headless_mode, slow_mo = browser_config.get_main_browser_config()
print(f"get_main_browser_config() 返回:")
print(f"  headless_mode: {headless_mode}")
print(f"  slow_mo: {slow_mo}")

with sync_playwright() as p:
    print("\n正在启动浏览器...")
    try:
        # 使用项目的配置
        context = browser_config.create_browser_context(p, headless_mode, slow_mo)
        print(f"浏览器启动成功 - headless模式: {headless_mode}")
        
        # 测试访问一个页面
        page = browser_config.create_configured_page(context)
        print("正在访问测试页面...")
        page.goto("https://httpbin.org/user-agent", timeout=30000)
        
        user_agent = page.evaluate("() => navigator.userAgent")
        print(f"User Agent: {user_agent}")
        
        print("测试完成，3秒后关闭浏览器...")
        import time
        time.sleep(3)
        
        context.close()
        print("浏览器已关闭")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc() 