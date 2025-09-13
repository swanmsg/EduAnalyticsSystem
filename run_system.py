#!/usr/bin/env python3
"""
系统启动和测试脚本
"""

import asyncio
import uvicorn
import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from config.database import init_db
from config.ollama_config import OllamaManager
from agents.agent_manager import AgentManager

async def check_ollama_service():
    """检查Ollama服务是否可用"""
    print("🔍 检查Ollama服务...")
    
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.OLLAMA_BASE_URL}/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    models = [model['name'] for model in data.get('models', [])]
                    print(f"✅ Ollama服务运行正常，可用模型: {models}")
                    
                    if settings.OLLAMA_MODEL in models:
                        print(f"✅ 目标模型 {settings.OLLAMA_MODEL} 已安装")
                        return True
                    else:
                        print(f"⚠️  目标模型 {settings.OLLAMA_MODEL} 未安装")
                        print(f"请运行: ollama pull {settings.OLLAMA_MODEL}")
                        return False
                else:
                    print(f"❌ Ollama服务响应异常: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ 无法连接到Ollama服务: {str(e)}")
        print("请确保Ollama服务正在运行:")
        print("1. 安装Ollama: https://ollama.com/")
        print("2. 启动服务: ollama serve")
        print(f"3. 拉取模型: ollama pull {settings.OLLAMA_MODEL}")
        return False


async def initialize_system():
    """初始化系统"""
    print("🚀 正在初始化多智能体教育数据管理与分析系统...")
    
    # 检查Ollama服务
    if not await check_ollama_service():
        print("❌ Ollama服务检查失败，无法继续启动")
        return False
    
    try:
        # 初始化数据库
        print("📊 初始化数据库...")
        await init_db()
        print("✅ 数据库初始化完成")
        
        # 初始化Ollama连接
        print("🤖 初始化Ollama连接...")
        ollama_manager = OllamaManager()
        if await ollama_manager.initialize():
            print("✅ Ollama连接初始化成功")
        else:
            print("❌ Ollama连接初始化失败")
            return False
        
        # 初始化智能体管理器
        print("🧠 初始化智能体管理器...")
        agent_manager = AgentManager()
        await agent_manager.initialize()
        print("✅ 智能体管理器初始化成功")
        
        # 设置全局智能体管理器
        from api.routes.analysis import set_agent_manager
        set_agent_manager(agent_manager)
        
        print("✅ 系统初始化完成！")
        return True
        
    except Exception as e:
        print(f"❌ 系统初始化失败: {str(e)}")
        return False


def create_app():
    """创建FastAPI应用"""
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from api import router
    
    app = FastAPI(
        title="多智能体教育数据管理与分析系统",
        description="基于LlamaIndex和Ollama的教育数据分析平台",
        version="0.1.0"
    )
    
    # 添加CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册API路由
    app.include_router(router, prefix="/api/v1")
    
    @app.get("/")
    async def root():
        return {
            "message": "多智能体教育数据管理与分析系统",
            "version": "0.1.0",
            "status": "running",
            "docs": "/docs",
            "api": "/api/v1"
        }
    
    @app.get("/health")
    async def health_check():
        """健康检查"""
        try:
            # 检查Ollama连接
            ollama_manager = OllamaManager()
            ollama_health = await ollama_manager.health_check()
            
            return {
                "status": "healthy",
                "timestamp": asyncio.get_event_loop().time(),
                "services": {
                    "ollama": ollama_health,
                    "database": {"status": "healthy"},
                    "agents": {"status": "healthy"}
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    return app


async def test_system():
    """测试系统功能"""
    print("\n🧪 开始系统功能测试...")
    
    try:
        # 测试Ollama连接
        print("1. 测试Ollama连接...")
        ollama_manager = OllamaManager()
        health = await ollama_manager.health_check()
        print(f"   Ollama状态: {health}")
        
        # 测试智能体
        print("2. 测试智能体系统...")
        agent_manager = AgentManager()
        if agent_manager.is_initialized:
            status = agent_manager.get_system_metrics()
            print(f"   智能体状态: {status}")
        
        print("✅ 系统功能测试通过")
        
    except Exception as e:
        print(f"❌ 系统功能测试失败: {str(e)}")


async def main():
    """主函数"""
    print("=" * 60)
    print("多智能体教育数据管理与分析系统")
    print("基于LlamaIndex框架和Ollama qwen3:4b模型")
    print("=" * 60)
    
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 初始化系统
    if not await initialize_system():
        print("系统初始化失败，退出...")
        return
    
    # 测试系统
    await test_system()
    
    # 创建应用
    app = create_app()
    
    print(f"\n🌐 启动Web服务...")
    print(f"服务地址: http://{settings.HOST}:{settings.PORT}")
    print(f"API文档: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"健康检查: http://{settings.HOST}:{settings.PORT}/health")
    print("\n按 Ctrl+C 停止服务")
    
    # 启动服务器
    config = uvicorn.Config(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info"
    )
    
    server = uvicorn.Server(config)
    try:
        await server.serve()
    except KeyboardInterrupt:
        print("\n🔄 正在关闭系统...")
        print("✅ 系统已安全关闭")


if __name__ == "__main__":
    # 检查Python版本
    if sys.version_info < (3, 9):
        print("❌ 需要Python 3.9或更高版本")
        sys.exit(1)
    
    # 检查依赖包
    required_packages = [
        "fastapi", "uvicorn", "sqlalchemy", "pandas", 
        "numpy", "plotly", "aiohttp", "pydantic"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        sys.exit(1)
    
    # 运行主程序
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 再见！")
    except Exception as e:
        print(f"❌ 系统运行失败: {str(e)}")
        sys.exit(1)