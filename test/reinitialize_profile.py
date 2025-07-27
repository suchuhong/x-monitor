#!/usr/bin/env python3
"""
重新初始化浏览器配置文件
如果登录状态丢失，使用此脚本重新登录
"""
import os
import shutil
import traceback
from playwright_stealth.stealth import Stealth
from playwright.sync_api import sync_playwright

# 定义持久化配置文件的路径
USER_DATA_DIR = "./browser_profile"
BACKUP_DIR = "./browser_profile_backup"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"

print("=" * 80)
print("重新初始化浏览器配置文件")
print("=" * 80)
print("此脚本将:")
print("1. 备份现有的浏览器配置文件")
print("2. 清除可能损坏的登录数据")
print("3. 重新进行登录初始化")
print("=" * 80)

# 询问用户是否继续
confirm = input("是否继续? (y/N): ").strip().lower()
if confirm not in ['y', 'yes']:
    print("操作已取消")
    exit()

try:
    # 备份现有配置文件
    if os.path.exists(USER_DATA_DIR):
        print(f"备份现有配置文件到 {BACKUP_DIR}...")
        if os.path.exists(BACKUP_DIR):
            shutil.rmtree(BACKUP_DIR)
        shutil.copytree(USER_DATA_DIR, BACKUP_DIR)
        print("✅ 备份完成")
        
        # 删除现有配置文件
        print("删除现有配置文件...")
        shutil.rmtree(USER_DATA_DIR)
        print("✅ 删除完成")
    
    print("\n开始重新初始化...")
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            user_agent=USER_AGENT,
            viewport={'width': 1920, 'height': 1080},
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
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

        # 应用隐身插件
        stealth = Stealth()
        stealth.apply_stealth_sync(page)
        
        # 添加反检测JavaScript
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en'],
            });
        """)

        target_url = "https://x.com/login"
        print(f"\n跳转到登录页面: {target_url}")

        try:
            page.goto(target_url, timeout=90000, wait_until='networkidle')
            print(f"✅ 成功跳转到: {page.url}")
            print("\n🔑 请在浏览器窗口中完成登录:")
            print("1. 输入用户名/邮箱和密码")
            print("2. 完成任何安全验证")
            print("3. 确保成功登录到主页")
            print("4. 登录完成后，关闭浏览器窗口")

        except Exception as e:
            print(f"⚠️ 自动跳转失败: {e}")
            print("\n请手动在浏览器中访问 https://x.com/login 并完成登录")

        print("\n等待你完成登录...")
        print("登录成功后，请关闭整个浏览器窗口来完成初始化")

        # 等待浏览器关闭
        context.wait_for_event('close', timeout=600000)  # 10分钟超时
        
        print(f"\n✅ 浏览器已关闭，配置文件重新初始化完成!")
        print(f"新的配置文件保存在: {USER_DATA_DIR}")
        print(f"备份文件保存在: {BACKUP_DIR}")
        print("\n现在可以运行主监控程序了")

except Exception as e:
    print(f"\n❌ 重新初始化过程中发生错误:")
    print(f"错误类型: {type(e).__name__}")
    print("详细错误信息:")
    traceback.print_exc()
    
    # 如果出错，尝试恢复备份
    if os.path.exists(BACKUP_DIR) and not os.path.exists(USER_DATA_DIR):
        print(f"\n尝试从备份恢复配置文件...")
        try:
            shutil.copytree(BACKUP_DIR, USER_DATA_DIR)
            print("✅ 配置文件已从备份恢复")
        except Exception as restore_error:
            print(f"❌ 恢复备份失败: {restore_error}")

print("\n脚本执行完毕")