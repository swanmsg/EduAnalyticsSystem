#!/usr/bin/env python3
"""
多智能体教育数据管理与分析系统演示脚本
"""

import asyncio
import json
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.ollama_config import OllamaManager
from agents.agent_manager import AgentManager
from agents.base_agent import AgentMessage
from datetime import datetime


async def demo_ollama_connection():
    """演示Ollama连接"""
    print("\n" + "="*50)
    print("🤖 Ollama模型连接演示")
    print("="*50)
    
    try:
        ollama_manager = OllamaManager()
        success = await ollama_manager.initialize()
        
        if success:
            print("✅ Ollama连接成功")
            
            # 测试对话
            llm = ollama_manager.get_llm()
            response = await llm.acomplete("你好，请简单介绍一下你的能力。")
            print(f"🗣️  模型响应: {response.text}")
            
            # 健康检查
            health = await ollama_manager.health_check()
            print(f"📊 健康状态: {json.dumps(health, ensure_ascii=False, indent=2)}")
            
        else:
            print("❌ Ollama连接失败")
            
    except Exception as e:
        print(f"❌ Ollama演示失败: {str(e)}")


async def demo_agents():
    """演示智能体系统"""
    print("\n" + "="*50)
    print("🧠 多智能体系统演示")
    print("="*50)
    
    try:
        # 初始化智能体管理器
        agent_manager = AgentManager()
        await agent_manager.initialize()
        
        print("✅ 智能体管理器初始化成功")
        
        # 显示智能体状态
        status = agent_manager.get_agent_status()
        print("📋 智能体状态:")
        for agent_id, agent_status in status.items():
            print(f"  - {agent_status['name']}: {'运行中' if agent_status['is_active'] else '停止'}")
            print(f"    能力: {', '.join(agent_status['capabilities'][:3])}...")
        
        # 演示数据分析任务
        print("\n🔬 执行数据分析任务...")
        analysis_request = {
            "type": "data_analysis",
            "analysis_type": "student_behavior",
            "student_ids": [1, 2, 3],
            "time_range": {"days": 30}
        }
        
        # 模拟分析任务（简化版）
        print("正在分析学生行为模式...")
        await asyncio.sleep(1)  # 模拟处理时间
        print("✅ 数据分析完成")
        
        # 演示报告生成
        print("\n📊 生成分析报告...")
        await asyncio.sleep(1)  # 模拟报告生成
        print("✅ 报告生成完成")
        
        # 显示系统指标
        metrics = agent_manager.get_system_metrics()
        print(f"\n📈 系统指标:")
        print(f"  - 总智能体数: {metrics['total_agents']}")
        print(f"  - 活跃智能体: {metrics['active_agents']}")
        print(f"  - 可用工作流: {', '.join(metrics['workflows_available'])}")
        
        # 关闭智能体
        await agent_manager.shutdown()
        print("🔄 智能体系统已关闭")
        
    except Exception as e:
        print(f"❌ 智能体演示失败: {str(e)}")


async def demo_data_analysis_workflow():
    """演示数据分析工作流程"""
    print("\n" + "="*50)
    print("📊 数据分析工作流程演示")
    print("="*50)
    
    # 模拟学生数据
    student_data = {
        "students": [
            {"id": 1, "name": "张三", "class": "计算机1班"},
            {"id": 2, "name": "李四", "class": "计算机1班"},
            {"id": 3, "name": "王五", "class": "计算机2班"}
        ],
        "scores": [
            {"student_id": 1, "subject": "数据结构", "score": 85, "attempts": 1},
            {"student_id": 2, "subject": "数据结构", "score": 78, "attempts": 2},
            {"student_id": 3, "subject": "数据结构", "score": 92, "attempts": 1}
        ],
        "logs": [
            {"student_id": 1, "action": "view_case", "timestamp": "2024-01-01T10:00:00"},
            {"student_id": 2, "action": "submit_answer", "timestamp": "2024-01-01T10:30:00"}
        ]
    }
    
    print("📋 模拟数据:")
    print(json.dumps(student_data, ensure_ascii=False, indent=2))
    
    print("\n🔍 执行分析步骤:")
    
    # 步骤1: 学生行为分析
    print("1. 学生行为分析...")
    behavior_analysis = {
        "total_operations": 15,
        "average_session_time": 45,  # 分钟
        "engagement_score": 0.78,
        "peak_hours": [9, 10, 14, 15]
    }
    print(f"   结果: 参与度 {behavior_analysis['engagement_score']:.1%}")
    
    # 步骤2: 成绩趋势分析
    print("2. 成绩趋势分析...")
    performance_analysis = {
        "average_score": 85.0,
        "pass_rate": 1.0,
        "improvement_trend": "positive"
    }
    print(f"   结果: 平均分 {performance_analysis['average_score']}, 通过率 {performance_analysis['pass_rate']:.1%}")
    
    # 步骤3: 知识点掌握分析
    print("3. 知识点掌握分析...")
    knowledge_analysis = {
        "data_structures": {"mastery": 0.85, "difficulty": "medium"},
        "algorithms": {"mastery": 0.78, "difficulty": "hard"},
        "programming": {"mastery": 0.92, "difficulty": "easy"}
    }
    print("   结果: 各知识点掌握情况分析完成")
    
    # 步骤4: 生成综合报告
    print("4. 生成综合分析报告...")
    report = {
        "title": "班级学习分析报告",
        "summary": "整体表现良好，建议加强算法相关知识点的练习",
        "recommendations": [
            "增加算法题目的练习时间",
            "组织小组讨论活动提高参与度",
            "针对薄弱知识点进行个性化辅导"
        ]
    }
    print("✅ 综合报告生成完成")
    print(f"   核心建议: {report['summary']}")


async def demo_ai_insights():
    """演示AI洞察能力"""
    print("\n" + "="*50)
    print("🧠 AI智能洞察演示")
    print("="*50)
    
    try:
        ollama_manager = OllamaManager()
        await ollama_manager.initialize()
        
        # 模拟分析数据
        analysis_data = {
            "student_count": 30,
            "average_score": 82.5,
            "completion_rate": 0.89,
            "common_errors": ["数组越界", "逻辑错误", "语法错误"],
            "time_distribution": {
                "morning": 0.35,
                "afternoon": 0.45, 
                "evening": 0.20
            }
        }
        
        prompt = f"""
        请基于以下教学数据分析结果，提供专业的教学洞察和建议：
        
        数据分析结果：
        - 学生人数：{analysis_data['student_count']}人
        - 平均成绩：{analysis_data['average_score']}分
        - 完成率：{analysis_data['completion_rate']:.1%}
        - 常见错误：{', '.join(analysis_data['common_errors'])}
        - 学习时间分布：上午{analysis_data['time_distribution']['morning']:.1%}，下午{analysis_data['time_distribution']['afternoon']:.1%}，晚上{analysis_data['time_distribution']['evening']:.1%}
        
        请从以下角度分析：
        1. 学习效果评估
        2. 存在的问题
        3. 改进建议
        4. 教学策略调整
        
        请用中文回答，控制在200字以内。
        """
        
        print("🤖 正在生成AI洞察...")
        llm = ollama_manager.get_llm()
        response = await llm.acomplete(prompt)
        
        print("💡 AI洞察结果:")
        print("-" * 40)
        print(response.text)
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ AI洞察演示失败: {str(e)}")


async def demo_system_integration():
    """演示系统集成能力"""
    print("\n" + "="*50)
    print("🔗 系统集成能力演示")
    print("="*50)
    
    # 模拟外部系统对接
    external_systems = {
        "学生管理系统": {
            "type": "database",
            "status": "connected",
            "data_types": ["student_info", "enrollment"]
        },
        "在线考试平台": {
            "type": "api",
            "status": "connected", 
            "data_types": ["exam_results", "question_bank"]
        },
        "教务管理系统": {
            "type": "file_export",
            "status": "available",
            "formats": ["excel", "csv", "pdf"]
        }
    }
    
    print("📡 外部系统连接状态:")
    for system_name, config in external_systems.items():
        status_icon = "✅" if config["status"] == "connected" else "⚠️"
        print(f"  {status_icon} {system_name} ({config['type']})")
        if "data_types" in config:
            print(f"     支持数据: {', '.join(config['data_types'])}")
    
    print("\n📊 数据导出格式支持:")
    formats = ["JSON", "XML", "CSV", "Excel", "PDF"]
    for fmt in formats:
        print(f"  ✅ {fmt}")
    
    print("\n🔄 数据同步能力:")
    sync_capabilities = [
        "实时数据同步",
        "定时批量同步", 
        "增量数据更新",
        "双向数据同步",
        "冲突检测与解决"
    ]
    for capability in sync_capabilities:
        print(f"  ✅ {capability}")


async def main():
    """主演示函数"""
    print("🎭 多智能体教育数据管理与分析系统")
    print("基于LlamaIndex框架和Ollama qwen3:4b模型")
    print("系统功能演示")
    print("="*60)
    
    try:
        # 1. Ollama连接演示
        await demo_ollama_connection()
        
        # 2. 智能体系统演示
        await demo_agents()
        
        # 3. 数据分析工作流程演示
        await demo_data_analysis_workflow()
        
        # 4. AI洞察能力演示
        await demo_ai_insights()
        
        # 5. 系统集成能力演示
        await demo_system_integration()
        
        print("\n" + "="*60)
        print("🎉 演示完成！")
        print("\n系统主要特性:")
        print("✅ 基于Ollama本地大模型，保证数据安全")
        print("✅ 多智能体协作，高效数据分析")
        print("✅ 支持多种数据格式导入导出")
        print("✅ AI驱动的智能洞察和建议")
        print("✅ 灵活的外部系统集成")
        print("✅ 实时分析和报告生成")
        
        print("\n启动完整系统请运行:")
        print("python run_system.py")
        
    except KeyboardInterrupt:
        print("\n演示被中断")
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {str(e)}")


if __name__ == "__main__":
    # 检查依赖
    try:
        import aiohttp
        import asyncio
    except ImportError as e:
        print(f"❌ 缺少必要依赖: {e}")
        print("请先安装依赖: pip install -r requirements.txt")
        sys.exit(1)
    
    asyncio.run(main())