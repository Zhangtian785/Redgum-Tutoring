"""
storage.py - Data Persistence Utilities
Owner: Member A (组员A - 后端 + 项目文档)
Role in assignment: US07 (预约数据存入数据库, 支持查询) + 通用数据读写工具
所有成员共享此文件提供的 load_data / save_data，保证数据统一读写。
"""
import json
import os

# 数据文件统一存放在 redgum-tutoring/data/ 目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

STUDENT_FILE = os.path.join(DATA_DIR, "students.json")
TUTOR_FILE = os.path.join(DATA_DIR, "tutors.json")
AVAIL_FILE = os.path.join(DATA_DIR, "availability.json")
SESSION_FILE = os.path.join(DATA_DIR, "sessions.json")


def _ensure_dir():
    """确保 data 目录存在（成员A负责的持久化基础能力）"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_data(filepath):
    """从 JSON 文件加载数据；文件不存在返回空列表"""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data(filepath, data):
    """把数据保存为 JSON 文件，实现持久化（重启程序数据不丢失）"""
    _ensure_dir()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def next_id(records, id_field):
    """生成自增主键 ID：取现有最大 ID + 1"""
    return max((r[id_field] for r in records), default=0) + 1
