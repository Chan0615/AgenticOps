"""
文档处理服务

负责：
- 解析多种格式文件（PDF、Word、Markdown、TXT）
- LLM 语义分割：利用大模型识别最佳切分点
- 生成分块元数据
"""

import io
import logging
import re
from typing import List, Optional

from app.core.ai import call_llm

logger = logging.getLogger(__name__)


# ============ 文件解析 ============


def parse_file(file_bytes: bytes, filename: str) -> str:
    """
    根据文件扩展名解析文件内容为纯文本

    支持：.txt, .md, .pdf, .docx
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext == "txt":
        return _parse_txt(file_bytes)
    elif ext == "md":
        return _parse_markdown(file_bytes)
    elif ext == "pdf":
        return _parse_pdf(file_bytes)
    elif ext in ("docx", "doc"):
        return _parse_docx(file_bytes)
    else:
        # 默认尝试当文本处理
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("gbk", errors="replace")


def _parse_txt(data: bytes) -> str:
    """解析纯文本"""
    for enc in ("utf-8", "gbk", "gb2312", "latin-1"):
        try:
            return data.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return data.decode("utf-8", errors="replace")


def _parse_markdown(data: bytes) -> str:
    """解析 Markdown（保留结构）"""
    text = _parse_txt(data)
    # Markdown 本身就是文本，直接返回（保留标题标记辅助分割）
    return text


def _parse_pdf(data: bytes) -> str:
    """解析 PDF"""
    try:
        from PyPDF2 import PdfReader

        reader = PdfReader(io.BytesIO(data))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
        return "\n\n".join(pages)
    except ImportError:
        raise RuntimeError("PDF 解析需要安装 PyPDF2: pip install PyPDF2")
    except Exception as e:
        logger.error(f"PDF 解析失败: {e}")
        raise ValueError(f"PDF 文件解析失败: {str(e)}")


def _parse_docx(data: bytes) -> str:
    """解析 Word 文档"""
    try:
        from docx import Document

        doc = Document(io.BytesIO(data))
        paragraphs = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)
        return "\n\n".join(paragraphs)
    except ImportError:
        raise RuntimeError("Word 解析需要安装 python-docx: pip install python-docx")
    except Exception as e:
        logger.error(f"Word 解析失败: {e}")
        raise ValueError(f"Word 文件解析失败: {str(e)}")


# ============ 文本清洗 ============


def clean_text(text: str) -> str:
    """清洗文本"""
    # 合并连续空白行
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 去除行首尾空白
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)
    # 去除首尾空白
    return text.strip()


# ============ 分割策略 ============


def split_by_rules(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[str]:
    """
    基于规则的文本分割（递归字符分割）

    作为 LLM 语义分割的回退方案，或用于小文档的快速分割。
    """
    separators = ["\n\n", "\n", "。", "；", ".", ";", " "]
    chunks = _recursive_split(text, separators, chunk_size, chunk_overlap)
    return [c.strip() for c in chunks if c.strip()]


def _recursive_split(
    text: str,
    separators: List[str],
    chunk_size: int,
    chunk_overlap: int,
) -> List[str]:
    """递归分割"""
    if len(text) <= chunk_size:
        return [text]

    # 尝试用当前分隔符分割
    sep = separators[0] if separators else ""
    if sep and sep in text:
        parts = text.split(sep)
    else:
        if len(separators) > 1:
            return _recursive_split(text, separators[1:], chunk_size, chunk_overlap)
        # 最后手段：硬切
        chunks = []
        for i in range(0, len(text), chunk_size - chunk_overlap):
            chunks.append(text[i : i + chunk_size])
        return chunks

    # 合并小段落到 chunk_size 以内
    chunks = []
    current = ""
    for part in parts:
        candidate = current + sep + part if current else part
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            if len(part) > chunk_size and len(separators) > 1:
                sub_chunks = _recursive_split(
                    part, separators[1:], chunk_size, chunk_overlap
                )
                chunks.extend(sub_chunks)
                current = ""
            else:
                current = part
    if current:
        chunks.append(current)

    # 添加重叠
    if chunk_overlap > 0 and len(chunks) > 1:
        overlapped = [chunks[0]]
        for i in range(1, len(chunks)):
            prev_tail = chunks[i - 1][-chunk_overlap:]
            overlapped.append(prev_tail + chunks[i])
        chunks = overlapped

    return chunks


async def split_by_llm(
    text: str,
    chunk_size: int = 500,
    max_chunks: int = 200,
) -> List[str]:
    """
    LLM 语义分割

    利用大模型的深层语义理解来识别最佳分割点。
    仅输出分割位置标记字符串，再由代码执行实际分割。

    流程：
    1. 将文本分成小段发给 LLM
    2. LLM 识别语义边界，输出分割标记（如 <SPLIT>）
    3. 按标记执行分割
    """
    # 文本太短，不需要 LLM 分割
    if len(text) <= chunk_size:
        return [text]

    # 文本太长时先粗切，再对每段做 LLM 语义分割
    if len(text) > 10000:
        rough_chunks = split_by_rules(text, chunk_size=3000, chunk_overlap=100)
        all_chunks = []
        for rough in rough_chunks:
            if len(rough) <= chunk_size:
                all_chunks.append(rough)
            else:
                sub = await _llm_split_segment(rough, chunk_size)
                all_chunks.extend(sub)
        return all_chunks[:max_chunks]

    return await _llm_split_segment(text, chunk_size)


async def _llm_split_segment(text: str, chunk_size: int) -> List[str]:
    """对单个文本段调用 LLM 进行语义分割"""
    prompt = f"""请将以下文本按照语义边界进行分割。

要求：
1. 每个分块控制在 {chunk_size} 字以内
2. 在你认为最合适的语义分割位置插入标记 <SPLIT>
3. 保持每个分块的语义完整性
4. 不要修改原文内容，只插入 <SPLIT> 标记
5. 直接输出带标记的文本，不要添加任何解释

文本内容：
---
{text}
---"""

    try:
        messages = [
            {"role": "system", "content": "你是一个文本分割专家。只需在文本中插入 <SPLIT> 标记，不要修改原文或添加解释。"},
            {"role": "user", "content": prompt},
        ]
        response = await call_llm(messages, stream=False)
        result = response.choices[0].message.content or text

        # 按 <SPLIT> 标记分割
        chunks = [c.strip() for c in result.split("<SPLIT>") if c.strip()]

        if not chunks:
            return split_by_rules(text, chunk_size)

        return chunks

    except Exception as e:
        logger.warning(f"LLM 语义分割失败，回退到规则分割: {e}")
        return split_by_rules(text, chunk_size)


# ============ 完整处理流程 ============


async def process_document(
    file_bytes: bytes,
    filename: str,
    use_llm_split: bool = True,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[dict]:
    """
    完整的文档处理流程：解析 → 清洗 → 分割 → 返回分块

    Args:
        file_bytes: 文件二进制内容
        filename: 文件名（用于识别格式）
        use_llm_split: 是否使用 LLM 语义分割
        chunk_size: 目标分块大小
        chunk_overlap: 分块重叠字数

    Returns:
        [{"content": "...", "chunk_index": 0, "metadata": {"source": filename}}]
    """
    # 1. 解析文件
    text = parse_file(file_bytes, filename)
    if not text.strip():
        return []

    # 2. 清洗
    text = clean_text(text)

    # 3. 分割
    if use_llm_split and len(text) > chunk_size:
        chunks = await split_by_llm(text, chunk_size)
    else:
        chunks = split_by_rules(text, chunk_size, chunk_overlap)

    # 4. 构建结果
    result = []
    for i, content in enumerate(chunks):
        if not content.strip():
            continue
        result.append({
            "content": content,
            "chunk_index": i,
            "metadata": {
                "source": filename,
                "chunk_total": len(chunks),
            },
        })

    return result


def process_text(
    text: str,
    source: str = "text_input",
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[dict]:
    """
    处理纯文本输入（同步版，不使用 LLM 分割）
    """
    text = clean_text(text)
    if not text:
        return []

    chunks = split_by_rules(text, chunk_size, chunk_overlap)
    result = []
    for i, content in enumerate(chunks):
        if not content.strip():
            continue
        result.append({
            "content": content,
            "chunk_index": i,
            "metadata": {"source": source, "chunk_total": len(chunks)},
        })
    return result
