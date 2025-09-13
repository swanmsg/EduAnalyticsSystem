"""
报告生成智能体
负责根据分析结果生成教学分析报告
"""
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
from jinja2 import Template
from config.database import get_async_db
from models import AnalysisResult, AnalysisType, ReportType
from agents.base_agent import BaseAgent, AgentMessage
import logging

logger = logging.getLogger(__name__)


class ReportGenerationAgent(BaseAgent):
    """报告生成智能体"""
    
    def __init__(self):
        super().__init__(
            agent_id="report_generation_agent",
            name="报告生成智能体", 
            description="负责生成各类教学分析报告"
        )
        self.capabilities = [
            "individual_report",
            "class_report", 
            "subject_report",
            "overall_report",
            "behavior_report",
            "performance_report",
            "trend_report",
            "comparison_report"
        ]
        
    async def handle_message(self, message: AgentMessage) -> Dict[str, Any]:
        """处理报告生成请求"""
        message_type = message.message_type
        content = message.content
        
        if message_type == "generate_individual_report":
            return await self._generate_individual_report(content)
        elif message_type == "generate_class_report":
            return await self._generate_class_report(content)
        elif message_type == "generate_subject_report":
            return await self._generate_subject_report(content)
        elif message_type == "generate_overall_report":
            return await self._generate_overall_report(content)
        elif message_type == "generate_custom_report":
            return await self._generate_custom_report(content)
        else:
            raise ValueError(f"不支持的消息类型: {message_type}")
            
    def get_capabilities(self) -> List[str]:
        """获取智能体能力列表"""
        return self.capabilities
        
    async def _generate_individual_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """生成个人分析报告"""
        student_id = params.get("student_id")
        analysis_data = params.get("analysis_data", {})
        time_range = params.get("time_range", {})
        
        try:
            # 获取学生基本信息
            student_info = await self._get_student_info(student_id)
            
            # 生成报告结构
            report_structure = {
                "report_type": "individual",
                "student_info": student_info,
                "time_range": time_range,
                "executive_summary": await self._generate_executive_summary(analysis_data, "individual"),
                "performance_overview": self._create_performance_overview(analysis_data),
                "learning_behavior": self._analyze_learning_behavior(analysis_data),
                "knowledge_mastery": self._analyze_knowledge_mastery_report(analysis_data),
                "improvement_recommendations": await self._generate_recommendations(analysis_data, "individual"),
                "detailed_metrics": self._extract_detailed_metrics(analysis_data),
                "charts": await self._generate_charts(analysis_data, "individual"),
                "generated_at": datetime.utcnow().isoformat()
            }
            
            # 生成最终报告内容
            report_content = await self._format_report(report_structure, "individual")
            
            return {
                "report_id": f"individual_{student_id}_{int(datetime.utcnow().timestamp())}",
                "report_type": "individual",
                "student_id": student_id,
                "content": report_content,
                "structure": report_structure,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"生成个人报告失败: {str(e)}")
            raise
            
    async def _generate_class_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """生成班级分析报告"""
        class_name = params.get("class_name")
        student_ids = params.get("student_ids", [])
        analysis_data = params.get("analysis_data", {})
        
        try:
            # 获取班级信息
            class_info = await self._get_class_info(class_name, student_ids)
            
            # 生成班级报告结构
            report_structure = {
                "report_type": "class",
                "class_info": class_info,
                "executive_summary": await self._generate_executive_summary(analysis_data, "class"),
                "class_performance": self._analyze_class_performance(analysis_data),
                "student_distribution": self._analyze_student_distribution(analysis_data),
                "learning_patterns": self._analyze_class_patterns(analysis_data),
                "knowledge_gaps": self._identify_knowledge_gaps(analysis_data),
                "teaching_recommendations": await self._generate_teaching_recommendations(analysis_data),
                "comparative_analysis": self._create_comparative_analysis(analysis_data),
                "charts": await self._generate_charts(analysis_data, "class"),
                "generated_at": datetime.utcnow().isoformat()
            }
            
            report_content = await self._format_report(report_structure, "class")
            
            return {
                "report_id": f"class_{class_name}_{int(datetime.utcnow().timestamp())}",
                "report_type": "class",
                "class_name": class_name,
                "content": report_content,
                "structure": report_structure,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"生成班级报告失败: {str(e)}")
            raise
            
    async def _generate_subject_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """生成学科分析报告"""
        subject = params.get("subject")
        analysis_data = params.get("analysis_data", {})
        
        try:
            report_structure = {
                "report_type": "subject",
                "subject_info": {"name": subject},
                "executive_summary": await self._generate_executive_summary(analysis_data, "subject"),
                "subject_performance": self._analyze_subject_performance(analysis_data),
                "difficulty_analysis": self._analyze_difficulty_distribution(analysis_data),
                "knowledge_point_analysis": self._analyze_knowledge_points_detailed(analysis_data),
                "teaching_effectiveness": self._evaluate_teaching_effectiveness(analysis_data),
                "curriculum_recommendations": await self._generate_curriculum_recommendations(analysis_data),
                "charts": await self._generate_charts(analysis_data, "subject"),
                "generated_at": datetime.utcnow().isoformat()
            }
            
            report_content = await self._format_report(report_structure, "subject")
            
            return {
                "report_id": f"subject_{subject}_{int(datetime.utcnow().timestamp())}",
                "report_type": "subject",
                "subject": subject,
                "content": report_content,
                "structure": report_structure,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"生成学科报告失败: {str(e)}")
            raise
            
    async def _generate_overall_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """生成整体分析报告"""
        analysis_data = params.get("analysis_data", {})
        scope = params.get("scope", "institution")
        
        try:
            report_structure = {
                "report_type": "overall",
                "scope_info": {"scope": scope},
                "executive_summary": await self._generate_executive_summary(analysis_data, "overall"),
                "overall_statistics": self._compile_overall_statistics(analysis_data),
                "trend_analysis": self._analyze_trends(analysis_data),
                "performance_benchmarks": self._establish_benchmarks(analysis_data),
                "system_insights": await self._generate_system_insights(analysis_data),
                "strategic_recommendations": await self._generate_strategic_recommendations(analysis_data),
                "charts": await self._generate_charts(analysis_data, "overall"),
                "generated_at": datetime.utcnow().isoformat()
            }
            
            report_content = await self._format_report(report_structure, "overall")
            
            return {
                "report_id": f"overall_{scope}_{int(datetime.utcnow().timestamp())}",
                "report_type": "overall",
                "scope": scope,
                "content": report_content,
                "structure": report_structure,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"生成整体报告失败: {str(e)}")
            raise
            
    async def _generate_charts(self, analysis_data: Dict[str, Any], report_type: str) -> Dict[str, Any]:
        """生成图表数据"""
        charts = {}
        
        try:
            # 成绩分布图
            if "scores" in analysis_data:
                charts["score_distribution"] = self._create_score_distribution_chart(analysis_data["scores"])
            
            # 学习趋势图  
            if "trends" in analysis_data:
                charts["learning_trends"] = self._create_trend_chart(analysis_data["trends"])
                
            # 知识点掌握雷达图
            if "knowledge_mastery" in analysis_data:
                charts["knowledge_radar"] = self._create_knowledge_radar_chart(analysis_data["knowledge_mastery"])
                
            # 行为模式图
            if "behavior_patterns" in analysis_data:
                charts["behavior_patterns"] = self._create_behavior_chart(analysis_data["behavior_patterns"])
                
            # 时间分布图
            if "time_analysis" in analysis_data:
                charts["time_distribution"] = self._create_time_distribution_chart(analysis_data["time_analysis"])
                
            return charts
            
        except Exception as e:
            logger.error(f"生成图表失败: {str(e)}")
            return {}
            
    def _create_score_distribution_chart(self, score_data: Dict) -> str:
        """创建成绩分布图"""
        try:
            fig = px.histogram(
                x=score_data.get("scores", []),
                title="成绩分布",
                labels={"x": "成绩", "y": "人数"}
            )
            return json.dumps(fig, cls=PlotlyJSONEncoder)
        except:
            return "{}"
            
    def _create_trend_chart(self, trend_data: Dict) -> str:
        """创建趋势图"""
        try:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=trend_data.get("dates", []),
                y=trend_data.get("scores", []),
                mode='lines+markers',
                name='成绩趋势'
            ))
            fig.update_layout(title="学习成绩趋势")
            return json.dumps(fig, cls=PlotlyJSONEncoder)
        except:
            return "{}"
            
    async def _generate_executive_summary(self, analysis_data: Dict, report_type: str) -> str:
        """生成执行摘要"""
        prompt = f"""
        基于以下数据分析结果，为{report_type}类型的教学分析报告生成一个执行摘要。
        
        分析数据：
        {json.dumps(analysis_data, ensure_ascii=False, indent=2)}
        
        请生成一个简洁明了的执行摘要，包含：
        1. 主要发现
        2. 关键指标 
        3. 重要趋势
        4. 核心建议
        
        字数控制在200-300字内。
        """
        
        try:
            response = await self.get_llm_response(prompt)
            return response
        except Exception as e:
            logger.error(f"生成执行摘要失败: {str(e)}")
            return "执行摘要生成失败"
            
    async def _format_report(self, report_structure: Dict, report_type: str) -> str:
        """格式化报告内容"""
        # 使用模板引擎格式化报告
        template_content = self._get_report_template(report_type)
        template = Template(template_content)
        
        try:
            formatted_report = template.render(**report_structure)
            return formatted_report
        except Exception as e:
            logger.error(f"格式化报告失败: {str(e)}")
            return json.dumps(report_structure, ensure_ascii=False, indent=2)
            
    def _get_report_template(self, report_type: str) -> str:
        """获取报告模板"""
        templates = {
            "individual": """
# 个人学习分析报告

## 学生信息
- 姓名: {{ student_info.name }}
- 学号: {{ student_info.student_id }}
- 班级: {{ student_info.class_name }}

## 执行摘要
{{ executive_summary }}

## 学习表现概览
{{ performance_overview }}

## 学习行为分析
{{ learning_behavior }}

## 知识点掌握情况
{{ knowledge_mastery }}

## 改进建议
{{ improvement_recommendations }}

---
报告生成时间: {{ generated_at }}
            """,
            "class": """
# 班级学习分析报告

## 班级信息
- 班级名称: {{ class_info.name }}
- 学生人数: {{ class_info.student_count }}

## 执行摘要
{{ executive_summary }}

## 班级整体表现
{{ class_performance }}

## 学生分布分析
{{ student_distribution }}

## 教学建议
{{ teaching_recommendations }}

---
报告生成时间: {{ generated_at }}
            """,
            "subject": """
# 学科分析报告

## 学科信息
- 学科名称: {{ subject_info.name }}

## 执行摘要
{{ executive_summary }}

## 学科表现分析
{{ subject_performance }}

## 课程建议
{{ curriculum_recommendations }}

---
报告生成时间: {{ generated_at }}
            """
        }
        
        return templates.get(report_type, "# 分析报告\n\n{{ executive_summary }}")
        
    # 其他辅助方法实现...
    async def _get_student_info(self, student_id: int) -> Dict:
        """获取学生信息"""
        return {"name": "学生姓名", "student_id": student_id, "class_name": "班级"}
        
    async def _get_class_info(self, class_name: str, student_ids: List[int]) -> Dict:
        """获取班级信息"""
        return {"name": class_name, "student_count": len(student_ids)}