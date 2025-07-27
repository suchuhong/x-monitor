#!/usr/bin/env python3
"""
调试模式的推文抓取脚本
- 可视化浏览器窗口
- 详细的步骤说明
- 手动控制抓取过程
"""
import sys
import os
sys.path.append('src')

import logging
import time
from playwright.sync_api import sync_playwright
from playwright_stealth.stealth import Stealth

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def debug_scraper():
    """调试模式的推文抓取"""
    USER_DATA_DIR = "./browser_profile"
    
    if not os.path.exists(USER_DATA_DIR):
        print("错误: 浏览器配置文件目录未找到。请先运行 initialize_profile.py")
        return
    
    print("=" * 80)
    print("推文抓取调试模式")
    print("=" * 80)
    print("这个脚本会:")
    print("1. 打开可视化浏览器窗口")
    print("2. 显示每个抓取步骤")
    print("3. 让你观察整个过程")
    print("4. 在每个关键步骤暂停，等待你的确认")
    print("=" * 80)
    
    # 获取用户输入
    target_user = input("请输入要测试的X用户名 (例如: zyailive): ").strip()
    if not target_user:
        print("错误: 用户名不能为空")
        return
    
    with sync_playwright() as p:
        print("\n步骤1: 启动浏览器...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,  # 可视化模式
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            # 使用与初始化时相同的参数
            args=[
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-blink-features=AutomationControlled',
                '--disable-features=VizDisplayCompositor',
                '--disable-ipc-flooding-protection',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--disable-field-trial-config',
                '--disable-back-forward-cache',
                '--disable-hang-monitor',
                '--disable-prompt-on-repost',
                '--disable-sync',
                '--disable-translate',
                '--metrics-recording-only',
                '--safebrowsing-disable-auto-update',
                '--enable-automation=false',
                '--password-store=basic',
                '--use-mock-keychain'
            ],
            ignore_default_args=['--enable-automation'],
            java_script_enabled=True,
            bypass_csp=True,
            ignore_https_errors=True
        )
        
        page = context.new_page()
        
        # 应用stealth插件
        print("步骤2: 应用反检测插件...")
        stealth = Stealth()
        stealth.apply_stealth_sync(page)
        
        url = f"https://x.com/{target_user}"
        print(f"步骤3: 访问用户页面: {url}")
        
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            print("✅ 页面加载完成")
        except Exception as e:
            print(f"❌ 页面加载失败: {e}")
            return
        
        input("\n按回车键继续到下一步...")
        
        print("步骤4: 等待推文元素加载...")
        try:
            tweet_selector = "article[data-testid='tweet']"
            page.wait_for_selector(tweet_selector, timeout=30000)
            print("✅ 推文元素已找到")
        except Exception as e:
            print(f"❌ 推文元素加载失败: {e}")
            return
        
        input("\n按回车键开始分析推文...")
        
        print("步骤5: 分析页面上的推文...")
        tweet_elements = page.locator(tweet_selector).all()
        print(f"找到 {len(tweet_elements)} 个推文元素")
        
        found_tweets = []
        
        for i, tweet_element in enumerate(tweet_elements[:5]):  # 只分析前5个
            print(f"\n分析第 {i+1} 个推文:")
            
            try:
                # 查找推文链接
                tweet_link_element = tweet_element.locator("a[href*='/status/']").filter(has_not_text="analytics").first
                tweet_url = tweet_link_element.get_attribute('href')
                
                if tweet_url and "/status/" in tweet_url:
                    tweet_id = tweet_url.split('/status/')[-1].split('?')[0]
                    print(f"  ✅ 推文ID: {tweet_id}")
                    print(f"  ✅ 推文URL: https://x.com{tweet_url}")
                else:
                    print("  ❌ 未找到有效的推文URL")
                    continue
                
                # 查找时间元素
                time_element = tweet_element.locator("time").first
                if time_element:
                    datetime_attr = time_element.get_attribute('datetime')
                    time_text = time_element.inner_text()
                    print(f"  ✅ 推文时间: {time_text} (原始: {datetime_attr})")
                else:
                    print("  ❌ 未找到时间元素")
                
                # 查找推文文本
                text_element = tweet_element.locator("[data-testid='tweetText']").first
                if text_element:
                    tweet_text = text_element.inner_text()
                    print(f"  ✅ 推文内容: {tweet_text[:100]}{'...' if len(tweet_text) > 100 else ''}")
                else:
                    print("  ❌ 未找到推文文本")
                
                found_tweets.append({
                    'id': tweet_id,
                    'url': f"https://x.com{tweet_url}",
                    'text': tweet_text if 'tweet_text' in locals() else '',
                    'time': time_text if 'time_text' in locals() else ''
                })
                
            except Exception as e:
                print(f"  ❌ 分析失败: {e}")
            
            if i < 4:  # 不是最后一个
                input("按回车键分析下一个推文...")
        
        print(f"\n步骤6: 分析完成，共找到 {len(found_tweets)} 条有效推文")
        
        if found_tweets:
            print("\n推文摘要:")
            for i, tweet in enumerate(found_tweets):
                print(f"{i+1}. ID: {tweet['id']}")
                print(f"   时间: {tweet['time']}")
                print(f"   内容: {tweet['text'][:80]}...")
                print()
        
        print("调试完成。浏览器窗口将保持打开状态，你可以手动检查页面。")
        print("按 Ctrl+C 退出程序。")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n程序已退出")
        finally:
            context.close()

if __name__ == "__main__":
    debug_scraper()