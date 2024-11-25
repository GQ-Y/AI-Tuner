# 施工安全隐患分析系统 V3.0

一个基于多种 AI 大模型的施工现场安全隐患智能分析系统，支持多种 AI 提供商的图像分析能力。

## 功能特点

### 1. 多模型支持
- 智谱 AI（GLM-4V, GLM-3V）
- 通义千问（Qwen-VL-Plus, Qwen-VL-Max）
- Anthropic（Claude-3-Opus, Claude-3-Sonnet）
- Mistral AI（自定义智能体）

### 2. 核心功能
- 🔍 施工场景智能识别
- ⚠️ 安全隐患自动分析
- 📊 详细的性能统计
- 🖼️ 支持批量图片处理
- ⚙️ 可自定义分析提示词

### 3. 界面特性
- 清晰直观的用户界面
- 实时分析进度显示
- 多标签页结果展示
- 便捷的设置管理

## 安装说明

### 1. 环境要求
- Python 3.9 或更高版本
- pip 包管理器

### 2. 安装步骤
```bash
# 克隆项目
git clone https://github.com/yourusername/construction-safety-analysis.git
cd construction-safety-analysis

# 创建虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 依赖包列表
```txt
streamlit>=1.24.0
pillow>=9.0.0
zhipuai>=2.0.0
dashscope>=1.0.0
anthropic>=0.5.0
mistralai>=0.0.7
requests>=2.28.0
```

## 使用说明

### 1. 启动系统
```bash
streamlit run Home.py
```

### 2. 配置步骤
1. 点击左侧菜单中的"设置"
2. 选择 AI 提供商
3. 选择对应的模型
4. 输入 API 密钥
5. 保存设置

### 3. 开始分析
1. 点击首页的"开始使用"或左侧菜单的"首页"
2. 上传一张或多张图片
3. 可选择自定义提示词
4. 点击"开始分析"
5. 查看分析结果

### 4. 分析结果说明
分析结果包含三个部分：
1. 场景识别结果
   - 场景判定（是/否施工场景）
   - 满足的判定项
   - 判定可信度
   - 判定依据
2. 安全隐患分析结果（如果是施工场景）
   - 发现的隐患
   - 违反的规范
   - 风险等级
   - 整改建议
   - 时限要求
3. 性能统计信息
   - 处理时间
   - 资源使用情况
   - API调用详情
   - 带宽速度

## 项目结构
```
construction-safety-analysis/
├── Home.py                    # 主页
├── pages/                     # 页面目录
│   ├── 0_Home.py             # 分析主页
│   ├── 1_Settings.py         # 设置页面
│   └── 2_Help.py             # 帮助页面
├── safety_inspection/         # 核心代码包
│   ├── __init__.py
│   ├── analyzer.py           # 分析器核心
│   ├── config.py             # 配置管理
│   ├── utils.py              # 工具函数
│   ├── page_config.py        # 页面配置
│   └── api_clients/          # API客户端
│       ├── __init__.py
│       ├── zhipu_client.py
│       ├── dashscope_client.py
│       ├── anthropic_client.py
│       └── mistral_client.py
└── requirements.txt          # 依赖清单
```

## 配置文件说明
系统配置保存在 `safety_inspection/data/config.json` 中，包含：
- API 密钥
- 选中的提供商
- 选中的模型

## 提示词模板
系统包含两个核心提示词模板：
1. 场景识别提示词
   - 基础要素检查（人员、场地、设备、标识）
   - 场景分析要求
   - 判定标准和输出格式
2. 安全检查提示词
   - 作业环境安全检查
   - 人员安全规范
   - 机械设备安全
   - 材料堆放和现场管理
   - 风险评估和建议

## 性能优化
1. 图片处理优化
   - 图片大小限制：10MB
   - 最小尺寸要求：100x100
   - 支持格式：JPG、JPEG、PNG
2. API调用优化
   - 请求超时设置
   - 错误重试机制
   - 详细的错误信息

## 注意事项
1. API密钥安全
   - 密钥保存在本地配置文件中
   - 请勿泄露或分享密钥
2. 图片要求
   - 清晰的施工现场照片
   - 合适的拍摄角度
   - 足够的光线条件
3. 使用建议
   - 建议使用支持多模态的模型
   - 可以适当调整提示词
   - 批量处理时注意图片数量

## 常见问题解决
1. API调用失败
   - 检查API密钥是否正确
   - 确认网络连接状态
   - 查看具体错误信息
2. 图片处理问题
   - 确保图片格式正确
   - 检查图片大小是否合适
   - 验证图片是否损坏
3. 分析结果问题
   - 检查提示词设置
   - 确认模型选择是否合适
   - 查看完整的错误日志

## 联系支持
- 邮件：1959595510@qq.com
- 电话：18181630321

## 版本历史
- V3.0: 增加多模型支持，优化界面交互
- V2.0: 添加批量处理功能，增加性能统计
- V1.0: 基础功能实现

## 许可证
MIT License

## 贡献指南
欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 致谢
感谢以下 AI 提供商的支持：
- 智谱 AI
- 通义千问
- Anthropic
- Mistral AI