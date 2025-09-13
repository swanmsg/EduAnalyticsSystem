# 多智能体教育数据管理与分析系统

基于LlamaIndex框架和本地Ollama qwen3:4b模型的教育数据分析系统。

## 功能特性

### 1. 数据存储与管理功能
- 支持教学案例数据、学生操作日志、考核成绩、AI分析结果等数据的分类存储
- 提供数据查询、导出、备份功能
- 支持多种条件组合查询（学生姓名、案例名称、时间范围、考核题型等）
- 支持Excel、CSV等格式的数据导出

### 2. 数据分析功能
- 基于机器学习算法的深度数据挖掘和分析
- 生成多维度教学分析报告
- 学生学习行为分析（含选择题答题习惯分析）
- 教学效果评估（分析各选择题知识点掌握情况）
- 标准数据接口，支持与外部系统对接

### 3. 多智能体架构
- 数据分析智能体：负责数据处理和分析
- 报告生成智能体：负责生成教学分析报告
- 接口管理智能体：负责外部系统对接

## 技术栈

- **AI框架**: LlamaIndex
- **语言模型**: Ollama qwen3:4b (本地部署)
- **后端框架**: FastAPI
- **数据库**: SQLAlchemy + SQLite/PostgreSQL
- **数据分析**: Pandas, NumPy, Scikit-learn
- **可视化**: Plotly
- **前端**: HTML/CSS/JavaScript (管理界面)

## 快速开始

### 环境要求
- Python 3.9+
- Poetry
- Ollama (需要安装qwen3:4b模型)

### 安装步骤

1. 克隆项目并安装依赖
```bash
cd edu_analytics_system
poetry install
```

2. 启动Ollama服务
```bash
ollama serve
ollama pull qwen3:4b
```

3. 初始化数据库
```bash
poetry run alembic upgrade head
```

4. 启动系统
```bash
poetry run python main.py
```

## 项目结构

```
edu_analytics_system/
├── agents/              # 多智能体模块
├── api/                 # API接口
├── data_management/     # 数据管理模块
├── data_analysis/       # 数据分析模块
├── models/              # 数据模型
├── web/                 # Web界面
├── config/              # 配置文件
├── tests/               # 测试文件
└── main.py              # 主程序入口
```

## 性能指标

- 报告生成时间：最大不超过30分钟（根据数据量）
- 支持常见数据格式和协议
- 支持并发访问和处理

## 许可证

MIT License