#!/usr/bin/env python3
"""
可视化抓取测试脚本
专门用于可视化模式下的推文抓取测试
"""
import sys
import os
sys.path.append('src')

import time
from playwright.sync_api import sync_playwright
import scraper
import config
import logger
import browser_config

# 获取日志器
log = logger.get_logger('visual_test')

def visual_scraping_test():
    """可视化抓取测试"""
    if not os.path.exists(browser_config.USER_DATA_DIR):
        print("❌ 浏览器配置文件目录未找到。请先运行 initialize_profile.py")
        return
    
    print("=" * 80)
    print("可视化抓取测试")
    print("=" * 80)
    print("此脚本将:")
    print("1. 以可视化模式启动浏览器")
    print("2. 显示抓取过程的每个步骤")
    print("3. 使用慢动作模式便于观察")
    print("4. 提供详细的日志输出")
    print("=" * 80)
    
    # 获取用户输入
    available_users = [user.strip() for user in config.TARGET_USERS if user.strip()]
    if not available_users:
        print("❌ 没有配置目标用户")
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
    
    # 获取可视化配置
    slow_mo = input(f"\n请输入慢动作延迟时间（毫秒，默认2000）: ").strip()
    try:
        slow_mo = int(slow_mo) if slow_mo else 2000
    except ValueError:
        slow_mo = 2000
    
    print(f"\n开始可视化抓取测试:")
    print(f"  目标用户: {test_user}")
    print(f"  慢动作延迟: {slow_mo} 毫秒")
    print(f"  抓取天数: {config.DAYS_TO_SCRAPE} 天")
    print(f"  最大推文数: {config.MAX_TWEETS_PER_USER} 条")
    print("\n浏览器窗口将打开，你可以观察整个抓取过程...")
    
    with sync_playwright() as p:
        # 使用统一的浏览器配置，可视化模式带慢动作
        print("应用反检测插件...")
        context = browser_config.create_browser_context(p, headless=False, slow_mo=slow_mo)
        page = browser_config.create_configured_page(context)
        
        print(f"\n开始抓取用户 {test_user} 的推文...")
        print("你可以在浏览器窗口中观察以下过程:")
        print("1. 页面导航到用户主页")
        print("2. 等待推文元素加载")
        print("3. 滚动页面加载更多推文")
        print("4. 解析每个推文的内容")
        print("\n按 Ctrl+C 可以随时停止测试")
        
        try:
            # 记录开始时间
            start_time = time.time()
            
            # 执行抓取
            tweets = scraper.scrape_user_tweets(page, test_user)
            
            # 记录结束时间
            end_time = time.time()
            duration = end_time - start_time
            
            print("\n" + "=" * 80)
            print("抓取完成!")
            print("=" * 80)
            print(f"用时: {duration:.2f} 秒")
            print(f"找到推文: {len(tweets)} 条")
            
            if tweets:
                print(f"\n推文摘要:")
                for i, tweet in enumerate(tweets[:5]):  # 只显示前5条
                    print(f"{i+1}. ID: {tweet['id']}")
                    print(f"   时间: {tweet['timestamp']}")
                    print(f"   内容: {tweet['text'][:100]}{'...' if len(tweet['text']) > 100 else ''}")
                    print()
                
                if len(tweets) > 5:
                    print(f"... 还有 {len(tweets) - 5} 条推文")
            else:
                print("❌ 未找到任何推文")
            
            print(f"\n浏览器窗口将在10秒后关闭...")
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n用户中断了测试")
        except Exception as e:
            print(f"\n❌ 测试过程中发生错误: {e}")
            log.error(f"可视化抓取测试失败: {e}", exc_info=True)
        finally:
            context.close()

def interactive_mode():
    """交互式可视化模式"""
    if not os.path.exists(browser_config.USER_DATA_DIR):
        print("❌ 浏览器配置文件目录未找到。请先运行 initialize_profile.py")
        return
    
    print("=" * 80)
    print("交互式可视化抓取模式")
    print("=" * 80)
    print("在这个模式下，你可以:")
    print("1. 手动控制抓取过程")
    print("2. 在每个步骤暂停")
    print("3. 观察页面变化")
    print("4. 调试特定问题")
    print("=" * 80)
    
    with sync_playwright() as p:
        # 使用统一的浏览器配置，适中的延迟
        context = browser_config.create_browser_context(p, headless=False, slow_mo=500)
        page = browser_config.create_configured_page(context)
        
        print("\n浏览器已启动。你现在可以:")
        print("1. 手动导航到任何X用户页面")
        print("2. 观察页面加载过程")
        print("3. 检查登录状态")
        print("4. 测试页面元素")
        print("\n浏览器窗口将保持打开状态。")
        print("按 Ctrl+C 退出程序。")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n退出交互式模式")
        finally:
            context.close()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='可视化抓取测试工具')
    parser.add_argument('mode', choices=['test', 'interactive'], 
                       help='运行模式: test=自动测试, interactive=交互式')
    
    args = parser.parse_args()
    
    if args.mode == 'test':
        visual_scraping_test()
    elif args.mode == 'interactive':
        interactive_mode()

if __name__ == "__main__":
    main()