import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# Monitor Configuration
TARGET_USERS = os.getenv("TARGET_USERS", "").split(',')
MONITOR_INTERVAL_SECONDS = int(os.getenv("MONITOR_INTERVAL_SECONDS", 600))
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true").lower() == "true"

# Browser Visualization Configuration
ENABLE_VISUAL_SCRAPING = os.getenv("ENABLE_VISUAL_SCRAPING", "false").lower() == "true"  # 是否启用可视化抓取
VISUAL_SCRAPING_SLOW_MO = int(os.getenv("VISUAL_SCRAPING_SLOW_MO", 1000))  # 可视化模式下的操作延迟（毫秒）

# Tweet Date Range Configuration
DAYS_TO_SCRAPE = int(os.getenv("DAYS_TO_SCRAPE", 3))  # 默认获取最近3天的推文
MAX_TWEETS_PER_USER = int(os.getenv("MAX_TWEETS_PER_USER", 50))  # 每个用户最多获取的推文数量

# File Paths
DB_FILE_PATH = os.getenv("DB_FILE_PATH", "data/seen_tweets.json")

# Telegram Notification
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()  # DEBUG, INFO, WARNING, ERROR, CRITICAL
ENABLE_FILE_LOGGING = os.getenv("ENABLE_FILE_LOGGING", "true").lower() == "true"
ENABLE_CONSOLE_LOGGING = os.getenv("ENABLE_CONSOLE_LOGGING", "true").lower() == "true"
ENABLE_COLORED_LOGS = os.getenv("ENABLE_COLORED_LOGS", "true").lower() == "true"

# 确保必要的文件夹存在
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)