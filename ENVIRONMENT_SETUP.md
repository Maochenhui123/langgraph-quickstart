# 环境变量配置说明

在启动docker-compose部署之前，请确保设置以下环境变量：

## 必需的环境变量

### 1. GEMINI_API_KEY
- **描述**: Gemini API密钥，用于访问Google的Gemini模型
- **获取方式**: 在 [Google AI Studio](https://makersuite.google.com/app/apikey) 创建API密钥
- **示例**: `GEMINI_API_KEY=AIzaSyBcvNfIJa1WKXgYjVHzOlKtYXFp2h0WSfQ`

### 2. CUSTOM_SEARCH_API_KEY
- **描述**: Google Custom Search API密钥，用于自定义搜索功能
- **获取方式**: 
  1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
  2. 启用 Custom Search API
  3. 创建API密钥
- **示例**: `CUSTOM_SEARCH_API_KEY=your_custom_search_api_key_here`

### 3. CUSTOM_SEARCH_ENGINE_ID
- **描述**: Google Custom Search引擎ID
- **获取方式**:
  1. 访问 [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
  2. 创建新的搜索引擎
  3. 获取搜索引擎ID
- **示例**: `CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id_here`

### 4. SCHOLAR_SEARCH_ENGINE_ID
- **描述**: Scholar Search引擎ID，用于学术资源搜索
- **获取方式**:
  1. 访问 [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
  2. 创建专门用于学术搜索的搜索引擎
  3. 配置搜索引擎以包含学术网站和数据库
  4. 获取搜索引擎ID
- **示例**: `SCHOLAR_SEARCH_ENGINE_ID=your_scholar_search_engine_id_here`

## 可选的环境变量

### LANGSMITH_API_KEY
- **描述**: LangSmith API密钥，用于日志记录和监控
- **获取方式**: 在 [LangSmith](https://smith.langchain.com/) 创建账户并获取API密钥
- **示例**: `LANGSMITH_API_KEY=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`

## 设置环境变量的方法

### 方法1: 使用export命令（临时）
```bash
export GEMINI_API_KEY="your_gemini_api_key"
export CUSTOM_SEARCH_API_KEY="your_custom_search_api_key"
export CUSTOM_SEARCH_ENGINE_ID="your_search_engine_id"
export SCHOLAR_SEARCH_API_KEY="your_scholar_search_api_key"
export SCHOLAR_SEARCH_ENGINE_ID="your_scholar_search_engine_id"
export LANGSMITH_API_KEY="your_langsmith_api_key"
```

### 方法2: 创建.env文件（推荐）
在项目根目录创建`.env`文件：
```bash
# .env文件内容
GEMINI_API_KEY=your_gemini_api_key_here
CUSTOM_SEARCH_API_KEY=your_custom_search_api_key_here
CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id_here
SCHOLAR_SEARCH_API_KEY=your_scholar_search_api_key_here
SCHOLAR_SEARCH_ENGINE_ID=your_scholar_search_engine_id_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
```

### 方法3: 在命令行中直接设置
```bash
GEMINI_API_KEY=your_key CUSTOM_SEARCH_API_KEY=your_key CUSTOM_SEARCH_ENGINE_ID=your_id SCHOLAR_SEARCH_API_KEY=your_key SCHOLAR_SEARCH_ENGINE_ID=your_id docker-compose up -d
```

## 验证配置

运行部署脚本前，系统会自动检查必需的环境变量是否已设置：
```bash
./deploy.sh
```

如果缺少必需的环境变量，脚本会显示错误信息并退出。

## 注意事项

1. 请确保API密钥的安全性，不要将其提交到版本控制系统中
2. `.env`文件已被添加到`.gitignore`中，不会被意外提交
3. 如果使用Google Custom Search，请确保已正确配置搜索引擎的范围和设置 