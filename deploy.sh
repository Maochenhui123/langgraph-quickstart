#!/bin/bash

# 在deepsearch目录下
cd frontend
npm install
cd ..
docker-compose down --volumes --remove-orphans
docker build -t gemini-fullstack-langgraph -f Dockerfile .

# 使用环境变量启动docker-compose
APP_TOKEN=sk-0d19613fc1054f44acf7f0df7e7377e9 LANGSMITH_API_KEY=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 LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1 MCP_APP_ID=1ba45b1c6fdb4902a5e52fa0c79fb810 docker-compose  up -d
