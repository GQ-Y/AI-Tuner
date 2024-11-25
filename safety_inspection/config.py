import json
import os

# 配置文件路径
CONFIG_FILE = "safety_inspection/data/config.json"

# 支持的AI提供商和模型配置
PROVIDERS = {
    "智谱AI": {
        "models": {
            "GLM-4V": {
                "id": "glm-4v",
                "max_tokens": 2000,
                "temperature": 0.7,
            },
            "GLM-3V": {
                "id": "glm-3v",
                "max_tokens": 1500,
                "temperature": 0.7,
            }
        },
        "api_name": "zhipu",
        "api_key_format": "xxxxxxxx.xxxxxxxxxxxxx",
        "website": "https://open.bigmodel.cn/",
    },
    "通义千问": {
        "models": {
            "qwen-vl-plus": {
                "id": "qwen-vl-plus",
                "max_tokens": 2000,
                "temperature": 0.7,
            },
            "qwen-vl-max": {
                "id": "qwen-vl-max",
                "max_tokens": 2000,
                "temperature": 0.7,
            }
        },
        "api_name": "dashscope",
        "api_key_format": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "website": "https://dashscope.aliyun.com/",
    },
    "Anthropic": {
        "models": {
            "claude-3-opus": {
                "id": "claude-3-opus-20240229",
                "max_tokens": 4000,
                "temperature": 0.7,
            },
            "claude-3-sonnet": {
                "id": "claude-3-sonnet-20240229",
                "max_tokens": 4000,
                "temperature": 0.7,
            }
        },
        "api_name": "anthropic",
        "api_key_format": "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "website": "https://www.anthropic.com/",
    },
    "Mistral AI": {
        "models": {
            "Mistral Vision": {
                "id": "ag:5fbbe679:20241125:untitled-agent:841be5ce",
                "max_tokens": 4096,
                "temperature": 0.7,
                "vision": True
            }
        },
        "api_name": "mistral",
        "api_key_format": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "website": "https://console.mistral.ai/",
        "description": """
        Mistral AI提供多个系列的模型：
        - Vision：支持图像理解的自定义智能体
        """,
        "capabilities": {
            "multimodal": ["Mistral Vision"],
            "custom_agent": True
        }
    }
}

def load_config():
    """加载配置"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {"api_keys": {}, "selected_provider": "", "selected_model": ""}
    except Exception as e:
        print(f"加载配置失败: {str(e)}")
        return {"api_keys": {}, "selected_provider": "", "selected_model": ""}

def save_config(config):
    """保存配置"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"保存配置失败: {str(e)}")
        return False

# 提示词模板配置
PROMPT_TEMPLATES = {
    "scene_recognition": """
    请作为一位专业的施工安全检查员，仔细分析图片中的场景。请特别注意以下要点：

    1. 基础要素检查（满足任一大类即可判定为施工场景）：

    A. 人员特征：
    □ 作业人员着工作服
    □ 人员佩戴安全帽
    □ 人员正在进行施工作业

    B. 场地特征：
    □ 施工围挡/警示带/安全防护栏
    □ 裸露的地面/土方/沟槽
    □ 建筑材料堆放
    □ 临时设施搭建

    C. 设备特征：
    □ 施工机械设备（挖掘机、推土机等）
    □ 施工工具（铲子、钎子等）
    □ 临时用电设施

    D. 标识特征：
    □ 施工警示标志
    □ 安全提示牌
    □ 施工标识牌

    2. 场景分析要求：
    - 即使只拍到局部场景，也请基于可见要素进行综合判断
    - 考虑施工场景的动态性和连续性
    - 关注施工活动的直接和间接证据
    - 注意施工现场的典型环境特征

    3. 输出格式：
    场景判定：[是/否施工场景]
    满足的判定项：[按类别列举]
    判定可信度：[A-非常确信/B-比较确信/C-基本确信/D-不确定]
    判定依据：[详细说明观察到的特征和推理过程]
    补充说明：[如有特殊情况或需要补充的信息]
    """,
    
    "safety_inspection": """
    作为专业的安全检查员，请对该施工场景进行全面的安全隐患分析：

    1. 作业环境安全检查：
    □ 地面/基坑作业安全防护
    □ 临边防护设施规范性
    □ 施工区域隔离措施
    □ 照明和通风条件
    □ 临时用电安全
    □ 消防通道和应急通道

    2. 人员安全规范：
    □ 个人防护用品使用情况
       - 安全帽佩戴
       - 反光衣穿着
       - 其他防护装备
    □ 作业人员站位和操作方式
    □ 特种作业人员资质
    □ 现场人员数量管控

    3. 机械设备安全：
    □ 大型机械操作区域隔离
    □ 机械设备防护装置
    □ 设备运行状态
    □ 操作人员规范性

    4. 材料堆放和现场管理：
    □ 材料堆放规范性
    □ 工具摆放整齐度
    □ 现场卫生状况
    □ 临时设施稳固性

    5. 风险评估和建议：
    请详细说明：
    - 发现的具体隐患
    - 可能造成的后果
    - 违反的具体规范条款
    - 整改建议和措施
    - 整改时限要求

    6. 输出格式：
    发现的隐患：[分类详细描述]
    违反的规范：[具体条款]
    风险等级：[高/中/低，并说明理由]
    整改建议：[具体可执行的措施]
    时限要求：[立即/限期/长期]
    补充说明：[其他需要注意的事项]
    """
} 