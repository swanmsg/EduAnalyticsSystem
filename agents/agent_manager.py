"""
智能体管理器
负责协调和管理所有智能体的运行
"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import logging

from agents.base_agent import BaseAgent, AgentMessage, AgentResponse
from agents.data_analysis_agent import DataAnalysisAgent
from agents.report_generation_agent import ReportGenerationAgent
from agents.interface_management_agent import InterfaceManagementAgent

logger = logging.getLogger(__name__)


class AgentManager:
    """智能体管理器"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_workflows: Dict[str, List[str]] = {}
        self.message_history: List[Dict] = []
        self.is_initialized = False
        
    async def initialize(self):
        """初始化所有智能体"""
        try:
            logger.info("正在初始化智能体管理器...")
            
            # 创建智能体实例
            self.agents = {
                "data_analysis": DataAnalysisAgent(),
                "report_generation": ReportGenerationAgent(),
                "interface_management": InterfaceManagementAgent()
            }
            
            # 启动所有智能体
            for agent_id, agent in self.agents.items():
                await agent.start()
                logger.info(f"智能体 {agent_id} 已启动")
            
            # 定义工作流程
            self._setup_workflows()
            
            self.is_initialized = True
            logger.info("✅ 智能体管理器初始化完成")
            
        except Exception as e:
            logger.error(f"❌ 智能体管理器初始化失败: {str(e)}")
            raise
            
    def _setup_workflows(self):
        """设置智能体工作流程"""
        # 完整分析工作流：数据分析 -> 报告生成 -> 接口导出
        self.agent_workflows["complete_analysis"] = [
            "data_analysis",
            "report_generation", 
            "interface_management"
        ]
        
        # 数据导出工作流：数据分析 -> 接口导出
        self.agent_workflows["data_export"] = [
            "data_analysis",
            "interface_management"
        ]
        
        # 报告生成工作流：数据分析 -> 报告生成
        self.agent_workflows["report_only"] = [
            "data_analysis",
            "report_generation"
        ]
        
    async def shutdown(self):
        """关闭所有智能体"""
        logger.info("正在关闭智能体管理器...")
        
        for agent_id, agent in self.agents.items():
            await agent.stop()
            logger.info(f"智能体 {agent_id} 已关闭")
            
        self.is_initialized = False
        logger.info("智能体管理器已关闭")
        
    async def execute_analysis(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """执行分析请求"""
        if not self.is_initialized:
            raise RuntimeError("智能体管理器未初始化")
            
        correlation_id = str(uuid.uuid4())
        request_type = request.get("type", "complete_analysis")
        
        try:
            logger.info(f"开始执行分析请求: {correlation_id}")
            
            # 数据分析阶段
            analysis_result = await self._execute_data_analysis(request, correlation_id)
            
            results = {
                "correlation_id": correlation_id,
                "request_type": request_type,
                "analysis_result": analysis_result,
                "started_at": datetime.utcnow().isoformat()
            }
            
            # 根据请求类型执行后续步骤
            if request_type in ["complete_analysis", "report_only"]:
                # 报告生成阶段
                report_result = await self._execute_report_generation(
                    analysis_result, request, correlation_id
                )
                results["report_result"] = report_result
                
            if request_type in ["complete_analysis", "data_export"]:
                # 接口管理阶段
                export_result = await self._execute_data_export(
                    analysis_result, request, correlation_id
                )
                results["export_result"] = export_result
                
            results["completed_at"] = datetime.utcnow().isoformat()
            results["status"] = "completed"
            
            logger.info(f"分析请求执行完成: {correlation_id}")
            return results
            
        except Exception as e:
            logger.error(f"分析请求执行失败: {correlation_id}, 错误: {str(e)}")
            return {
                "correlation_id": correlation_id,
                "status": "failed",
                "error": str(e),
                "failed_at": datetime.utcnow().isoformat()
            }
            
    async def _execute_data_analysis(self, request: Dict[str, Any], correlation_id: str) -> Dict[str, Any]:
        """执行数据分析"""
        analysis_agent = self.agents["data_analysis"]
        
        # 构造分析消息
        analysis_params = {
            "student_ids": request.get("student_ids", []),
            "case_ids": request.get("case_ids", []),
            "time_range": request.get("time_range", {}),
            "analysis_types": request.get("analysis_types", ["comprehensive"])
        }
        
        message = AgentMessage(
            agent_id="data_analysis",
            message_type="comprehensive_analysis",
            content=analysis_params,
            timestamp=datetime.utcnow(),
            correlation_id=correlation_id
        )
        
        # 发送消息并等待结果
        await analysis_agent.send_message(message)
        
        # 等待分析完成（简化实现，实际应该有更好的异步处理机制）
        await asyncio.sleep(1)  # 给智能体处理时间
        
        return {
            "status": "completed",
            "message": "数据分析完成",
            "analysis_data": {}  # 这里应该包含实际的分析结果
        }
        
    async def _execute_report_generation(self, analysis_result: Dict, request: Dict, correlation_id: str) -> Dict[str, Any]:
        """执行报告生成"""
        report_agent = self.agents["report_generation"]
        
        report_params = {
            "report_type": request.get("report_type", "comprehensive"),
            "analysis_data": analysis_result.get("analysis_data", {}),
            "target_audience": request.get("target_audience", "teacher"),
            "format": request.get("report_format", "html")
        }
        
        message = AgentMessage(
            agent_id="report_generation",
            message_type=f"generate_{request.get('report_type', 'overall')}_report",
            content=report_params,
            timestamp=datetime.utcnow(),
            correlation_id=correlation_id
        )
        
        await report_agent.send_message(message)
        await asyncio.sleep(1)
        
        return {
            "status": "completed", 
            "message": "报告生成完成",
            "report_data": {}
        }
        
    async def _execute_data_export(self, analysis_result: Dict, request: Dict, correlation_id: str) -> Dict[str, Any]:
        """执行数据导出"""
        interface_agent = self.agents["interface_management"]
        
        export_params = {
            "data": analysis_result.get("analysis_data", {}),
            "format": request.get("export_format", "json"),
            "target_system": request.get("target_system"),
            "data_type": "analysis_result"
        }
        
        message = AgentMessage(
            agent_id="interface_management",
            message_type="export_data",
            content=export_params,
            timestamp=datetime.utcnow(),
            correlation_id=correlation_id
        )
        
        await interface_agent.send_message(message)
        await asyncio.sleep(1)
        
        return {
            "status": "completed",
            "message": "数据导出完成", 
            "export_info": {}
        }
        
    async def send_message_to_agent(self, agent_id: str, message: AgentMessage) -> bool:
        """发送消息到指定智能体"""
        if agent_id not in self.agents:
            raise ValueError(f"智能体不存在: {agent_id}")
            
        agent = self.agents[agent_id]
        success = await agent.send_message(message)
        
        # 记录消息历史
        self.message_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": agent_id,
            "message_type": message.message_type,
            "correlation_id": message.correlation_id,
            "success": success
        })
        
        return success
        
    def get_agent_status(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """获取智能体状态"""
        if agent_id:
            if agent_id not in self.agents:
                raise ValueError(f"智能体不存在: {agent_id}")
            return self.agents[agent_id].get_status()
        else:
            return {
                agent_id: agent.get_status() 
                for agent_id, agent in self.agents.items()
            }
            
    def get_system_metrics(self) -> Dict[str, Any]:
        """获取系统指标"""
        total_requests = sum(
            agent.performance_metrics["total_requests"] 
            for agent in self.agents.values()
        )
        
        total_successful = sum(
            agent.performance_metrics["successful_requests"]
            for agent in self.agents.values()
        )
        
        average_response_time = sum(
            agent.performance_metrics["average_response_time"]
            for agent in self.agents.values()
        ) / len(self.agents) if self.agents else 0
        
        return {
            "total_agents": len(self.agents),
            "active_agents": sum(1 for agent in self.agents.values() if agent.is_active),
            "total_requests": total_requests,
            "successful_requests": total_successful,
            "success_rate": total_successful / total_requests if total_requests > 0 else 0,
            "average_response_time": average_response_time,
            "message_history_count": len(self.message_history),
            "system_uptime": datetime.utcnow().isoformat(),
            "workflows_available": list(self.agent_workflows.keys())
        }