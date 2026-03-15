#!/usr/bin/env pwsh

# 仓配装SaaS系统一键部署脚本
# 该脚本会自动安装Docker（如果未安装）并部署项目

Write-Host "=====================================" -ForegroundColor Green
Write-Host "仓配装SaaS系统一键部署脚本" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# 检查是否以管理员身份运行
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "错误：请以管理员身份运行此脚本" -ForegroundColor Red
    Write-Host "请右键点击脚本文件，选择 '以管理员身份运行'" -ForegroundColor Yellow
    Pause
    exit 1
}

# 检查Docker是否已安装
Write-Host "检查Docker是否已安装..." -ForegroundColor Cyan
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "Docker已安装，版本：$(docker --version)" -ForegroundColor Green
} else {
    Write-Host "Docker未安装，开始安装Docker Desktop..." -ForegroundColor Yellow
    
    # 下载Docker Desktop安装包
    $dockerInstallerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
    $installerPath = "$env:TEMP\DockerDesktopInstaller.exe"
    
    Write-Host "下载Docker Desktop安装包..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $dockerInstallerUrl -OutFile $installerPath
    
    # 安装Docker Desktop
    Write-Host "安装Docker Desktop..." -ForegroundColor Cyan
    Start-Process -FilePath $installerPath -ArgumentList "install" -Wait
    
    # 删除安装包
    Remove-Item $installerPath -Force
    
    Write-Host "Docker Desktop安装完成，请手动启动Docker Desktop并等待服务启动" -ForegroundColor Green
    Write-Host "启动Docker Desktop后，按任意键继续..." -ForegroundColor Yellow
    Pause
}

# 检查Docker服务是否运行
Write-Host "检查Docker服务是否运行..." -ForegroundColor Cyan
try {
    docker info | Out-Null
    Write-Host "Docker服务运行正常" -ForegroundColor Green
} catch {
    Write-Host "Docker服务未运行，请确保Docker Desktop已启动" -ForegroundColor Red
    Write-Host "启动Docker Desktop后，按任意键继续..." -ForegroundColor Yellow
    Pause
    # 再次检查
    try {
        docker info | Out-Null
        Write-Host "Docker服务运行正常" -ForegroundColor Green
    } catch {
        Write-Host "错误：无法启动Docker服务，请手动启动Docker Desktop" -ForegroundColor Red
        Pause
        exit 1
    }
}

# 检查docker-compose是否可用
Write-Host "检查docker-compose是否可用..." -ForegroundColor Cyan
if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
    Write-Host "docker-compose已安装，版本：$(docker-compose --version)" -ForegroundColor Green
} else {
    Write-Host "docker-compose未安装，开始安装..." -ForegroundColor Yellow
    # Docker Desktop已包含docker-compose，这里只是验证
    try {
        docker compose version | Out-Null
        Write-Host "docker-compose已作为docker的子命令可用" -ForegroundColor Green
    } catch {
        Write-Host "错误：无法使用docker-compose，请确保Docker Desktop安装正确" -ForegroundColor Red
        Pause
        exit 1
    }
}

# 部署项目
Write-Host "开始部署仓配装SaaS系统..." -ForegroundColor Cyan

# 检查当前目录是否包含docker-compose.yml文件
if (-not (Test-Path "./docker-compose.yml")) {
    Write-Host "错误：当前目录没有docker-compose.yml文件，请在项目根目录运行此脚本" -ForegroundColor Red
    Pause
    exit 1
}

# 执行docker-compose命令
Write-Host "构建并启动容器..." -ForegroundColor Cyan
try {
    docker-compose up -d --build
    Write-Host "部署完成！" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host "系统访问地址：" -ForegroundColor Green
    Write-Host "- Web管理后台: http://localhost" -ForegroundColor Green
    Write-Host "- H5移动端: http://localhost:8080" -ForegroundColor Green
    Write-Host "- 后端API: http://localhost:8000" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
} catch {
    Write-Host "部署失败：$($_.Exception.Message)" -ForegroundColor Red
    Pause
    exit 1
}

Write-Host "按任意键退出..." -ForegroundColor Yellow
Pause