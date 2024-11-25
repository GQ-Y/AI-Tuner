import streamlit as st
from safety_inspection.page_config import setup_page_config
from safety_inspection.config import PROVIDERS, load_config, save_config

def save_settings(provider, model, api_key):
    """保存设置到配置文件"""
    config = load_config()
    config["api_keys"][provider] = api_key
    config["selected_provider"] = provider
    config["selected_model"] = model
    
    if save_config(config):
        st.session_state.api_key = api_key
        st.session_state.selected_provider = provider
        st.session_state.selected_model = model
        st.success("设置已保存！")
    else:
        st.error("设置保存失败！")

def main():
    setup_page_config()
    
    st.title("系统设置")
    
    # 加载已保存的配置
    config = load_config()
    
    # 初始化session state
    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = config.get("selected_provider", "")
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = config.get("selected_model", "")
    if "current_provider" not in st.session_state:
        st.session_state.current_provider = st.session_state.selected_provider
    
    # 创建设置表单
    with st.form("settings_form"):
        # 提供商选择
        provider = st.selectbox(
            "选择AI提供商",
            options=list(PROVIDERS.keys()),
            index=list(PROVIDERS.keys()).index(st.session_state.selected_provider) if st.session_state.selected_provider in PROVIDERS else 0,
            help="请选择AI服务提供商",
            key="provider_select"
        )
        
        # 检查提供商是否改变
        provider_changed = provider != st.session_state.current_provider
        st.session_state.current_provider = provider
        
        # 显示提供商信息
        if provider:
            provider_info = PROVIDERS[provider]
            st.markdown(f"""
            **API密钥格式**: `{provider_info['api_key_format']}`  
            **官方网站**: [{provider}]({provider_info['website']})
            """)
        
        # 模型选择
        available_models = list(PROVIDERS[provider]["models"].keys())
        default_model_index = 0
        if not provider_changed and st.session_state.selected_model in available_models:
            default_model_index = available_models.index(st.session_state.selected_model)
            
        model = st.selectbox(
            "选择模型",
            options=available_models,
            index=default_model_index,
            help="请选择要使用的AI模型",
            key=f"model_select_{provider}"  # 为每个提供商使用不同的key
        )
        
        # API密钥输入
        # 如果提供商改变，使用新提供商的保存密钥（如果有）
        saved_api_key = config["api_keys"].get(provider, "") if not provider_changed else ""
        api_key = st.text_input(
            "API密钥",
            value=saved_api_key,
            type="password",
            help=f"请输入{provider}的API密钥",
            key=f"api_key_{provider}"  # 为每个提供商使用不同的key
        )
        
        # 保存按钮
        submitted = st.form_submit_button("保存设置")
        
        if submitted:
            if not api_key:
                st.error("请输入API密钥")
            else:
                save_settings(provider, model, api_key)
    
    # 显示当前设置
    if config["selected_provider"] and config["selected_model"]:
        st.subheader("当前设置")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"当前提供商: {config['selected_provider']}")
            st.info(f"API密钥: {'*' * 20}")
            
        with col2:
            st.info(f"当前模型: {config['selected_model']}")
        
        # 显示模型详细信息
        current_model_info = PROVIDERS[config['selected_provider']]["models"][config['selected_model']]
        with st.expander("模型详细信息"):
            st.json({
                "模型ID": current_model_info["id"],
                "最大Token数": current_model_info["max_tokens"],
                "温度系数": current_model_info["temperature"],
                "提供商": config['selected_provider']
            })
        
        # 显示所有保存的API密钥
        with st.expander("已保存的API密钥"):
            for saved_provider, saved_key in config["api_keys"].items():
                st.text(f"{saved_provider}: {'*' * 20}")

if __name__ == "__main__":
    main() 