#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def verify_bot():
    """验证Bot Token是否有效"""
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(api_url, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                bot_info = data['result']
                print(f"✅ Bot验证成功!")
                print(f"Bot名称: {bot_info['first_name']}")
                print(f"Bot用户名: @{bot_info['username']}")
                print(f"Bot ID: {bot_info['id']}")
                return True
            else:
                print("❌ Bot验证失败")
                return False
        else:
            print("❌ Bot Token无效")
            return False
            
    except Exception as e:
        print(f"错误: {e}")
        return False

if __name__ == "__main__":
    print(f"Bot Token: {TELEGRAM_BOT_TOKEN}")
    verify_bot()