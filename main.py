import streamlit as st
from modules.authenticate import Authenticate
from logger import get_logger

def main():      
    # Style
    with open('css/style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    with open('css/bootstrap.min.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
        
    authenticator = Authenticate('StreamlitApp','gooner4ver')
    EmployeeName,EmployeeID,UserName,UserID, authentication_status,Logout = authenticator.login("Đăng nhập", "main")

    if authentication_status == False:
        st.error("Tên đăng nhập hoặc mật khẩu chưa chính xác")

    if authentication_status == None:
        st.warning("Điền tên đăng nhập và mật khẩu của bạn")

    if authentication_status:        
        authenticator.sidebar()
        authenticator.logout("Đăng xuất", "sidebar")    
    
if __name__ == "__main__":
    try:
        logger = get_logger(__name__)
        st.set_page_config(page_title="Streamlit Gallery by Okld", page_icon="🎈", layout="wide")
        main()
    except Exception as e:
        # Print the exception message
        logger.error(f'An error occurred: {e}')

