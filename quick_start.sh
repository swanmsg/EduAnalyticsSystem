#!/bin/bash

# 多智能体教育数据管理与分析系统 - 快速启动脚本

echo "🎓 多智能体教育数据管理与分析系统"
echo "基于LlamaIndex框架和Ollama qwen3:4b模型"
echo "============================================"

# 检查Python版本
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python版本检查通过: $python_version"
else
    echo "❌ Python版本不符合要求，需要3.9+，当前版本: $python_version"
    exit 1
fi

# 检查Ollama是否安装
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama未安装，请先安装Ollama:"
    echo "   macOS/Linux: curl -fsSL https://ollama.com/install.sh | sh"
    echo "   Windows: 访问 https://ollama.com/download"
    exit 1
fi

echo "✅ Ollama已安装"

# 检查Ollama服务是否运行
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Ollama服务未运行，正在启动..."
    ollama serve &
    sleep 5
fi

echo "✅ Ollama服务运行正常"

# 检查qwen3:4b模型是否已下载
if ! ollama list | grep -q "qwen3:4b"; then
    echo "⚠️  qwen3:4b模型未安装，正在下载..."
    echo "   这可能需要几分钟时间..."
    ollama pull qwen3:4b
fi

echo "✅ qwen3:4b模型已准备就绪"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

echo "✅ 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📦 安装Python依赖包..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo "✅ 依赖安装完成"

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "⚙️  创建配置文件..."
    cat > .env << EOF
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
REPORT_TIMEOUT=1800

# 安全配置
SECRET_KEY=dev-secret-key-change-in-production

# 日志配置
LOG_LEVEL=INFO
EOF
    echo "✅ 配置文件已创建"
fi

# 创建必要的目录
mkdir -p exports
mkdir -p logs
mkdir -p data

echo "📁 目录结构已创建"

# 运行系统检查
echo "🔍 运行系统检查..."
python3 -c "
import asyncio
import sys
import os
sys.path.append('.')

async def check_system():
    try:
        from config.ollama_config import OllamaManager
        ollama = OllamaManager()
        success = await ollama.initialize()
        if success:
            print('✅ 系统检查通过')
            return True
        else:
            print('❌ 系统检查失败')
            return False
    except Exception as e:
        print(f'❌ 系统检查失败: {e}')
        return False

result = asyncio.run(check_system())
exit(0 if result else 1)
"

if [ $? -ne 0 ]; then
    echo "❌ 系统检查失败，请检查配置"
    exit 1
fi

echo ""
echo "🚀 启动系统..."
echo "   系统地址: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo "   健康检查: http://localhost:8000/health"
echo ""
echo "   按 Ctrl+C 停止系统"
echo "============================================"

# 启动系统
python3 run_system.py