"""
数据分析智能体
负责学生数据的深度分析和挖掘
"""
import asyncio
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.database import get_async_db
from models import (
    Student, Score, OperationLog, Case,
    AnalysisResult, AnalysisType, AnalysisStatus
)
from agents.base_agent import BaseAgent, AgentMessage
import logging

logger = logging.getLogger(__name__)


class DataAnalysisAgent(BaseAgent):
    """数据分析智能体"""
    
    def __init__(self):
        super().__init__(
            agent_id="data_analysis_agent",
            name="数据分析智能体",
            description="负责学生学习数据的深度分析和挖掘"
        )
        self.capabilities = [
            "student_behavior_analysis",
            "learning_pattern_analysis", 
            "knowledge_mastery_analysis",
            "performance_trend_analysis",
            "choice_pattern_analysis",
            "time_analysis",
            "difficulty_analysis"
        ]
        
    async def handle_message(self, message: AgentMessage) -> Dict[str, Any]:
        """处理分析请求"""
        message_type = message.message_type
        content = message.content
        
        if message_type == "analyze_student_behavior":
            return await self._analyze_student_behavior(content)
        elif message_type == "analyze_learning_pattern":
            return await self._analyze_learning_pattern(content)
        elif message_type == "analyze_knowledge_mastery":
            return await self._analyze_knowledge_mastery(content)
        elif message_type == "analyze_performance_trend":
            return await self._analyze_performance_trend(content)
        elif message_type == "analyze_choice_pattern":
            return await self._analyze_choice_pattern(content)
        elif message_type == "comprehensive_analysis":
            return await self._comprehensive_analysis(content)
        else:
            raise ValueError(f"不支持的消息类型: {message_type}")
            
    def get_capabilities(self) -> List[str]:
        """获取智能体能力列表"""
        return self.capabilities
        
    async def _analyze_student_behavior(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """分析学生行为模式"""
        student_ids = params.get("student_ids", [])
        time_range = params.get("time_range", {})
        
        try:
            async with get_async_db() as db:
                # 获取学生操作日志
                logs_data = await self._get_operation_logs(db, student_ids, time_range)
                
                if not logs_data:
                    return {"error": "没有找到相关的操作日志数据"}
                
                # 转换为DataFrame进行分析
                df = pd.DataFrame(logs_data)
                
                # 分析结果
                behavior_analysis = {
                    "total_operations": len(df),
                    "unique_students": df['student_id'].nunique(),
                    "operation_distribution": df['log_type'].value_counts().to_dict(),
                    "average_session_duration": self._calculate_session_duration(df),
                    "peak_activity_hours": self._find_peak_hours(df),
                    "learning_patterns": await self._identify_learning_patterns(df),
                    "engagement_score": self._calculate_engagement_score(df)
                }
                
                # 使用LLM生成分析洞察
                insights = await self._generate_behavior_insights(behavior_analysis)
                
                return {
                    "analysis_type": "student_behavior",
                    "data": behavior_analysis,
                    "insights": insights,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"学生行为分析失败: {str(e)}")
            raise
            
    async def _analyze_learning_pattern(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """分析学习模式"""
        student_ids = params.get("student_ids", [])
        
        try:
            async with get_async_db() as db:
                # 获取成绩数据
                scores_data = await self._get_scores_data(db, student_ids)
                
                if not scores_data:
                    return {"error": "没有找到相关的成绩数据"}
                
                df = pd.DataFrame(scores_data)
                
                pattern_analysis = {
                    "learning_velocity": self._calculate_learning_velocity(df),
                    "improvement_trend": self._analyze_improvement_trend(df),
                    "attempt_patterns": self._analyze_attempt_patterns(df),
                    "time_management": self._analyze_time_management(df),
                    "difficulty_preference": self._analyze_difficulty_preference(df),
                    "consistency_score": self._calculate_consistency_score(df)
                }
                
                # 生成学习模式洞察
                insights = await self._generate_pattern_insights(pattern_analysis)
                
                return {
                    "analysis_type": "learning_pattern",
                    "data": pattern_analysis,
                    "insights": insights,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"学习模式分析失败: {str(e)}")
            raise
            
    async def _analyze_knowledge_mastery(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """分析知识点掌握情况"""
        student_ids = params.get("student_ids", [])
        subject = params.get("subject")
        
        try:
            async with get_async_db() as db:
                # 获取详细的答题数据
                detailed_data = await self._get_detailed_answer_data(db, student_ids, subject)
                
                if not detailed_data:
                    return {"error": "没有找到相关的答题数据"}
                
                mastery_analysis = {
                    "knowledge_points": self._analyze_knowledge_points(detailed_data),
                    "mastery_distribution": self._calculate_mastery_distribution(detailed_data),
                    "weak_areas": self._identify_weak_areas(detailed_data),
                    "strong_areas": self._identify_strong_areas(detailed_data),
                    "improvement_suggestions": await self._generate_improvement_suggestions(detailed_data)
                }
                
                return {
                    "analysis_type": "knowledge_mastery",
                    "data": mastery_analysis,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"知识点掌握分析失败: {str(e)}")
            raise
            
    async def _analyze_choice_pattern(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """分析选择题答题模式"""
        student_ids = params.get("student_ids", [])
        
        try:
            async with get_async_db() as db:
                # 获取选择题答题数据
                choice_data = await self._get_choice_question_data(db, student_ids)
                
                if not choice_data:
                    return {"error": "没有找到相关的选择题数据"}
                
                df = pd.DataFrame(choice_data)
                
                choice_analysis = {
                    "answer_distribution": self._analyze_answer_distribution(df),
                    "guessing_patterns": self._detect_guessing_patterns(df),
                    "option_preference": self._analyze_option_preference(df),
                    "response_time_patterns": self._analyze_response_time(df),
                    "confidence_indicators": self._calculate_confidence_indicators(df)
                }
                
                # 生成选择题分析洞察
                insights = await self._generate_choice_insights(choice_analysis)
                
                return {
                    "analysis_type": "choice_pattern",
                    "data": choice_analysis,
                    "insights": insights,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"选择题模式分析失败: {str(e)}")
            raise
            
    async def _comprehensive_analysis(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """综合分析"""
        try:
            # 运行所有分析
            behavior_result = await self._analyze_student_behavior(params)
            pattern_result = await self._analyze_learning_pattern(params)
            mastery_result = await self._analyze_knowledge_mastery(params)
            choice_result = await self._analyze_choice_pattern(params)
            
            # 综合分析结果
            comprehensive_result = {
                "behavior_analysis": behavior_result.get("data", {}),
                "learning_patterns": pattern_result.get("data", {}),
                "knowledge_mastery": mastery_result.get("data", {}),
                "choice_patterns": choice_result.get("data", {}),
                "overall_insights": await self._generate_comprehensive_insights({
                    "behavior": behavior_result,
                    "patterns": pattern_result,
                    "mastery": mastery_result,
                    "choices": choice_result
                })
            }
            
            return {
                "analysis_type": "comprehensive",
                "data": comprehensive_result,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"综合分析失败: {str(e)}")
            raise
            
    # 辅助方法
    async def _get_operation_logs(self, db: Session, student_ids: List[int], time_range: Dict) -> List[Dict]:
        """获取操作日志数据"""
        # 这里应该实现数据库查询逻辑
        # 返回格式化的日志数据
        pass
        
    async def _get_scores_data(self, db: Session, student_ids: List[int]) -> List[Dict]:
        """获取成绩数据"""
        # 实现成绩数据查询
        pass
        
    def _calculate_session_duration(self, df: pd.DataFrame) -> float:
        """计算平均会话时长"""
        # 实现会话时长计算逻辑
        return 0.0
        
    def _find_peak_hours(self, df: pd.DataFrame) -> List[int]:
        """找出活跃高峰时间"""
        # 实现高峰时间分析
        return []
        
    async def _identify_learning_patterns(self, df: pd.DataFrame) -> List[Dict]:
        """识别学习模式"""
        # 使用机器学习算法识别学习模式
        return []
        
    def _calculate_engagement_score(self, df: pd.DataFrame) -> float:
        """计算参与度分数"""
        # 实现参与度计算
        return 0.0
        
    async def _generate_behavior_insights(self, analysis_data: Dict) -> List[Dict]:
        """生成行为分析洞察"""
        prompt = f"""
        基于以下学生行为数据分析结果，请生成关键洞察和建议：
        
        数据分析结果：
        {json.dumps(analysis_data, ensure_ascii=False, indent=2)}
        
        请从以下角度分析：
        1. 学生参与度评估
        2. 学习行为模式识别
        3. 潜在问题识别
        4. 改进建议
        
        请以JSON格式返回，包含insights数组，每个insight包含type, description, evidence, recommendation字段。
        """
        
        response = await self.get_llm_response(prompt)
        try:
            return json.loads(response).get("insights", [])
        except:
            return [{"type": "analysis", "description": response}]
            
    async def _generate_pattern_insights(self, pattern_data: Dict) -> List[Dict]:
        """生成学习模式洞察"""
        # 类似的LLM调用逻辑
        return []
        
    async def _generate_choice_insights(self, choice_data: Dict) -> List[Dict]:
        """生成选择题分析洞察"""
        # 类似的LLM调用逻辑
        return []
        
    async def _generate_comprehensive_insights(self, all_data: Dict) -> List[Dict]:
        """生成综合分析洞察"""
        # 综合所有分析结果生成洞察
        return []