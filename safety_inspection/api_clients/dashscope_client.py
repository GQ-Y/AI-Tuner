import dashscope
from . import BaseAIClient

class DashscopeClient(BaseAIClient):
    def __init__(self, api_key, model_config):
        dashscope.api_key = api_key
        self.model_config = model_config
        
    def analyze_image(self, image_base64, prompt):
        try:
            response = dashscope.MultiModalConversation.call(
                model=self.model_config["id"],
                messages=[
                    {
                        'role': 'user',
                        'content': [
                            {
                                'text': prompt
                            },
                            {
                                'image': f"data:image/jpeg;base64,{image_base64}"
                            }
                        ]
                    }
                ],
                temperature=self.model_config["temperature"]
            )
            return response.output.text
        except Exception as e:
            raise Exception(f"通义千问调用失败: {str(e)}") 