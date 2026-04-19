import json
import os
from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer

class RedCultureRAG:
    """红色文化RAG检索器 - 专为小学生优化"""
    
    def __init__(self, kb_path: str = None):
        self.kb_path = kb_path or os.path.join(os.path.dirname(__file__), "red_culture_terms.json")
        # 使用轻量级中文嵌入模型
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.client = chromadb.Client()
        
        # 创建或加载collection
        self.collection = self.client.get_or_create_collection(
            name="red_culture_kids",
            metadata={"description": "红色文化知识库 - 小学生版"}
        )
        
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """加载知识库并向量化"""
        with open(self.kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        documents = []
        metadatas = []
        ids = []
        
        # 添加术语
        for idx, term in enumerate(data['terms']):
            # 为小学生创建友好的文本表示
            doc = f"【词汇】{term['term']} - {term['kids_explanation']} (正式含义：{term['definition_zh']})"
            documents.append(doc)
            metadatas.append({"type": "term", "term": term['term'], "chinese": term['chinese']})
            ids.append(f"term_{idx}")
        
        # 添加历史事实
        for idx, fact in enumerate(data['historical_facts']):
            doc = f"【历史小知识】{fact['kids_friendly']} (事实：{fact['fact']})"
            documents.append(doc)
            metadatas.append({"type": "fact", "fact_en": fact['fact'], "chinese": fact['chinese']})
            ids.append(f"fact_{idx}")
        
        # 向量化并存储
        embeddings = self.embedder.encode(documents).tolist()
        
        # 如果collection已有数据，先清空
        if self.collection.count() > 0:
            existing_ids = self.collection.get()['ids']
            if existing_ids:
                self.collection.delete(ids=existing_ids)
        
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """搜索相关内容 - 返回小学生友好格式"""
        query_embedding = self.embedder.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                "content": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "distance": results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
    
    def get_kids_answer(self, query: str) -> str:
        """获取面向小学生的回答"""
        results = self.search(query, top_k=2)
        if not results:
            return "🤔 这个问题有点难，让我想想... 你能说得更详细一点吗？"
        
        answer_parts = []
        for r in results:
            if r['metadata']['type'] == 'term':
                answer_parts.append(f"📖 {r['content']}")
            else:
                answer_parts.append(f"🌟 {r['content']}")
        
        return "\n\n".join(answer_parts)