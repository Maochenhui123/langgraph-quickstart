from openai import OpenAI
import os

class openaiLLM:
    app_token = os.getenv('APP_TOKEN')
    url = os.getenv('LLM_BASE_URL')
    def __init__(self, model_id=""):
        self.model_id = model_id

    def generate_response(self, query):
        client = OpenAI(
            api_key=self.app_token,
            base_url=self.url,
        )

        response = client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        return response.choices[0].message.content