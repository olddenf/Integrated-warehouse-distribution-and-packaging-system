# 仓配装一体系统一键部署脚本
# 该脚本会自动克隆项目并使用Docker Compose部署

Write-Host "=====================================" -ForegroundColor Green
Write-Host "仓配装一体系统一键部署" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# 克隆项目
Write-Host "正在克隆项目..." -ForegroundColor Yellow
git clone https://github.com/olddenf/Integrated-warehouse-distribution-and-packaging-system.git

# 进入项目目录
Set-Location Integrated-warehouse-distribution-and-packaging-system

# 构建并启动服务
Write-Host "正在构建并启动服务..." -ForegroundColor Yellow
docker-compose up -d --build

Write-Host "=====================================" -ForegroundColor Green
Write-Host "部署完成！" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host "Web管理后台: http://localhost" -ForegroundColor Cyan
Write-Host "H5移动端: http://localhost:8080" -ForegroundColor Cyan
Write-Host "后端API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Green

Pause