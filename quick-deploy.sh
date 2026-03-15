#!/bin/bash

# 仓配装一体系统一键部署脚本

echo "====================================="
echo "仓配装一体系统一键部署"
echo "====================================="

# 克隆项目
echo "正在克隆项目..."
git clone https://github.com/olddenf/Integrated-warehouse-distribution-and-packaging-system.git

# 进入项目目录
cd Integrated-warehouse-distribution-and-packaging-system

# 构建并启动服务
echo "正在构建并启动服务..."
docker-compose up -d --build

echo "====================================="
echo "部署完成！"
echo "====================================="
echo "Web管理后台: http://localhost"
echo "H5移动端: http://localhost:8080"
echo "后端API: http://localhost:8000"
echo "====================================="