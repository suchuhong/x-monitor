#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def test_telegram():
    print(f"Bot Token: {TELEGRAM_BOT_TOKEN}")
    print(f"Chat ID: {TELEGRAM_CHAT_ID}")
    
    # 测试简单消息
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': "测试消息 - 简单文本"
    }
    
    try:
        response = requests.post(api_url, data=payload, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ 简单消息发送成功!")
        else:
            print("❌ 简单消息发送失败")
            return
            
        # 测试HTML格式消息
        payload_html = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': "<b>测试消息</b>\n\n<b>用户:</b> test\n<a href='https://example.com'>查看链接</a>",
            'parse_mode': 'HTML'
        }
        
        response = requests.post(api_url, data=payload_html, timeout=10)
        print(f"HTML消息状态码: {response.status_code}")
        print(f"HTML消息响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ HTML消息发送成功!")
        else:
            print("❌ HTML消息发送失败")
            return
        
        # 测试带用户标签的消息
        payload_with_tag = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': "<b>新动态!</b>\n\n<b>用户:</b> elonmusk\n<b>内容:</b>\n这是一条测试推文内容\n\n<a href='https://x.com/elonmusk/status/123456789'>查看原文</a>\n\n#elonmusk",
            'parse_mode': 'HTML'
        }
        
        response = requests.post(api_url, data=payload_with_tag, timeout=10)
        print(f"带标签消息状态码: {response.status_code}")
        print(f"带标签消息响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ 带用户标签消息发送成功!")
        else:
            print("❌ 带用户标签消息发送失败")
            
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    test_telegram()