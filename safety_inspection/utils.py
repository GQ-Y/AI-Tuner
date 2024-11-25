import base64
from PIL import Image
import os

def encode_image(image_path):
    """将图片转换为base64编码"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        raise Exception(f"图片编码失败: {str(e)}")

def validate_image(image_path):
    """验证图片是否有效且符合要求"""
    try:
        with Image.open(image_path) as img:
            # 检查图片大小
            if img.size[0] < 100 or img.size[1] < 100:
                raise ValueError("图片尺寸太小")
            # 检查文件大小
            if os.path.getsize(image_path) > 10 * 1024 * 1024:  # 10MB
                raise ValueError("图片文件太大")
            return True
    except Exception as e:
        raise Exception(f"图片验证失败: {str(e)}") 