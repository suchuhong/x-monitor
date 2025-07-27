#!/usr/bin/env python3
"""
日志查看工具
用于查看和分析X Monitor的日志文件
"""
import os
import sys
import argparse
from datetime import datetime, timedelta
import re

def parse_log_line(line):
    """解析日志行"""
    # 匹配日志格式: 2025-01-27 16:41:04,911 - x_monitor.main - INFO - 消息
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - ([^-]+) - ([^-]+) - (.+)'
    match = re.match(pattern, line.strip())
    if match:
        return {
            'timestamp': match.group(1),
            'logger': match.group(2).strip(),
            'level': match.group(3).strip(),
            'message': match.group(4).strip()
        }
    return None

def filter_logs(logs, level=None, logger=None, since=None, until=None, keyword=None):
    """过滤日志"""
    filtered = []
    
    for log in logs:
        # 级别过滤
        if level and log['level'] != level.upper():
            continue
        
        # 日志器过滤
        if logger and logger.lower() not in log['logger'].lower():
            continue
        
        # 关键词过滤
        if keyword and keyword.lower() not in log['message'].lower():
            continue
        
        # 时间过滤
        try:
            log_time = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S,%f')
            if since and log_time < since:
                continue
            if until and log_time > until:
                continue
        except ValueError:
            continue
        
        filtered.append(log)
    
    return filtered

def view_main_log():
    """查看主日志文件"""
    log_file = "logs/x_monitor.log"
    if not os.path.exists(log_file):
        print(f"❌ 日志文件不存在: {log_file}")
        return
    
    print(f"📄 查看主日志文件: {log_file}")
    print("=" * 80)
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 显示最后50行
        recent_lines = lines[-50:] if len(lines) > 50 else lines
        
        for line in recent_lines:
            parsed = parse_log_line(line)
            if parsed:
                # 添加颜色
                color = {
                    'DEBUG': '\033[36m',
                    'INFO': '\033[32m',
                    'WARNING': '\033[33m',
                    'ERROR': '\033[31m',
                    'CRITICAL': '\033[35m'
                }.get(parsed['level'], '\033[0m')
                
                print(f"{color}{parsed['timestamp']} - {parsed['level']:<8}\033[0m {parsed['message']}")
            else:
                print(line.strip())
    
    except Exception as e:
        print(f"❌ 读取日志文件失败: {e}")

def view_tweet_log():
    """查看推文日志文件"""
    log_file = "logs/tweets.log"
    if not os.path.exists(log_file):
        print(f"❌ 推文日志文件不存在: {log_file}")
        return
    
    print(f"🐦 查看推文日志文件: {log_file}")
    print("=" * 80)
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 显示最后30行
        recent_lines = lines[-30:] if len(lines) > 30 else lines
        
        for line in recent_lines:
            if "[新推文]" in line:
                print(f"\033[32m{line.strip()}\033[0m")  # 绿色
            elif "[已见推文]" in line:
                print(f"\033[90m{line.strip()}\033[0m")  # 灰色
            else:
                print(line.strip())
    
    except Exception as e:
        print(f"❌ 读取推文日志文件失败: {e}")

def view_error_log():
    """查看错误日志文件"""
    log_file = "logs/errors.log"
    if not os.path.exists(log_file):
        print(f"✅ 没有错误日志文件，说明没有错误发生")
        return
    
    print(f"❌ 查看错误日志文件: {log_file}")
    print("=" * 80)
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.strip():
            print(f"\033[31m{content}\033[0m")  # 红色
        else:
            print("✅ 错误日志文件为空")
    
    except Exception as e:
        print(f"❌ 读取错误日志文件失败: {e}")

def analyze_logs():
    """分析日志统计信息"""
    log_file = "logs/x_monitor.log"
    if not os.path.exists(log_file):
        print(f"❌ 日志文件不存在: {log_file}")
        return
    
    print("📊 日志分析统计")
    print("=" * 80)
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        logs = []
        for line in lines:
            parsed = parse_log_line(line)
            if parsed:
                logs.append(parsed)
        
        if not logs:
            print("没有找到有效的日志条目")
            return
        
        # 统计信息
        total_logs = len(logs)
        level_counts = {}
        logger_counts = {}
        
        for log in logs:
            level_counts[log['level']] = level_counts.get(log['level'], 0) + 1
            logger_counts[log['logger']] = logger_counts.get(log['logger'], 0) + 1
        
        print(f"总日志条数: {total_logs}")
        print(f"时间范围: {logs[0]['timestamp']} 到 {logs[-1]['timestamp']}")
        
        print("\n📈 日志级别统计:")
        for level, count in sorted(level_counts.items()):
            percentage = (count / total_logs) * 100
            print(f"  {level:<8}: {count:>6} ({percentage:5.1f}%)")
        
        print("\n🔧 日志器统计:")
        for logger, count in sorted(logger_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_logs) * 100
            print(f"  {logger:<20}: {count:>6} ({percentage:5.1f}%)")
        
        # 查找推文相关统计
        tweet_logs = [log for log in logs if 'tweet' in log['message'].lower() or 'scraper' in log['logger']]
        if tweet_logs:
            print(f"\n🐦 推文相关日志: {len(tweet_logs)} 条")
        
        # 查找错误
        error_logs = [log for log in logs if log['level'] in ['ERROR', 'CRITICAL']]
        if error_logs:
            print(f"\n❌ 错误日志: {len(error_logs)} 条")
            print("最近的错误:")
            for log in error_logs[-5:]:
                print(f"  {log['timestamp']}: {log['message'][:80]}...")
    
    except Exception as e:
        print(f"❌ 分析日志失败: {e}")

def tail_log(lines=20):
    """实时查看日志"""
    log_file = "logs/x_monitor.log"
    if not os.path.exists(log_file):
        print(f"❌ 日志文件不存在: {log_file}")
        return
    
    print(f"👁️ 实时查看日志 (最后 {lines} 行)")
    print("按 Ctrl+C 退出")
    print("=" * 80)
    
    try:
        import time
        
        # 显示最后几行
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            
            for line in recent_lines:
                parsed = parse_log_line(line)
                if parsed:
                    color = {
                        'DEBUG': '\033[36m',
                        'INFO': '\033[32m',
                        'WARNING': '\033[33m',
                        'ERROR': '\033[31m',
                        'CRITICAL': '\033[35m'
                    }.get(parsed['level'], '\033[0m')
                    
                    print(f"{color}{parsed['timestamp']} - {parsed['level']:<8}\033[0m {parsed['message']}")
                else:
                    print(line.strip())
        
        # 监控新日志
        last_size = os.path.getsize(log_file)
        
        while True:
            time.sleep(1)
            current_size = os.path.getsize(log_file)
            
            if current_size > last_size:
                with open(log_file, 'r', encoding='utf-8') as f:
                    f.seek(last_size)
                    new_lines = f.readlines()
                    
                    for line in new_lines:
                        parsed = parse_log_line(line)
                        if parsed:
                            color = {
                                'DEBUG': '\033[36m',
                                'INFO': '\033[32m',
                                'WARNING': '\033[33m',
                                'ERROR': '\033[31m',
                                'CRITICAL': '\033[35m'
                            }.get(parsed['level'], '\033[0m')
                            
                            print(f"{color}{parsed['timestamp']} - {parsed['level']:<8}\033[0m {parsed['message']}")
                        else:
                            print(line.strip())
                
                last_size = current_size
    
    except KeyboardInterrupt:
        print("\n👋 退出日志监控")
    except Exception as e:
        print(f"❌ 监控日志失败: {e}")

def main():
    parser = argparse.ArgumentParser(description='X Monitor 日志查看工具')
    parser.add_argument('command', choices=['main', 'tweets', 'errors', 'analyze', 'tail'], 
                       help='要执行的命令')
    parser.add_argument('--lines', '-n', type=int, default=20, 
                       help='显示的行数 (用于 tail 命令)')
    
    args = parser.parse_args()
    
    if not os.path.exists('logs'):
        print("❌ logs 目录不存在，请先运行 X Monitor 生成日志")
        return
    
    if args.command == 'main':
        view_main_log()
    elif args.command == 'tweets':
        view_tweet_log()
    elif args.command == 'errors':
        view_error_log()
    elif args.command == 'analyze':
        analyze_logs()
    elif args.command == 'tail':
        tail_log(args.lines)

if __name__ == "__main__":
    main()