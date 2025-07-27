# X Monitor - Twitter/X 用户动态监控工具

一个基于 Playwright 的 Twitter/X 用户动态监控工具，支持获取最近几天的推文并通过 Telegram 发送通知。

## 功能特性

- 🔍 监控指定 X/Twitter 用户的最新推文
- 📅 支持获取最近几天的推文（可配置天数）
- 🤖 通过 Telegram Bot 发送新推文通知（自动添加用户标签）
- 🔄 自动定时检查更新
- 💾 持久化存储已见推文，避免重复通知
- 🎭 使用 playwright-stealth 绕过反爬虫检测

## 前提条件

- **Python 3.8+**: 确保你的系统已安装 Python
- **uv**: 安装 uv 包管理器
  ```bash
  # macOS / Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # Windows
  irm https://astral.sh/uv/install.ps1 | iex
  ```
- **Telegram Bot**: 你需要一个自己的 Telegram Bot
  1. 在 Telegram 中与 @BotFather 对话
  2. 使用 `/newbot` 命令创建一个新的 Bot，获得 Bot Token
  3. 与你的 Bot 开始对话（发送 `/start` 命令）
  4. 运行 `python test/get_chat_id.py` 获取你的 Chat ID

## 快速开始

### 1. 克隆项目并安装依赖

```bash
# 进入项目目录
cd x-monitor

# 使用 uv 创建虚拟环境并安装依赖
uv sync

# 激活虚拟环境
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# 安装 Playwright 浏览器驱动
playwright install chromium
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并填写配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# --- Monitor Configuration ---
# 用逗号分隔的X用户名列表
TARGET_USERS=google,playwrightweb,elonmusk
# 监控检查的间隔时间（秒）
MONITOR_INTERVAL_SECONDS=1200
# 是否以无头模式运行浏览器 (true/false)
HEADLESS_MODE=true

# --- Tweet Scraping Configuration ---
# 获取最近几天的推文（天数）
DAYS_TO_SCRAPE=3
# 每个用户最多获取的推文数量
MAX_TWEETS_PER_USER=50

# --- Browser Visualization Configuration ---
# 是否启用可视化抓取模式 (true/false)
ENABLE_VISUAL_SCRAPING=false
# 可视化模式下的操作延迟（毫秒）
VISUAL_SCRAPING_SLOW_MO=1000

# --- Telegram Notification ---
# 从 @BotFather 获取的 Bot Token
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
# 你的 Chat ID
TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID
```

### 3. 初始化浏览器配置文件

```bash
python initialize_profile.py
```

这会打开一个浏览器窗口，请完成 X.com 的登录过程。

### 4. 运行监控程序

```bash
python -m src.main
```

## 可视化抓取模式

对于调试和观察抓取过程，可以启用可视化模式：

### 方法1：使用配置助手（推荐）
```bash
python test/configure_browser_mode.py
```
选择适合的使用场景，自动配置正确的参数。

### 方法2：手动修改配置文件
在 `.env` 文件中设置：
```env
ENABLE_VISUAL_SCRAPING=true
VISUAL_SCRAPING_SLOW_MO=2000
```

然后正常运行程序，浏览器窗口将可见，操作会有延迟便于观察。

### 方法2：使用专门的测试工具
```bash
# 自动测试模式
python test/visual_scraper.py test

# 交互式模式（手动控制）
python test/visual_scraper.py interactive
```

## 配置说明

### 监控配置
- `TARGET_USERS`: 要监控的 X 用户名列表，用逗号分隔
- `MONITOR_INTERVAL_SECONDS`: 检查间隔时间（秒）
- `HEADLESS_MODE`: 是否以无头模式运行浏览器

### 浏览器可视化配置
- `ENABLE_VISUAL_SCRAPING`: 是否启用可视化抓取模式（调试用）
- `VISUAL_SCRAPING_SLOW_MO`: 可视化模式下的操作延迟（毫秒）

**配置组合说明:**
- `HEADLESS_MODE=true, ENABLE_VISUAL_SCRAPING=false`: 无头模式（生产环境推荐）
- `HEADLESS_MODE=false, ENABLE_VISUAL_SCRAPING=false`: 普通可视模式（快速调试）
- `ENABLE_VISUAL_SCRAPING=true`: 可视化抓取模式（详细调试，会覆盖HEADLESS_MODE）

### 推文抓取配置
- `DAYS_TO_SCRAPE`: 获取最近几天的推文（默认3天）
- `MAX_TWEETS_PER_USER`: 每个用户最多获取的推文数量（默认50条）

### Telegram 通知配置
- `TELEGRAM_BOT_TOKEN`: 从 @BotFather 获取的 Bot Token
- `TELEGRAM_CHAT_ID`: 你的 Telegram Chat ID

### 日志配置
- `LOG_LEVEL`: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `ENABLE_FILE_LOGGING`: 是否启用文件日志 (true/false)
- `ENABLE_CONSOLE_LOGGING`: 是否启用控制台日志 (true/false)
- `ENABLE_COLORED_LOGS`: 是否启用彩色日志 (true/false)

## 工具脚本

项目在 `test/` 目录中包含一些有用的工具脚本：

### Telegram 相关测试
- `test/get_chat_id.py`: 获取你的 Telegram Chat ID
- `test/test_telegram.py`: 测试 Telegram API 基础功能
- `test/test_notifier.py`: 测试 notifier 模块（包括用户标签功能）
- `test/verify_bot.py`: 验证 Telegram Bot Token 是否有效

### 浏览器和登录测试
- `test/check_login.py`: 检查 X.com 登录状态
- `test/reinitialize_profile.py`: 重新初始化浏览器配置文件
- `test/test_scraper.py`: 测试推文抓取功能
- `test/debug_scraper.py`: 调试模式的推文抓取（逐步执行）

### 日志和调试工具
- `test/log_viewer.py`: 日志查看和分析工具
- `test/visual_scraper.py`: 可视化抓取测试工具
- `test/test_browser_modes.py`: 浏览器模式配置测试
- `test/configure_browser_mode.py`: 浏览器模式配置助手

## 故障排除

如果遇到问题，请检查：

1. **浏览器配置文件**: 确保已运行 `initialize_profile.py` 并完成登录
2. **Telegram 配置**: 使用 `test/` 目录中的工具脚本验证 Bot Token 和 Chat ID
3. **网络连接**: 确保能够访问 X.com 和 Telegram API
4. **依赖安装**: 确保所有依赖都已正确安装

## 日志系统

项目使用分层日志系统，自动生成以下日志文件：

- `logs/x_monitor.log`: 主日志文件（所有日志）
- `logs/tweets.log`: 推文专用日志（推文发现和处理记录）
- `logs/errors.log`: 错误日志（仅记录错误和严重问题）

### 日志查看命令

```bash
# 查看主日志
python test/log_viewer.py main

# 查看推文日志
python test/log_viewer.py tweets

# 查看错误日志
python test/log_viewer.py errors

# 分析日志统计
python test/log_viewer.py analyze

# 实时监控日志
python test/log_viewer.py tail
```

## 注意事项

- 请遵守 X.com 的使用条款和 API 限制
- 建议设置合理的监控间隔，避免过于频繁的请求
- 首次运行时会获取最近几天的推文，可能会有较多通知
- 日志文件会自动轮转，避免占用过多磁盘空间
