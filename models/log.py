"""
操作日志数据模型
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from config.database import Base
from enum import Enum


class LogType(str, Enum):
    """日志类型枚举"""
    LOGIN = "login"  # 登录
    LOGOUT = "logout"  # 登出
    VIEW_CASE = "view_case"  # 查看案例
    START_CASE = "start_case"  # 开始案例
    SUBMIT_ANSWER = "submit_answer"  # 提交答案
    COMPLETE_CASE = "complete_case"  # 完成案例
    DOWNLOAD = "download"  # 下载资源
    UPLOAD = "upload"  # 上传文件
    SEARCH = "search"  # 搜索操作
    EXPORT_DATA = "export_data"  # 导出数据
    OTHER = "other"  # 其他


class OperationLog(Base):
    """操作日志数据表"""
    __tablename__ = "operation_logs"
    
    id = Column(Integer, primary_key=True, index=True, comment="日志ID")
    
    # 用户信息
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, comment="学生ID")
    
    # 案例信息
    case_id = Column(Integer, ForeignKey("cases.id"), comment="案例ID")
    
    # 操作信息
    log_type = Column(String(50), nullable=False, comment="操作类型")
    action = Column(String(200), comment="具体操作")
    description = Column(Text, comment="操作描述")
    
    # 操作结果
    success = Column(Boolean, default=True, comment="操作是否成功")
    error_message = Column(Text, comment="错误信息")
    
    # 操作详情
    operation_data = Column(JSON, comment="操作数据")
    request_data = Column(JSON, comment="请求数据")
    response_data = Column(JSON, comment="响应数据")
    
    # 时间信息
    duration = Column(Integer, comment="操作耗时(毫秒)")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, comment="操作时间")
    
    # 环境信息
    ip_address = Column(String(45), comment="IP地址")
    user_agent = Column(Text, comment="用户代理")
    device_info = Column(Text, comment="设备信息")
    
    # 会话信息
    session_id = Column(String(100), comment="会话ID")
    
    # 关联关系
    student = relationship("Student", back_populates="operation_logs")
    case = relationship("Case", back_populates="operation_logs")


class OperationLogCreate(BaseModel):
    """创建操作日志的数据模型"""
    student_id: int = Field(..., description="学生ID")
    case_id: Optional[int] = Field(None, description="案例ID")
    log_type: LogType = Field(..., description="操作类型")
    action: Optional[str] = Field(None, description="具体操作")
    description: Optional[str] = Field(None, description="操作描述")
    success: bool = Field(True, description="操作是否成功")
    error_message: Optional[str] = Field(None, description="错误信息")
    operation_data: Optional[Dict[str, Any]] = Field(None, description="操作数据")
    request_data: Optional[Dict[str, Any]] = Field(None, description="请求数据")
    response_data: Optional[Dict[str, Any]] = Field(None, description="响应数据")
    duration: Optional[int] = Field(None, description="操作耗时(毫秒)")
    ip_address: Optional[str] = Field(None, description="IP地址")
    user_agent: Optional[str] = Field(None, description="用户代理")
    device_info: Optional[str] = Field(None, description="设备信息")
    session_id: Optional[str] = Field(None, description="会话ID")


class OperationLogResponse(BaseModel):
    """操作日志响应数据模型"""
    id: int
    student_id: int
    case_id: Optional[int] = None
    log_type: str
    action: Optional[str] = None
    description: Optional[str] = None
    success: bool
    error_message: Optional[str] = None
    operation_data: Optional[Dict[str, Any]] = None
    request_data: Optional[Dict[str, Any]] = None
    response_data: Optional[Dict[str, Any]] = None
    duration: Optional[int] = None
    timestamp: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_info: Optional[str] = None
    session_id: Optional[str] = None
    
    class Config:
        from_attributes = True


class OperationLogListResponse(BaseModel):
    """操作日志列表响应数据模型"""
    logs: List[OperationLogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class OperationLogQuery(BaseModel):
    """操作日志查询参数"""
    student_id: Optional[int] = Field(None, description="学生ID")
    case_id: Optional[int] = Field(None, description="案例ID")
    log_type: Optional[LogType] = Field(None, description="操作类型")
    action: Optional[str] = Field(None, description="具体操作")
    success: Optional[bool] = Field(None, description="操作是否成功")
    ip_address: Optional[str] = Field(None, description="IP地址")
    session_id: Optional[str] = Field(None, description="会话ID")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    duration_min: Optional[int] = Field(None, description="最小耗时(毫秒)")
    duration_max: Optional[int] = Field(None, description="最大耗时(毫秒)")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")


class LogStatistics(BaseModel):
    """日志统计数据模型"""
    total_logs: int = Field(..., description="总日志数")
    successful_operations: int = Field(..., description="成功操作数")
    failed_operations: int = Field(..., description="失败操作数")
    success_rate: float = Field(..., description="成功率")
    average_duration: Optional[float] = Field(None, description="平均耗时(毫秒)")
    most_active_students: List[Dict[str, Any]] = Field(..., description="最活跃学生")
    most_popular_cases: List[Dict[str, Any]] = Field(..., description="最热门案例")
    operation_type_distribution: Dict[str, int] = Field(..., description="操作类型分布")
    hourly_distribution: Dict[int, int] = Field(..., description="小时分布")
    daily_distribution: Dict[str, int] = Field(..., description="日期分布")