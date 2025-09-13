"""
分析结果数据模型
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from config.database import Base
from enum import Enum


class AnalysisType(str, Enum):
    """分析类型枚举"""
    STUDENT_BEHAVIOR = "student_behavior"  # 学生行为分析
    LEARNING_PATTERN = "learning_pattern"  # 学习模式分析
    KNOWLEDGE_MASTERY = "knowledge_mastery"  # 知识点掌握分析
    PERFORMANCE_TREND = "performance_trend"  # 成绩趋势分析
    CHOICE_PATTERN = "choice_pattern"  # 选择题答题模式分析
    TIME_ANALYSIS = "time_analysis"  # 时间分析
    DIFFICULTY_ANALYSIS = "difficulty_analysis"  # 难度分析
    COMPREHENSIVE = "comprehensive"  # 综合分析


class ReportType(str, Enum):
    """报告类型枚举"""
    INDIVIDUAL = "individual"  # 个人报告
    CLASS = "class"  # 班级报告
    SUBJECT = "subject"  # 学科报告
    OVERALL = "overall"  # 整体报告


class AnalysisStatus(str, Enum):
    """分析状态枚举"""
    PENDING = "pending"  # 待分析
    PROCESSING = "processing"  # 分析中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 分析失败


class AnalysisResult(Base):
    """分析结果数据表"""
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True, comment="分析ID")
    
    # 分析基本信息
    analysis_id = Column(String(100), unique=True, index=True, nullable=False, comment="分析编号")
    title = Column(String(200), nullable=False, comment="分析标题")
    description = Column(Text, comment="分析描述")
    
    # 分析类型和范围
    analysis_type = Column(String(50), nullable=False, comment="分析类型")
    report_type = Column(String(50), nullable=False, comment="报告类型")
    
    # 分析目标
    target_students = Column(JSON, comment="目标学生列表")
    target_cases = Column(JSON, comment="目标案例列表")
    target_time_range = Column(JSON, comment="目标时间范围")
    
    # 分析结果
    analysis_data = Column(JSON, comment="分析数据")
    summary = Column(Text, comment="分析摘要")
    insights = Column(JSON, comment="关键洞察")
    recommendations = Column(JSON, comment="建议")
    
    # 统计指标
    metrics = Column(JSON, comment="统计指标")
    
    # 可视化数据
    charts_data = Column(JSON, comment="图表数据")
    
    # 状态信息
    status = Column(String(20), default=AnalysisStatus.PENDING, comment="分析状态")
    progress = Column(Float, default=0.0, comment="进度百分比")
    
    # 执行信息
    started_at = Column(DateTime, comment="开始时间")
    completed_at = Column(DateTime, comment="完成时间")
    duration = Column(Integer, comment="执行时长(秒)")
    
    # 创建者信息
    created_by = Column(String(100), comment="创建者")
    
    # 错误信息
    error_message = Column(Text, comment="错误信息")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 访问控制
    is_public = Column(Boolean, default=False, comment="是否公开")
    
    # 版本控制
    version = Column(String(20), default="1.0", comment="版本号")
    
    # 备注
    notes = Column(Text, comment="备注")


class AnalysisCreate(BaseModel):
    """创建分析的数据模型"""
    title: str = Field(..., description="分析标题")
    description: Optional[str] = Field(None, description="分析描述")
    analysis_type: AnalysisType = Field(..., description="分析类型")
    report_type: ReportType = Field(..., description="报告类型")
    target_students: Optional[List[int]] = Field(None, description="目标学生ID列表")
    target_cases: Optional[List[int]] = Field(None, description="目标案例ID列表")
    target_time_range: Optional[Dict[str, Any]] = Field(None, description="目标时间范围")
    created_by: Optional[str] = Field(None, description="创建者")
    is_public: bool = Field(False, description="是否公开")
    notes: Optional[str] = Field(None, description="备注")


class AnalysisUpdate(BaseModel):
    """更新分析的数据模型"""
    title: Optional[str] = Field(None, description="分析标题")
    description: Optional[str] = Field(None, description="分析描述")
    analysis_data: Optional[Dict[str, Any]] = Field(None, description="分析数据")
    summary: Optional[str] = Field(None, description="分析摘要")
    insights: Optional[List[Dict[str, Any]]] = Field(None, description="关键洞察")
    recommendations: Optional[List[Dict[str, Any]]] = Field(None, description="建议")
    metrics: Optional[Dict[str, Any]] = Field(None, description="统计指标")
    charts_data: Optional[Dict[str, Any]] = Field(None, description="图表数据")
    status: Optional[AnalysisStatus] = Field(None, description="分析状态")
    progress: Optional[float] = Field(None, description="进度百分比")
    completed_at: Optional[datetime] = Field(None, description="完成时间")
    duration: Optional[int] = Field(None, description="执行时长(秒)")
    error_message: Optional[str] = Field(None, description="错误信息")
    is_public: Optional[bool] = Field(None, description="是否公开")
    notes: Optional[str] = Field(None, description="备注")


class AnalysisResponse(BaseModel):
    """分析结果响应数据模型"""
    id: int
    analysis_id: str
    title: str
    description: Optional[str] = None
    analysis_type: str
    report_type: str
    target_students: Optional[List[int]] = None
    target_cases: Optional[List[int]] = None
    target_time_range: Optional[Dict[str, Any]] = None
    analysis_data: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    insights: Optional[List[Dict[str, Any]]] = None
    recommendations: Optional[List[Dict[str, Any]]] = None
    metrics: Optional[Dict[str, Any]] = None
    charts_data: Optional[Dict[str, Any]] = None
    status: str
    progress: float
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration: Optional[int] = None
    created_by: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_public: bool
    version: str
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True


class AnalysisListResponse(BaseModel):
    """分析结果列表响应数据模型"""
    analyses: List[AnalysisResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AnalysisQuery(BaseModel):
    """分析结果查询参数"""
    analysis_id: Optional[str] = Field(None, description="分析编号")
    title: Optional[str] = Field(None, description="分析标题")
    analysis_type: Optional[AnalysisType] = Field(None, description="分析类型")
    report_type: Optional[ReportType] = Field(None, description="报告类型")
    status: Optional[AnalysisStatus] = Field(None, description="分析状态")
    created_by: Optional[str] = Field(None, description="创建者")
    is_public: Optional[bool] = Field(None, description="是否公开")
    created_after: Optional[datetime] = Field(None, description="创建时间起始")
    created_before: Optional[datetime] = Field(None, description="创建时间结束")
    completed_after: Optional[datetime] = Field(None, description="完成时间起始")
    completed_before: Optional[datetime] = Field(None, description="完成时间结束")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")


class BehaviorInsight(BaseModel):
    """行为洞察数据模型"""
    pattern_type: str = Field(..., description="模式类型")
    description: str = Field(..., description="描述")
    confidence: float = Field(..., description="置信度")
    evidence: List[str] = Field(..., description="证据")
    impact: str = Field(..., description="影响")


class KnowledgePoint(BaseModel):
    """知识点掌握情况数据模型"""
    name: str = Field(..., description="知识点名称")
    mastery_level: float = Field(..., description="掌握程度(0-1)")
    attempted_count: int = Field(..., description="尝试次数")
    correct_count: int = Field(..., description="正确次数")
    difficulty: float = Field(..., description="难度系数")
    improvement_suggestions: List[str] = Field(..., description="改进建议")


class LearningRecommendation(BaseModel):
    """学习建议数据模型"""
    type: str = Field(..., description="建议类型")
    priority: str = Field(..., description="优先级")
    title: str = Field(..., description="建议标题")
    description: str = Field(..., description="建议描述")
    action_items: List[str] = Field(..., description="行动项")
    expected_outcome: str = Field(..., description="预期结果")