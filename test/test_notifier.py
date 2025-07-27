#!/usr/bin/env python3
"""
测试notifier模块的Telegram通知功能
"""
import sys
import os
sys.path.append('src')

import notifier

def test_notifier():
    """测试notifier模块的功能"""
    print("=" * 60)
    print("测试 notifier 模块")
    print("=" * 60)
    
    # 测试1: 简单消息（无用户标签）
    print("1. 测试简单消息（无用户标签）")
    simple_message = "这是一条测试消息"
    success = notifier.send_telegram_notification(simple_message)
    print(f"   结果: {'✅ 成功' if success else '❌ 失败'}")
    
    # 测试2: HTML格式消息（无用户标签）
    print("\n2. 测试HTML格式消息（无用户标签）")
    html_message = "<b>测试消息</b>\n\n这是一条<b>HTML格式</b>的测试消息"
    success = notifier.send_telegram_notification(html_message)
    print(f"   结果: {'✅ 成功' if success else '❌ 失败'}")
    
    # 测试3: 带用户标签的消息
    print("\n3. 测试带用户标签的消息")
    tagged_message = "<b>新动态!</b>\n\n<b>用户:</b> testuser\n<b>内容:</b>\n这是一条测试推文内容"
    success = notifier.send_telegram_notification(tagged_message, "testuser")
    print(f"   结果: {'✅ 成功' if success else '❌ 失败'}")
    
    # 测试4: 模拟真实推文通知
    print("\n4. 测试模拟真实推文通知")
    real_tweet_message = (
        "<b>新动态!</b>\n\n"
        "<b>用户:</b> elonmusk\n"
        "<b>内容:</b>\n"
        "Just had a great meeting about the future of sustainable transport. "
        "Exciting times ahead! 🚀\n\n"
        "<a href='https://x.com/elonmusk/status/1234567890'>查看原文</a>"
    )
    success = notifier.send_telegram_notification(real_tweet_message, "elonmusk")
    print(f"   结果: {'✅ 成功' if success else '❌ 失败'}")
    
    # 测试5: 长消息测试
    print("\n5. 测试长消息")
    long_message = (
        "<b>新动态!</b>\n\n"
        "<b>用户:</b> longuser\n"
        "<b>内容:</b>\n"
        + "这是一条很长的测试消息。" * 20 + "\n\n"
        "<a href='https://x.com/longuser/status/9876543210'>查看原文</a>"
    )
    success = notifier.send_telegram_notification(long_message, "longuser")
    print(f"   结果: {'✅ 成功' if success else '❌ 失败'}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print("\n注意事项:")
    print("- 用户标签会自动添加到消息末尾")
    print("- 格式为 #用户名")
    print("- 如果HTML格式失败，会自动尝试纯文本格式")
    print("- 检查你的Telegram Bot配置是否正确")

if __name__ == "__main__":
    test_notifier()