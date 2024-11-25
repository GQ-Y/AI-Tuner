import streamlit as st
from safety_inspection.page_config import setup_page_config

def main():
    setup_page_config()
    
    st.title("欢迎使用施工安全隐患分析系统V3.0")
    
    
    # 添加开始使用按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # 添加一些空间
        if st.button("📸 开始使用", use_container_width=True, type="primary"):
            st.switch_page("pages/0_Home.py")
            
    # 添加功能卡片
    st.markdown("<br>", unsafe_allow_html=True)  # 添加一些空间
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🔍 场景识别
        自动识别施工场景，包括：
        - 人员特征分析
        - 场地特征识别
        - 设备特征检测
        - 标识特征判断
        """)
        
    with col2:
        st.markdown("""
        #### ⚠️ 安全分析
        全面的安全隐患检查：
        - 作业环境安全
        - 人员操作规范
        - 设备使用安全
        - 现场管理评估
        """)
        
    with col3:
        st.markdown("""
        #### 📊 性能统计
        详细的分析报告：
        - 处理时间统计
        - 资源使用情况
        - API调用详情
        - 带宽速度分析
        """)

if __name__ == "__main__":
    main() 