"""
成绩数据模型
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from config.database import Base
from enum import Enum


class ScoreStatus(str, Enum):
    """成绩状态枚举"""
    PENDING = "pending"  # 待评分
    GRADED = "graded"  # 已评分
    REVIEWING = "reviewing"  # 复核中
    FINAL = "final"  # 最终成绩


class QuestionType(str, Enum):
    """题目类型枚举"""
    SINGLE_CHOICE = "single_choice"  # 单选题
    MULTI_CHOICE = "multi_choice"  # 多选题
    TRUE_FALSE = "true_false"  # 判断题
    FILL_BLANK = "fill_blank"  # 填空题
    SHORT_ANSWER = "short_answer"  # 简答题
    ESSAY = "essay"  # 论述题
    PRACTICAL = "practical"  # 实践题


class Score(Base):
    """成绩数据表"""
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True, comment="成绩ID")
    
    # 关联信息
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, comment="学生ID")
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False, comment="案例ID")
    
    # 基本成绩信息
    total_score = Column(Float, comment="总分")
    obtained_score = Column(Float, comment="得分")
    percentage = Column(Float, comment="得分率")
    grade = Column(String(10), comment="等级(A/B/C/D/F)")
    
    # 考试信息
    attempt_number = Column(Integer, default=1, comment="尝试次数")
    max_attempts = Column(Integer, default=3, comment="最大尝试次数")
    is_passed = Column(Boolean, default=False, comment="是否通过")
    
    # 时间信息
    start_time = Column(DateTime, comment="开始时间")
    submit_time = Column(DateTime, comment="提交时间")
    duration = Column(Integer, comment="用时(秒)")
    time_limit = Column(Integer, comment="时间限制(秒)")
    
    # 答题详情
    question_details = Column(JSON, comment="题目详情")
    answer_analysis = Column(JSON, comment="答案分析")
    
    # 智能分析结果
    ai_feedback = Column(Text, comment="AI反馈")
    behavior_analysis = Column(JSON, comment="行为分析")
    knowledge_mastery = Column(JSON, comment="知识点掌握情况")
    
    # 状态信息
    status = Column(String(20), default=ScoreStatus.PENDING, comment="成绩状态")
    
    # 评分信息
    auto_graded = Column(Boolean, default=True, comment="是否自动评分")
    manual_graded = Column(Boolean, default=False, comment="是否人工评分")
    grader_id = Column(String(100), comment="评分人ID")
    graded_at = Column(DateTime, comment="评分时间")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关联关系
    student = relationship("Student", back_populates="scores")
    case = relationship("Case", back_populates="scores")


class QuestionScore(BaseModel):
    """单题成绩数据模型"""
    question_id: str = Field(..., description="题目ID")
    question_type: QuestionType = Field(..., description="题目类型")
    question_content: str = Field(..., description="题目内容")
    student_answer: Optional[str] = Field(None, description="学生答案")
    correct_answer: Optional[str] = Field(None, description="正确答案")
    score: float = Field(..., description="得分")
    max_score: float = Field(..., description="满分")
    is_correct: bool = Field(..., description="是否正确")
    time_spent: Optional[int] = Field(None, description="用时(秒)")
    knowledge_points: Optional[List[str]] = Field(None, description="涉及知识点")
    ai_analysis: Optional[str] = Field(None, description="AI分析")


class ScoreCreate(BaseModel):
    """创建成绩的数据模型"""
    student_id: int = Field(..., description="学生ID")
    case_id: int = Field(..., description="案例ID")
    total_score: float = Field(..., description="总分")
    obtained_score: float = Field(..., description="得分")
    attempt_number: int = Field(1, description="尝试次数")
    start_time: datetime = Field(..., description="开始时间")
    submit_time: datetime = Field(..., description="提交时间")
    duration: int = Field(..., description="用时(秒)")
    time_limit: Optional[int] = Field(None, description="时间限制(秒)")
    question_details: Optional[List[QuestionScore]] = Field(None, description="题目详情")
    notes: Optional[str] = Field(None, description="备注")


class ScoreUpdate(BaseModel):
    """更新成绩的数据模型"""
    obtained_score: Optional[float] = Field(None, description="得分")
    grade: Optional[str] = Field(None, description="等级")
    is_passed: Optional[bool] = Field(None, description="是否通过")
    ai_feedback: Optional[str] = Field(None, description="AI反馈")
    behavior_analysis: Optional[Dict[str, Any]] = Field(None, description="行为分析")
    knowledge_mastery: Optional[Dict[str, Any]] = Field(None, description="知识点掌握情况")
    status: Optional[ScoreStatus] = Field(None, description="成绩状态")
    manual_graded: Optional[bool] = Field(None, description="是否人工评分")
    grader_id: Optional[str] = Field(None, description="评分人ID")
    notes: Optional[str] = Field(None, description="备注")


class ScoreResponse(BaseModel):
    """成绩响应数据模型"""
    id: int
    student_id: int
    case_id: int
    total_score: Optional[float] = None
    obtained_score: Optional[float] = None
    percentage: Optional[float] = None
    grade: Optional[str] = None
    attempt_number: int
    max_attempts: int
    is_passed: bool
    start_time: Optional[datetime] = None
    submit_time: Optional[datetime] = None
    duration: Optional[int] = None
    time_limit: Optional[int] = None
    question_details: Optional[List[Dict[str, Any]]] = None
    answer_analysis: Optional[Dict[str, Any]] = None
    ai_feedback: Optional[str] = None
    behavior_analysis: Optional[Dict[str, Any]] = None
    knowledge_mastery: Optional[Dict[str, Any]] = None
    status: str
    auto_graded: bool
    manual_graded: bool
    grader_id: Optional[str] = None
    graded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True


class ScoreListResponse(BaseModel):
    """成绩列表响应数据模型"""
    scores: List[ScoreResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ScoreQuery(BaseModel):
    """成绩查询参数"""
    student_id: Optional[int] = Field(None, description="学生ID")
    case_id: Optional[int] = Field(None, description="案例ID")
    min_score: Optional[float] = Field(None, description="最低分数")
    max_score: Optional[float] = Field(None, description="最高分数")
    grade: Optional[str] = Field(None, description="等级")
    is_passed: Optional[bool] = Field(None, description="是否通过")
    status: Optional[ScoreStatus] = Field(None, description="成绩状态")
    attempt_number: Optional[int] = Field(None, description="尝试次数")
    start_after: Optional[datetime] = Field(None, description="开始时间起始")
    start_before: Optional[datetime] = Field(None, description="开始时间结束")
    submit_after: Optional[datetime] = Field(None, description="提交时间起始")
    submit_before: Optional[datetime] = Field(None, description="提交时间结束")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")


class ScoreStatistics(BaseModel):
    """成绩统计数据模型"""
    total_submissions: int = Field(..., description="总提交数")
    passed_submissions: int = Field(..., description="通过数")
    failed_submissions: int = Field(..., description="未通过数")
    pass_rate: float = Field(..., description="通过率")
    average_score: Optional[float] = Field(None, description="平均分")
    highest_score: Optional[float] = Field(None, description="最高分")
    lowest_score: Optional[float] = Field(None, description="最低分")
    average_duration: Optional[float] = Field(None, description="平均用时(秒)")
    score_distribution: Dict[str, int] = Field(..., description="分数分布")
    grade_distribution: Dict[str, int] = Field(..., description="等级分布")
    attempt_distribution: Dict[int, int] = Field(..., description="尝试次数分布")