"""
RAG API 路由
提供知识库管理和智能问答接口
"""

from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks

from app.rag.agents import (
    MultiAgentRAG, 
    DocumentProcessor, 
    VectorStoreManager,
    create_knowledge_base,
    query_knowledge_base
)

router = APIRouter(prefix="/rag", tags=["RAG 知识库"])


# ============ 请求/响应模型 ============

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float
    steps: List[dict]


class DocumentInfo(BaseModel):
    filename: str
    content_type: str
    size: int


class KnowledgeBaseStatus(BaseModel):
    name: str
    document_count: int
    chunk_count: int
    last_updated: str


# ============ 全局 RAG 实例 ============

_rag_instance: Optional[MultiAgentRAG] = None


def get_rag() -> MultiAgentRAG:
    """获取或初始化 RAG 实例"""
    global _rag_instance
    if _rag_instance is None:
        try:
            _rag_instance = MultiAgentRAG("vector_db")
        except Exception as e:
            # 向量数据库不存在，返回 None
            return None
    return _rag_instance


# ============ API 路由 ============

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    智能问答 - 迭代式 RAG Agent
    
    核心流程：
    1. 问题 → 陈述句转换
    2. 陈述句 → RAG 检索
    3. 判断相关性
    4. 不相关 → 生成新陈述句 → 回到步骤2（迭代）
    """
    rag = get_rag()
    if rag is None:
        raise HTTPException(
            status_code=503,
            detail="知识库未初始化，请先上传文档创建知识库"
        )
    
    try:
        result = rag.query(request.message, max_iterations=3)
        
        # 转换步骤为可序列化的格式
        steps = []
        for step in result.steps:
            step_data = {
                "agent": step.agent.value,
                "action": step.action,
                "status": step.status,
            }
            
            # 简化 result 输出
            if step.result:
                if isinstance(step.result, dict):
                    if "statement" in step.result:
                        step_data["result"] = f"陈述句: {step.result['statement']}"
                    elif "relevant" in step.result:
                        step_data["result"] = f"相关: {step.result['relevant']}, {step.result.get('reason', '')}"
                    elif "answer" in step.result:
                        step_data["result"] = "回答生成完成"
                    else:
                        step_data["result"] = str(step.result)[:100]
                else:
                    step_data["result"] = str(step.result)[:100]
            
            steps.append(step_data)
        
        return ChatResponse(
            answer=result.answer,
            sources=result.sources,
            confidence=round(result.confidence, 2),
            steps=steps
        )
    except Exception as e:
        import traceback
        logger.error(f"查询失败: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.post("/documents/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    auto_process: bool = Form(True)
):
    """
    上传文档到知识库
    
    - 支持 .txt 文件
    - 自动清洗和分片
    - 更新向量数据库
    """
    # 验证文件类型
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="仅支持 .txt 文件")
    
    # 保存文件
    upload_dir = "uploads"
    import os
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, file.filename)
    
    try:
        content = await file.read()
        with open(file_path, 'wb') as f:
            f.write(content)
        
        if auto_process:
            # 后台处理文档
            background_tasks.add_task(_process_document, file_path)
        
        return {
            "success": True,
            "filename": file.filename,
            "size": len(content),
            "message": "文档上传成功，正在后台处理"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


@router.post("/knowledge-base/build")
async def build_knowledge_base(
    background_tasks: BackgroundTasks,
    input_path: str = Form("uploads"),
    output_path: str = Form("vector_db")
):
    """
    从上传的文档构建知识库
    
    - 自动清洗文档
    - 智能分片
    - 生成向量索引
    """
    background_tasks.add_task(_build_knowledge_base_task, input_path, output_path)
    
    return {
        "success": True,
        "message": "知识库构建任务已启动，请稍后查询状态"
    }


@router.get("/knowledge-base/status", response_model=KnowledgeBaseStatus)
async def get_knowledge_base_status():
    """获取知识库状态"""
    import os
    
    vector_db_exists = os.path.exists("vector_db")
    
    if not vector_db_exists:
        return KnowledgeBaseStatus(
            name="default",
            document_count=0,
            chunk_count=0,
            last_updated="未创建"
        )
    
    # 尝试获取统计信息
    try:
        processor = DocumentProcessor()
        # 这里可以添加更详细的统计
        return KnowledgeBaseStatus(
            name="default",
            document_count=0,  # 从元数据读取
            chunk_count=0,
            last_updated="刚刚"
        )
    except Exception:
        return KnowledgeBaseStatus(
            name="default",
            document_count=0,
            chunk_count=0,
            last_updated="未知"
        )


@router.get("/documents")
async def list_documents():
    """列出已上传的文档"""
    import os
    
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        return {"documents": []}
    
    documents = []
    for filename in os.listdir(upload_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(upload_dir, filename)
            stat = os.stat(file_path)
            documents.append({
                "filename": filename,
                "size": stat.st_size,
                "modified": stat.st_mtime
            })
    
    return {"documents": documents}


@router.delete("/documents/{filename}")
async def delete_document(filename: str):
    """删除文档"""
    import os
    
    file_path = os.path.join("uploads", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    try:
        os.remove(file_path)
        return {"success": True, "message": f"已删除 {filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")


# ============ 后台任务 ============

def _process_document(file_path: str):
    """处理单个文档"""
    try:
        processor = DocumentProcessor()
        documents = processor.load_documents(file_path)
        chunks = processor.process_documents(documents)
        
        # 添加到现有向量数据库
        vector_store = VectorStoreManager()
        try:
            vector_store.load_vector_store("vector_db")
        except:
            pass  # 数据库不存在，会创建新的
        
        vector_store.add_documents(chunks)
        vector_store.vector_store.save_local("vector_db")
        
        print(f"文档处理完成: {file_path}, 生成 {len(chunks)} 个片段")
    except Exception as e:
        print(f"文档处理失败: {file_path}, 错误: {e}")


def _build_knowledge_base_task(input_path: str, output_path: str):
    """构建知识库的后台任务"""
    try:
        create_knowledge_base(input_path, output_path)
        print(f"知识库构建完成: {output_path}")
    except Exception as e:
        print(f"知识库构建失败: {e}")
