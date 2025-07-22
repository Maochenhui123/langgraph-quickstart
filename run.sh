# 改成自己的内容
export APP_TOKEN="sk-b5d3c6134a7c473e9db05b894c48b332"
export LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export APP_ID="d09e1854da1040f3838eb3c4af32ce33"
cd backend
pip install .

# python test.py
cd ..
cd frontend
npm install
cd ..
make dev