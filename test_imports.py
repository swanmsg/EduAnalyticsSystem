#!/usr/bin/env python3
"""
简化测试启动脚本 - 用于验证导入问题修复
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试所有关键模块的导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试配置模块
        print("1. 测试配置模块...")
        from config.settings import settings
        from config.database import init_db
        from config.ollama_config import OllamaManager
        print("   ✅ 配置模块导入成功")
        
        # 测试数据模型
        print("2. 测试数据模型...")
        from models import Student, Case, Score, OperationLog, AnalysisResult
        print("   ✅ 数据模型导入成功")
        
        # 测试智能体模块
        print("3. 测试智能体模块...")
        from agents.agent_manager import AgentManager
        from agents.data_analysis_agent import DataAnalysisAgent
        from agents.report_generation_agent import ReportGenerationAgent
        from agents.interface_management_agent import InterfaceManagementAgent
        print("   ✅ 智能体模块导入成功")
        
        # 测试API模块
        print("4. 测试API模块...")
        from api import router
        from api.routes import students_router, analysis_router
        print("   ✅ API模块导入成功")
        
        # 测试数据管理模块
        print("5. 测试数据管理模块...")
        from data_management.student_service import StudentService
        print("   ✅ 数据管理模块导入成功")
        
        print("\n🎉 所有模块导入测试通过！")
        return True
        
    except ImportError as e:
        print(f"\n❌ 导入错误: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ 其他错误: {str(e)}")
        return False

def test_basic_functionality():
    """测试基础功能"""
    print("\n🧪 测试基础功能...")
    
    try:
        # 测试FastAPI应用创建
        print("1. 测试FastAPI应用创建...")
        from fastapi import FastAPI
        from api import router
        
        app = FastAPI(title="测试应用")
        app.include_router(router, prefix="/api/v1")
        print("   ✅ FastAPI应用创建成功")
        
        # 测试智能体管理器创建
        print("2. 测试智能体管理器创建...")
        from agents.agent_manager import AgentManager
        
        agent_manager = AgentManager()
        print(f"   ✅ 智能体管理器创建成功，包含智能体: {list(agent_manager.agents.keys())}")
        
        print("\n🎉 基础功能测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 功能测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("🛠️  模块导入测试工具")
    print("=" * 50)
    
    # 测试导入
    if not test_imports():
        print("\n❌ 导入测试失败，请检查代码")
        sys.exit(1)
    
    # 测试基础功能
    if not test_basic_functionality():
        print("\n❌ 功能测试失败，请检查代码")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！系统模块结构正常")
    print("现在可以运行: python run_system.py")
    print("=" * 50)

if __name__ == "__main__":
    main()