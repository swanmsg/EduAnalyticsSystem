"""
学生数据模型
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from config.database import Base


class Student(Base):
    """学生数据表"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True, comment="学生ID")
    student_id = Column(String(50), unique=True, index=True, nullable=False, comment="学号")
    name = Column(String(100), nullable=False, comment="学生姓名")
    class_name = Column(String(100), comment="班级")
    grade = Column(String(50), comment="年级")
    major = Column(String(100), comment="专业")
    email = Column(String(255), comment="邮箱")
    phone = Column(String(20), comment="电话")
    gender = Column(String(10), comment="性别")
    
    # 状态信息
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 备注信息
    notes = Column(Text, comment="备注")
    
    # 关联关系
    operation_logs = relationship("OperationLog", back_populates="student")
    scores = relationship("Score", back_populates="student")


class StudentCreate(BaseModel):
    """创建学生的数据模型"""
    student_id: str = Field(..., description="学号")
    name: str = Field(..., description="学生姓名")
    class_name: Optional[str] = Field(None, description="班级")
    grade: Optional[str] = Field(None, description="年级")
    major: Optional[str] = Field(None, description="专业")
    email: Optional[str] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, description="电话")
    gender: Optional[str] = Field(None, description="性别")
    notes: Optional[str] = Field(None, description="备注")


class StudentUpdate(BaseModel):
    """更新学生的数据模型"""
    name: Optional[str] = Field(None, description="学生姓名")
    class_name: Optional[str] = Field(None, description="班级")
    grade: Optional[str] = Field(None, description="年级")
    major: Optional[str] = Field(None, description="专业")
    email: Optional[str] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, description="电话")
    gender: Optional[str] = Field(None, description="性别")
    is_active: Optional[bool] = Field(None, description="是否激活")
    notes: Optional[str] = Field(None, description="备注")


class StudentResponse(BaseModel):
    """学生响应数据模型"""
    id: int
    student_id: str
    name: str
    class_name: Optional[str] = None
    grade: Optional[str] = None
    major: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True


class StudentListResponse(BaseModel):
    """学生列表响应数据模型"""
    students: List[StudentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class StudentQuery(BaseModel):
    """学生查询参数"""
    student_id: Optional[str] = Field(None, description="学号")
    name: Optional[str] = Field(None, description="学生姓名")
    class_name: Optional[str] = Field(None, description="班级")
    grade: Optional[str] = Field(None, description="年级")
    major: Optional[str] = Field(None, description="专业")
    is_active: Optional[bool] = Field(None, description="是否激活")
    created_after: Optional[datetime] = Field(None, description="创建时间起始")
    created_before: Optional[datetime] = Field(None, description="创建时间结束")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")