import streamlit as st
from modules.database import Database
from modules.common import Common
from modules.components import Html
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from logger import get_logger


def main():         
    db = Database()
    st.write('# :bar_chart: Doanh Số Theo Ngành')      

    CHOICES = {1: "Mẹ bầu và sau sinh", 2: "Sữa bột, thực phẩm cho bé", 3: "Bỉm, tã cho bé", 4: "Đồ sơ sinh", 5: "Đồ dùng", 6: "Thời trang cho bé", 7: "Đồ chơi"}
    def format_func(option):
        return CHOICES[option]

    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        start_date = st.date_input("Từ ngày", value=datetime.now() - timedelta(days=2))

    with col2:
        end_date = st.date_input("Đến ngày", value=datetime.now() - timedelta(days=1))

    with col3:
        option = st.selectbox("Ngành cấp 1", options=list(CHOICES.keys()), format_func=format_func)

    with col4:
        btnSubmit = st.button("Xem báo cáo")

    if "start_date" not in st.session_state:
        st.session_state.start_date = start_date

    if "end_date" not in st.session_state:
        st.session_state.end_date = end_date

    if "option" not in st.session_state:
        st.session_state.option = option
    #Initialize session state
    if "load_state" not in st.session_state: 
        st.session_state.load_state = False
        
    if btnSubmit or st.session_state.load_state:
        st.session_state.load_state = True
        if btnSubmit:
            query = f"EXEC USP_KIDS_TEST '{start_date}','{end_date}','{option}'" 
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
            st.session_state.option = option        
        elif st.session_state.load_state:
            query = f"EXEC USP_KIDS_TEST '{st.session_state.start_date}','{st.session_state.end_date}','{st.session_state.option}'" 

        dataframes = db.run_query_multi_tables(db,query)
        #Design and visualize data
        df_0 = dataframes[0]
        df_1 = dataframes[1]
        df_2 = dataframes[2]
        df_3 = dataframes[3]
        df_4 = dataframes[4]

        cols_A = st.columns([3,2])
        with cols_A[0] :
            st.subheader(f'Tổng quan từ :blue[{st.session_state.start_date.strftime("%d/%m/%Y")}] đến :blue[{st.session_state.end_date.strftime("%d/%m/%Y")}]')
            cols_B = st.columns([1,1,1])
            with cols_B[0]:
                html = Html.html_block_4(
                    "Doanh Số"
                    ,Common.format_number(df_0.at[0, 'DoanhSoThangNay'])
                    ,Common.value_to_arrow(
                        df_0.at[0, 'TangTruongDoanhSoPercent']
                        ,Common.format_percentage(df_0.at[0, 'TangTruongDoanhSoPercent'])
                        )
                    ,Common.value_to_arrow(
                        df_0.at[0, 'TangTruongDoanhSo']
                        ,Common.format_number(df_0.at[0, 'TangTruongDoanhSo'])
                        )
                    )
                st.markdown(html, unsafe_allow_html=True)            
                
            with cols_B[1]:
                html = Html.html_block_4(
                    "Tổng LNG"
                    ,Common.format_number(df_0.at[0,'LNGThangNay'])
                    ,Common.value_to_arrow(
                        df_0.at[0, 'TangTruongLNGPercent']
                        ,Common.format_percentage(df_0.at[0, 'TangTruongLNGPercent']))
                    ,Common.value_to_arrow(
                        df_0.at[0, 'TangTruongLNG']
                        ,Common.format_number(df_0.at[0, 'TangTruongLNG']))
                    )
                st.markdown(html, unsafe_allow_html=True)           

            with cols_B[2]:
                html = Html.html_block_3(
                    "Tỷ suất LNG"
                    ,Common.format_percentage(df_0.at[0,'TyLeLNG'])
                    ,Common.value_to_arrow(
                        df_0.at[0, 'TangTruongTyLeLNGPercent']
                        ,Common.format_percentage(df_0.at[0,'TangTruongTyLeLNGPercent'])
                        )
                )
                st.markdown(html, unsafe_allow_html=True)

            st.write("")
            st.write("")
            st.write("")

            st.subheader('Ngành hàng :blue[{}]'.format(format_func(st.session_state.option)))
            cols_B = st.columns([1,1,1])
            with cols_B[0]:
                html = Html.html_block_4(
                    "Doanh Số"
                    ,Common.format_number(df_1.at[0, 'DoanhSoNganhThangNay'])
                    ,Common.value_to_arrow(
                        df_1.at[0, 'TangTruongDoanhSoPercent']
                        ,Common.format_percentage(df_1.at[0, 'TangTruongDoanhSoPercent'])
                        )
                    ,Common.value_to_arrow(
                        df_0.at[0, 'TangTruongDoanhSo']
                        ,Common.format_number(df_0.at[0, 'TangTruongDoanhSo']))
                    )
                st.markdown(html, unsafe_allow_html=True)   
            
            with cols_B[1]:
                html = Html.html_block_3(
                    "Tỷ trọng"
                    ,Common.format_percentage(df_1.at[0,'TyTrongDoanhSo'])
                    ,Common.value_to_arrow(
                        df_1.at[0, 'TangTruongTyTrong']
                        ,Common.format_percentage(df_1.at[0, 'TangTruongTyTrong'])
                        )
                )
                st.markdown(html, unsafe_allow_html=True)            

        with cols_A[1]:
            df_4['DoanhSo_divided'] = df_4['DoanhSoVAT'].apply(lambda x: Common.divide_number(x,"M"))            
            # Create the doughnut chart
            fig = px.pie(
                df_4, 
                height=300,                
                values='DoanhSo_divided', 
                names='Nganh', 
                #custom_data=['DoanhSo_formatted'],
                color='Nganh',
                title='Phân bố tỷ trọng các nhóm Ngành<br>Đơn vị : Triệu đồng, %',
                color_discrete_sequence=Common.new_list_color(7, st.session_state.option -1,Common.color_palette_3,Common.color_palette_3_blurred)
            )
            # Update the chart layout
            fig.update_layout(
                title_font=dict(size=15, color='black'),
                margin = dict(t=100, l=50, r=0, b=0),
                uniformtext_minsize=8, 
                uniformtext_mode='hide',
                showlegend=False,
                legend_title_text='Ngành',
                legend=dict(
                    orientation='v',
                    x=1.3,
                    y=1,
                    traceorder='normal',
                    font=dict(
                        family='sans-serif',
                        size=10,
                        color='black'
                    ),
                    bgcolor='white',
                    bordercolor='black',
                    borderwidth=0
                ),
                paper_bgcolor='white',
                plot_bgcolor='white',
            )
            fig.update_traces(
                sort=False,
                opacity=1,
                pull=Common.list_pull(7, st.session_state.option - 1, 0.1),                
                hole=.5,
                textinfo='percent+label+value',
                textfont_size=11, 
                textfont_color='black', 
                textposition='outside', 
                texttemplate='%{label}<br>%{value:,.0f} (%{percent})',
                hoverinfo='percent+label+value',
                hovertemplate ='Ngành : %{label}<br>Doanh số : %{value:,.0f} | Tỷ trọng : %{percent}',
            )
            st.plotly_chart(fig,use_container_width=True)

        st.write("")
        st.write("")
        st.subheader('Biểu đồ')
        cols = st.columns([1,1])        
        with cols[0]:        
            df_2['DoanhSoNganh'] = df_2['DoanhSoNganh'].apply(lambda x: Common.divide_number(x,"M"))   
            fig = go.Figure(            
                data=go.Bar(
                    x=df_2["Ngay"],
                    y=df_2["DoanhSoNganh"],
                    name="Doanh số {}".format(format_func(st.session_state.option)),
                    marker=dict(color="#1877F2"),
                )            
            )
            fig.add_trace(
                go.Scatter(
                    x=df_2["Ngay"],
                    y=df_2["TyTrongNganh"],
                    yaxis="y2",
                    name="Tỷ trọng (%)",
                    line=dict(width=2, color='#FFBE31'),
                    mode='markers+lines'
                )
            )
            fig.update_layout(
                title_text="Phân tích xu hướng {} theo ngày<br>Đơn vị: Triệu đồng | %".format(format_func(st.session_state.option)),            
                legend=dict(
                    orientation='h',
                    x=0,
                    y=-0.15
                ),
                showlegend=True,
                xaxis= dict(
                    tickformat='%d/%m',
                    tickmode='array',
                    tickvals=df_2["Ngay"].tolist(),
                    showgrid=False
                ), 
                yaxis=dict(
                    side="left",
                    showgrid=False,
                    tickformat= ',.0f',
                ),
                yaxis2=dict(
                    side="right",
                    overlaying="y",
                    tickformat= ',.0%',
                    rangemode = "tozero",
                    showgrid=False 
                ),   
                hovermode='x unified'          
            )
            st.plotly_chart(fig,use_container_width=True)
        with cols[1]:    
            df_3['DoanhSoNganh'] = df_3['DoanhSoNganh'].apply(lambda x: Common.divide_number(x,"M")) 
            fig = go.Figure(            
                data=go.Bar(
                    x=df_3["Thang"],
                    y=df_3["DoanhSoNganh"],
                    name="Doanh số {}".format(format_func(st.session_state.option)),
                    marker=dict(color="#1877F2"),
                )            
            )
            fig.add_trace(
                go.Scatter(
                    x=df_3["Thang"],
                    y=df_3["TyTrongNganh"],
                    yaxis="y2",
                    name="Tỷ trọng (%)",
                    line=dict(width=2, color='#FFBE31'),
                    mode='markers+lines'
                )
            )
            fig.update_layout(
                title_text="Phân tích xu hướng {} theo tháng<br>Đơn vị: Triệu đồng | %".format(format_func(st.session_state.option)),            
                legend=dict(
                    orientation='h',
                    x=0,
                    y=-0.15
                ),
                showlegend=True,
                xaxis= dict(
                    tickformat='%m/%y',
                    tickmode='array',
                    tickvals=df_3["Thang"].tolist(),
                    showgrid=False
                ),           
                yaxis=dict(
                    #title=dict(text="Total number of diners (millions)"),
                    side="left",
                    showgrid=False,
                    tickformat= ',.0f',
                ),
                yaxis2=dict(
                    #title=dict(text="Total bill amount"),
                    side="right",
                    overlaying="y",
                    tickformat= ',.0%',
                    rangemode = "tozero",
                    showgrid=False
                ),   
                hovermode='x unified' 
            )
            st.plotly_chart(fig,use_container_width=True)
    
        #st.dataframe(df_4)
        #st.dataframe(df_5)

if __name__ == "__main__":
    try:
        logger = get_logger(__name__)
        main()
    except Exception as e:
        # Print the exception message
        logger.error(f'An error occurred: {e}')
