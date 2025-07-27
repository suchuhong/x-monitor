"""
日志配置模块
提供统一的日志配置和管理功能
"""
import os
import logging
import logging.handlers
from datetime import datetime
from typing import Optional
from . import config

class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""
    
    # ANSI 颜色代码
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m', # 紫色
        'RESET': '\033[0m'      # 重置
    }
    
    def format(self, record):
        # 添加颜色
        if hasattr(record, 'levelname'):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        
        # 格式化消息
        formatted = super().format(record)
        return formatted

class XMonitorLogger:
    """X Monitor 专用日志管理器"""
    
    def __init__(self):
        self.logger = None
        self.log_dir = "logs"
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志配置"""
        # 创建日志目录
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 获取日志级别配置
        log_level = getattr(config, 'LOG_LEVEL', 'INFO').upper()
        enable_file_logging = getattr(config, 'ENABLE_FILE_LOGGING', True)
        enable_console_logging = getattr(config, 'ENABLE_CONSOLE_LOGGING', True)
        
        # 创建根日志器
        self.logger = logging.getLogger('x_monitor')
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))
        
        # 清除现有的处理器
        self.logger.handlers.clear()
        
        # 控制台处理器
        if enable_console_logging:
            console_handler = logging.StreamHandler()
            console_formatter = ColoredFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # 文件处理器
        if enable_file_logging:
            # 主日志文件（所有日志）
            main_log_file = os.path.join(self.log_dir, 'x_monitor.log')
            file_handler = logging.handlers.RotatingFileHandler(
                main_log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # 错误日志文件（只记录错误）
            error_log_file = os.path.join(self.log_dir, 'errors.log')
            error_handler = logging.handlers.RotatingFileHandler(
                error_log_file,
                maxBytes=5*1024*1024,  # 5MB
                backupCount=3,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(file_formatter)
            self.logger.addHandler(error_handler)
            
            # 推文日志文件（专门记录推文相关信息）
            tweet_log_file = os.path.join(self.log_dir, 'tweets.log')
            tweet_handler = logging.handlers.RotatingFileHandler(
                tweet_log_file,
                maxBytes=20*1024*1024,  # 20MB
                backupCount=10,
                encoding='utf-8'
            )
            tweet_formatter = logging.Formatter(
                '%(asctime)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            tweet_handler.setFormatter(tweet_formatter)
            
            # 创建推文专用日志器
            tweet_logger = logging.getLogger('x_monitor.tweets')
            tweet_logger.setLevel(logging.INFO)
            tweet_logger.addHandler(tweet_handler)
            tweet_logger.propagate = False  # 不传播到父日志器
        
        # 防止重复日志
        self.logger.propagate = False
    
    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """获取日志器"""
        if name:
            return logging.getLogger(f'x_monitor.{name}')
        return self.logger
    
    def log_tweet_found(self, user: str, tweet_id: str, timestamp: str, content: str, is_new: bool = True):
        """记录发现的推文"""
        tweet_logger = logging.getLogger('x_monitor.tweets')
        status = "新推文" if is_new else "已见推文"
        tweet_logger.info(f"[{status}] 用户: {user} | ID: {tweet_id} | 时间: {timestamp} | 内容: {content[:100]}...")
    
    def log_scraping_start(self, user: str, days: int, max_tweets: int):
        """记录开始抓取"""
        self.logger.info(f"开始抓取用户 {user} 的推文 (最近{days}天, 最多{max_tweets}条)")
    
    def log_scraping_result(self, user: str, found_count: int, new_count: int):
        """记录抓取结果"""
        self.logger.info(f"用户 {user} 抓取完成: 找到 {found_count} 条推文, 其中 {new_count} 条为新推文")
    
    def log_notification_sent(self, user: str, tweet_id: str, success: bool = True):
        """记录通知发送"""
        status = "成功" if success else "失败"
        self.logger.info(f"推文通知发送{status}: 用户 {user}, ID: {tweet_id}")
    
    def log_round_start(self, round_num: int = None):
        """记录监控轮次开始"""
        if round_num:
            self.logger.info(f"=" * 60)
            self.logger.info(f"开始第 {round_num} 轮监控检查")
            self.logger.info(f"=" * 60)
        else:
            self.logger.info("=" * 60)
            self.logger.info("开始新一轮监控检查")
            self.logger.info("=" * 60)
    
    def log_round_end(self, total_new_tweets: int, next_check_seconds: int):
        """记录监控轮次结束"""
        self.logger.info(f"本轮检查完成: 发现 {total_new_tweets} 条新推文")
        self.logger.info(f"等待 {next_check_seconds} 秒后进行下一轮检查")
        self.logger.info("=" * 60)

# 全局日志管理器实例
_logger_manager = None

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """获取日志器的便捷函数"""
    global _logger_manager
    if _logger_manager is None:
        _logger_manager = XMonitorLogger()
    return _logger_manager.get_logger(name)

def log_tweet_found(user: str, tweet_id: str, timestamp: str, content: str, is_new: bool = True):
    """记录发现推文的便捷函数"""
    global _logger_manager
    if _logger_manager is None:
        _logger_manager = XMonitorLogger()
    _logger_manager.log_tweet_found(user, tweet_id, timestamp, content, is_new)

def log_scraping_start(user: str, days: int, max_tweets: int):
    """记录开始抓取的便捷函数"""
    global _logger_manager
    if _logger_manager is None:
        _logger_manager = XMonitorLogger()
    _logger_manager.log_scraping_start(user, days, max_tweets)

def log_scraping_result(user: str, found_count: int, new_count: int):
    """记录抓取结果的便捷函数"""
    global _logger_manager
    if _logger_manager is None:
        _logger_manager = XMonitorLogger()
    _logger_manager.log_scraping_result(user, found_count, new_count)

def log_notification_sent(user: str, tweet_id: str, success: bool = True):
    """记录通知发送的便捷函数"""
    global _logger_manager
    if _logger_manager is None:
        _logger_manager = XMonitorLogger()
    _logger_manager.log_notification_sent(user, tweet_id, success)

def log_round_start(round_num: int = None):
    """记录监控轮次开始的便捷函数"""
    global _logger_manager
    if _logger_manager is None:
        _logger_manager = XMonitorLogger()
    _logger_manager.log_round_start(round_num)

def log_round_end(total_new_tweets: int, next_check_seconds: int):
    """记录监控轮次结束的便捷函数"""
    global _logger_manager
    if _logger_manager is None:
        _logger_manager = XMonitorLogger()
    _logger_manager.log_round_end(total_new_tweets, next_check_seconds)