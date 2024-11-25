from abc import ABC, abstractmethod

class BaseAIClient(ABC):
    """AI客户端基类"""
    @abstractmethod
    def analyze_image(self, image_base64, prompt):
        """分析图片的抽象方法"""
        pass

def create_ai_client(provider, api_key, model_config):
    """AI客户端工厂函数"""
    if provider == "智谱AI":
        from .zhipu_client import ZhipuAIClient
        return ZhipuAIClient(api_key, model_config)
    elif provider == "通义千问":
        from .dashscope_client import DashscopeClient
        return DashscopeClient(api_key, model_config)
    elif provider == "Anthropic":
        from .anthropic_client import AnthropicClient
        return AnthropicClient(api_key, model_config)
    elif provider == "Mistral AI":
        from .mistral_client import MistralAIClient
        return MistralAIClient(api_key, model_config)
    else:
        raise ValueError(f"不支持的AI提供商: {provider}") 