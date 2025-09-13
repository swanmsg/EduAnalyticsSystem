"""
数据分析API路由
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from datetime import datetime
from agents.agent_manager import AgentManager
from agents.base_agent import AgentMessage
from models import AnalysisType, ReportType

router = APIRouter()

# 全局智能体管理器实例（将在应用启动时设置）
agent_manager = None


class AnalysisRequest(BaseModel):
    """分析请求模型"""
    analysis_type: AnalysisType = Field(..., description="分析类型")
    student_ids: Optional[List[int]] = Field(None, description="目标学生ID列表")
    case_ids: Optional[List[int]] = Field(None, description="目标案例ID列表")
    time_range: Optional[dict] = Field(None, description="时间范围")
    parameters: Optional[dict] = Field({}, description="额外参数")


class ReportRequest(BaseModel):
    """报告生成请求模型"""
    report_type: ReportType = Field(..., description="报告类型")
    analysis_id: Optional[str] = Field(None, description="基于的分析ID")
    student_ids: Optional[List[int]] = Field(None, description="目标学生ID列表")
    class_name: Optional[str] = Field(None, description="班级名称")
    subject: Optional[str] = Field(None, description="学科")
    format: str = Field("html", description="报告格式")
    parameters: Optional[dict] = Field({}, description="额外参数")


def get_agent_manager() -> AgentManager:
    """获取智能体管理器"""
    global agent_manager
    if agent_manager is None:
        raise HTTPException(status_code=503, detail="智能体管理器未初始化")
    return agent_manager


@router.post("/analyze", summary="执行数据分析")
async def execute_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    manager: AgentManager = Depends(get_agent_manager)
):
    """执行数据分析任务"""
    try:
        # 构造分析参数
        analysis_params = {
            "type": "data_analysis",
            "analysis_type": request.analysis_type,
            "student_ids": request.student_ids or [],
            "case_ids": request.case_ids or [],
            "time_range": request.time_range or {},
            "parameters": request.parameters
        }
        
        # 在后台执行分析
        def run_analysis():
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(manager.execute_analysis(analysis_params))
        
        background_tasks.add_task(run_analysis)
        
        return {
            "message": "分析任务已启动",
            "analysis_type": request.analysis_type,
            "status": "started",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动分析任务失败: {str(e)}")


@router.post("/analyze/sync", summary="同步执行数据分析")
async def execute_analysis_sync(
    request: AnalysisRequest,
    manager: AgentManager = Depends(get_agent_manager)
):
    """同步执行数据分析（等待结果）"""
    try:
        analysis_params = {
            "type": "data_analysis",
            "analysis_type": request.analysis_type,
            "student_ids": request.student_ids or [],
            "case_ids": request.case_ids or [],
            "time_range": request.time_range or {},
            "parameters": request.parameters
        }
        
        result = await manager.execute_analysis(analysis_params)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行分析失败: {str(e)}")


@router.post("/reports/generate", summary="生成分析报告")
async def generate_report(
    request: ReportRequest,
    background_tasks: BackgroundTasks,
    manager: AgentManager = Depends(get_agent_manager)
):
    """生成分析报告"""
    try:
        report_params = {
            "type": "report_only",
            "report_type": request.report_type,
            "student_ids": request.student_ids or [],
            "class_name": request.class_name,
            "subject": request.subject,
            "report_format": request.format,
            "parameters": request.parameters
        }
        
        def run_report_generation():
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(manager.execute_analysis(report_params))
        
        background_tasks.add_task(run_report_generation)
        
        return {
            "message": "报告生成任务已启动",
            "report_type": request.report_type,
            "format": request.format,
            "status": "started",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动报告生成失败: {str(e)}")


@router.post("/comprehensive", summary="综合分析（分析+报告）")
async def comprehensive_analysis(
    analysis_request: AnalysisRequest,
    report_request: ReportRequest,
    background_tasks: BackgroundTasks,
    manager: AgentManager = Depends(get_agent_manager)
):
    """执行综合分析，包括数据分析和报告生成"""
    try:
        comprehensive_params = {
            "type": "complete_analysis",
            "analysis_type": analysis_request.analysis_type,
            "report_type": report_request.report_type,
            "student_ids": analysis_request.student_ids or [],
            "case_ids": analysis_request.case_ids or [],
            "time_range": analysis_request.time_range or {},
            "report_format": report_request.format,
            "class_name": report_request.class_name,
            "subject": report_request.subject,
            "analysis_parameters": analysis_request.parameters,
            "report_parameters": report_request.parameters
        }
        
        def run_comprehensive_analysis():
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(manager.execute_analysis(comprehensive_params))
        
        background_tasks.add_task(run_comprehensive_analysis)
        
        return {
            "message": "综合分析任务已启动",
            "analysis_type": analysis_request.analysis_type,
            "report_type": report_request.report_type,
            "status": "started",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动综合分析失败: {str(e)}")


@router.get("/student/{student_id}/behavior", summary="学生行为分析")
async def analyze_student_behavior(
    student_id: int,
    days: int = 30,
    manager: AgentManager = Depends(get_agent_manager)
):
    """分析特定学生的行为模式"""
    try:
        analysis_params = {
            "type": "data_analysis",
            "analysis_type": "student_behavior",
            "student_ids": [student_id],
            "time_range": {"days": days}
        }
        
        result = await manager.execute_analysis(analysis_params)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"学生行为分析失败: {str(e)}")


@router.get("/class/{class_name}/performance", summary="班级成绩分析")
async def analyze_class_performance(
    class_name: str,
    subject: Optional[str] = None,
    manager: AgentManager = Depends(get_agent_manager)
):
    """分析班级整体成绩表现"""
    try:
        # 这里需要先获取班级学生ID列表
        # 简化实现，实际应该从数据库查询
        analysis_params = {
            "type": "data_analysis",
            "analysis_type": "performance_trend",
            "class_name": class_name,
            "subject": subject
        }
        
        result = await manager.execute_analysis(analysis_params)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"班级成绩分析失败: {str(e)}")


@router.get("/knowledge-points/{subject}/mastery", summary="知识点掌握分析")
async def analyze_knowledge_mastery(
    subject: str,
    student_ids: Optional[List[int]] = None,
    manager: AgentManager = Depends(get_agent_manager)
):
    """分析知识点掌握情况"""
    try:
        analysis_params = {
            "type": "data_analysis",
            "analysis_type": "knowledge_mastery",
            "subject": subject,
            "student_ids": student_ids or []
        }
        
        result = await manager.execute_analysis(analysis_params)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"知识点掌握分析失败: {str(e)}")


@router.get("/choice-patterns/analysis", summary="选择题答题模式分析")
async def analyze_choice_patterns(
    student_ids: Optional[List[int]] = None,
    time_range_days: int = 90,
    manager: AgentManager = Depends(get_agent_manager)
):
    """分析选择题答题模式和习惯"""
    try:
        analysis_params = {
            "type": "data_analysis",
            "analysis_type": "choice_pattern",
            "student_ids": student_ids or [],
            "time_range": {"days": time_range_days}
        }
        
        result = await manager.execute_analysis(analysis_params)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"选择题模式分析失败: {str(e)}")


@router.get("/trends/learning", summary="学习趋势分析")
async def analyze_learning_trends(
    student_ids: Optional[List[int]] = None,
    time_range_days: int = 180,
    manager: AgentManager = Depends(get_agent_manager)
):
    """分析学习趋势和发展轨迹"""
    try:
        analysis_params = {
            "type": "data_analysis", 
            "analysis_type": "performance_trend",
            "student_ids": student_ids or [],
            "time_range": {"days": time_range_days}
        }
        
        result = await manager.execute_analysis(analysis_params)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"学习趋势分析失败: {str(e)}")


# 在应用启动时设置智能体管理器
def set_agent_manager(manager: AgentManager):
    """设置全局智能体管理器"""
    global agent_manager
    agent_manager = manager