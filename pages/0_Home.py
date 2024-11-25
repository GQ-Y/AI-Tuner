import streamlit as st
from safety_inspection.page_config import setup_page_config
from safety_inspection.analyzer import SafetyAnalyzer
from safety_inspection.config import PROMPT_TEMPLATES, PROVIDERS, load_config
import os

def save_uploaded_file(uploaded_file):
    """保存上传的文件并返回路径"""
    try:
        # 创建临时目录
        if not os.path.exists("safety_inspection/temp"):
            os.makedirs("safety_inspection/temp")
        
        # 保存文件
        file_path = os.path.join("safety_inspection/temp", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"文件保存失败: {str(e)}")
        return None

def main():
    setup_page_config()
    
    # 加载配置
    config = load_config()
    
    # 检查是否已设置API密钥
    if not config["selected_provider"] or not config["api_keys"].get(config["selected_provider"]):
        st.warning("请先在设置页面配置API密钥")
        if st.button("前往设置"):
            st.switch_page("pages/1_Settings.py")
        st.stop()
    
    # 标题
    st.title("施工安全隐患分析")
    
    # 创建两列布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("图片上传")
        # 多图片上传
        uploaded_files = st.file_uploader(
            "上传图片进行分析（可多选）", 
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True
        )
        
        # 提示词自定义
        st.subheader("提示词设置（可选）")
        
        # 使用expander来节省空间
        with st.expander("场景识别提示词"):
            scene_prompt = st.text_area(
                "场景识别提示词",
                PROMPT_TEMPLATES["scene_recognition"],
                height=300
            )
            
        with st.expander("安全检查提示词"):
            safety_prompt = st.text_area(
                "安全检查提示词",
                PROMPT_TEMPLATES["safety_inspection"],
                height=300
            )
        
        # 分析按钮
        analyze_button = st.button(
            "开始分析",
            disabled=not uploaded_files  # 没有文件时禁用按钮
        )
        
    with col2:
        st.subheader("分析结果")
        
        if uploaded_files and analyze_button:
            # 更新提示词模板
            custom_templates = {
                "scene_recognition": scene_prompt,
                "safety_inspection": safety_prompt
            }
            
            # 获取选中的模型配置
            provider = config["selected_provider"]
            model = config["selected_model"]
            model_config = PROVIDERS[provider]["models"][model]
            
            # 创建分析器实例
            analyzer = SafetyAnalyzer(
                custom_templates,
                api_key=config["api_keys"][provider],
                provider=provider,
                model_config=model_config
            )
            
            # 遍历处理每张图片
            for idx, uploaded_file in enumerate(uploaded_files, 1):
                try:
                    # 使用markdown创建视觉分隔
                    st.markdown(f"### 图片 {idx}: {uploaded_file.name}")
                    
                    # 显示当前图片
                    st.image(uploaded_file, caption=f"图片 {idx}", use_container_width=True)
                    
                    # 保存上传的文件
                    file_path = save_uploaded_file(uploaded_file)
                    
                    if file_path:
                        # 显示进度条
                        with st.spinner(f"正在分析图片 {idx}..."):
                            # 执行分析
                            result = analyzer.analyze(file_path)
                            
                            # 删除临时文件
                            os.remove(file_path)
                            
                            # 显示结果
                            if "error" in result:
                                st.error(f"分析失败: {result['error']}")
                            else:
                                st.success("分析完成！")
                                
                                # 使用tabs来组织结果显示
                                tab1, tab2, tab3 = st.tabs(["场景识别结果", "安全隐患分析结果", "性能统计"])
                                
                                with tab1:
                                    st.markdown("#### 场景识别结果")
                                    st.write(result["scene_recognition"])
                                
                                with tab2:
                                    st.markdown("#### 安全隐患分析结果")
                                    if "safety_inspection" in result:
                                        st.write(result["safety_inspection"])
                                    else:
                                        st.info(result["message"])
                                
                                with tab3:
                                    st.markdown("#### 性能统计信息")
                                    if "performance_stats" in result:
                                        stats = result["performance_stats"]
                                        
                                        # 添加模型信息
                                        st.markdown("##### 模型信息")
                                        st.json({
                                            "模型名称": model,
                                            "模型ID": model_config["id"],
                                            "提供商": provider
                                        })
                                        
                                        # 使用列布局展示关键指标
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("总耗时", stats["总耗时"])
                                            st.metric("编码耗时", stats["编码耗时"])
                                        with col2:
                                            st.metric("图片大小", stats["图片大小"])
                                            st.metric("图片尺寸", stats["图片尺寸"])
                                        with col3:
                                            st.metric("带宽速度", stats["带宽速度"])
                                        
                                        # 时间信息
                                        st.markdown("##### 详细时间信息")
                                        st.text(f"开始时间: {stats['开始时间']}")
                                        st.text(f"结束时间: {stats['结束时间']}")
                                        
                                        # API调用详情
                                        st.markdown("##### API调用详情")
                                        for call in stats["API调用详情"]:
                                            st.text(f"{call['类型']}: {call['耗时']}")
                                    
                except Exception as e:
                    st.error(f"处理图片 {idx} 时出现错误: {str(e)}")
                
                # 添加分隔线
                if idx < len(uploaded_files):
                    st.markdown("---")
        else:
            st.info("请上传图片并点击分析按钮开始分析")

if __name__ == "__main__":
    main() 