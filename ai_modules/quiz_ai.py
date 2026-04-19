import os
from openai import OpenAI
from typing import List, Dict, Any
import streamlit as st



class AIQuizExplainer:
    """AI题目解析器 - 活泼生动风格（已适配本地 DeepSeek）"""

def __init__(self, api_key: str = None):
        # 这里的名字要和 Secrets 里的 DEEPSEEK_API_KEY 一致
        final_api_key = os.getenv("DEEPSEEK_API_KEY") or api_key or "sk-xxx"
        final_base_url = os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"

        self.client = OpenAI(
            base_url=final_base_url,
            api_key=final_api_key,
        )

    def explain_answer(self, question: str, user_answer: str, correct_answer: str,
                       context: str = "", is_correct: bool = False) -> str:
        """生成生动活泼的题目解析"""

        if is_correct:
            prompt = f"""
            你是一个超级有趣的红色文化讲解员"小红星" 🌟，正在给五六年级的小学生讲题。

            题目：{question}
            小朋友的答案：{user_answer}（这个答案是正确的！）
            相关背景：{context}

            请用非常活泼、生动、童趣的方式表扬小朋友，并简单解释为什么这个答案是对的。
            要求：
            1. 使用表情符号 🎉 🎈 ⭐ 👍
            2. 语气要亲切，像在讲故事
            3. 控制在80字以内
            """
        else:
            prompt = f"""
            你是一个超级有趣的红色文化讲解员"小红星" 🌟，正在给五六年级的小学生讲题。

            题目：{question}
            小朋友的答案：{user_answer}（这个答案是错误的）
            正确答案：{correct_answer}
            相关背景：{context}

            请用活泼生动的方式：
            1. 先用鼓励的语气安慰小朋友（比如“没关系，小红星带你转个弯~”）
            2. 解释正确答案背后的故事或道理
            3. 使用表情符号 😊 📖 🌟
            4. 控制在120字以内
            """

        try:
            # 核心改动：调用本地 ds-7b 模型
            response = self.client.chat.completions.create(
               model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个活泼有趣的小学老师，专门讲解红色文化故事。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=250
            )
            return response.choices[0].message.content
        except Exception as e:
            # 调试用：如果报错可以在控制台看到
            print(f"Quiz AI Error: {e}")
            return self._fallback_explanation(question, user_answer, correct_answer, is_correct)

    def _fallback_explanation(self, question: str, user_answer: str,
                              correct_answer: str, is_correct: bool) -> str:
        """备用解析（当 API 离线时使用）"""
        if is_correct:
            return f"🎉 太棒啦！{user_answer} 是完全正确的！你对陈毅爷爷的故事了解得真清楚，真是一个红色文化小达人！👍"
        else:
            return f"😊 别灰心，这道题有点小陷阱哦！正确答案是：{correct_answer}。跟着小红星继续探索，你一定会越来越棒的！🌟"
