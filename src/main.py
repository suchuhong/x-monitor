import os
import time
from playwright.sync_api import sync_playwright, Playwright
from . import config, database, notifier, scraper, logger, browser_config

# 获取日志器
log = logger.get_logger('main')

def process_all_users():
    """主处理函数，监控所有配置的用户"""
    logger.log_round_start()
    seen_tweet_ids = database.load_seen_tweet_ids(config.DB_FILE_PATH)
    all_new_tweets = []

    # 检查浏览器配置文件是否存在
    if not os.path.exists(browser_config.USER_DATA_DIR):
        log.error(f"浏览器配置文件目录 '{browser_config.USER_DATA_DIR}' 未找到")
        log.error("请先运行 'python initialize_profile.py' 来完成首次登录和初始化")
        return

    with sync_playwright() as p:
        context = None # 先声明 context
        try:
            # === 使用统一的浏览器配置，确保与initialize_profile.py完全一致 ===
            headless_mode, slow_mo = browser_config.get_main_browser_config()
            
            # 记录浏览器模式
            is_visual_mode = config.ENABLE_VISUAL_SCRAPING
            if is_visual_mode:
                log.info("启用可视化抓取模式 - 浏览器窗口将可见")
                log.info(f"可视化延迟: {slow_mo} 毫秒")
            else:
                log.info(f"浏览器模式: {'无头模式' if headless_mode else '可视模式'}")
            
            # 创建浏览器上下文和页面
            context = browser_config.create_browser_context(p, headless_mode, slow_mo)
            page = browser_config.create_configured_page(context)
            # =====================

            for user in config.TARGET_USERS:
                if not user: continue
                
                user = user.strip()
                logger.log_scraping_start(user, config.DAYS_TO_SCRAPE, config.MAX_TWEETS_PER_USER)
                
                found_tweets = scraper.scrape_user_tweets(page, user)
                new_tweets_count = 0
                
                log.info(f"用户 {user}: 检查 {len(found_tweets)} 条推文是否为新推文...")
                
                for tweet in found_tweets:
                    is_new = tweet['id'] not in seen_tweet_ids
                    
                    # 记录推文发现
                    logger.log_tweet_found(
                        tweet['user'], 
                        tweet['id'], 
                        tweet['timestamp'], 
                        tweet['text'], 
                        is_new
                    )
                    
                    if is_new:
                        all_new_tweets.append(tweet)
                        seen_tweet_ids.add(tweet['id'])
                        new_tweets_count += 1
                
                logger.log_scraping_result(user, len(found_tweets), new_tweets_count)
        
        except Exception as e:
            log.error(f"Playwright 执行过程中发生未知错误: {e}", exc_info=True)
        finally:
            if context:
                context.close()

    if all_new_tweets:
        # 按时间戳排序，最新的推文先通知
        all_new_tweets.sort(key=lambda x: x['timestamp'], reverse=True)
        log.info(f"准备发送 {len(all_new_tweets)} 条新推文通知（按时间从新到旧）")
        
        # 显示将要发送通知的推文列表
        log.info("新推文通知列表:")
        for i, tweet in enumerate(all_new_tweets):
            log.info(f"  {i+1}. 用户: {tweet['user']}, ID: {tweet['id']}, 时间: {tweet['timestamp']}")
        
        for tweet in all_new_tweets:
            message = (
                f"<b>新动态!</b>\n\n"
                f"<b>用户:</b> {tweet['user']}\n"
                f"<b>内容:</b>\n{tweet['text'][:1000]}\n\n" # 限制长度避免消息过长
                f"<a href='{tweet['url']}'>查看原文</a>"
            )
            success = notifier.send_telegram_notification(message, tweet['user'])
            logger.log_notification_sent(tweet['user'], tweet['id'], success)
            time.sleep(1) # 短暂延迟，避免触发Telegram的速率限制

        database.save_seen_tweet_ids(config.DB_FILE_PATH, seen_tweet_ids)
        log.info(f"处理完成，共发现 {len(all_new_tweets)} 条新推文，数据库已更新")
    
    logger.log_round_end(len(all_new_tweets), config.MONITOR_INTERVAL_SECONDS)


def main():
    """主入口函数"""
    log.info("X Monitor 启动")
    log.info(f"监控用户: {', '.join([u.strip() for u in config.TARGET_USERS if u.strip()])}")
    log.info(f"检查间隔: {config.MONITOR_INTERVAL_SECONDS} 秒")
    log.info(f"抓取天数: {config.DAYS_TO_SCRAPE} 天")
    log.info(f"每用户最大推文数: {config.MAX_TWEETS_PER_USER} 条")
    log.info(f"无头模式: {'启用' if config.HEADLESS_MODE else '禁用'}")
    log.info(f"可视化抓取: {'启用' if config.ENABLE_VISUAL_SCRAPING else '禁用'}")
    if config.ENABLE_VISUAL_SCRAPING:
        log.info(f"可视化延迟: {config.VISUAL_SCRAPING_SLOW_MO} 毫秒")
    
    round_num = 1
    try:
        while True:
            process_all_users()
            time.sleep(config.MONITOR_INTERVAL_SECONDS)
            round_num += 1
    except KeyboardInterrupt:
        log.info("收到中断信号，正在停止 X Monitor...")
    except Exception as e:
        log.error(f"程序发生未预期错误: {e}", exc_info=True)
    finally:
        log.info("X Monitor 已停止")


if __name__ == "__main__":
    main()