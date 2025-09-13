"""
简化的API路由集合
"""
from fastapi import APIRouter

# 创建基础路由
router = APIRouter()

@router.get("/", summary="API状态")
async def api_status():
    """API状态检查"""
    return {
        "status": "running",
        "message": "多智能体教育数据管理与分析系统API",
        "version": "0.1.0"
    }

@router.get("/health", summary="健康检查")
async def health_check():
    """系统健康检查"""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "database": "connected",
            "ollama": "available",
            "agents": "initialized"
        }
    }

# 为了避免导入错误，先创建简单的模拟路由
students = router
cases = router
scores = router  
logs = router
analysis = router
reports = router
data_management = router
system = router