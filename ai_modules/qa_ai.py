import os
from typing import List, Dict, Any
import streamlit as st
from openai import OpenAI

# 确保能找到你的知识库模块，如果还没写好，这里会创建一个空的防止报错
try:
    from knowledge_base.rag_retriever import RedCultureRAG
except ImportError:
    class RedCultureRAG:
        def search(self, question, top_k=2):
            return []  # 暂时返回空列表，后续你写完 rag_retriever.py 就会自动替换


class AIQASystem:
    """AI智能问答系统 - 已适配本地 DeepSeek (Ollama)"""

    def __init__(self, api_key: str = None):
        # 1. 优先从环境变量获取（Streamlit Secrets 会自动注入环境变量）
        # 如果没有环境变量，则使用传入的参数或默认值
        final_api_key = os.getenv("DEEPSEEK_API_KEY") or api_key or "sk-xxx"
        final_base_url = os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"

        self.client = OpenAI(
            base_url=final_base_url,
            api_key=final_api_key,
        )
        self.rag = RedCultureRAG()
        self.conversation_history: List[Dict] = []

    def ask(self, question: str, context: str = "") -> str:
        """回答问题，使用本地 RAG 增强"""
        # 1. 检索本地知识库
        relevant_info = self.rag.search(question, top_k=2)

        # 2. 构建增强的 prompt
        context_from_kb = "\n".join([r.get('content', '') for r in relevant_info])

        prompt = f"""
        你是一个超有趣的红色文化AI讲解员，叫"小红星" 🌟，正在和五六年级的小学生聊天。

        当前学习的主题背景：{context}

        知识库中的相关信息：
        {context_from_kb}

        小朋友问：{question}

        请用以下风格回答：
        1. 语气活泼、生动，像在讲故事
        2. 多用比喻和生活中的例子
        3. 适当使用表情符号 😊 🏠 🌳 📖 ⭐
        4. 如果小朋友问的是英文词汇，解释意思并教一个记忆小窍门
        5. 回答长度控制在150字以内
        6. 最后可以问一个小问题，鼓励继续提问

        记住：你是小红星，要让孩子觉得学习红色文化很有趣！
        """

        try:
            # 核心改动：调用本地 ds-7b 模型
            response = self.client.chat.completions.create(
              model="deepseek-chat",  #
                messages=[
                    {"role": "system", "content": "你是小红星，一个活泼有趣的红色文化讲解AI，专门和小学生聊天。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=300
            )
            answer = response.choices[0].message.content

            # 保存对话历史
            self.conversation_history.append({
                "question": question,
                "answer": answer,
                "context": context
            })

            return answer
        except Exception as e:
            # 如果本地模型没开启或报错，进入备用回答
            print(f"Error calling local AI: {e}")
            return self._fallback_answer(question, relevant_info)

    def _fallback_answer(self, question: str, relevant_info: List) -> str:
        """备用回答：当 AI 出错时，至少能把检索到的事实说出来"""
        if relevant_info and len(relevant_info) > 0:
            return f"📖 让我想想... 根据记录：{relevant_info[0].get('content', '')}\n\n还有什么想了解的吗？小红星随时在线哦！🌟"
        else:
            return f"🤔 这个问题有点特别... 不如我们一起在纪念馆里找找答案？或者换个问题问我？😊"

    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []

    def get_question_quality_score(self, question: str) -> int:
        """评估问题质量（用于徽章奖励）"""
        score = 0
        keywords = ["为什么", "how", "what", "when", "who", "where", "can you tell me",
                    "meaning", "difference", "compare", "story", "history", "陈毅", "革命"]

        question_lower = question.lower()
        for kw in keywords:
            if kw in question_lower:
                score += 10

        if len(question) > 15:
            score += 5

        return min(score, 50)
