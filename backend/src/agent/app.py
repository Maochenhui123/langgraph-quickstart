# mypy: disable - error - code = "no-untyped-def,misc"
import pathlib
import logging
from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware as StarletteCORSMiddleware

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the FastAPI app
app = FastAPI()

# 添加健康检查端点
@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy", "message": "Backend service is running"}

# 添加调试端点
@app.get("/debug")
async def debug_info(request: Request):
    logger.info(f"Debug endpoint called from {request.client.host}:{request.client.port}")
    return {
        "client_ip": request.client.host,
        "client_port": request.client.port,
        "headers": dict(request.headers),
        "method": request.method,
        "url": str(request.url)
    }

# Add CORS middleware to FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # 本机开发环境
        "http://localhost:3000",      # 其他本地端口
        "http://localhost:8080",      # 其他本地端口
        "http://127.0.0.1:5173",     # 本机IP访问
        "http://127.0.0.1:3000",     # 本机IP访问
        "http://127.0.0.1:8080",     # 本机IP访问
        "http://localhost:2024",      # 本地其他端口
        "http://127.0.0.1:2024",     # 本地其他端口
    ],
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 为了确保LangGraph的HTTP服务也能正确处理CORS，我们添加一个全局的CORS处理
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    # 动态设置CORS头，支持多个前端地址
    origin = request.headers.get("origin")
    if origin in [
        "http://localhost:5173",
        "http://127.0.0.1:5173", 
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]:
        response.headers["Access-Control-Allow-Origin"] = origin
    logging.info(f"CORS header set for origin: {origin}")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


def create_frontend_router(build_dir="../frontend/dist"):
    """Creates a router to serve the React frontend.

    Args:
        build_dir: Path to the React build directory relative to this file.

    Returns:
        A Starlette application serving the frontend.
    """
    build_path = pathlib.Path(__file__).parent.parent.parent / build_dir

    if not build_path.is_dir() or not (build_path / "index.html").is_file():
        print(
            f"WARN: Frontend build directory not found or incomplete at {build_path}. Serving frontend will likely fail."
        )
        # Return a dummy router if build isn't ready
        from starlette.routing import Route

        async def dummy_frontend(request):
            return Response(
                "Frontend not built. Run 'npm run build' in the frontend directory.",
                media_type="text/plain",
                status_code=503,
            )

        return Route("/{path:path}", endpoint=dummy_frontend)

    return StaticFiles(directory=build_path, html=True)


# Mount the frontend under /app to not conflict with the LangGraph API routes
app.mount(
    "/app",
    create_frontend_router(),
    name="frontend",
)
