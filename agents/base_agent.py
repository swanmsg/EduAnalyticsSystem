"""
基础智能体类
"""
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel
from config.ollama_config import ollama_manager
from llama_index.core.llms import ChatMessage
import json

logger = logging.getLogger(__name__)


class AgentMessage(BaseModel):
    """智能体消息模型"""
    agent_id: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime
    correlation_id: Optional[str] = None


class AgentResponse(BaseModel):
    """智能体响应模型"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    agent_id: str
    timestamp: datetime


class BaseAgent(ABC):
    """基础智能体类"""
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.is_active = False
        self.message_queue = asyncio.Queue()
        self.capabilities: List[str] = []
        self.performance_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0
        }
        self._task: Optional[asyncio.Task] = None
        
    async def start(self):
        """启动智能体"""
        if self.is_active:
            logger.warning(f"智能体 {self.name} 已经在运行中")
            return
            
        self.is_active = True
        self._task = asyncio.create_task(self._run())
        logger.info(f"✅ 智能体 {self.name} 已启动")
        
    async def stop(self):
        """停止智能体"""
        if not self.is_active:
            return
            
        self.is_active = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info(f"🔄 智能体 {self.name} 已停止")
        
    async def _run(self):
        """智能体主运行循环"""
        while self.is_active:
            try:
                # 处理消息队列
                message = await asyncio.wait_for(
                    self.message_queue.get(), 
                    timeout=1.0
                )
                await self._process_message(message)
            except asyncio.TimeoutError:
                # 超时是正常的，继续循环
                continue
            except Exception as e:
                logger.error(f"智能体 {self.name} 处理消息时发生错误: {str(e)}")
                
    async def _process_message(self, message: AgentMessage) -> AgentResponse:
        """处理消息"""
        start_time = asyncio.get_event_loop().time()
        
        try:
            self.performance_metrics["total_requests"] += 1
            
            # 调用具体的处理方法
            result = await self.handle_message(message)
            
            self.performance_metrics["successful_requests"] += 1
            execution_time = asyncio.get_event_loop().time() - start_time
            
            # 更新平均响应时间
            self._update_average_response_time(execution_time)
            
            return AgentResponse(
                success=True,
                data=result,
                execution_time=execution_time,
                agent_id=self.agent_id,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            self.performance_metrics["failed_requests"] += 1
            execution_time = asyncio.get_event_loop().time() - start_time
            
            logger.error(f"智能体 {self.name} 执行失败: {str(e)}")
            
            return AgentResponse(
                success=False,
                error=str(e),
                execution_time=execution_time,
                agent_id=self.agent_id,
                timestamp=datetime.utcnow()
            )
            
    def _update_average_response_time(self, execution_time: float):
        """更新平均响应时间"""
        current_avg = self.performance_metrics["average_response_time"]
        total_requests = self.performance_metrics["total_requests"]
        
        if total_requests == 1:
            self.performance_metrics["average_response_time"] = execution_time
        else:
            new_avg = ((current_avg * (total_requests - 1)) + execution_time) / total_requests
            self.performance_metrics["average_response_time"] = new_avg
            
    async def send_message(self, message: AgentMessage) -> bool:
        """发送消息到智能体"""
        try:
            await self.message_queue.put(message)
            return True
        except Exception as e:
            logger.error(f"发送消息到智能体 {self.name} 失败: {str(e)}")
            return False
            
    async def get_llm_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """获取LLM响应"""
        try:
            llm = ollama_manager.get_llm()
            
            messages = []
            if system_prompt:
                messages.append(ChatMessage(role="system", content=system_prompt))
            messages.append(ChatMessage(role="user", content=prompt))
            
            response = await llm.achat(messages)
            return response.message.content
            
        except Exception as e:
            logger.error(f"获取LLM响应失败: {str(e)}")
            raise
            
    def get_status(self) -> Dict[str, Any]:
        """获取智能体状态"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "capabilities": self.capabilities,
            "performance_metrics": self.performance_metrics,
            "queue_size": self.message_queue.qsize()
        }
        
    @abstractmethod
    async def handle_message(self, message: AgentMessage) -> Dict[str, Any]:
        """处理消息的抽象方法，由子类实现"""
        pass
        
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """获取智能体能力列表"""
        pass