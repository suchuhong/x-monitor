#!/usr/bin/env python3
import sys
import os
sys.path.append('src')

import logging
import time
from playwright.sync_api import sync_playwright
import scraper
import config
import browser_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_scraper():
    """测试推文抓取功能 - 可视化模式"""
    if not os.path.exists(browser_config.USER_DATA_DIR):
        print("错误: 浏览器配置文件目录未找到。请先运行 initialize_profile.py")
        return
    
    print("=" * 60)
    print("推文抓取测试 - 可视化模式")
    print("=" * 60)
    print(f"配置信息:")
    print(f"  日期范围: {config.DAYS_TO_SCRAPE} 天")
    print(f"  最大推文数: {config.MAX_TWEETS_PER_USER}")
    print(f"  目标用户: {config.TARGET_USERS}")
    print("=" * 60)
    
    with sync_playwright() as p:
        # 使用统一的浏览器配置，可视化模式
        context = browser_config.create_browser_context(p, headless=False, slow_mo=0)
        page = browser_config.create_configured_page(context)
        
        page = context.new_page()
        
        # 让用户选择要测试的用户
        available_users = [user.strip() for user in config.TARGET_USERS if user.strip()]
        if not available_users:
            print("错误: 没有配置目标用户")
            return
            
        print(f"\n可用的用户列表:")
        for i, user in enumerate(available_users):
            print(f"  {i+1}. {user}")
        
        try:
            choice = input(f"\n请选择要测试的用户 (1-{len(available_users)}, 直接回车选择第一个): ").strip()
            if not choice:
                test_user = available_users[0]
            else:
                test_user = available_users[int(choice) - 1]
        except (ValueError, IndexError):
            test_user = available_users[0]
        
        print(f"\n开始测试用户: {test_user}")
        print("浏览器窗口已打开，你可以观察整个抓取过程...")
        print("按 Ctrl+C 可以随时停止")
        
        try:
            tweets = scraper.scrape_user_tweets(page, test_user)
            
            print("\n" + "=" * 60)
            print(f"抓取完成! 找到 {len(tweets)} 条推文")
            print("=" * 60)
            
            if tweets:
                for i, tweet in enumerate(tweets):
                    print(f"\n{i+1}. 推文详情:")
                    print(f"   ID: {tweet['id']}")
                    print(f"   时间: {tweet['timestamp']}")
                    print(f"   用户: {tweet['user']}")
                    print(f"   内容: {tweet['text'][:150]}{'...' if len(tweet['text']) > 150 else ''}")
                    print(f"   URL: {tweet['url']}")
            else:
                print("未找到任何推文")
            
            print(f"\n测试完成。浏览器窗口将在10秒后关闭...")
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n用户中断了测试")
        except Exception as e:
            print(f"\n测试过程中发生错误: {e}")
        finally:
            context.close()

if __name__ == "__main__":
    test_scraper()