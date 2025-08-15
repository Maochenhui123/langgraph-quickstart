#!/bin/bash

echo "启动LangGraph后端服务..."

# 检查Python环境
echo "检查Python环境..."
python3 --version
pip3 --version

# 检查依赖
echo "检查依赖..."
pip3 list | grep langgraph

# 停止可能存在的旧进程
echo "停止旧进程..."
pkill -f "langgraph dev" || true

# 等待进程完全停止
sleep 2

# 启动服务 - 明确指定监听所有接口
echo "启动服务在端口2024，监听所有网络接口..."
langgraph dev --port 2024 --host 0.0.0.0

echo "服务启动完成"
