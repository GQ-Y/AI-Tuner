import streamlit as st
from safety_inspection.page_config import setup_page_config

def main():
    setup_page_config()
    
    st.title("帮助文档")
    
    st.markdown("""
    ### 常见问题
    
    #### 1. 如何配置API密钥？
    在"设置"页面中输入您的API密钥并保存。
    
    #### 2. 支持哪些图片格式？
    支持 JPG、JPEG、PNG 格式的图片。
    
    #### 3. 如何批量分析图片？
    在分析页面可以一次选择多张图片进行上传分析。
    
    ### 联系支持
    
    如果您遇到问题或需要帮助，请通过以下方式联系我们：
    - 邮件：1959595510@qq.com
    - 电话：18181630321
    """)

if __name__ == "__main__":
    main() 