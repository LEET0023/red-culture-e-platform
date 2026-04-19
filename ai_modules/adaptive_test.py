import json
import random
from typing import List, Dict, Any
from datetime import datetime
import streamlit as st
from openai import OpenAI  # 修改导入方式


class AdaptiveTestGenerator:
    """根据错题和提问个性化生成巩固测试"""

    def __init__(self, api_key: str = None):
        # ==========================================
        # 修改点：适配本地 Ollama
        # ==========================================
        self.client = OpenAI(
            base_url='http://localhost:11434/v1/',
            api_key='ollama',  # 本地 Ollama 不需要真实 key，随便填即可
        )
        self.model_name = "ds-7b"  # 确保和你 Ollama 里的模型名一致

        self.mistake_records: Dict[str, List[Dict]] = {}  # 用户错题记录
        self.question_history: Dict[str, List[str]] = {}  # 用户提问历史

    def record_mistake(self, user_id: str, question: str, user_answer: str,
                       correct_answer: str, section: str):
        """记录错题"""
        if user_id not in self.mistake_records:
            self.mistake_records[user_id] = []

        self.mistake_records[user_id].append({
            "question": question,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "section": section,
            "timestamp": datetime.now().isoformat(),
            "attempt_count": 1
        })

    def record_question(self, user_id: str, question: str, section: str):
        """记录用户提问"""
        if user_id not in self.question_history:
            self.question_history[user_id] = []

        self.question_history[user_id].append({
            "question": question,
            "section": section,
            "timestamp": datetime.now().isoformat()
        })

    def generate_personalized_test(self, user_id: str, section: str) -> Dict:
        """根据用户学习历史生成个性化测试"""
        user_mistakes = self.mistake_records.get(user_id, [])
        user_questions = self.question_history.get(user_id, [])

        section_mistakes = [m for m in user_mistakes if m['section'] == section]
        section_questions = [q for q in user_questions if q['section'] == section]

        if not section_mistakes and not section_questions:
            return self._generate_normal_test(section)

        # 实际调用 AI 生成或逻辑生成
        return self._generate_ai_test(section, section_mistakes, section_questions)

    def _generate_normal_test(self, section: str) -> Dict:
        """生成常规测试"""
        test_bank = {
            "走进陈毅旧居——一座夯土房里的革命史 / Entering Chen Yi’s Former Residence — A Revolutionary Story in a Rammed-Earth House": {
                "questions": [
                    {
                        "question": "陈毅一家在这里住了多长时间？",
                        "question_en": "How long did Chen Yi's family live here?",
                        "options": ["A. 两个月 / Two months", "B. 八个月 / Eight months", "C. 两年 / Two years"],
                        "answer": "B. 八个月 / Eight months",
                        "hint": "从1946年6月到1947年2月，一共是8个月哦！"
                    },
                    {
                        "question": "这座房子是什么时候建造的？",
                        "question_en": "When was this house built?",
                        "options": ["A. 1927年", "B. 1937年", "C. 1945年"],
                        "answer": "A. 1927年",
                        "hint": "是钟维坤爷爷在1927年建造的~"
                    }
                ]
            },
            "百年丹桂见证鱼水情深 / A Century-Old Osmanthus Tree Witnessing the Bond Between Soldiers and Civilians": {
                "questions": [
                    {
                        "question": "陈毅把桂花树从花盆里移到了哪里？",
                        "question_en": "Where did Chen Yi move the osmanthus tree from the flowerpot?",
                        "options": ["A. 房间里", "B. 院子里", "C. 花园里"],
                        "answer": "B. 院子里",
                        "hint": "陈爷爷说树要栽到地上才能长大！"
                    }
                ]
            }
        }

        # 注意：这里使用了你的 SECTIONS 里的全名进行匹配
        test = test_bank.get(section, list(test_bank.values())[0])
        questions = random.sample(test["questions"], min(3, len(test["questions"])))

        return {
            "title": "🎯 巩固小测试",
            "title_en": "Review Quiz",
            "questions": questions,
            "message": "这是为你准备的常规练习，加油！🌟"
        }

    def _generate_ai_test(self, section: str, mistakes: List, questions: List) -> Dict:
        """逻辑生成个性化提示文本，并返回练习题"""
        mistake_topics = []
        for m in mistakes[:5]:
            if "八个月" in m['correct_answer']:
                mistake_topics.append("居住时间")
            elif "院子" in m['correct_answer']:
                mistake_topics.append("桂花树位置")
            elif "诗" in m['correct_answer']:
                mistake_topics.append("陈昊苏写诗")

        question_topics = []
        for q in questions[:3]:
            if "桂花" in q['question']:
                question_topics.append("桂花树故事")
            elif "陈毅" in q['question']:
                question_topics.append("陈毅生平")

        if mistake_topics or question_topics:
            focus = mistake_topics if mistake_topics else question_topics
            message = f"🎯 根据记录，小红星发现你对「{', '.join(set(focus))}」很感兴趣~ 试试这几道题！"
        else:
            message = "🎯 小红星为你准备了专属巩固练习，继续加油！"

        test = self._generate_normal_test(section)
        test["message"] = message
        test["title"] = "🎯 你的专属巩固练习"

        return test