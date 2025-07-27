#!/usr/bin/env python3
"""
检查X.com登录状态的脚本
"""
import sys
import os
sys.path.append('src')

import time
from playwright.sync_api import sync_playwright
import browser_config

def check_login_status():
    """检查X.com登录状态"""
    if not os.path.exists(browser_config.USER_DATA_DIR):
        print("❌ 浏览器配置文件目录未找到。请先运行 initialize_profile.py")
        return
    
    print("🔍 检查X.com登录状态...")
    print("=" * 60)
    
    with sync_playwright() as p:
        # 使用统一的浏览器配置，强制可视化模式便于观察
        context = browser_config.create_browser_context(p, headless=False, slow_mo=0)
        page = browser_config.create_configured_page(context)
        
        print("1. 访问X.com主页...")
        try:
            page.goto("https://x.com", wait_until="networkidle", timeout=30000)
            print(f"✅ 成功访问: {page.url}")
        except Exception as e:
            print(f"❌ 访问失败: {e}")
            return
        
        time.sleep(3)  # 等待页面完全加载
        
        print("\n2. 检查登录状态...")
        
        # 检查是否有登录按钮（未登录的标志）
        login_button = page.locator("a[href='/login']").first
        if login_button.is_visible():
            print("❌ 未登录 - 发现登录按钮")
            
            # 尝试查找其他登录相关元素
            signup_button = page.locator("a[href='/i/flow/signup']").first
            if signup_button.is_visible():
                print("❌ 发现注册按钮，确认未登录")
        else:
            print("✅ 未发现登录按钮")
        
        # 检查是否有用户菜单（已登录的标志）
        try:
            # 查找用户头像或菜单
            user_menu = page.locator("[data-testid='SideNav_AccountSwitcher_Button']").first
            if user_menu.is_visible():
                print("✅ 已登录 - 发现用户菜单")
                
                # 尝试获取用户名
                try:
                    username_element = page.locator("[data-testid='UserName']").first
                    if username_element.is_visible():
                        username = username_element.inner_text()
                        print(f"✅ 登录用户: {username}")
                except:
                    print("✅ 已登录但无法获取用户名")
            else:
                print("❌ 未发现用户菜单")
        except Exception as e:
            print(f"⚠️ 检查用户菜单时出错: {e}")
        
        # 检查页面标题
        title = page.title()
        print(f"\n页面标题: {title}")
        
        # 检查当前URL
        current_url = page.url
        print(f"当前URL: {current_url}")
        
        # 如果重定向到登录页面，说明未登录
        if "/login" in current_url or "/i/flow/login" in current_url:
            print("❌ 页面重定向到登录页面，确认未登录")
        
        print("\n3. 尝试访问需要登录的页面...")
        try:
            page.goto("https://x.com/home", wait_until="networkidle", timeout=15000)
            time.sleep(2)
            
            current_url = page.url
            print(f"访问/home后的URL: {current_url}")
            
            if "/login" in current_url or "/i/flow/login" in current_url:
                print("❌ 访问/home被重定向到登录页面，确认未登录")
            else:
                print("✅ 成功访问/home页面，可能已登录")
                
                # 检查是否有时间线内容
                timeline = page.locator("[data-testid='primaryColumn']").first
                if timeline.is_visible():
                    print("✅ 发现时间线内容，确认已登录")
                else:
                    print("⚠️ 未发现时间线内容")
        except Exception as e:
            print(f"❌ 访问/home失败: {e}")
        
        print("\n" + "=" * 60)
        print("检查完成。浏览器窗口将保持打开10秒供你观察...")
        time.sleep(10)
        
        context.close()

if __name__ == "__main__":
    check_login_status()