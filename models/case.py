"""
教学案例数据模型
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from config.database import Base
from enum import Enum


class CaseType(str, Enum):
    """案例类型枚举"""
    THEORY = "theory"  # 理论案例
    PRACTICE = "practice"  # 实践案例
    EXPERIMENT = "experiment"  # 实验案例
    PROJECT = "project"  # 项目案例


class CaseDifficulty(str, Enum):
    """案例难度枚举"""
    EASY = "easy"  # 简单
    MEDIUM = "medium"  # 中等
    HARD = "hard"  # 困难


class Case(Base):
    """教学案例数据表"""
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True, comment="案例ID")
    case_id = Column(String(50), unique=True, index=True, nullable=False, comment="案例编号")
    title = Column(String(200), nullable=False, comment="案例标题")
    description = Column(Text, comment="案例描述")
    content = Column(Text, comment="案例内容")
    
    # 案例分类信息
    case_type = Column(String(20), default=CaseType.THEORY, comment="案例类型")
    difficulty = Column(String(20), default=CaseDifficulty.MEDIUM, comment="难度等级")
    subject = Column(String(100), comment="学科")
    chapter = Column(String(100), comment="章节")
    knowledge_points = Column(JSON, comment="知识点列表")
    
    # 案例配置
    time_limit = Column(Integer, comment="时间限制(分钟)")
    max_attempts = Column(Integer, default=3, comment="最大尝试次数")
    passing_score = Column(Integer, default=60, comment="及格分数")
    
    # 案例状态
    is_active = Column(Boolean, default=True, comment="是否启用")
    is_published = Column(Boolean, default=False, comment="是否发布")
    
    # 创建者信息
    author = Column(String(100), comment="作者")
    created_by = Column(String(100), comment="创建者")
    
    # 时间信息
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    published_at = Column(DateTime, comment="发布时间")
    
    # 统计信息
    view_count = Column(Integer, default=0, comment="查看次数")
    attempt_count = Column(Integer, default=0, comment="尝试次数")
    
    # 备注信息
    notes = Column(Text, comment="备注")
    
    # 关联关系
    operation_logs = relationship("OperationLog", back_populates="case")
    scores = relationship("Score", back_populates="case")


class CaseCreate(BaseModel):
    """创建案例的数据模型"""
    case_id: str = Field(..., description="案例编号")
    title: str = Field(..., description="案例标题")
    description: Optional[str] = Field(None, description="案例描述")
    content: Optional[str] = Field(None, description="案例内容")
    case_type: CaseType = Field(CaseType.THEORY, description="案例类型")
    difficulty: CaseDifficulty = Field(CaseDifficulty.MEDIUM, description="难度等级")
    subject: Optional[str] = Field(None, description="学科")
    chapter: Optional[str] = Field(None, description="章节")
    knowledge_points: Optional[List[str]] = Field(None, description="知识点列表")
    time_limit: Optional[int] = Field(None, description="时间限制(分钟)")
    max_attempts: int = Field(3, description="最大尝试次数")
    passing_score: int = Field(60, description="及格分数")
    author: Optional[str] = Field(None, description="作者")
    created_by: Optional[str] = Field(None, description="创建者")
    notes: Optional[str] = Field(None, description="备注")


class CaseUpdate(BaseModel):
    """更新案例的数据模型"""
    title: Optional[str] = Field(None, description="案例标题")
    description: Optional[str] = Field(None, description="案例描述")
    content: Optional[str] = Field(None, description="案例内容")
    case_type: Optional[CaseType] = Field(None, description="案例类型")
    difficulty: Optional[CaseDifficulty] = Field(None, description="难度等级")
    subject: Optional[str] = Field(None, description="学科")
    chapter: Optional[str] = Field(None, description="章节")
    knowledge_points: Optional[List[str]] = Field(None, description="知识点列表")
    time_limit: Optional[int] = Field(None, description="时间限制(分钟)")
    max_attempts: Optional[int] = Field(None, description="最大尝试次数")
    passing_score: Optional[int] = Field(None, description="及格分数")
    is_active: Optional[bool] = Field(None, description="是否启用")
    is_published: Optional[bool] = Field(None, description="是否发布")
    author: Optional[str] = Field(None, description="作者")
    notes: Optional[str] = Field(None, description="备注")


class CaseResponse(BaseModel):
    """案例响应数据模型"""
    id: int
    case_id: str
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    case_type: str
    difficulty: str
    subject: Optional[str] = None
    chapter: Optional[str] = None
    knowledge_points: Optional[List[str]] = None
    time_limit: Optional[int] = None
    max_attempts: int
    passing_score: int
    is_active: bool
    is_published: bool
    author: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    view_count: int
    attempt_count: int
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True


class CaseListResponse(BaseModel):
    """案例列表响应数据模型"""
    cases: List[CaseResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class CaseQuery(BaseModel):
    """案例查询参数"""
    case_id: Optional[str] = Field(None, description="案例编号")
    title: Optional[str] = Field(None, description="案例标题")
    case_type: Optional[CaseType] = Field(None, description="案例类型")
    difficulty: Optional[CaseDifficulty] = Field(None, description="难度等级")
    subject: Optional[str] = Field(None, description="学科")
    chapter: Optional[str] = Field(None, description="章节")
    knowledge_point: Optional[str] = Field(None, description="知识点")
    is_active: Optional[bool] = Field(None, description="是否启用")
    is_published: Optional[bool] = Field(None, description="是否发布")
    author: Optional[str] = Field(None, description="作者")
    created_after: Optional[datetime] = Field(None, description="创建时间起始")
    created_before: Optional[datetime] = Field(None, description="创建时间结束")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")