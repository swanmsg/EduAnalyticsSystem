#!/usr/bin/env python3
"""
多智能体教育数据管理与分析系统
主程序入口
"""

import asyncio
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.settings import Settings
from config.database import init_db
from config.ollama_config import OllamaManager
from api import router
from agents.agent_manager import AgentManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    print("🚀 启动多智能体教育数据管理与分析系统...")
    
    # 初始化数据库
    await init_db()
    
    # 初始化Ollama连接
    ollama_manager = OllamaManager()
    await ollama_manager.initialize()
    
    # 初始化智能体管理器
    agent_manager = AgentManager()
    await agent_manager.initialize()
    
    print("✅ 系统初始化完成")
    
    yield
    
    # 关闭时执行
    print("🔄 正在关闭系统...")
    await agent_manager.shutdown()
    print("✅ 系统已安全关闭")


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    app = FastAPI(
        title="教育数据管理与分析系统",
        description="基于LlamaIndex和Ollama的多智能体教育数据分析平台",
        version="0.1.0",
        lifespan=lifespan
    )
    
    # 注册路由
    app.include_router(router, prefix="/api/v1")
    
    return app


async def main():
    """主函数"""
    settings = Settings()
    app = create_app()
    
    # 启动服务器
    config = uvicorn.Config(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info",
        reload=settings.DEBUG
    )
    
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())