from typing import Any, Dict, List
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage


def get_research_topic(messages: List[AnyMessage], ignore_contexts: List[str]=None) -> str:
    """
    Get the research topic from the messages.
    """
    # check if request has a history and combine the messages into a single string
    if not ignore_contexts:
        ignore_contexts = []
    if len(messages) == 1:
        research_topic = messages[-1].content
    else:
        research_topic = ""
        for message in messages:
            if isinstance(message, HumanMessage):
                research_topic += f"User: {message.content}\n"
            elif isinstance(message, AIMessage) and message.content not in ignore_contexts:
                research_topic += f"Assistant: {message.content}\n"
    return research_topic

def get_last_user_response(messages: List[AnyMessage]) -> str:
    user_messages = [msg for msg in messages if isinstance(msg, HumanMessage)]
    if user_messages:
        return f"User: {user_messages[-1].content}\n"
    return ""

def resolve_urls(urls_to_resolve: List[Any], id: int) -> Dict[str, str]:
    """
    Create a map of the vertex ai search urls (very long) to a short url with a unique id for each url.
    Ensures each original URL gets a consistent shortened form while maintaining uniqueness.
    """
    prefix = f"https://search.com/id/"
    urls = [site["url"] for site in urls_to_resolve]

    # Create a dictionary that maps each unique URL to its first occurrence index
    resolved_map = {}
    for idx, url in enumerate(urls):
        if url not in resolved_map:
            resolved_map[url] = f"{prefix}{id}-{idx}"

    return resolved_map
