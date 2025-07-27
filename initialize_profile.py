import os
import sys
import traceback
from playwright.sync_api import sync_playwright

# 修复导入问题：使用正确的模块导入方式
# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 使用绝对导入，这样src模块内部的相对导入就能正常工作
from src import browser_config

print("--- 初始化浏览器配置文件 (使用 playwright-stealth) ---")

try:
    with sync_playwright() as p:
        # 使用统一的浏览器配置
        headless_mode, slow_mo = browser_config.get_init_browser_config()
        context = browser_config.create_browser_context(p, headless_mode, slow_mo)
        page = browser_config.create_configured_page(context)

        target_url = "https://x.com/login"
        print(f"\n[调试] 准备跳转到: {target_url}")

        try:
            page.goto(target_url, timeout=90000, wait_until='networkidle')
            # 修正点：去掉了 page.url 后面的括号 ()
            print(f"[调试] 成功跳转到: {page.url}")
            print("\n[成功] 浏览器已自动跳转。请在窗口中完成登录。")

        except Exception as e:
            print("\n" + "="*50)
            print("[注意] 自动跳转失败。这通常是由于网络或防火墙问题。")
            print(f"错误信息: {e}")
            print("\n[下一步] 不过没关系，请在已打开的浏览器窗口中，【手动输入】地址 https://x.com/login 并完成登录。")
            print("="*50 + "\n")

        print("\n请完成所有登录步骤（包括可能出现的安全验证）。")
        print("登录成功后，请直接【关闭整个浏览器窗口】来完成本次初始化。")
        print("脚本将在此期间一直等待...")

        # 增加超时时间到10分钟，给用户充足的操作时间
        context.wait_for_event('close', timeout=600000)
        
        print(f"\n浏览器已关闭。配置文件在目录 '{browser_config.USER_DATA_DIR}' 中创建/更新成功！")
        print("现在可以运行主监控程序了。")

except Exception as e:
    print("\n" + "="*50)
    print("[严重错误] Playwright 启动或执行时发生严重问题。")
    print(f"错误类型: {type(e).__name__}")
    print("详细追溯信息:")
    traceback.print_exc()
    print("="*50 + "\n")

print("\n脚本执行完毕。")