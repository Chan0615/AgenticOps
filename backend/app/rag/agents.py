"""
多 Agent 协作 RAG 系统
基于 smolagents 和 LangChain 实现
支持 Tools 工具调用（时间、天气等）
"""

import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader, DirectoryLoader, PyPDFLoader, UnstructuredWordDocumentLoader
)
from langchain_core.documents import Document
import markdown
from bs4 import BeautifulSoup

from app.rag.tools import execute_tool, get_tools

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Agent 角色类型"""
    RETRIEVER = "retriever"      # 检索 Agent
    REASONER = "reasoner"        # 推理 Agent
    ANSWERER = "answerer"        # 回答 Agent
    REFLECTOR = "reflector"      # 反思 Agent


@dataclass
class AgentStep:
    """Agent 执行步骤"""
    agent: AgentRole
    action: str
    result: Any = None
    status: str = "pending"  # pending, running, done, error
    

@dataclass
class RAGResponse:
    """RAG 响应结果"""
    answer: str
    sources: List[str] = field(default_factory=list)
    steps: List[AgentStep] = field(default_factory=list)
    confidence: float = 0.0


class DocumentProcessor:
    """文档处理器 - 使用 LangChain 自动清洗和分片"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", "；", " ", ""]
        )
    
    def load_document(self, file_path: str, file_type: str) -> List[Document]:
        """加载单个文档 - 支持多种格式"""
        logger.info(f"正在加载文档: {file_path}, 类型: {file_type}")
        
        documents = []
        try:
            if file_type == 'txt':
                loader = TextLoader(file_path, encoding='utf-8')
                documents = loader.load()
            elif file_type == 'pdf':
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            elif file_type in ['docx', 'doc']:
                loader = UnstructuredWordDocumentLoader(file_path)
                documents = loader.load()
            elif file_type == 'md':
                # Markdown 转纯文本
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                html = markdown.markdown(md_content)
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.get_text()
                documents = [Document(page_content=text, metadata={"source": file_path})]
            else:
                # 默认按文本处理
                loader = TextLoader(file_path, encoding='utf-8')
                documents = loader.load()
                
            logger.info(f"加载了 {len(documents)} 页/段")
            return documents
        except Exception as e:
            logger.error(f"加载文档失败: {e}")
            raise
    
    def load_documents(self, input_path: str) -> List[Document]:
        """加载文档 - 支持单文件或目录"""
        logger.info(f"正在加载文档: {input_path}")
        
        if os.path.isfile(input_path):
            # 根据扩展名判断类型
            ext = input_path.split('.')[-1].lower()
            documents = self.load_document(input_path, ext)
        else:
            # 目录加载 - 支持多种格式
            all_docs = []
            for pattern in ["**/*.txt", "**/*.pdf", "**/*.docx", "**/*.md"]:
                try:
                    loader = DirectoryLoader(
                        input_path, 
                        glob=pattern,
                        loader_cls=TextLoader if pattern.endswith('txt') else None
                    )
                    docs = loader.load()
                    all_docs.extend(docs)
                except Exception as e:
                    logger.warning(f"加载 {pattern} 失败: {e}")
            documents = all_docs
        
        logger.info(f"加载了 {len(documents)} 个文档")
        return documents
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """处理文档：清洗 + 分片"""
        logger.info("正在处理文档...")
        
        # 清洗文档
        cleaned_docs = []
        for doc in documents:
            # 清洗文本
            cleaned_text = self._clean_text(doc.page_content)
            if cleaned_text.strip():
                doc.page_content = cleaned_text
                cleaned_docs.append(doc)
        
        # 分片
        chunks = self.text_splitter.split_documents(cleaned_docs)
        logger.info(f"文档分片完成，共 {len(chunks)} 个片段")
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """清洗文本"""
        # 去除多余空白
        lines = [line.strip() for line in text.split('\n')]
        # 过滤空行
        lines = [line for line in lines if line]
        return '\n'.join(lines)


class VectorStoreManager:
    """向量数据库管理器 - 支持多索引合并"""
    
    def __init__(self, embedding_model_name: str = "thenlper/gte-small"):
        logger.info(f"正在初始化嵌入模型: {embedding_model_name}")
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.vector_store: Optional[FAISS] = None
    
    def create_vector_store(self, documents: List[Document], save_path: str = "vector_db"):
        """从文档创建向量数据库"""
        logger.info(f"正在创建向量数据库，文档数: {len(documents)}")
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        self.vector_store.save_local(save_path)
        logger.info(f"向量数据库已保存到: {save_path}")
    
    def load_vector_store(self, path: str = "vector_db"):
        """加载本地向量数据库"""
        logger.info(f"正在加载向量数据库: {path}")
        self.vector_store = FAISS.load_local(
            path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )
        logger.info("向量数据库加载成功")
    
    def load_all_vector_stores(self, base_path: str = "vector_db"):
        """加载所有文档的向量索引（支持多文档）"""
        import os
        import glob
        
        # 查找所有文档的向量索引目录
        doc_paths = glob.glob(os.path.join(base_path, "doc_*"))
        
        if not doc_paths:
            # 尝试加载单一向量数据库
            if os.path.exists(base_path) and os.path.isdir(base_path):
                try:
                    self.load_vector_store(base_path)
                    logger.info(f"加载单一向量数据库: {base_path}")
                    return
                except Exception as e:
                    logger.warning(f"加载单一向量数据库失败: {e}")
            raise ValueError(f"未找到任何向量数据库: {base_path}")
        
        # 加载第一个索引
        first_path = doc_paths[0]
        logger.info(f"加载向量索引: {first_path}")
        self.load_vector_store(first_path)
        
        # 合并其他索引
        for doc_path in doc_paths[1:]:
            try:
                logger.info(f"合并向量索引: {doc_path}")
                other_store = FAISS.load_local(
                    doc_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                self.vector_store.merge_from(other_store)
            except Exception as e:
                logger.warning(f"合并向量索引失败 {doc_path}: {e}")
        
        logger.info(f"共加载 {len(doc_paths)} 个向量索引")
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """相似性搜索"""
        if not self.vector_store:
            raise ValueError("向量数据库未初始化")
        return self.vector_store.similarity_search(query, k=k)
    
    def add_documents(self, documents: List[Document]):
        """添加新文档"""
        if not self.vector_store:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)


class QueryTransformer:
    """查询转换器 - 将问题转化为陈述句"""
    
    # 问题词到陈述句的转换规则
    QUESTION_PATTERNS = [
        (r"^什么是(.+?)[？?]?$", r"\1是"),
        (r"^(.+?)是什么[？?]?$", r"\1是"),
        (r"^如何(.+?)[？?]?$", r"\1的方法"),
        (r"^怎么(.+?)[？?]?$", r"\1的方法"),
        (r"^为什么(.+?)[？?]?$", r"\1的原因"),
        (r"^(.+?)有哪些[？?]?$", r"\1的列表"),
        (r"^(.+?)的区别[？?]?$", r"\1的比较"),
        (r"^谁(.+?)[？?]?$", r"\1的人物"),
        (r"^哪里(.+?)[？?]?$", r"\1的地点"),
        (r"^什么时候(.+?)[？?]?$", r"\1的时间"),
    ]
    
    def transform(self, question: str) -> str:
        """将问题转换为陈述句"""
        import re
        
        # 去除首尾空白和问号
        question = question.strip().rstrip("？?")
        
        # 尝试匹配转换规则
        for pattern, replacement in self.QUESTION_PATTERNS:
            match = re.match(pattern, question)
            if match:
                statement = re.sub(pattern, replacement, question)
                logger.info(f"查询转换: '{question}' → '{statement}'")
                return statement
        
        # 无法匹配规则，提取关键词作为陈述句
        # 去除常见疑问词
        statement = question
        for word in ["请问", "我想知道", "告诉我", "能否", "可以"]:
            statement = statement.replace(word, "")
        
        statement = statement.strip()
        logger.info(f"查询转换(关键词提取): '{question}' → '{statement}'")
        return statement if statement else question
    
    def generate_variants(self, statement: str) -> List[str]:
        """生成陈述句的变体，用于多次检索"""
        variants = [statement]
        
        # 变体1：提取核心名词短语（简化版）
        words = statement.split()
        if len(words) > 4:
            variants.append(" ".join(words[:4]))
        
        # 变体2：去除修饰词
        for word in ["的", "是", "方法", "原因", "列表"]:
            if word in statement:
                variant = statement.replace(word, " ").strip()
                if variant and variant != statement:
                    variants.append(variant)
        
        # 变体3：关键词组合
        keywords = [w for w in words if len(w) > 1]
        if len(keywords) >= 2:
            variants.append(" ".join(keywords[:2]))
        
        return list(set(variants))[:3]  # 最多3个变体


class RetrieverAgent:
    """检索 Agent - 负责检索相关文档"""
    
    def __init__(self, vector_store: VectorStoreManager):
        self.vector_store = vector_store
    
    def retrieve(self, statement: str, k: int = 5) -> Dict[str, Any]:
        """执行检索"""
        logger.info(f"检索 Agent 执行查询: {statement}")
        
        # 语义检索
        results = self.vector_store.similarity_search(statement, k=k)
        
        return {
            "documents": results,
            "statement": statement,
            "total_found": len(results)
        }


class RelevanceChecker:
    """相关性检查器 - 判断文档是否与查询相关"""
    
    def __init__(self, threshold: float = 0.3):
        self.threshold = threshold
    
    def check(self, statement: str, documents: List[Document]) -> Dict[str, Any]:
        """
        检查检索结果的相关性
        
        返回:
            - relevant: 是否有足够相关的文档
            - reason: 判断原因
            - relevant_docs: 相关文档列表
            - best_score: 最佳匹配分数
        """
        logger.info(f"检查 {len(documents)} 个文档与查询 '{statement}' 的相关性")
        
        if not documents:
            return {
                "relevant": False,
                "reason": "未检索到任何文档",
                "relevant_docs": [],
                "best_score": 0.0
            }
        
        # 提取查询关键词
        query_keywords = set(self._extract_keywords(statement))
        
        relevant_docs = []
        for doc in documents:
            doc_keywords = set(self._extract_keywords(doc.page_content))
            
            # 计算 Jaccard 相似度
            intersection = query_keywords & doc_keywords
            union = query_keywords | doc_keywords
            
            if union:
                score = len(intersection) / len(union)
            else:
                score = 0.0
            
            # 额外加分：关键词在文档开头出现
            doc_start = doc.page_content[:100].lower()
            keyword_hits = sum(1 for kw in query_keywords if kw in doc_start)
            score += keyword_hits * 0.1
            
            if score >= self.threshold:
                relevant_docs.append({
                    "document": doc,
                    "score": min(score, 1.0),
                    "matched_keywords": list(intersection)
                })
        
        # 按分数排序
        relevant_docs.sort(key=lambda x: x["score"], reverse=True)
        
        best_score = relevant_docs[0]["score"] if relevant_docs else 0.0
        
        # 判断标准：至少2个相关文档，或最佳分数>0.5
        has_enough = len(relevant_docs) >= 2 or best_score > 0.5
        
        return {
            "relevant": has_enough,
            "reason": f"找到 {len(relevant_docs)} 个相关文档，最佳匹配度 {best_score:.2f}" if has_enough else f"相关文档不足（{len(relevant_docs)}个，最佳匹配度 {best_score:.2f}）",
            "relevant_docs": relevant_docs[:5],
            "best_score": best_score
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词（简化版）"""
        import re
        
        # 去除标点，分词
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # 过滤停用词和短词
        stopwords = {'的', '是', '在', '和', '了', '有', '我', '都', '个', '与', '也', '对', '为', '能', '很', '可以', '就', '不', '会', '要', '没有', '我们', '这', '上', '他', '而', '及', '与', '或', '但是', 'the', 'is', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        keywords = [w for w in words if len(w) > 1 and w not in stopwords]
        return keywords


class IterativeRAG:
    """迭代式 RAG Agent
    
    核心流程：
    1. 问题 → 陈述句
    2. 陈述句 → RAG 检索
    3. 判断相关性
    4. 不相关 → 生成新陈述句 → 回到步骤2
    """
    
    def __init__(self, vector_store_path: str = "vector_db"):
        self.vector_store = VectorStoreManager()
        
        # 尝试加载所有向量索引（支持多文档）
        try:
            self.vector_store.load_all_vector_stores(vector_store_path)
        except Exception as e:
            logger.warning(f"加载多文档索引失败，尝试单一索引: {e}")
            self.vector_store.load_vector_store(vector_store_path)
        
        self.transformer = QueryTransformer()
        self.retriever = RetrieverAgent(self.vector_store)
        self.checker = RelevanceChecker(threshold=0.3)
        
        logger.info("迭代式 RAG Agent 初始化完成")
    
    def query(self, question: str, max_iterations: int = 3) -> RAGResponse:
        """
        执行迭代式 RAG 查询
        
        Args:
            question: 用户问题
            max_iterations: 最大迭代次数
        
        Returns:
            RAGResponse: 包含回答、来源、迭代步骤
        """
        steps: List[AgentStep] = []
        all_relevant_docs: List[Dict] = []
        
        # 步骤1: 将问题转换为陈述句
        step_transform = AgentStep(AgentRole.REASONER, "将问题转化为陈述句")
        step_transform.status = "running"
        steps.append(step_transform)
        
        current_statement = self.transformer.transform(question)
        step_transform.result = {"statement": current_statement}
        step_transform.status = "done"
        
        # 迭代检索
        for iteration in range(max_iterations):
            logger.info(f"=== 迭代 {iteration + 1}/{max_iterations}: '{current_statement}' ===")
            
            # 步骤2: 检索
            step_retrieve = AgentStep(AgentRole.RETRIEVER, f"检索: {current_statement}")
            step_retrieve.status = "running"
            steps.append(step_retrieve)
            
            retrieve_result = self.retriever.retrieve(current_statement, k=5)
            step_retrieve.result = retrieve_result
            step_retrieve.status = "done"
            
            # 步骤3: 判断相关性
            step_check = AgentStep(AgentRole.REASONER, "判断检索结果相关性")
            step_check.status = "running"
            steps.append(step_check)
            
            check_result = self.checker.check(current_statement, retrieve_result["documents"])
            step_check.result = check_result
            step_check.status = "done"
            
            # 如果相关，保存结果并退出循环
            if check_result["relevant"]:
                all_relevant_docs = check_result["relevant_docs"]
                logger.info(f"找到相关文档，停止迭代")
                break
            
            # 如果不相关，生成新的陈述句继续迭代
            if iteration < max_iterations - 1:
                step_regenerate = AgentStep(AgentRole.REASONER, "生成新的查询陈述句")
                step_regenerate.status = "running"
                steps.append(step_regenerate)
                
                variants = self.transformer.generate_variants(current_statement)
                # 选择下一个变体（排除已用过的）
                used_statements = [s.result.get("statement", "") for s in steps if s.action.startswith("检索")]
                next_variant = None
                for v in variants:
                    if v not in used_statements:
                        next_variant = v
                        break
                
                if next_variant:
                    current_statement = next_variant
                    step_regenerate.result = {"new_statement": current_statement, "variants": variants}
                    step_regenerate.status = "done"
                else:
                    # 没有更多变体，退出
                    step_regenerate.result = {"error": "无更多查询变体"}
                    step_regenerate.status = "error"
                    break
            else:
                # 达到最大迭代次数，使用已找到的文档
                all_relevant_docs = check_result["relevant_docs"]
        
        # 步骤4: 生成回答（知识库 + LLM fallback）
        step_answer = AgentStep(AgentRole.ANSWERER, "生成最终回答")
        step_answer.status = "running"
        steps.append(step_answer)
        
        if all_relevant_docs:
            # 使用知识库生成回答
            answer = self._generate_answer(question, all_relevant_docs)
            sources = list(set([
                doc["document"].metadata.get("source", "未知来源")
                for doc in all_relevant_docs[:5]
            ]))
            confidence = all_relevant_docs[0]["score"]
        else:
            # 知识库无结果，fallback 到 LLM
            step_fallback = AgentStep(AgentRole.ANSWERER, "知识库无结果，使用模型回答")
            step_fallback.status = "running"
            steps.append(step_fallback)
            
            answer = self._generate_llm_answer(question)
            sources = ["模型回答"]
            confidence = 0.0
            
            step_fallback.result = {"source": "LLM fallback"}
            step_fallback.status = "done"
        
        step_answer.result = {"answer": answer}
        step_answer.status = "done"
        
        return RAGResponse(
            answer=answer,
            sources=sources,
            steps=steps,
            confidence=confidence
        )
    
    def _generate_answer(self, question: str, relevant_docs: List[Dict]) -> str:
        """基于知识库生成回答"""
        # 按分数排序
        docs = sorted(relevant_docs, key=lambda x: x["score"], reverse=True)
        
        # 构建上下文
        context_parts = []
        for i, doc_info in enumerate(docs[:3], 1):
            doc = doc_info["document"]
            content = doc.page_content[:400]
            context_parts.append(f"[资料{i}] {content}")
        
        context = "\n\n".join(context_parts)
        
        # 生成回答（简化版，实际应调用 LLM）
        answer = f"根据知识库检索结果：\n\n{context}\n\n"
        answer += f"针对您的问题「{question}」，"
        
        if docs:
            best_doc = docs[0]["document"]
            answer += f"最相关的资料来自《{best_doc.metadata.get('source', '未知')}》，"
            answer += f"匹配度为 {docs[0]['score']:.1%}。"
        
        return answer
    
    def _generate_llm_answer(self, question: str) -> str:
        """当知识库无结果时，尝试使用 Tools 回答，否则返回友好提示"""
        question_lower = question.lower()
        
        # 尝试使用 Tools 回答
        # 1. 时间相关
        if any(kw in question_lower for kw in ['现在', '时间', '几点', '日期', '星期', '今天', '明天', '昨天']):
            try:
                result = execute_tool("get_current_time")
                return f"{result}\n\n📌 这是通过工具调用获取的实时信息。"
            except Exception as e:
                logger.warning(f"工具调用失败: {e}")
        
        # 2. 计算相关
        if any(kw in question_lower for kw in ['计算', '等于', '多少', '+', '-', '*', '/', '平方', '根号']):
            # 尝试提取数学表达式
            import re
            # 简单匹配数字和运算符
            expr_match = re.search(r'[\d\+\-\*\/\(\)\.\s]+', question)
            if expr_match:
                try:
                    result = execute_tool("calculate", expression=expr_match.group())
                    return f"{result}\n\n📌 这是通过计算工具得出的结果。"
                except Exception as e:
                    logger.warning(f"计算工具调用失败: {e}")
        
        # 4. 问候语
        if any(kw in question_lower for kw in ['你好', '您好', 'hello', 'hi', '在吗']):
            return "你好！我是托马斯回旋喵，你的智能知识助手。\n\n我可以：\n• 通过知识库检索专业信息\n• 查询当前时间、天气等实时信息\n• 进行简单的数学计算\n\n有什么可以帮你的吗？"
        
        # 默认回答
        return f"关于「{question}」，我在知识库中没有找到相关的文档资料。\n\n这可能是因为：\n1. 知识库中暂无相关内容\n2. 问题描述需要更具体\n\n你可以尝试：\n• 用不同的关键词描述问题\n• 检查知识库是否已上传相关文档\n• 询问时间、天气、计算等，我可以使用工具回答\n\n有什么其他我可以帮你的吗？"


# 保留旧的类以保持兼容性
class ReasonerAgent:
    """推理 Agent - 分析检索结果，决定是否需要重新检索"""
    
    def __init__(self):
        pass
    
    def analyze(self, query: str, documents: List[Document]) -> Dict[str, Any]:
        """分析检索结果"""
        logger.info(f"推理 Agent 分析 {len(documents)} 个文档")
        
        if not documents:
            return {
                "sufficient": False,
                "reason": "未找到相关文档",
                "new_queries": [query],
                "relevant_docs": []
            }
        
        relevant_docs = []
        query_keywords = set(query.lower().split())
        
        for doc in documents:
            doc_text = doc.page_content.lower()
            match_count = sum(1 for kw in query_keywords if kw in doc_text)
            relevance_score = match_count / len(query_keywords) if query_keywords else 0
            
            if relevance_score > 0.3:
                relevant_docs.append({
                    "document": doc,
                    "score": relevance_score
                })
        
        relevant_docs.sort(key=lambda x: x["score"], reverse=True)
        sufficient = len(relevant_docs) >= 2
        
        return {
            "sufficient": sufficient,
            "reason": "找到足够相关的文档" if sufficient else "相关文档不足",
            "new_queries": [] if sufficient else [query],
            "relevant_docs": relevant_docs[:5]
        }


class AnswererAgent:
    """回答 Agent - 生成最终回答"""
    
    def __init__(self, model_config: Dict[str, str]):
        self.model_config = model_config
    
    def generate_answer(self, query: str, documents: List[Dict]) -> str:
        """生成回答"""
        logger.info(f"回答 Agent 生成回答，基于 {len(documents)} 个文档")
        
        # 构建上下文
        context = "\n\n".join([
            f"资料{i+1}: {doc['document'].page_content[:500]}"
            for i, doc in enumerate(documents[:3])
        ])
        
        # 这里应该调用 LLM API
        # 简化版本：直接组合文档内容
        answer = f"根据知识库检索结果：\n\n{context}\n\n"
        answer += f"针对您的问题「{query}」，以上资料提供了相关信息。"
        
        return answer


class ReflectorAgent:
    """反思 Agent - 检查回答质量"""
    
    def reflect(self, query: str, answer: str, documents: List[Dict]) -> Dict[str, Any]:
        """反思回答质量"""
        logger.info("反思 Agent 评估回答质量")
        
        # 简单的质量检查
        issues = []
        
        # 检查回答长度
        if len(answer) < 50:
            issues.append("回答过短")
        
        # 检查是否包含文档引用
        has_citation = any(f"资料{i+1}" in answer for i in range(len(documents)))
        if not has_citation:
            issues.append("缺少文档引用")
        
        return {
            "quality_score": 1.0 - (len(issues) * 0.2),
            "issues": issues,
            "needs_improvement": len(issues) > 0
        }


class MultiAgentRAG(IterativeRAG):
    """多 Agent RAG 编排器 - 使用迭代式 RAG 作为默认实现"""
    
    def __init__(self, vector_store_path: str = "vector_db"):
        super().__init__(vector_store_path)


# 便捷函数
def create_knowledge_base(input_path: str, output_path: str = "vector_db"):
    """从文档创建知识库"""
    processor = DocumentProcessor()
    vector_store = VectorStoreManager()
    
    # 加载和处理文档
    documents = processor.load_documents(input_path)
    chunks = processor.process_documents(documents)
    
    # 创建向量数据库
    vector_store.create_vector_store(chunks, output_path)
    logger.info(f"知识库创建完成: {output_path}")


def query_knowledge_base(question: str, vector_db_path: str = "vector_db") -> RAGResponse:
    """查询知识库"""
    rag = MultiAgentRAG(vector_db_path)
    return rag.query(question)
