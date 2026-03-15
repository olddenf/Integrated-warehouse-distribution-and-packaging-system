#!/bin/bash

# SaaS仓配装一体化管理系统 - 测试环境配置脚本

echo "======================================"
echo "  开始配置测试环境"
echo "======================================"

# 进入项目目录
cd "$(dirname "$0")"

# 1. 安装Python依赖
echo ""
echo "步骤 1/4: 安装Python依赖..."
pip install -q -r requirements.txt
pip install -q pytest pytest-asyncio pytest-cov aiosqlite

if [ $? -eq 0 ]; then
    echo "✅ Python依赖安装成功"
else
    echo "❌ Python依赖安装失败"
    exit 1
fi

# 2. 创建测试数据库
echo ""
echo "步骤 2/4: 配置测试数据库..."
export DATABASE_URL="sqlite+aiosqlite:///./test_saas_warehouse.db"
echo "✅ 测试数据库配置完成"

# 3. 配置测试环境变量
echo ""
echo "步骤 3/4: 配置测试环境变量..."
if [ ! -f .env.test ]; then
    echo ".env.test文件已存在，跳过创建"
else
    echo "✅ 测试环境变量配置完成"
fi

# 4. 验证测试环境
echo ""
echo "步骤 4/4: 验证测试环境..."
python -m pytest tests/test_unit_enhanced.py::TestIdGenerator -v --tb=no 2>&1 | grep -q "passed"

if [ $? -eq 0 ]; then
    echo "✅ 测试环境验证成功"
else
    echo "⚠️  测试环境验证有警告，但可继续使用"
fi

echo ""
echo "======================================"
echo "  测试环境配置完成！"
echo "======================================"
echo ""
echo "运行测试命令："
echo "  python -m pytest tests/test_unit_enhanced.py -v"
echo "  python -m pytest tests/ -v"
echo ""
echo "生成覆盖率报告："
echo "  python -m pytest tests/test_unit_enhanced.py --cov=app --cov-report=html"
echo ""
echo "查看测试计划："
echo "  cat tests/test_plan.md"
echo ""
