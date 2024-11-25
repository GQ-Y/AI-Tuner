import zhipuai
from . import BaseAIClient

class ZhipuAIClient(BaseAIClient):
    def __init__(self, api_key, model_config):
        self.client = zhipuai.ZhipuAI(api_key=api_key)
        self.model_config = model_config
        
    def analyze_image(self, image_base64, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model_config["id"],
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=self.model_config["temperature"]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"智谱AI调用失败: {str(e)}") 