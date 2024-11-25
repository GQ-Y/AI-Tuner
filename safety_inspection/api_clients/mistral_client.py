import requests
from . import BaseAIClient

class MistralAIClient(BaseAIClient):
    def __init__(self, api_key, model_config):
        self.api_key = api_key
        self.model_config = model_config
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        
    def analyze_image(self, image_base64, prompt):
        try:
            # 检查是否是支持多模态的模型
            if not self.model_config.get("vision", False):
                raise Exception(f"当前选择的模型 {self.model_config['id']} 不支持图像分析，请选择支持多模态的模型。")
            
            # 构建请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            data = {
                "model": self.model_config["id"],
                "messages": [
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
                ],
                "temperature": self.model_config.get("temperature", 0.7),
                "max_tokens": self.model_config.get("max_tokens", 4096)
            }
            
            # 发送请求
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            # 检查响应
            if response.status_code != 200:
                error_detail = ""
                try:
                    error_json = response.json()
                    error_detail = f"\n详细信息: {error_json}"
                except:
                    error_detail = f"\n响应内容: {response.text}"
                
                raise Exception(f"API请求失败: {response.status_code}{error_detail}")
            
            # 解析响应
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception("API返回结果为空")
                
        except Exception as e:
            raise Exception(f"Mistral AI调用失败: {str(e)}") 