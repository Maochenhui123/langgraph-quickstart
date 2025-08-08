import json
import logging

from agent.tools_and_schemas import SearchQueryList, Reflection
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langgraph.types import Send
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langchain_core.runnables import RunnableConfig

from agent.state import (
    OverallState,
    QueryGenerationState,
    ReflectionState,
    WebSearchState,
)
from agent.configuration import Configuration
from agent.prompts import (
    get_current_date,
    query_writer_instructions,
    web_searcher_instructions,
    reflection_instructions,
    answer_instructions,
)
from agent.post import Post
from agent.utils import (
    get_research_topic,
    resolve_urls,
)
from agent.base_agent import Agent, JsonAgent, WebSearchAgent

load_dotenv()


# Nodes
def generate_query(state: OverallState, config: RunnableConfig) -> QueryGenerationState:
    """
    基于用户问题生成搜索查询的LangGraph节点

    使用LLM为用户的问题创建优化的网络搜索查询，用于网络研究。

    Args:
        state: 包含用户问题的当前图状态
        config: 可运行配置，包括LLM提供商设置

    Returns:
        包含状态更新的字典，包括search_query键，包含生成的查询
    """
    configurable = Configuration.from_runnable_config(config)
    # 检查自定义初始搜索查询数量
    if state.get("initial_search_query_count") is None:
        state["initial_search_query_count"] = configurable.number_of_initial_queries

    agent = JsonAgent(model_id=configurable.query_generator_model, keys=SearchQueryList)
    agent.set_step_prompt(query_writer_instructions)
    result = agent.step(
        current_date=get_current_date(),
        research_topic=get_research_topic(state["messages"]),
        number_queries=state["initial_search_query_count"],
    )
    logging.info("生成查询")
    logging.info(state)
    logging.info(f"查询生成结果: {result}")
    return {"search_query": result.query}


def continue_to_web_research(state: QueryGenerationState):
    """
    将搜索查询发送到网络研究节点的LangGraph节点

    用于为每个搜索查询生成n个网络研究节点，实现并行搜索。

    Args:
        state: 包含搜索查询的查询生成状态

    Returns:
        发送到web_research节点的消息列表
    """
    return [
        Send("web_research", {"search_query": search_query, "id": int(idx)})
        for idx, search_query in enumerate(state["search_query"])
    ]


def web_research(state: WebSearchState, config: RunnableConfig) -> OverallState:
    """
    使用web search agent执行网络搜索的LangGraph节点
    Args:
        state: 包含搜索查询和研究循环计数的当前图状态
        config: 可运行配置，包括搜索API设置

    Returns:
        包含状态更新的字典，包括sources_gathered、research_loop_count和web_research_results
    """
    # 配置
    configurable = Configuration.from_runnable_config(config)
    # 使用google genai客户端，因为langchain客户端不返回基础元数据
    web_searcher = WebSearchAgent()

    # 执行搜索
    response = web_searcher.step(prompt=state["search_query"],
                                 count=10)
    # 长URL到短URL的映射
    long2short_url_mappings = resolve_urls(response, state["id"])
    sources_gathered = [{"short_url": long2short_url_mappings[item["url"]], "value": item["url"], "label": item["title"]} for item in response]
    web_search_result = [{"snippet": item["snippet"], "title": item["title"], "url": long2short_url_mappings[item["url"]]} for item in response]
    web_search_result = json.dumps(web_search_result, ensure_ascii=False, indent=4)

    agent = Agent(model_id=configurable.query_generator_model)
    agent.set_step_prompt(web_searcher_instructions)
    modified_text = agent.step(query=state["search_query"], current_date=get_current_date(), web_search_result=web_search_result)
    modified_text = Post.extract_pattern(modified_text, pattern="text")
    logging.info(f"网络搜索")
    logging.info(f"搜索标题: {state['search_query']}")
    logging.info(f"网络搜索结果: {modified_text}")
    return {
        "sources_gathered": sources_gathered,
        "search_query": [state["search_query"]],
        "web_research_result": [modified_text],
    }


def reflection(state: OverallState, config: RunnableConfig) -> ReflectionState:
    """
    识别知识差距并生成潜在后续查询的LangGraph节点

    分析当前摘要以识别需要进一步研究的领域，并生成潜在的后续查询。
    使用结构化输出来提取JSON格式的后续查询。

    Args:
        state: 包含运行摘要和研究主题的当前图状态
        config: 可运行配置，包括LLM提供商设置

    Returns:
        包含状态更新的字典，包括search_query键，包含生成的后续查询
    """
    configurable = Configuration.from_runnable_config(config)
    # 增加研究循环计数并获取推理模型
    state["research_loop_count"] = state.get("research_loop_count", 0) + 1
    reasoning_model = state.get("reasoning_model", configurable.reflection_model)

    # 格式化提示
    agent = JsonAgent(model_id=reasoning_model, keys=Reflection)
    agent.set_step_prompt(reflection_instructions)
    result = agent.step(
        current_date=get_current_date(),
        number_queries=state["initial_search_query_count"],
        research_topic=get_research_topic(state["messages"]),
        summaries="\n\n---\n\n".join(state["web_research_result"]),
    )

    logging.info("反思分析")
    logging.info(result)
    return {
        "is_sufficient": result.is_sufficient,
        "knowledge_gap": result.knowledge_gap,
        "follow_up_queries": result.follow_up_queries,
        "research_loop_count": state["research_loop_count"],
        "number_of_ran_queries": len(state["search_query"]),
        "max_research_loops": state.get("max_research_loops", configurable.max_research_loops),
    }


def evaluate_research(
    state: ReflectionState,
    config: RunnableConfig,
) -> OverallState:
    """
    确定研究中下一步的LangGraph路由函数

    通过决定是否继续收集信息或基于配置的最大研究循环次数来最终确定摘要，
    从而控制研究循环。

    Args:
        state: 包含研究循环计数的当前图状态
        config: 可运行配置，包括max_research_loops设置

    Returns:
        字符串字面量，指示下一个要访问的节点（"web_research"或"finalize_summary"）
    """
    configurable = Configuration.from_runnable_config(config)
    max_research_loops = (
        state.get("max_research_loops")
        if state.get("max_research_loops") is not None
        else configurable.max_research_loops
    )
    logging.info("评估研究")
    logging.info(state)
    logging.info(f"最大研究循环数: {max_research_loops}")
    logging.info(f"研究循环计数: {state['research_loop_count']}")
    if state["is_sufficient"] or state["research_loop_count"] >= max_research_loops:
        return "finalize_answer"
    else:
        return [
            Send(
                "web_research",
                {
                    "search_query": follow_up_query,
                    "id": state["number_of_ran_queries"] + int(idx),
                },
            )
            for idx, follow_up_query in enumerate(state["follow_up_queries"])
        ]


def finalize_answer(state: OverallState, config: RunnableConfig):
    """
    最终确定研究摘要的LangGraph节点

    通过去重和格式化源，然后将它们与运行摘要结合，
    创建结构良好的研究报告，包含适当的引用。

    Args:
        state: 包含运行摘要和收集源的当前图状态

    Returns:
        包含状态更新的字典，包括running_summary键，包含格式化的最终摘要和源
    """
    configurable = Configuration.from_runnable_config(config)
    reasoning_model = state.get("reasoning_model") or configurable.answer_model

    # 格式化提示
    agent = Agent(model_id=reasoning_model)
    agent.set_step_prompt(answer_instructions)
    content = agent.step(
        current_date=get_current_date(),
        research_topic=get_research_topic(state["messages"]),
        summaries="\n---\n\n".join(state["web_research_result"]),
    )

    # 用原始URL替换短URL，并将所有使用的URL添加到sources_gathered
    unique_sources = []
    for source in state["sources_gathered"]:
        if source["short_url"] in content:
            content= content.replace(
                source["short_url"], source["value"]
            )
            unique_sources.append(source)

    logging.info("最终确定答案")
    logging.info(content)
    return {
        "messages": [AIMessage(content=content)],
        "sources_gathered": unique_sources,
    }


# 创建我们的代理图
builder = StateGraph(OverallState, config_schema=Configuration)

# 定义我们将在其间循环的节点
builder.add_node("generate_query", generate_query)
builder.add_node("web_research", web_research)
builder.add_node("reflection", reflection)
builder.add_node("finalize_answer", finalize_answer)

# 将入口点设置为`generate_query`
# 这意味着这个节点是第一个被调用的
builder.add_edge(START, "generate_query")
# 添加条件边以在并行分支中继续搜索查询
builder.add_conditional_edges(
    "generate_query", continue_to_web_research, ["web_research"]
)
# 对网络研究进行反思
builder.add_edge("web_research", "reflection")
# 评估研究
builder.add_conditional_edges(
    "reflection", evaluate_research, ["web_research", "finalize_answer"]
)
# 最终确定答案
builder.add_edge("finalize_answer", END)

# 编译图
graph = builder.compile(name="pro-search-agent")
