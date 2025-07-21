import os
import copy
from agent.llm.llm import openaiLLM
from dashscope import Application
from agent.post import Post
import json

class Agent:
    step_prompt = """{prompt}"""
    def __init__(self, model_id="qwen2.5-72b-instruct"):
        self.llm = openaiLLM(model_id=model_id)

    def __call__(self, prompt):
        response = self.llm.generate_response(prompt)
        return response

    def set_step_prompt(self, prompt):
        self.step_prompt = prompt

    def step(self, **kwargs):
        step_prompt = self.prompt_format(self.step_prompt, **kwargs)
        response = ""
        for _ in range(10):
            try:
                response = self(step_prompt)
                response = self.post_process(response)
                break
            except Exception as e:
                print(e)
                continue
        return response

    def post_process(self, response):
        return response

    def prompt_format(self, prompt, **kwargs):
        prompt_ = copy.deepcopy(prompt)
        for k in kwargs.keys():
            rep = "{"+k+"}"
            prompt_ = prompt_.replace(rep, str(kwargs[k]))
        return prompt_


class JsonAgent(Agent):
    def __init__(self, model_id="qwen2.5-72b-instruct", keys=None):
        super().__init__(model_id)
        self.keys = keys

    def post_process(self, response):
        result = json.loads(Post.extract_pattern(response, pattern="json"))
        if not self.keys:
            return result
        return self.keys(**result)


class MCPAgent(Agent):

    def step(self, **kwargs):
        try:
            step_prompt = self.step_prompt.format(**kwargs)
        except Exception as e:
            step_prompt = self.step_prompt

        for _ in range(10):
            try:
                response = Application.call(
                    api_key=os.getenv("APP_TOKEN"),
                    app_id=os.getenv("APP_ID"),
                    prompt = step_prompt,
                    biz_params=kwargs
                )
                response = self.post_process(response)
                return response
            except Exception as e:
                print(e)
                continue
        return None

    def post_process(self, response):
        # TODO 执行MCP工具
        assert response.status_code == 200, "调用失败"
        response = json.loads(response.output.text)
        return response

class WebSearchAgent(MCPAgent):
    def step(self, prompt, **kwargs):
        try:
            step_prompt = self.step_prompt.format(prompt=prompt)
        except Exception as e:
            step_prompt = self.step_prompt

        for _ in range(10):
            try:
                response = Application.call(
                    api_key=os.getenv("APP_TOKEN"),
                    app_id=os.getenv("APP_ID"),
                    prompt = step_prompt,
                    biz_params=kwargs
                )
                response = self.post_process(response)
                return response
            except Exception as e:
                print(e)
                continue
        return None
    def post_process(self, response):
        response = super().post_process(response)
        pages = json.loads(response["result"]["content"][0]["text"])["pages"]
        pages = [{"snippet": page["snippet"], "title": page["title"], "url": page["url"]} for page in pages]
        return pages