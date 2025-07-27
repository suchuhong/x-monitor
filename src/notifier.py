import requests
from . import config, logger

# 获取日志器
log = logger.get_logger('notifier')

def send_telegram_notification(message: str, username: str = None) -> bool:
    """
    使用Telegram Bot API发送消息
    
    Args:
        message: 要发送的消息内容
        username: 用户名，用于生成标签
        
    Returns:
        bool: 发送是否成功
    """
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        log.warning("Telegram Bot Token 或 Chat ID 未配置，跳过通知")
        return False

    api_url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # 如果提供了用户名，添加标签
    final_message = message
    if username:
        user_tag = f"#{username}"
        final_message = f"{message}\n\n{user_tag}"
    
    payload = {
        'chat_id': config.TELEGRAM_CHAT_ID,
        'text': final_message,
        'parse_mode': 'HTML' # 允许简单的HTML格式
    }
    
    try:
        response = requests.post(api_url, data=payload, timeout=10)
        
        if response.status_code != 200:
            log.error(f"Telegram API返回错误: {response.status_code}")
            log.error(f"响应内容: {response.text}")
            
            # 尝试不使用HTML格式重新发送
            log.info("尝试以纯文本格式重新发送...")
            payload_plain = {
                'chat_id': config.TELEGRAM_CHAT_ID,
                'text': _strip_html(final_message),
                'parse_mode': None
            }
            response = requests.post(api_url, data=payload_plain, timeout=10)
        
        response.raise_for_status() # 如果请求失败则抛出异常
        log.debug(f"成功发送通知到 Chat ID: {config.TELEGRAM_CHAT_ID}")
        return True
        
    except requests.exceptions.RequestException as e:
        log.error(f"发送Telegram通知失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            log.error(f"错误详情: {e.response.text}")
        return False

def _strip_html(text: str) -> str:
    """移除HTML标签"""
    import re
    # 简单的HTML标签移除
    text = re.sub(r'<b>(.*?)</b>', r'\1', text)
    text = re.sub(r'<a href=[\'"]([^\'"]*)[\'"]>(.*?)</a>', r'\2 (\1)', text)
    return text