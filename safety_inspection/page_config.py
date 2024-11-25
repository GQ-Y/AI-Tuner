import streamlit as st
import os

def get_current_page():
    """获取当前页面名称"""
    try:
        # 获取当前文件路径
        current_file = os.path.basename(__file__)
        # 如果是在pages目录下的文件
        if os.path.exists("pages"):
            for file in os.listdir("pages"):
                if file.endswith(".py"):
                    if os.path.abspath(f"pages/{file}") == os.path.abspath(current_file):
                        return file
        # 如果是主页
        if os.path.abspath("Home.py") == os.path.abspath(current_file):
            return "Home.py"
        return ""
    except:
        return ""

def setup_page_config():
    """设置页面配置"""
    st.set_page_config(
        page_title="施工安全隐患分析系统",
        page_icon="🏗️",
        layout="wide",
        menu_items={
            'Get Help': 'https://github.com/yourusername/your-repo',
            'Report a bug': "https://github.com/yourusername/your-repo/issues",
            'About': """
            # 施工安全隐患分析系统
            
            该系统使用AI技术自动识别施工现场安全隐患。
            
            版本: 1.0.0
            """
        }
    )
    
    # 自定义侧边栏
    # st.sidebar.image("path/to/your/logo.png", use_container_width=True)  # 可选：添加logo
    
    # 隐藏默认的导航菜单标题
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none}
            .stButton button {
                width: 100%;
                text-align: left;
                padding: 0.75rem 1rem;
                margin: 0.25rem 0;
            }
            .stButton button:hover {
                background-color: #f0f2f6;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # 添加自定义导航菜单标题
    st.sidebar.title("导航菜单")
    
    # 创建导航链接
    if st.sidebar.button("首页", use_container_width=True):
        st.switch_page("Home.py")
        
    if st.sidebar.button("设置", use_container_width=True):
        st.switch_page("pages/1_Settings.py")
        
    if st.sidebar.button("帮助文档", use_container_width=True):
        st.switch_page("pages/2_Help.py")
    
    # 添加版本信息到侧边栏底部
    st.sidebar.markdown("---")
    st.sidebar.caption("Version 2.0.0")