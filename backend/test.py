import argparse
from langchain_core.messages import HumanMessage
from agent.graph import graph
import os

os.environ['APP_TOKEN'] = 'sk-b5d3c6134a7c473e9db05b894c48b332'
os.environ['LLM_BASE_URL'] = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
os.environ['APP_ID'] = 'd09e1854da1040f3838eb3c4af32ce33'
os.environ['GEMINI_API_KEY'] = 'AIzaSyBcvNfIJa1WKXgYjVHzOlKtYXFp2h0WSfQ'

def main() -> None:
    """Run the research agent from the command line."""
    state = {
        "messages": [HumanMessage(content="稳定币是什么？")],
        "initial_search_query_count": 3,
        "max_research_loops": 2,
        "reasoning_model": "qwen-plus-latest",
    }

    result = graph.invoke(state)
    messages = result.get("messages", [])
    if messages:
        print(messages[-1].content)


if __name__ == "__main__":
    main()
