import streamlit as st

class Common:
    color_palette_1 = ['#0081C9','#FFC93C','#5BC0F8']
    color_palette_2 = ['#ffbe0b','#fb5607','#ff006e','#8338ec','#3a86ff','#70e000','#9d4edd']
    color_palette_3 = ['#9221ba','#4675ed','#1bcfd4','#61fc6c','#ddff00','#fb8f13','#fa2e00','#7a0402']    
    color_palette_3_blurred = ['#d3a2e5','#9db0e1','#a1dfe1','#caf8cd','#e8efbc','#f5d1a7','#d68870','#bf5553']
    color_palette_4 = ['#FFD700','#C0C0C0','#CD7F32']
    def format_number(x, n=3):
        if x >= 10**9 or x <= -10**9:
            return "{:,.{}f}T".format(x/10**9, n)
        elif x >= 10**6 or x <= -10**6:
            return "{:,.{}f}Tr".format(x/10**6, 0)
        else:
            return "{:,}".format(x)

    def format_number_from_string(x, n=3):
        x = float(x)
        if x >= 10**9 or x <= -10**9:
            return "{:,.{}f}T".format(x/10**9, n)
        elif x >= 10**6 or x <= -10**6:
            return "{:,.{}f}Tr".format(x/10**6, n)
        else:
            return "{:,}".format(x)

    def format_percentage(x, n=2):
        if x == 0:
            return "0%"
        else:
            return "{:.{}%}".format(x, n)

    def divide_number(value, valueType):
        if valueType == "B":
            return value / 10**9
        if valueType == "M":
            return value / 10**6
        if valueType == "T":
            return value / 10**3

    def value_to_markdown(value, formatvalue):
        if value > 0:
            return st.markdown("<span style='color:#5FC752'>&#x21E7; {}</span>".format(formatvalue), unsafe_allow_html=True)
        elif value < 0:
            return st.markdown("<span style='color:#ff2b2b'>&#x21E9; {}</span>".format(formatvalue), unsafe_allow_html=True)
        else:
            return st.markdown("<span>0</span>", unsafe_allow_html=True)

    def value_to_arrow(value, formatvalue):
        if value > 0:
            return "<p class='block-4-p-green'>&#x21E7; {}</p>".format(formatvalue)
        elif value < 0:
            return "<p class='block-4-p-red'>&#x21E9; {}</p>".format(formatvalue)
        else:
            return "<p class='block-4-p'>0%</p>"

    def list_pull(x, y, z):
        result = [0] * x
        result[y] = z
        return result
    
    def new_list_color(x, y, list_color, list_color_blur):
        new_list = [list_color_blur[i] if i != y else list_color[y] for i in range(x)]
        return new_list