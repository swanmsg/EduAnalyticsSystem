"""
系统配置模块
"""
import os
from typing import Optional
#from pydantic import BaseSettings, Field
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """系统配置"""
    
    # 基础配置
    DEBUG: bool = Field(default=True, env="DEBUG")
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # 数据库配置
    DATABASE_URL: str = Field(
        default="sqlite:///./edu_analytics.db",
        env="DATABASE_URL"
    )
    
    # Ollama配置
    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434",
        env="OLLAMA_BASE_URL"
    )
    OLLAMA_MODEL: str = Field(
        default="qwen3:4b",
        env="OLLAMA_MODEL"
    )
    OLLAMA_TIMEOUT: float = Field(
        default=120.0,
        env="OLLAMA_TIMEOUT"
    )
    
    # 数据导出配置
    EXPORT_DIR: str = Field(
        default="./exports",
        env="EXPORT_DIR"
    )
    MAX_EXPORT_ROWS: int = Field(
        default=100000,
        env="MAX_EXPORT_ROWS"
    )
    
    # 报告生成配置
    REPORT_TIMEOUT: int = Field(
        default=1800,  # 30分钟
        env="REPORT_TIMEOUT"
    )
    
    # 安全配置
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    
    # 日志配置
    LOG_LEVEL: str = Field(
        default="INFO",
        env="LOG_LEVEL"
    )
    
    # 文件上传配置
    MAX_FILE_SIZE: int = Field(
        default=50 * 1024 * 1024,  # 50MB
        env="MAX_FILE_SIZE"
    )
    ALLOWED_FILE_TYPES: list = Field(
        default=["xlsx", "xls", "csv", "json"],
        env="ALLOWED_FILE_TYPES"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()