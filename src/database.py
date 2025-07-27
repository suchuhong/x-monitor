import json
from typing import Set

def load_seen_tweet_ids(db_path: str) -> Set[str]:
    """从JSON文件加载已见推文ID集合"""
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_seen_tweet_ids(db_path: str, tweet_ids: Set[str]):
    """将推文ID集合保存到JSON文件"""
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(list(tweet_ids), f, indent=2)