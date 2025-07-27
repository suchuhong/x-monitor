import time
from datetime import datetime, timedelta, timezone
from typing import List, Dict
from playwright.sync_api import Page, TimeoutError
from . import config, logger

# 获取日志器
log = logger.get_logger('scraper')

def parse_tweet_time(time_element) -> datetime:
    """解析推文时间元素，返回datetime对象（时区无关）"""
    try:
        # 尝试获取time元素的datetime属性
        datetime_attr = time_element.get_attribute('datetime')
        if datetime_attr:
            # 解析ISO格式时间并转换为本地时间（时区无关）
            dt = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
            return dt.replace(tzinfo=None)  # 移除时区信息，统一使用时区无关的datetime
        
        # 如果没有datetime属性，尝试解析文本内容
        time_text = time_element.inner_text().strip()
        now = datetime.now()  # 时区无关的当前时间
        
        if '分钟' in time_text or 'min' in time_text or 'm' in time_text:
            minutes = int(''.join(filter(str.isdigit, time_text)))
            return now - timedelta(minutes=minutes)
        elif '小时' in time_text or 'hour' in time_text or 'h' in time_text:
            hours = int(''.join(filter(str.isdigit, time_text)))
            return now - timedelta(hours=hours)
        elif '天' in time_text or 'day' in time_text or 'd' in time_text:
            days = int(''.join(filter(str.isdigit, time_text)))
            return now - timedelta(days=days)
        else:
            # 如果无法解析，返回当前时间
            return now
            
    except Exception as e:
        log.warning(f"解析推文时间失败: {e}")
        return datetime.now()


def is_tweet_within_date_range(tweet_time: datetime, days_limit: int) -> bool:
    """检查推文是否在指定的日期范围内"""
    cutoff_date = datetime.now() - timedelta(days=days_limit)  # 时区无关的当前时间
    return tweet_time >= cutoff_date


def scrape_user_tweets(page: Page, username: str) -> List[Dict]:
    """
    抓取指定用户主页上最近几天的推文，按时间从新到旧排序。
    返回一个包含推文信息的字典列表。
    """
    url = f"https://x.com/{username}"
    log.info(f"访问用户页面: {url}")
    all_tweets = []  # 存储所有找到的推文
    processed_tweet_ids = set()  # 避免重复处理
    scroll_attempts = 0
    max_scroll_attempts = 5

    try:
        page.goto(url, wait_until="networkidle", timeout=60000)
        log.debug(f"成功访问页面: {url}")
    except TimeoutError:
        log.warning(f"访问 {url} 超时，但仍尝试继续处理")
    except Exception as e:
        log.error(f"访问 {url} 时发生严重错误: {e}")
        return []

    try:
        # X的前端选择器非常不稳定，这是目前常用的一个。如果失效，需要手动更新。
        tweet_selector = "article[data-testid='tweet']"
        page.wait_for_selector(tweet_selector, timeout=30000)
        log.debug(f"找到推文选择器: {tweet_selector}")
        
        # 滚动加载更多推文，直到获得足够的推文或达到日期限制
        consecutive_no_new_tweets = 0
        
        while len(all_tweets) < config.MAX_TWEETS_PER_USER and scroll_attempts < max_scroll_attempts:
            # 获取当前页面上所有推文元素
            tweet_elements = page.locator(tweet_selector).all()
            log.debug(f"用户 {username}: 页面上找到 {len(tweet_elements)} 个推文元素")

            found_old_tweets = False
            new_tweets_in_this_batch = 0
            
            for i, tweet_element in enumerate(tweet_elements):
                try:
                    # 寻找包含 /status/ 的链接来确定推文ID和URL
                    tweet_link_element = tweet_element.locator("a[href*='/status/']").filter(has_not_text="analytics").first
                    tweet_url = tweet_link_element.get_attribute('href')
                    
                    if not tweet_url or "/status/" not in tweet_url:
                        continue
                    
                    tweet_id = tweet_url.split('/status/')[-1].split('?')[0]
                    
                    # 检查是否已经处理过这条推文
                    if tweet_id in processed_tweet_ids:
                        continue
                    
                    processed_tweet_ids.add(tweet_id)
                    
                    # 尝试获取推文时间
                    time_element = tweet_element.locator("time").first
                    if time_element:
                        tweet_time = parse_tweet_time(time_element)
                        
                        # 检查推文是否在日期范围内
                        if not is_tweet_within_date_range(tweet_time, config.DAYS_TO_SCRAPE):
                            found_old_tweets = True
                            continue
                    else:
                        # 如果找不到时间元素，假设是最近的推文
                        tweet_time = datetime.now()
                    
                    # 提取推文文本
                    text_element = tweet_element.locator("[data-testid='tweetText']").first
                    tweet_text = text_element.inner_text() if text_element else ""

                    tweet_data = {
                        "id": tweet_id,
                        "text": tweet_text,
                        "url": f"https://x.com{tweet_url}",
                        "user": username,
                        "timestamp": tweet_time.isoformat(),
                        "datetime": tweet_time  # 用于排序
                    }
                    
                    all_tweets.append(tweet_data)
                    new_tweets_in_this_batch += 1
                    
                    log.debug(f"找到推文 ID: {tweet_id}, 时间: {tweet_time}, 内容: {tweet_text[:50]}...")
                        
                except Exception as e:
                    # 忽略解析单个推文时的错误，继续处理下一个
                    log.warning(f"解析推文 {i+1} 时出错: {e}")
                    continue
            
            log.debug(f"用户 {username}: 本轮找到 {new_tweets_in_this_batch} 条新推文，总计 {len(all_tweets)} 条")
            
            # 如果找到了超出日期范围的推文，说明已经加载了足够的历史内容
            if found_old_tweets and len(all_tweets) > 0:
                log.info(f"用户 {username}: 已找到超出日期范围的推文，停止加载更多内容")
                break
            
            # 如果连续几轮都没有找到新推文，可能已经到底了
            if new_tweets_in_this_batch == 0:
                consecutive_no_new_tweets += 1
                if consecutive_no_new_tweets >= 2:
                    log.info(f"用户 {username}: 连续 {consecutive_no_new_tweets} 轮未找到新推文，停止滚动")
                    break
            else:
                consecutive_no_new_tweets = 0
            
            # 如果还需要更多推文，尝试滚动加载
            if len(all_tweets) < config.MAX_TWEETS_PER_USER:
                log.debug(f"用户 {username}: 尝试滚动加载更多推文...")
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(3)  # 增加等待时间，确保内容加载
                scroll_attempts += 1
            else:
                break

    except TimeoutError:
        log.warning(f"在用户 {username} 页面上等待推文元素超时，页面可能未加载或没有推文")
    except Exception as e:
        log.error(f"在抓取用户 {username} 页面时发生错误: {e}")
        page.screenshot(path=f"error_screenshot_{username}.png")
        log.info(f"已保存错误截图: error_screenshot_{username}.png")

    # 按时间排序，最新的在前面
    all_tweets.sort(key=lambda x: x['datetime'], reverse=True)
    
    # 移除用于排序的datetime字段，只保留需要的数据
    result_tweets = []
    for tweet in all_tweets:
        result_tweet = {k: v for k, v in tweet.items() if k != 'datetime'}
        result_tweets.append(result_tweet)
    
    log.info(f"用户 {username}: 成功获取 {len(result_tweets)} 条推文")
    
    # 显示推文摘要（只在DEBUG级别显示详细列表）
    if result_tweets:
        if log.isEnabledFor(10):  # DEBUG级别
            log.debug(f"用户 {username}: 获取到的推文列表:")
            for i, tweet in enumerate(result_tweets):
                log.debug(f"  {i+1}. ID: {tweet['id']}, 时间: {tweet['timestamp']}")
        
        log.info(f"用户 {username}: 最新推文时间: {result_tweets[0]['timestamp']}")
        if len(result_tweets) > 1:
            log.info(f"用户 {username}: 最旧推文时间: {result_tweets[-1]['timestamp']}")
    else:
        log.warning(f"用户 {username}: 未获取到任何推文")
    
    return result_tweets