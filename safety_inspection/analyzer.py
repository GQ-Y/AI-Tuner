from .utils import encode_image, validate_image
from .api_clients import create_ai_client
from .config import PROMPT_TEMPLATES, PROVIDERS
import time
import os
from datetime import datetime
from PIL import Image

class SafetyAnalyzer:
    def __init__(self, custom_templates=None, api_key=None, provider=None, model_config=None):
        self.templates = custom_templates if custom_templates else PROMPT_TEMPLATES
        if not all([api_key, provider, model_config]):
            raise ValueError("缺少必要的配置信息")
            
        self.client = create_ai_client(provider, api_key, model_config)
        self.provider = provider
        self.model_config = model_config
        
    def analyze(self, image_path):
        """执行完整的安全分析流程"""
        # 初始化性能统计
        stats = {
            "start_time": datetime.now(),
            "file_size": os.path.getsize(image_path),
            "image_dimensions": None,
            "api_calls": [],
            "provider_info": {
                "provider": self.provider,
                "model": self.model_config["id"]
            }
        }
        
        try:
            # 验证图片
            validate_image(image_path)
            with Image.open(image_path) as img:
                stats["image_dimensions"] = img.size
            
            # 编码图片
            encode_start = time.time()
            image_base64 = encode_image(image_path)
            stats["encoding_time"] = time.time() - encode_start
            
            # 第一步：场景识别
            scene_start = time.time()
            scene_result = self.client.analyze_image(
                image_base64,
                self.templates["scene_recognition"]
            )
            scene_time = time.time() - scene_start
            stats["api_calls"].append({
                "type": "scene_recognition",
                "duration": scene_time
            })
            
            # 改进场景识别结果的判断逻辑
            is_construction_site = any([
                "是施工场景" in scene_result,
                "场景判定：[是]" in scene_result,
                "场景判定：是" in scene_result,
                "判定：是施工场景" in scene_result
            ])
            
            if is_construction_site:
                # 第二步：安全隐患分析
                safety_start = time.time()
                safety_result = self.client.analyze_image(
                    image_base64,
                    self.templates["safety_inspection"]
                )
                safety_time = time.time() - safety_start
                stats["api_calls"].append({
                    "type": "safety_inspection",
                    "duration": safety_time
                })
                
                result = {
                    "scene_recognition": scene_result,
                    "safety_inspection": safety_result
                }
            else:
                result = {
                    "scene_recognition": scene_result,
                    "message": "非施工场景，不进行安全隐患分析"
                }
            
            # 完成性能统计
            stats["end_time"] = datetime.now()
            stats["total_duration"] = (stats["end_time"] - stats["start_time"]).total_seconds()
            stats["bandwidth"] = stats["file_size"] / (stats["total_duration"] * 1024 * 1024)  # MB/s
            
            # 添加性能统计到结果中
            result["performance_stats"] = {
                "开始时间": stats["start_time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                "结束时间": stats["end_time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                "总耗时": f"{stats['total_duration']:.2f}秒",
                "图片大小": f"{stats['file_size'] / 1024:.2f}KB",
                "图片尺寸": f"{stats['image_dimensions'][0]}x{stats['image_dimensions'][1]}",
                "编码耗时": f"{stats['encoding_time']:.2f}秒",
                "带宽速度": f"{stats['bandwidth']:.2f}MB/s",
                "提供商信息": {
                    "名称": stats["provider_info"]["provider"],
                    "模型": stats["provider_info"]["model"]
                },
                "API调用详情": [
                    {
                        "类型": call["type"],
                        "耗时": f"{call['duration']:.2f}秒"
                    } for call in stats["api_calls"]
                ]
            }
            
            return result
                
        except Exception as e:
            stats["end_time"] = datetime.now()
            stats["total_duration"] = (stats["end_time"] - stats["start_time"]).total_seconds()
            return {
                "error": str(e),
                "performance_stats": {
                    "开始时间": stats["start_time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                    "结束时间": stats["end_time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                    "总耗时": f"{stats['total_duration']:.2f}秒",
                    "错误发生时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                    "提供商信息": {
                        "名称": stats["provider_info"]["provider"],
                        "模型": stats["provider_info"]["model"]
                    }
                }
            } 