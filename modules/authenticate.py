import streamlit as st
import pandas as pd
import jwt
import hashlib
from datetime import datetime, timedelta
import extra_streamlit_components as stx
from modules.database import Database
from streamlit_gallery import apps
from streamlit_gallery.utils.page import page_group

class Authenticate:
    def __init__(self, cookie_name: str, key: str, cookie_expiry_days: int=1):
        self.cookie_name = cookie_name
        self.key = key
        self.cookie_expiry_days = cookie_expiry_days
        self.cookie_manager = stx.CookieManager()
        self.db = Database()
        
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'EmployeeName' not in st.session_state:
            st.session_state['EmployeeName'] = None
        if 'EmployeeID' not in st.session_state:
            st.session_state['EmployeeID'] = None
        if 'UserName' not in st.session_state:
            st.session_state['UserName'] = None
        if 'UserID' not in st.session_state:
            st.session_state['UserID'] = None
        if 'Logout' not in st.session_state:
            st.session_state['Logout'] = None
    
    def _token_encode(self) -> str:        
        return jwt.encode(
            {
                'EmployeeName':st.session_state['EmployeeName'],
                'EmployeeID':st.session_state['EmployeeID'],
                'UserName':st.session_state['UserName'],
                'UserID':st.session_state['UserID'],
                'exp_date':self.exp_date
            }
            , self.key
            , algorithm='HS256')

    def _token_decode(self) -> str:        
        try:
            return jwt.decode(self.token, self.key, algorithms=['HS256'])
        except:
            return False

    def _set_exp_date(self) -> str:
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()

    def _check_cookie(self):        
        self.token = self.cookie_manager.get(self.cookie_name)
        if self.token is not None:
            self.token = self._token_decode()
            if self.token is not False:
                if not st.session_state['Logout']:
                    if self.token['exp_date'] > datetime.utcnow().timestamp():
                        if 'EmployeeName' and 'UserName' in self.token:
                            st.session_state['EmployeeName'] = self.token['EmployeeName']
                            st.session_state['EmployeeID'] = self.token['EmployeeID']
                            st.session_state['UserName'] = self.token['UserName']
                            st.session_state['UserID'] = self.token['UserID']
                            st.session_state['authentication_status'] = True

    def _check_credentials(self, inplace: bool=True) -> bool:        
        hash_object = hashlib.md5(self.password.encode())
        hashed_pass = hash_object.hexdigest()
        query = f"EXEC USP_KIDS_LOGIN '{self.username}','{hashed_pass}'" 

        result = self.db.run_query(self.db,query)
        if not result.empty:
            try:
                if inplace:
                    st.session_state['UserID'] = result.at[0, 'UserID']
                    st.session_state['UserName'] = result.at[0, 'UserName']
                    st.session_state['EmployeeID'] = result.at[0, 'EmployeeID']
                    st.session_state['EmployeeName'] = result.at[0, 'EmployeeName']
                    self.exp_date = self._set_exp_date()
                    self.token = self._token_encode()
                    self.cookie_manager.set(self.cookie_name, self.token,
                        expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
                    st.session_state['authentication_status'] = True
                    st.session_state['Logout'] = False
                    st.cache_data.clear()                    

                else:
                    return True
            except Exception as e:
                print(e)
        else:
            if inplace:
                st.session_state['authentication_status'] = False
            else:
                return False
    
    def login(self, form_name: str, location: str='main') -> tuple:
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if not st.session_state['authentication_status']:
            self._check_cookie()
            if st.session_state['authentication_status'] != True:
                if location == 'main':
                    login_form = st.form('Login')                        
                elif location == 'sidebar':
                    login_form = st.sidebar.form('Login')

                login_form.subheader(form_name)
                self.username = login_form.text_input('Username').lower()
                st.session_state['UserName'] = self.username
                self.password = login_form.text_input('Password', type='password')

                if login_form.form_submit_button('Login'):
                    self._check_credentials()

        return st.session_state['EmployeeName'],st.session_state['EmployeeID'], st.session_state['UserName'],st.session_state['UserID'], st.session_state['authentication_status'],st.session_state['Logout']

    def logout(self, button_name: str, location: str='main'):
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            if st.button(button_name):
                self.cookie_manager.delete(self.cookie_name)
                st.cache_data.clear()
                st.session_state.clear()
                st.session_state['Logout'] = True
                st.session_state['authentication_status'] = False
                st.session_state['UserID'] = None
                st.session_state['UserName'] = None
                st.session_state['EmployeeID'] = None
                st.session_state['EmployeeName'] = None
                
                
        elif location == 'sidebar':
            if st.sidebar.button(button_name):
                self.cookie_manager.delete(self.cookie_name)
                st.cache_data.clear()
                st.session_state.clear()
                st.session_state['Logout'] = True
                st.session_state['authentication_status'] = False
                st.session_state['UserID'] = None
                st.session_state['UserName'] = None
                st.session_state['EmployeeID'] = None
                st.session_state['EmployeeName'] = None
                        
    def sidebar(self):
        query = f"EXEC USP_KIDS_PermissionLeftMenu '{st.session_state['UserID']}'"
        result = self.db.run_query(self.db,query)
        st.sidebar.title(":chart_with_upwards_trend: **KIDSPLAZA**")
        st.sidebar.title(f":sparkler: Welcome {st.session_state['EmployeeName']} :tada:")
        if not result.empty:
            page = page_group("p")
        
            with st.sidebar:
                page.item(":house: Home", apps.Home, default=True)
                with st.expander("✨ COMPONENTS", False):
                    if 'StreamlitComponents' in result['PageName'].values:
                        page.item(":closed_book: Streamlit components", apps.gallery, default=False)
                    if 'ChartComponents' in result['PageName'].values:
                        page.item(":rainbow: Chart components", apps.ChartComponents, default=False)                    

                with st.expander("🧩 REPORTS", False):
                    if 'DoanhSoTheoNganh' in result['PageName'].values:
                        page.item(":bar_chart: Doanh Số Theo Ngành", apps.DoanhSoTheoNganh, default=False)
            page.show()

                

