from anthropic import Anthropic
from . import BaseAIClient
import base64

class AnthropicClient(BaseAIClient):
    def __init__(self, api_key, model_config):
        self.client = Anthropic(api_key=api_key)
        self.model_config = model_config
        
    def analyze_image(self, image_base64, prompt):
        try:
            response = self.client.messages.create(
                model=self.model_config["id"],
                max_tokens=self.model_config["max_tokens"],
                temperature=self.model_config["temperature"],
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
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_base64
                                }
                            }
                        ]
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic调用失败: {str(e)}") 