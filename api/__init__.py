"""
API路由主文件
"""
from fastapi import APIRouter
from .routes import (
    students_router, cases, scores, logs,
    analysis_router, reports, system, data_management
)

router = APIRouter()

# 注册各模块路由
router.include_router(
    students_router, 
    prefix="/students", 
    tags=["学生管理"]
)

router.include_router(
    cases, 
    prefix="/cases", 
    tags=["案例管理"]
)

router.include_router(
    scores, 
    prefix="/scores", 
    tags=["成绩管理"]
)

router.include_router(
    logs, 
    prefix="/logs", 
    tags=["日志管理"]
)

router.include_router(
    analysis_router, 
    prefix="/analysis", 
    tags=["数据分析"]
)

router.include_router(
    reports, 
    prefix="/reports", 
    tags=["报告生成"]
)

router.include_router(
    data_management, 
    prefix="/data", 
    tags=["数据管理"]
)

router.include_router(
    system, 
    prefix="/system", 
    tags=["系统管理"]
)

@router.get("/", summary="API根路径")
async def root():
    """API根路径"""
    return {
        "message": "多智能体教育数据管理与分析系统 API",
        "version": "0.1.0",
        "documentation": "/docs"
    }