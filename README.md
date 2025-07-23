# DeepResearch Quick Start

当前项目展示了如何使用Langgraph搭建一个DeepResearch的应用
<img src="./app.png" title="Gemini Fullstack LangGraph" alt="Gemini Fullstack LangGraph" width="90%">

## 项目结构
当前项目目录分为以下两个结构
-   `frontend/`: 项目前端
-   `backend/`: 包含了核心的后端逻辑，所有的Agent体系的后端逻辑都在当前目录下

## Quick Start
**1. 前期准备:**
- Node.js and npm (or yarn/pnpm)
- Python 3.11+
- API Key，可以从[百炼](https://bailian.console.aliyun.com/)官网注册登录获取

**2. Install Dependencies:**

**Backend:**

```bash
cd backend
pip install .
```

**Frontend:**

```bash
cd frontend
npm install
```

**3. Run Development Servers:**
```bash
make dev
```

整体的部署脚本可以运行
```bash
sh run.sh
```


