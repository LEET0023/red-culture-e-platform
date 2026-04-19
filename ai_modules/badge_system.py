import json
import os
from typing import Dict, List, Set
from datetime import datetime
import streamlit as st


class BadgeSystem:
    """徽章奖励 system - 根据学习完成情况和提问质量"""

    BADGES = {
        "first_correct": {
            "name": "🌟 初战告捷",
            "name_en": "First Victory",
            "description": "第一次答对题目！",
            "emoji": "🌟",
            "condition": "first_correct_answer"
        },
        "quiz_master": {
            "name": "🎓 答题小能手",
            "name_en": "Quiz Master",
            "description": "连续答对3道题",
            "emoji": "🎓",
            "condition": "streak_3_correct"
        },
        "curious_star": {
            "name": "💭 好奇小明星",
            "name_en": "Curious Star",
            "description": "提出了3个好问题",
            "emoji": "💭",
            "condition": "asked_3_quality_questions"
        },
        "story_teller": {
            "name": "📖 红色故事家",
            "name_en": "Story Teller",
            "description": "完成了所有学习模块",
            "emoji": "📖",
            "condition": "completed_all_sections"
        },
        "persistence_king": {
            "name": "👑 坚持小勇士",
            "name_en": "Persistence King",
            "description": "答错后重新答对",
            "emoji": "👑",
            "condition": "correct_after_mistake"
        },
        "vocabulary_explorer": {
            "name": "📚 词汇探险家",
            "name_en": "Vocabulary Explorer",
            "description": "学习了10个新词汇",
            "emoji": "📚",
            "condition": "learned_10_words"
        },
        "qa_champion": {
            "name": "🎙️ 问答小达人",
            "name_en": "QA Champion",
            "description": "参与了5次智能问答",
            "emoji": "🎙️",
            "condition": "asked_5_questions"
        }
    }

    def __init__(self, user_data_path: str = None):
        # 修改点 1：确保在当前目录下创建 data 文件夹，避免 Windows 路径报错
        if user_data_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.user_data_path = os.path.join(os.path.dirname(current_dir), "data", "user_progress.json")
        else:
            self.user_data_path = user_data_path

        self._ensure_data_dir()

    def _ensure_data_dir(self):
        directory = os.path.dirname(self.user_data_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def _load_user_data(self, user_id: str) -> Dict:
        """加载用户数据"""
        if os.path.exists(self.user_data_path):
            try:
                with open(self.user_data_path, 'r', encoding='utf-8') as f:
                    all_data = json.load(f)
                    user_data = all_data.get(user_id, self._get_default_user_dict())
                    # 确保加载进来后 sections 是列表格式
                    if not isinstance(user_data["stats"]["sections_completed"], list):
                        user_data["stats"]["sections_completed"] = []
                    return user_data
            except Exception:
                return self._get_default_user_dict()
        return self._get_default_user_dict()

    def _get_default_user_dict(self):
        """返回初始化的用户结构"""
        return {
            "badges": [],
            "stats": {
                "correct_answers": 0,
                "total_answers": 0,
                "current_streak": 0,
                "max_streak": 0,
                "quality_questions": 0,
                "total_questions_asked": 0,
                "vocabulary_learned": [],
                "sections_completed": [],  # 统一使用 list
                "mistake_recovery_count": 0
            },
            "last_mistake_question": None
        }

    def _save_user_data(self, user_id: str, data: Dict):
        """保存用户数据"""
        all_data = {}
        if os.path.exists(self.user_data_path):
            try:
                with open(self.user_data_path, 'r', encoding='utf-8') as f:
                    all_data = json.load(f)
            except:
                all_data = {}

        all_data[user_id] = data
        with open(self.user_data_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)

    def record_answer(self, user_id: str, is_correct: bool, question: str, section: str):
        """记录答题情况，更新徽章"""
        data = self._load_user_data(user_id)
        stats = data["stats"]
        stats["total_answers"] += 1

        if is_correct:
            stats["correct_answers"] += 1
            stats["current_streak"] += 1
            stats["max_streak"] = max(stats["max_streak"], stats["current_streak"])
            if data["last_mistake_question"] == question:
                stats["mistake_recovery_count"] += 1
                data["last_mistake_question"] = None
        else:
            stats["current_streak"] = 0
            data["last_mistake_question"] = question

        # 记录完成的主题
        if section not in stats["sections_completed"]:
            stats["sections_completed"].append(section)

        self._save_user_data(user_id, data)
        return self._check_badges(user_id, data)

    def record_question_asked(self, user_id: str, question: str, quality_score: int):
        """记录提问，用于徽章"""
        data = self._load_user_data(user_id)
        stats = data["stats"]
        stats["total_questions_asked"] += 1
        if quality_score >= 15:  # 调低门槛，鼓励小学生提问
            stats["quality_questions"] += 1

        self._save_user_data(user_id, data)
        return self._check_badges(user_id, data)

    def record_vocabulary_learned(self, user_id: str, word: str):
        data = self._load_user_data(user_id)
        stats = data["stats"]
        if word not in stats["vocabulary_learned"]:
            stats["vocabulary_learned"].append(word)
        self._save_user_data(user_id, data)
        return self._check_badges(user_id, data)

    def _check_badges(self, user_id: str, data: Dict) -> List[Dict]:
        stats = data["stats"]
        current_badges = set(data["badges"])
        new_badges = []

        # 逻辑判断
        if stats["correct_answers"] >= 1 and "first_correct" not in current_badges:
            new_badges.append(self.BADGES["first_correct"]), current_badges.add("first_correct")
        if stats["max_streak"] >= 3 and "quiz_master" not in current_badges:
            new_badges.append(self.BADGES["quiz_master"]), current_badges.add("quiz_master")
        if stats["quality_questions"] >= 3 and "curious_star" not in current_badges:
            new_badges.append(self.BADGES["curious_star"]), current_badges.add("curious_star")
        if len(stats["sections_completed"]) >= 5 and "story_teller" not in current_badges:
            new_badges.append(self.BADGES["story_teller"]), current_badges.add("story_teller")
        if stats["mistake_recovery_count"] >= 1 and "persistence_king" not in current_badges:
            new_badges.append(self.BADGES["persistence_king"]), current_badges.add("persistence_king")

        if new_badges:
            data["badges"] = list(current_badges)
            self._save_user_data(user_id, data)
        return new_badges

    def get_user_badges(self, user_id: str) -> List[Dict]:
        data = self._load_user_data(user_id)
        return [self.BADGES[bid] for bid in data["badges"] if bid in self.BADGES]

    def render_badge_display(self, user_id: str):
        """在侧边栏显示徽章，匹配主程序风格"""
        badges = self.get_user_badges(user_id)
        if badges:
            st.markdown("---")
            st.markdown("### 🏆 我的荣誉徽章")
            # 每行显示 2 个徽章
            for i in range(0, len(badges), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(badges):
                        badge = badges[i + j]
                        cols[j].markdown(f"""
                        <div style="text-align:center; padding:10px; background:#fff7ef; border:1px solid #e8b37f; border-radius:12px; margin-bottom:8px;">
                            <span style="font-size:28px;">{badge['emoji']}</span><br>
                            <b style="font-size:14px; color:#8b1f1f;">{badge['name']}</b><br>
                            <small style="color:#6b3a2e;">{badge['description']}</small>
                        </div>
                        """, unsafe_allow_html=True)