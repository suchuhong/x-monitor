#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def get_chat_id():
    """获取与Bot对话的Chat ID"""
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(api_url, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Bot收到的消息:")
            
            if data['result']:
                for update in data['result']:
                    if 'message' in update:
                        chat = update['message']['chat']
                        print(f"Chat ID: {chat['id']}")
                        print(f"Chat类型: {chat['type']}")
                        if 'username' in chat:
                            print(f"用户名: {chat['username']}")
                        if 'first_name' in chat:
                            print(f"名字: {chat['first_name']}")
                        print("---")
                        
                        # 返回第一个找到的chat ID
                        return str(chat['id'])
            else:
                print("没有找到任何消息。请确保:")
                print("1. 你已经在Telegram中找到了你的Bot")
                print("2. 向Bot发送了 /start 命令")
                print("3. 向Bot发送了至少一条消息")
        else:
            print(f"获取更新失败: {response.text}")
            
    except Exception as e:
        print(f"错误: {e}")
    
    return None

if __name__ == "__main__":
    print(f"Bot Token: {TELEGRAM_BOT_TOKEN}")
    print("正在获取Chat ID...")
    
    chat_id = get_chat_id()
    if chat_id:
        print(f"\n✅ 找到Chat ID: {chat_id}")
        print(f"请将此Chat ID更新到.env文件中:")
        print(f"TELEGRAM_CHAT_ID={chat_id}")
    else:
        print("\n❌ 未找到Chat ID")
        print("请按照以下步骤操作:")
        print("1. 在Telegram中搜索你的Bot")
        print("2. 点击'Start'按钮")
        print("3. 发送任意消息给Bot")
        print("4. 重新运行此脚本")