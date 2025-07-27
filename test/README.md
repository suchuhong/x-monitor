# 测试脚本说明

这个目录包含了 X Monitor 项目的各种测试和调试脚本。

## 脚本分类概览

- **Telegram 相关测试**: 验证 Bot Token、Chat ID 和通知功能
- **浏览器和登录测试**: 检查登录状态、浏览器配置和无头模式
- **推文抓取测试**: 测试和调试推文抓取功能
- **日志和调试工具**: 配置助手、日志查看和分析工具

## Telegram 相关测试

### `get_chat_id.py`
获取你的 Telegram Chat ID。

**使用方法:**
```bash
python test/get_chat_id.py
```

**前提条件:**
- 已在 `.env` 文件中配置 `TELEGRAM_BOT_TOKEN`
- 已与你的 Bot 开始对话并发送过消息

### `test_telegram.py`
测试 Telegram API 基础功能。

**使用方法:**
```bash
python test/test_telegram.py
```

**功能:**
- 测试简单文本消息发送
- 测试 HTML 格式消息发送
- 测试带用户标签的消息
- 显示详细的错误信息

### `test_notifier.py`
测试 notifier 模块的完整功能。

**使用方法:**
```bash
python test/test_notifier.py
```

**功能:**
- 测试各种消息格式
- 测试用户标签自动添加功能
- 模拟真实推文通知
- 测试长消息处理

### `verify_bot.py`
验证 Telegram Bot Token 是否有效。

**使用方法:**
```bash
python test/verify_bot.py
```

## 浏览器和登录测试

### `check_login.py`
检查 X.com 登录状态。

**使用方法:**
```bash
python test/check_login.py
```

**功能:**
- 检查是否已登录 X.com
- 显示详细的登录状态信息
- 可视化浏览器窗口，方便观察

### `test_headless.py`
测试浏览器无头模式。

**使用方法:**
```bash
python test/test_headless.py
```

**功能:**
- 验证浏览器无头模式配置是否正确
- 测试基本的页面访问功能
- 检查 User Agent 和反检测配置
- 适合排查浏览器显示问题

### `test_main_browser.py`
测试 main.py 的浏览器启动逻辑。

**使用方法:**
```bash
python test/test_main_browser.py
```

**功能:**
- 完全复制 main.py 的浏览器配置逻辑
- 详细显示配置参数和调试信息
- 验证可视化模式和无头模式的切换
- 适合排查配置与实际行为不一致的问题

### `reinitialize_profile.py`
重新初始化浏览器配置文件。

**使用方法:**
```bash
python test/reinitialize_profile.py
```

**功能:**
- 备份现有浏览器配置文件
- 清除可能损坏的登录数据
- 重新进行登录初始化

**注意:** 这会删除现有的登录状态，需要重新登录。

## 推文抓取测试

### `test_scraper.py`
测试推文抓取功能。

**使用方法:**
```bash
python test/test_scraper.py
```

**功能:**
- 可视化模式运行浏览器
- 让你选择要测试的用户
- 显示抓取到的推文详情
- 适合快速测试抓取功能

### `debug_scraper.py`
调试模式的推文抓取。

**使用方法:**
```bash
python test/debug_scraper.py
```

**功能:**
- 逐步执行抓取过程
- 在关键步骤暂停等待确认
- 详细分析每个推文元素
- 适合深入调试抓取问题

## 日志和调试工具

### `configure_browser_mode.py`
浏览器模式配置助手。

**使用方法:**
```bash
python test/configure_browser_mode.py
```

**功能:**
- 交互式配置浏览器模式
- 提供预设的使用场景选择
- 自动更新.env文件
- 验证配置正确性

### `test_browser_modes.py`
浏览器模式配置测试工具。

**使用方法:**
```bash
python test/test_browser_modes.py
```

**功能:**
- 显示当前浏览器模式配置
- 解释不同配置组合的行为
- 提供配置建议
- 模拟不同配置的结果

### `log_viewer.py`
日志查看和分析工具。

**使用方法:**
```bash
# 查看主日志（最近50行）
python test/log_viewer.py main

# 查看推文日志（最近30行）
python test/log_viewer.py tweets

# 查看错误日志
python test/log_viewer.py errors

# 分析日志统计信息
python test/log_viewer.py analyze

# 实时监控日志（类似 tail -f）
python test/log_viewer.py tail

# 指定显示行数
python test/log_viewer.py tail --lines 50
```

**功能:**
- 彩色显示不同级别的日志
- 统计分析日志信息
- 实时监控新日志
- 专门查看推文和错误日志

### `visual_scraper.py`
可视化抓取测试工具。

**使用方法:**
```bash
# 自动测试模式（选择用户进行可视化抓取）
python test/visual_scraper.py test

# 交互式模式（手动控制浏览器）
python test/visual_scraper.py interactive
```

**功能:**
- 可视化显示抓取过程
- 慢动作模式便于观察
- 交互式调试模式
- 详细的步骤说明
- 适合理解抓取机制和调试问题

## 使用建议

### 首次设置时
1. 运行 `python test/verify_bot.py` 验证 Bot Token
2. 运行 `python test/get_chat_id.py` 获取 Chat ID
3. 运行 `python test/test_telegram.py` 测试基础API功能
4. 运行 `python test/test_notifier.py` 测试完整通知功能
5. 运行 `python test/check_login.py` 检查登录状态

### 遇到问题时
1. **Telegram 通知失败**: 使用 `test_telegram.py`、`test_notifier.py` 和 `verify_bot.py`
2. **登录问题**: 使用 `check_login.py`，必要时使用 `reinitialize_profile.py`
3. **浏览器显示问题**: 使用 `test_headless.py` 验证无头模式，或 `test_main_browser.py` 检查启动逻辑
4. **抓取问题**: 使用 `test_scraper.py` 快速测试，或 `debug_scraper.py` 详细调试

### 开发调试时
- 使用 `debug_scraper.py` 来理解抓取过程
- 使用 `test_scraper.py` 来快速验证修改效果
- 使用 `visual_scraper.py` 来可视化观察抓取过程
- 使用 `check_login.py` 来确认登录状态
- 使用 `test_headless.py` 来验证浏览器无头模式配置
- 使用 `test_main_browser.py` 来调试浏览器启动逻辑
- 使用 `log_viewer.py` 来查看详细的运行日志和调试信息

## 注意事项

- 所有脚本都需要在项目根目录下运行
- 确保已安装所有依赖 (`uv sync`)
- 确保已配置 `.env` 文件
- 浏览器相关脚本需要先运行 `initialize_profile.py` 完成初始登录