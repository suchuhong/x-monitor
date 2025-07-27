"""
浏览器配置模块
为 initialize_profile.py 和 main.py 提供统一的浏览器配置
确保登录状态能够正确共享
"""
import os
from playwright_stealth.stealth import Stealth
from . import config

# 浏览器配置常量
USER_DATA_DIR = "./browser_profile"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"

def get_browser_args():
    """获取统一的浏览器启动参数"""
    return [
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
    ]

def get_browser_context_options(headless=False, slow_mo=0):
    """
    获取统一的浏览器上下文选项
    
    Args:
        headless: 是否使用无头模式
        slow_mo: 慢动作延迟（毫秒）
    
    Returns:
        dict: 浏览器上下文选项
    """
    return {
        'user_data_dir': USER_DATA_DIR,
        'headless': headless,
        'user_agent': USER_AGENT,
        'viewport': {'width': 1920, 'height': 1080},
        'locale': 'zh-CN',
        'timezone_id': 'Asia/Shanghai',
        'slow_mo': slow_mo,
        'args': get_browser_args(),
        'ignore_default_args': ['--enable-automation'],
        'java_script_enabled': True,
        'bypass_csp': True,
        'ignore_https_errors': True
    }

def apply_stealth_and_scripts(page):
    """
    应用统一的反检测插件和脚本
    
    Args:
        page: Playwright页面对象
    """
    # 应用stealth插件
    stealth = Stealth()
    stealth.apply_stealth_sync(page)
    
    # 添加统一的反检测JavaScript
    page.add_init_script("""
        // 移除webdriver属性
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // 伪造chrome对象
        window.chrome = {
            runtime: {},
            loadTimes: function() {},
            csi: function() {},
            app: {}
        };
        
        // 伪造插件信息
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // 伪造语言信息
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'zh', 'en'],
        });
    """)

def create_browser_context(playwright_instance, headless=False, slow_mo=0):
    """
    创建统一配置的浏览器上下文
    
    Args:
        playwright_instance: Playwright实例
        headless: 是否使用无头模式
        slow_mo: 慢动作延迟（毫秒）
    
    Returns:
        BrowserContext: 配置好的浏览器上下文
    """
    options = get_browser_context_options(headless, slow_mo)
    return playwright_instance.chromium.launch_persistent_context(**options)

def create_configured_page(context):
    """
    创建配置好的页面（应用反检测）
    
    Args:
        context: 浏览器上下文
    
    Returns:
        Page: 配置好的页面对象
    """
    page = context.new_page()
    apply_stealth_and_scripts(page)
    return page

def get_main_browser_config():
    """
    获取main.py使用的浏览器配置
    根据配置决定无头模式和慢动作延迟
    
    Returns:
        tuple: (headless_mode, slow_mo)
    """
    is_visual_mode = config.ENABLE_VISUAL_SCRAPING
    
    if is_visual_mode:
        headless_mode = False  # 可视化模式强制显示浏览器
        slow_mo = config.VISUAL_SCRAPING_SLOW_MO
    else:
        headless_mode = config.HEADLESS_MODE  # 按照配置决定
        slow_mo = 0
    
    return headless_mode, slow_mo

def get_init_browser_config():
    """
    获取initialize_profile.py使用的浏览器配置
    初始化时总是显示浏览器窗口
    
    Returns:
        tuple: (headless_mode, slow_mo)
    """
    return False, 0  # 初始化时总是显示浏览器，无延迟

# 向后兼容的常量导出
__all__ = [
    'USER_DATA_DIR',
    'USER_AGENT',
    'get_browser_args',
    'get_browser_context_options',
    'apply_stealth_and_scripts',
    'create_browser_context',
    'create_configured_page',
    'get_main_browser_config',
    'get_init_browser_config'
]