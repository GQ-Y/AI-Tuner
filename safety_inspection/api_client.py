import zhipuai

class ZhipuAIClient:
    def __init__(self, api_key=None, model_config=None):
        self.api_key = api_key
        self.model_config = model_config
        self.client = zhipuai.ZhipuAI(api_key=self.api_key)
        
    def analyze_image(self, image_base64, prompt):
        """调用智谱AI进行图片分析"""
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
            return self._parse_response(response)
        except Exception as e:
            raise Exception(f"API调用失败: {str(e)}")
    
    def _parse_response(self, response):
        """解析API响应"""
        try:
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"API响应解析失败: {str(e)}") 