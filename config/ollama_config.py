"""
Ollama模型配置和连接管理
"""
import asyncio
from typing import Optional, Dict, Any
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings as LlamaSettings
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class OllamaManager:
    """Ollama模型管理器"""
    
    def __init__(self):
        self.llm: Optional[Ollama] = None
        self.embedding: Optional[OllamaEmbedding] = None
        self._initialized = False
    
    async def initialize(self) -> bool:
        """初始化Ollama连接"""
        try:
            logger.info(f"正在连接Ollama服务: {settings.OLLAMA_BASE_URL}")
            
            # 初始化LLM
            self.llm = Ollama(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
                request_timeout=settings.OLLAMA_TIMEOUT,
                temperature=0.7,
                context_window=4096,
                is_function_calling_model=True
            )
            
            # 初始化嵌入模型
            self.embedding = OllamaEmbedding(
                model_name=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL
            )
            
            # 设置全局LlamaIndex配置
            LlamaSettings.llm = self.llm
            LlamaSettings.embed_model = self.embedding
            
            # 测试连接
            await self._test_connection()
            
            self._initialized = True
            logger.info("✅ Ollama连接初始化成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ollama连接初始化失败: {str(e)}")
            return False
    
    async def _test_connection(self):
        """测试Ollama连接"""
        try:
            # 测试LLM连接
            response = await self.llm.acomplete("Hello")
            logger.info(f"LLM测试响应: {response.text[:50]}...")
            
            # 测试嵌入模型连接
            embeddings = await self.embedding.aget_text_embedding("test")
            logger.info(f"嵌入模型测试成功，维度: {len(embeddings)}")
            
        except Exception as e:
            raise Exception(f"Ollama连接测试失败: {str(e)}")
    
    def get_llm(self) -> Ollama:
        """获取LLM实例"""
        if not self._initialized or self.llm is None:
            raise RuntimeError("Ollama尚未初始化")
        return self.llm
    
    def get_embedding(self) -> OllamaEmbedding:
        """获取嵌入模型实例"""
        if not self._initialized or self.embedding is None:
            raise RuntimeError("Ollama嵌入模型尚未初始化")
        return self.embedding
    
    async def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            if not self._initialized:
                return {"status": "error", "message": "未初始化"}
            
            # 简单的健康检查
            start_time = asyncio.get_event_loop().time()
            response = await self.llm.acomplete("ping")
            end_time = asyncio.get_event_loop().time()
            
            return {
                "status": "healthy",
                "model": settings.OLLAMA_MODEL,
                "base_url": settings.OLLAMA_BASE_URL,
                "response_time": round(end_time - start_time, 3),
                "response_length": len(response.text)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


# 全局Ollama管理器实例
ollama_manager = OllamaManager()