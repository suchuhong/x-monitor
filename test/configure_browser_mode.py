#!/usr/bin/env python3
"""
浏览器模式配置助手
帮助用户设置正确的浏览器模式配置
"""
import os
import sys

def read_env_file():
    """读取.env文件内容"""
    env_path = ".env"
    if not os.path.exists(env_path):
        print("❌ .env文件不存在，请先创建.env文件")
        return None
    
    with open(env_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_env_file(content):
    """写入.env文件"""
    with open(".env", 'w', encoding='utf-8') as f:
        f.write(content)

def update_env_setting(content, key, value):
    """更新.env文件中的设置"""
    lines = content.split('\n')
    updated = False
    
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            updated = True
            break
    
    if not updated:
        # 如果没找到，添加到相应的部分
        for i, line in enumerate(lines):
            if "Browser Visualization Configuration" in line:
                # 在这个部分后面添加
                insert_pos = i + 1
                while insert_pos < len(lines) and lines[insert_pos].strip() and not lines[insert_pos].startswith('#'):
                    insert_pos += 1
                lines.insert(insert_pos, f"{key}={value}")
                updated = True
                break
    
    return '\n'.join(lines)

def configure_browser_mode():
    """配置浏览器模式"""
    print("=" * 80)
    print("浏览器模式配置助手")
    print("=" * 80)
    
    print("请选择你的使用场景:")
    print("1. 生产环境 - 无头模式，性能最佳")
    print("2. 快速调试 - 可视模式，无延迟")
    print("3. 详细调试 - 可视化抓取模式，有延迟便于观察")
    print("4. 自定义配置")
    print("5. 查看当前配置")
    
    while True:
        try:
            choice = input("\n请输入选择 (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                break
            else:
                print("请输入有效的选择 (1-5)")
        except KeyboardInterrupt:
            print("\n操作已取消")
            return
    
    content = read_env_file()
    if content is None:
        return
    
    if choice == '5':
        # 查看当前配置
        print("\n当前配置:")
        for line in content.split('\n'):
            if 'HEADLESS_MODE=' in line or 'ENABLE_VISUAL_SCRAPING=' in line or 'VISUAL_SCRAPING_SLOW_MO=' in line:
                print(f"  {line}")
        
        # 解释当前配置
        headless = "true" in content and "HEADLESS_MODE=true" in content
        visual = "ENABLE_VISUAL_SCRAPING=true" in content
        
        print(f"\n当前行为:")
        if visual:
            print("  ✅ 可视化抓取模式 - 浏览器可见，有延迟")
        elif not headless:
            print("  ✅ 普通可视模式 - 浏览器可见，无延迟")
        else:
            print("  ✅ 无头模式 - 浏览器不可见")
        return
    
    # 配置设置
    configs = {
        '1': {  # 生产环境
            'HEADLESS_MODE': 'true',
            'ENABLE_VISUAL_SCRAPING': 'false',
            'description': '生产环境 - 无头模式，性能最佳'
        },
        '2': {  # 快速调试
            'HEADLESS_MODE': 'false',
            'ENABLE_VISUAL_SCRAPING': 'false',
            'description': '快速调试 - 可视模式，无延迟'
        },
        '3': {  # 详细调试
            'HEADLESS_MODE': 'true',  # 这个会被ENABLE_VISUAL_SCRAPING覆盖
            'ENABLE_VISUAL_SCRAPING': 'true',
            'description': '详细调试 - 可视化抓取模式，有延迟便于观察'
        }
    }
    
    if choice in configs:
        config = configs[choice]
        print(f"\n将配置为: {config['description']}")
        
        # 更新配置
        content = update_env_setting(content, 'HEADLESS_MODE', config['HEADLESS_MODE'])
        content = update_env_setting(content, 'ENABLE_VISUAL_SCRAPING', config['ENABLE_VISUAL_SCRAPING'])
        
        # 如果是可视化模式，询问延迟时间
        if config['ENABLE_VISUAL_SCRAPING'] == 'true':
            while True:
                try:
                    slow_mo = input("请输入操作延迟时间（毫秒，默认1000）: ").strip()
                    if not slow_mo:
                        slow_mo = "1000"
                    int(slow_mo)  # 验证是否为数字
                    break
                except ValueError:
                    print("请输入有效的数字")
            
            content = update_env_setting(content, 'VISUAL_SCRAPING_SLOW_MO', slow_mo)
        
        # 确认更改
        confirm = input("确认应用这些更改吗? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            write_env_file(content)
            print("✅ 配置已更新")
            print("\n新配置:")
            print(f"  HEADLESS_MODE={config['HEADLESS_MODE']}")
            print(f"  ENABLE_VISUAL_SCRAPING={config['ENABLE_VISUAL_SCRAPING']}")
            if config['ENABLE_VISUAL_SCRAPING'] == 'true':
                print(f"  VISUAL_SCRAPING_SLOW_MO={slow_mo}")
        else:
            print("配置未更改")
    
    elif choice == '4':
        # 自定义配置
        print("\n自定义配置:")
        
        # HEADLESS_MODE
        while True:
            headless = input("HEADLESS_MODE (true/false): ").strip().lower()
            if headless in ['true', 'false']:
                break
            print("请输入 true 或 false")
        
        # ENABLE_VISUAL_SCRAPING
        while True:
            visual = input("ENABLE_VISUAL_SCRAPING (true/false): ").strip().lower()
            if visual in ['true', 'false']:
                break
            print("请输入 true 或 false")
        
        # VISUAL_SCRAPING_SLOW_MO
        if visual == 'true':
            while True:
                try:
                    slow_mo = input("VISUAL_SCRAPING_SLOW_MO (毫秒): ").strip()
                    int(slow_mo)
                    break
                except ValueError:
                    print("请输入有效的数字")
        else:
            slow_mo = "1000"  # 默认值
        
        # 显示预期行为
        print(f"\n预期行为:")
        if visual == 'true':
            print("  ✅ 可视化抓取模式 - 浏览器可见，有延迟")
        elif headless == 'false':
            print("  ✅ 普通可视模式 - 浏览器可见，无延迟")
        else:
            print("  ✅ 无头模式 - 浏览器不可见")
        
        # 确认更改
        confirm = input("确认应用这些更改吗? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            content = update_env_setting(content, 'HEADLESS_MODE', headless)
            content = update_env_setting(content, 'ENABLE_VISUAL_SCRAPING', visual)
            content = update_env_setting(content, 'VISUAL_SCRAPING_SLOW_MO', slow_mo)
            
            write_env_file(content)
            print("✅ 配置已更新")
        else:
            print("配置未更改")

if __name__ == "__main__":
    configure_browser_mode()