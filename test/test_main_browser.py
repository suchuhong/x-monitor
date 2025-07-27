#!/usr/bin/env python3
"""
测试main.py的浏览器启动逻辑
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright
from src import browser_config, config, logger

# 获取日志器
log = logger.get_logger('main_test')

print("=== Main.py浏览器启动逻辑测试 ===")

# 复制main.py的检查逻辑
if not os.path.exists(browser_config.USER_DATA_DIR):
    log.error(f"浏览器配置文件目录 '{browser_config.USER_DATA_DIR}' 未找到")
    log.error("请先运行 'python initialize_profile.py' 来完成首次登录和初始化")
    exit(1)

with sync_playwright() as p:
    context = None
    try:
        # === 完全复制main.py的浏览器配置逻辑 ===
        headless_mode, slow_mo = browser_config.get_main_browser_config()
        
        # 记录浏览器模式
        is_visual_mode = config.ENABLE_VISUAL_SCRAPING
        if is_visual_mode:
            log.info("启用可视化抓取模式 - 浏览器窗口将可见")
            log.info(f"可视化延迟: {slow_mo} 毫秒")
        else:
            log.info(f"浏览器模式: {'无头模式' if headless_mode else '可视模式'}")
        
        print(f"\n调试信息:")
        print(f"  is_visual_mode: {is_visual_mode}")
        print(f"  headless_mode: {headless_mode}")
        print(f"  slow_mo: {slow_mo}")
        
        # 创建浏览器上下文和页面 - 完全复制main.py的逻辑
        context = browser_config.create_browser_context(p, headless_mode, slow_mo)
        page = browser_config.create_configured_page(context)
        # =====================
        
        print(f"\n浏览器启动成功！")
        print(f"如果看到了浏览器窗口，说明问题可能在其他地方")
        print(f"5秒后关闭...")
        
        import time
        time.sleep(5)
        
        context.close()
        print("测试完成")
        
    except Exception as e:
        log.error(f"程序发生未预期错误: {e}", exc_info=True)
        if context:
            context.close() 