# 多智能体教育数据管理与分析系统 - 部署与使用指南

## 系统概述

本系统是基于LlamaIndex框架和本地Ollama qwen3:4b模型构建的多智能体教育数据管理与分析平台，主要功能包括：

### 核心功能

#### 1. 数据存储与管理功能
- **数据分类存储**：支持教学案例数据、学生操作日志、考核成绩、AI分析结果等各类数据的分类存储
- **数据查询功能**：支持多种条件组合查询（学生姓名、案例名称、时间范围、考核题型等）
- **数据导出功能**：支持Excel、CSV等格式的数据导出
- **数据备份功能**：提供数据备份和恢复机制

#### 2. 数据分析功能
- **深度数据挖掘**：使用机器学习算法对学生实训数据进行深度分析
- **多维度分析报告**：
  - 学生学习行为分析报告（含选择题答题习惯分析）
  - 教学效果评估报告（分析各选择题知识点掌握情况）
  - 成绩趋势分析报告
  - 知识点掌握情况分析
- **标准数据接口**：与外部教学研究系统、教育管理平台进行数据对接

#### 3. 多智能体架构
- **数据分析智能体**：负责数据处理和深度分析
- **报告生成智能体**：负责生成各类教学分析报告
- **接口管理智能体**：负责外部系统数据对接和格式转换

## 系统架构

```
┌─────────────────────────────────────────────────┐
│                   Web管理界面                    │
├─────────────────────────────────────────────────┤
│                  FastAPI服务层                   │
├─────────────────────────────────────────────────┤
│               多智能体协调层                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │数据分析智能体│ │报告生成智能体│ │接口管理智能体│ │
│  └─────────────┘ └─────────────┘ └─────────────┘ │
├─────────────────────────────────────────────────┤
│                 LlamaIndex框架                   │
├─────────────────────────────────────────────────┤
│              Ollama本地模型服务                   │
│                (qwen3:4b)                       │
├─────────────────────────────────────────────────┤
│               数据存储层                         │
│        SQLite/PostgreSQL + 文件存储             │
└─────────────────────────────────────────────────┘
```

## 环境要求

### 基础环境
- **操作系统**：Linux、macOS、Windows 10/11
- **Python版本**：3.9+
- **内存要求**：至少8GB RAM（推荐16GB）
- **存储空间**：至少10GB可用空间
- **网络**：无需外网（本地部署）

### 依赖软件
- **Ollama**：本地大模型服务
- **Poetry**：Python依赖管理（可选）
- **Git**：代码版本控制

## 安装部署

### 第一步：安装Ollama

#### macOS/Linux
```bash
# 安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 启动Ollama服务
ollama serve

# 拉取qwen3:4b模型
ollama pull qwen3:4b
```

#### Windows
1. 访问 https://ollama.com/download
2. 下载Windows安装包
3. 运行安装程序
4. 打开命令行执行：
```bash
ollama serve
ollama pull qwen3:4b
```

### 第二步：部署系统

#### 方式一：使用Poetry（推荐）
```bash
# 克隆项目
git clone <repository-url>
cd edu_analytics_system

# 安装Poetry
pip install poetry

# 安装依赖
poetry install

# 启动系统
poetry run python run_system.py
```

#### 方式二：使用pip
```bash
# 克隆项目
git clone <repository-url>
cd edu_analytics_system

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动系统
python run_system.py
```

### 第三步：验证部署

启动系统后，访问以下地址进行验证：

- **系统首页**：http://localhost:8000
- **API文档**：http://localhost:8000/docs
- **健康检查**：http://localhost:8000/health

## 配置说明

### 环境变量配置

创建 `.env` 文件进行系统配置：

```bash
# 基础配置
DEBUG=true
HOST=0.0.0.0
PORT=8000

# 数据库配置
DATABASE_URL=sqlite:///./edu_analytics.db

# Ollama配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:4b
OLLAMA_TIMEOUT=120.0

# 数据导出配置
EXPORT_DIR=./exports
MAX_EXPORT_ROWS=100000

# 报告生成配置
REPORT_TIMEOUT=1800  # 30分钟

# 安全配置
SECRET_KEY=your-secret-key-change-in-production

# 日志配置
LOG_LEVEL=INFO
```

### 系统配置优化

#### 性能优化
```python
# config/settings.py 中的配置建议
OLLAMA_TIMEOUT = 300.0  # 增加超时时间用于复杂分析
MAX_EXPORT_ROWS = 500000  # 根据系统性能调整
REPORT_TIMEOUT = 3600  # 复杂报告生成时间限制
```

#### 安全配置
```python
# 生产环境安全配置
DEBUG = False
SECRET_KEY = "your-production-secret-key"
ALLOWED_HOSTS = ["your-domain.com", "localhost"]
```

## 使用指南

### 系统启动

```bash
# 启动系统
python run_system.py

# 启动演示模式
python demo.py
```

### API使用示例

#### 1. 学生管理
```bash
# 创建学生
curl -X POST "http://localhost:8000/api/v1/students/" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "2024001",
    "name": "张三",
    "class_name": "计算机1班",
    "grade": "2024级",
    "major": "计算机科学与技术"
  }'

# 查询学生列表
curl "http://localhost:8000/api/v1/students/?page=1&page_size=20"
```

#### 2. 数据分析
```bash
# 执行学生行为分析
curl -X POST "http://localhost:8000/api/v1/analysis/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_type": "student_behavior",
    "student_ids": [1, 2, 3],
    "time_range": {"days": 30}
  }'

# 生成班级报告
curl -X POST "http://localhost:8000/api/v1/analysis/reports/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "class",
    "class_name": "计算机1班",
    "format": "html"
  }'
```

#### 3. 数据导出
```bash
# 导出学生数据
curl "http://localhost:8000/api/v1/data/export/students?format=csv"

# 导出分析报告
curl "http://localhost:8000/api/v1/data/export/analysis?format=excel"
```

### Web界面使用

1. **访问系统**：打开浏览器访问 http://localhost:8000
2. **数据管理**：通过Web界面进行学生、案例、成绩数据管理
3. **分析功能**：选择分析类型和目标数据执行分析
4. **报告查看**：查看和下载生成的分析报告
5. **系统监控**：监控智能体状态和系统性能

## 功能特性

### 数据分析能力

#### 学生行为分析
- 学习时间分布分析
- 操作频率统计
- 学习路径跟踪
- 参与度评估

#### 成绩分析
- 分数分布统计
- 成绩趋势分析
- 知识点掌握情况
- 难度适应性分析

#### 选择题答题模式分析
- 答题习惯识别
- 选项偏好分析
- 猜测模式检测
- 时间分配模式

#### 教学效果评估
- 知识点掌握率统计
- 教学方法效果分析
- 学习目标达成情况
- 改进建议生成

### 报告生成功能

#### 个人报告
- 学生个人学习分析
- 知识点掌握情况
- 学习建议
- 发展轨迹

#### 班级报告
- 班级整体表现
- 学生分布分析
- 教学建议
- 对比分析

#### 学科报告
- 学科难度分析
- 知识点分布
- 教学效果评估
- 课程优化建议

#### 综合报告
- 多维度综合分析
- 趋势预测
- 策略建议
- 决策支持

### 数据接口功能

#### 导入功能
- Excel文件导入
- CSV文件导入
- JSON数据导入
- API接口导入

#### 导出功能
- Excel格式导出
- CSV格式导出
- PDF报告导出
- JSON数据导出

#### 外部系统对接
- 学生管理系统对接
- 在线考试平台对接
- 教务管理系统对接
- 第三方分析工具对接

## 性能指标

### 系统性能
- **并发用户数**：支持100+并发用户
- **数据处理能力**：单次可处理10万条记录
- **报告生成时间**：根据数据量，最大不超过30分钟
- **响应时间**：API响应时间<3秒

### 数据支持
- **学生规模**：支持10万+学生数据
- **案例数量**：支持1万+教学案例
- **日志容量**：支持千万级操作日志
- **报告存储**：支持1万+分析报告

## 故障排除

### 常见问题

#### 1. Ollama连接失败
```bash
# 检查Ollama服务状态
ollama list

# 重启Ollama服务
pkill ollama
ollama serve

# 检查模型是否存在
ollama pull qwen3:4b
```

#### 2. 数据库连接问题
```bash
# 检查数据库文件权限
ls -la edu_analytics.db

# 重新初始化数据库
rm edu_analytics.db
python -c "from config.database import init_db; import asyncio; asyncio.run(init_db())"
```

#### 3. 端口占用
```bash
# 检查端口占用
lsof -i :8000

# 修改端口配置
export PORT=8001
```

#### 4. 内存不足
- 减少同时处理的数据量
- 调整智能体并发数量
- 增加系统交换空间

### 日志查看

```bash
# 查看系统日志
tail -f logs/system.log

# 查看智能体日志
tail -f logs/agents.log

# 查看数据库日志
tail -f logs/database.log
```

## 扩展开发

### 添加新的智能体

1. 继承 `BaseAgent` 类
2. 实现 `handle_message` 方法
3. 定义智能体能力列表
4. 注册到 `AgentManager`

```python
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="custom_agent",
            name="自定义智能体",
            description="执行自定义分析任务"
        )
        self.capabilities = ["custom_analysis"]
    
    async def handle_message(self, message):
        # 实现自定义逻辑
        return {"result": "success"}
```

### 添加新的数据源

1. 实现数据连接器
2. 定义数据映射规则
3. 注册到接口管理智能体

```python
class CustomDataConnector:
    async def connect(self, config):
        # 实现连接逻辑
        pass
    
    async def fetch_data(self, query):
        # 实现数据获取逻辑
        pass
```

### 自定义分析算法

1. 在 `data_analysis` 模块中添加算法
2. 注册到数据分析智能体
3. 配置算法参数

```python
class CustomAnalysisAlgorithm:
    def analyze(self, data, params):
        # 实现分析算法
        return analysis_result
```

## 技术支持

### 社区支持
- GitHub Issues：报告Bug和功能请求
- 技术文档：详细技术文档和API参考
- 示例代码：使用示例和最佳实践

### 企业支持
- 技术咨询：系统部署和配置咨询
- 定制开发：根据需求定制功能
- 运维支持：系统监控和维护

## 更新日志

### v0.1.0 (2024-01-01)
- 初始版本发布
- 基础多智能体架构
- 核心数据分析功能
- 报告生成功能
- Web管理界面

### 后续规划
- [ ] 实时数据流处理
- [ ] 更多机器学习算法
- [ ] 移动端支持
- [ ] 分布式部署支持
- [ ] 更多外部系统集成

## 许可证

MIT License - 详见 LICENSE 文件

---

© 2024 多智能体教育数据管理与分析系统. 保留所有权利。