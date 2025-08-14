# LangGraph 智能代理研究系统

一个基于 LangGraph 框架构建的智能研究代理系统，支持网络搜索、信息分析和智能问答功能。

## 项目目录结构

```
langgraph-quickstart/
├── backend/                          # 后端服务目录
│   ├── src/
│   │   ├── agent/                    # 核心代理模块
│   │   │   ├── __init__.py
│   │   │   ├── app.py               # FastAPI 应用入口
│   │   │   ├── base_agent.py        # 基础代理类定义
│   │   │   ├── configuration.py     # 系统配置管理
│   │   │   ├── graph.py             # LangGraph 工作流定义
│   │   │   ├── state.py             # 状态数据结构定义
│   │   │   ├── tools_and_schemas.py # 工具和模式定义
│   │   │   ├── prompts.py           # 提示词模板
│   │   │   ├── post.py              # 后处理工具
│   │   │   ├── utils.py             # 工具函数
│   │   │   └── llm/                 # LLM 集成模块
│   │   │       ├── __init__.py
│   │   │       └── llm.py           # 大语言模型接口
│   │   └── main.py                  # 主程序入口
│   ├── langgraph.json               # LangGraph 配置文件
│   ├── pyproject.toml               # Python 项目配置
│   └── examples/                    # 示例代码
│       └── cli_research.py         # 命令行研究示例
├── frontend/                        # 前端应用目录
│   ├── src/
│   │   ├── components/              # React 组件
│   │   │   ├── ActivityTimeline.tsx # 活动时间线组件
│   │   │   ├── ChatMessagesView.tsx # 聊天消息视图
│   │   │   ├── InputForm.tsx        # 输入表单组件
│   │   │   ├── WelcomeScreen.tsx    # 欢迎界面组件
│   │   │   └── ui/                  # UI 组件库
│   │   ├── App.tsx                  # 主应用组件
│   │   ├── main.tsx                 # 应用入口
│   │   └── global.css               # 全局样式
│   ├── package.json                 # Node.js 依赖配置
│   └── vite.config.ts               # Vite 构建配置
├── README.md                        # 项目说明文档
├── LICENSE                          # 许可证文件
└── run.sh                           # 启动脚本
```

## 关键文件说明

### 后端核心文件
- **`backend/langgraph.json`**: LangGraph 服务配置，定义图服务和 HTTP 应用
- **`backend/src/agent/graph.py`**: 核心工作流定义，包含所有节点和状态转换逻辑
- **`backend/src/agent/state.py`**: 状态数据结构，定义图执行过程中的数据流
- **`backend/src/agent/base_agent.py`**: 代理基类，支持多种代理类型（基础、JSON、MCP、Web搜索）
- **`backend/src/agent/app.py`**: FastAPI 应用，集成前端静态文件服务

### 前端核心文件
- **`frontend/src/App.tsx`**: 主应用逻辑，集成 LangGraph SDK 流式通信
- **`frontend/src/components/ActivityTimeline.tsx`**: 研究进度可视化组件
- **`frontend/src/components/ChatMessagesView.tsx`**: 聊天消息显示组件
- **`frontend/package.json`**: 前端依赖配置，包含 LangGraph SDK 和 UI 组件库

### 配置文件
- **`backend/pyproject.toml`**: Python 项目配置，定义依赖和构建要求
- **`frontend/vite.config.ts`**: Vite 构建工具配置
- **`run.sh`**: 项目启动脚本

## 项目架构

### 前后端接口定义
- **后端 API**: 基于 FastAPI 构建，提供 LangGraph 代理服务
- **前端接口**: 使用 LangGraph SDK React 组件进行实时流式通信
- **通信协议**: 基于 LangGraph 的流式事件系统

### 后端架构
- **API 层**: FastAPI 应用，集成 LangGraph 服务
- **Graph 层**: 状态管理和 LangGraph 工作流定义
- **Node 层**: 查询生成、网络研究、反思、答案生成等节点
- **组件层**: Agent、LLM、MCP 等核心组件

### 前端架构
- **页面层**: 主应用、欢迎界面等页面组件
- **组件层**: 聊天界面、输入表单、活动时间线等 UI 组件

## 项目实现

### API 层实现
- **FastAPI 应用集成**: 通过 `backend/src/agent/app.py` 创建 FastAPI 应用，集成 LangGraph 服务
- **静态文件服务**: 自动检测前端构建状态，提供前端访问，支持开发和生产环境
- **跨域和错误处理**: 完善的异常处理机制，支持开发调试

### 接口实现
- **LangGraph HTTP 接口**: 通过 `backend/langgraph.json` 自动暴露图服务，支持流式响应
- **实时事件流**: 前端通过 `@langchain/langgraph-sdk/react` 的 `useStream` Hook 实时获取研究进度
- **事件处理**: 支持 `generate_query`、`web_research`、`reflection`、`finalize_answer` 等事件类型

### Graph 层实现
- **状态图定义**: 使用 LangGraph 的 `StateGraph` 构建工作流，定义在 `backend/src/agent/graph.py`
- **节点连接**: 通过 `Send` 机制实现节点间的消息传递，支持并行和串行执行
- **状态管理**: 使用 TypedDict 定义强类型状态，如 `OverallState`、`ReflectionState` 等

### Node 层实现
- **查询生成节点** (`generate_query`): 使用 `JsonAgent` 生成结构化搜索查询，支持自定义查询数量
- **网络研究节点** (`web_research`): 集成 `WebSearchAgent` 执行网络搜索，返回标题、摘要、URL等信息
- **反思节点** (`reflection`): 分析搜索结果，识别知识缺口，生成后续查询建议
- **答案生成节点** (`finalize_answer`): 综合所有信息生成最终答案

### Query 节点实现
- **智能查询生成**: 基于用户问题和上下文生成优化搜索查询，支持中文和英文
- **查询数量控制**: 可配置的初始查询数量，支持低、中、高三种努力级别
- **查询质量评估**: 通过反思机制优化查询策略，自动识别需要进一步研究的领域

### 组件层实现

#### 基础代理类 (`Agent`)
位于 `backend/src/agent/base_agent.py`，是所有代理的基类，提供核心功能：

```python
class Agent:
    def __init__(self, model_id="qwen2.5-72b-instruct"):
        self.llm = openaiLLM(model_id=model_id)
    
    def step(self, **kwargs):
        # 执行代理步骤，支持重试机制
        step_prompt = self.prompt_format(self.step_prompt, **kwargs)
        for _ in range(10):  # 最多重试10次
            try:
                response = self(step_prompt)
                response = self.post_process(response)
                break
            except Exception as e:
                print(e)
                continue
        return response
```

**核心特性**：
- 支持多种 LLM 模型（默认使用 qwen2.5-72b-instruct）
- 内置重试机制，提高稳定性
- 可配置的步骤提示词模板
- 支持动态参数替换和格式化

#### JSON 代理 (`JsonAgent`)
继承自基础代理，专门处理结构化 JSON 输出：

```python
class JsonAgent(Agent):
    def __init__(self, model_id="qwen2.5-72b-instruct", keys=None):
        super().__init__(model_id)
        self.keys = keys  # 可选的 Pydantic 模型验证
    
    def post_process(self, response):
        # 提取 JSON 内容并验证格式
        result = json.loads(Post.extract_pattern(response, pattern="json"))
        if not self.keys:
            return result
        return self.keys(**result)  # 使用 Pydantic 模型验证
```

**应用场景**：
- 查询生成：在 `graph.py` 中用于生成搜索查询列表
- 结构化输出：确保 LLM 返回符合预期格式的数据
- 数据验证：支持 Pydantic 模型进行类型检查

#### MCP 代理 (`MCPAgent`)
支持 Model Context Protocol 的代理，集成外部服务：

```python
class MCPAgent(Agent):
    def step(self, **kwargs):
        for _ in range(10):
            try:
                # 调用阿里云 DashScope MCP 服务
                response = Application.call(
                    api_key=os.getenv("APP_TOKEN"),
                    app_id=os.getenv("MCP_APP_ID"),
                    prompt=step_prompt,
                    biz_params=kwargs
                )
                response = self.post_process(response)
                return response
            except Exception as e:
                print(e)
                continue
        return None
```

**集成特性**：
- 阿里云 DashScope MCP 服务集成
- 支持业务参数传递
- 错误处理和重试机制

#### 网络搜索代理 (`WebSearchAgent`)
专门用于网络信息检索的代理，继承自 MCP 代理：

```python
class WebSearchAgent(MCPAgent):
    def post_process(self, response):
        response = super().post_process(response)
        # 提取搜索结果页面信息
        pages = json.loads(response["result"]["content"][0]["text"])["pages"]
        pages = [{
            "snippet": page["snippet"], 
            "title": page["title"], 
            "url": page["url"]
        } for page in pages]
        return pages
```

**搜索功能**：
- 结构化搜索结果：标题、摘要、URL
- 在 `graph.py` 的 `web_research` 节点中使用
- 支持并行搜索多个查询

#### LLM 集成层 (`openaiLLM`)
位于 `backend/src/agent/llm/llm.py`，提供统一的 LLM 接口：

```python
class openaiLLM:
    def __init__(self, model_id=""):
        self.model_id = model_id
    
    def generate_response(self, query):
        client = OpenAI(
            api_key=os.getenv('APP_TOKEN'),
            base_url=os.getenv("LLM_BASE_URL"),
        )
        response = client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            extra_body={"enable_thinking": False},
        )
        return response.choices[0].message.content
```

**配置支持**：
- 环境变量配置：`APP_TOKEN`（API 密钥）、`LLM_BASE_URL`（服务地址）
- OpenAI 兼容接口，支持多种 LLM 提供商
- 可配置的模型 ID 和系统提示词

#### 提示词系统 (`prompts.py`)
提供预定义的提示词模板，支持动态参数替换：

```python
query_writer_instructions = """# 任务说明
你的任务是根据当前的研究主题决定多个用于网络搜索的标题...

# Context
{research_topic}

# Output"""
```

**主要提示词**：
- `query_writer_instructions`: 查询生成指令
- `web_searcher_instructions`: 网络搜索整合指令  
- `reflection_instructions`: 反思和评估指令
- `answer_instructions`: 最终答案生成指令

#### 工作流图 (`graph.py`)
使用 LangGraph 构建的研究工作流，包含多个节点：

```python
def generate_query(state: OverallState, config: RunnableConfig) -> QueryGenerationState:
    """基于用户问题生成搜索查询的LangGraph节点"""
    configurable = Configuration.from_runnable_config(config)
    agent = JsonAgent(model_id=configurable.query_generator_model, keys=SearchQueryList)
    agent.set_step_prompt(query_writer_instructions)
    result = agent.step(
        current_date=get_current_date(),
        research_topic=get_research_topic(state["messages"]),
        number_queries=state["initial_search_query_count"],
    )
    return {"search_query": result.query}
```

**工作流节点**：
- `generate_query`: 生成搜索查询
- `web_research`: 执行网络搜索
- `reflection`: 评估信息充足性
- `answer`: 生成最终答案

## 项目部署

### 环境要求
- Python >= 3.11
- Node.js >= 18.0.0

### 后端部署
```bash
cd backend
pip install -e .
langgraph dev
```

### 前端部署
```bash
cd frontend
npm install
npm run dev  # 开发模式
npm run build  # 生产构建
```

### 环境配置
- APP_TOKEN: 阿里云 DashScope API 密钥
- LLM_BASE_URL: LLM 服务基础 URL
- MCP_APP_ID: 搜索MCP APP ID

### 服务启动
- 开发模式: 后端运行在 localhost:2024，前端运行在 localhost:5173
- 生产模式: 通过 langgraph dev 启动，前端集成到后端服务中

简单运行可以通过运行如下命令，进入根目录下
```bash
sh run.sh
```

## 技术栈

### 后端技术栈
- **LangGraph 0.2.6+**: 核心工作流框架，用于构建复杂的 AI 代理工作流
  - 支持状态图定义和节点间消息传递
  - 提供 `StateGraph`、`Send` 等核心概念
  - 示例：在 `backend/src/agent/graph.py` 中定义研究工作流
- **FastAPI**: 现代 Python Web 框架，提供高性能的 API 服务
  - 自动 API 文档生成
  - 异步支持，适合流式响应
- **LangChain 0.3.19+**: LLM 集成框架，提供统一的 AI 模型接口
  - 支持多种 LLM 提供商
  - 提供消息处理和工具调用能力
- **Python 3.11+**: 运行时环境，支持现代 Python 特性

### 前端技术栈
- **React 19**: 最新版本的 React 框架，提供现代化的用户界面开发体验
  - 支持并发特性和自动批处理
  - 示例：在 `frontend/src/App.tsx` 中使用 `useStream` Hook 实现实时通信
- **TypeScript**: 类型安全的 JavaScript 超集
  - 提供完整的类型定义和智能提示
  - 支持接口定义，如 `ProcessedEvent` 类型
- **Tailwind CSS 4.1.5**: 实用优先的 CSS 框架
  - 提供丰富的预设样式类
  - 支持响应式设计和暗色主题
- **Radix UI**: 无样式的可访问组件库
  - 提供 `Card`、`ScrollArea`、`Select` 等基础组件
  - 示例：在 `frontend/src/components/ActivityTimeline.tsx` 中构建活动时间线
- **Vite 6.3.4**: 现代前端构建工具
  - 快速的开发服务器和热重载
  - 优化的生产构建

### 集成服务
- **阿里云 DashScope**: 主要的 LLM 服务提供商
  - 支持 Qwen 系列模型（如 qwen2.5-72b-instruct）
  - 通过 `APP_TOKEN` 和 `LLM_BASE_URL` 配置
  - 示例：在 `backend/src/agent/llm/llm.py` 中集成 OpenAI 兼容接口
- **Google Gemini**: 备选 LLM 服务
  - 通过 `GEMINI_API_KEY` 配置
  - 提供备选的 AI 模型选择
- **MCP 搜索服务**: Model Context Protocol 集成的网络搜索
  - 通过 `MCP_APP_ID` 配置
  - 支持结构化的网络搜索结果
  - 示例：在 `backend/src/agent/base_agent.py` 中的 `WebSearchAgent` 类

### 开发工具
- **LangGraph CLI**: 用于开发和部署 LangGraph 应用
- **ESLint**: 代码质量检查工具
- **Ruff**: Python 代码格式化和检查工具
- **TypeScript ESLint**: TypeScript 代码质量检查

## 使用说明

1. 启动服务: 按照部署说明启动前后端服务
2. 访问界面: 通过浏览器访问前端界面
3. 提出问题: 输入研究问题，系统自动生成搜索查询
4. 实时监控: 通过活动时间线查看研究进度
5. 获取答案: 系统综合搜索结果生成最终答案
