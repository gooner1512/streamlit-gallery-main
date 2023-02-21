import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_elements import elements,nivo, mui
from modules.common import Common
from logger import get_logger

def convert_df_to_dict(df, id_col, x_col, y_col):
    result = []
    for i, row in df.iterrows():
        id_value = row[id_col]
        x_value = str(row[x_col])
        y_value = row[y_col]
        data = {"x": x_value, "y": y_value}
        
        found = False
        for item in result:
            if item["id"] == id_value:
                item["data"].append(data)
                found = True
                break
        
        if not found:
            result.append({"id": id_value, "data": [data]})
    
    return result


def main():  
    df_line = px.data.gapminder().query("country in ['Vietnam', 'Thailand', 'Malaysia']")
    data_line = convert_df_to_dict(df_line, "country", "year", "gdpPercap")
    # Create sample data
    df = px.data.gapminder(year=2007)
    # Sum the population by continent
    df_sum = df.groupby('continent').sum(numeric_only=True)['pop']        
    # Reset the index and rename the columns
    df_sum = df_sum.reset_index().rename(columns={'pop': 'population'})
    df_sum['population_formatted'] = df_sum['population'].apply(lambda x: Common.format_number(x))
          

    st.header('**Plotly**')
    cols = st.columns([1,1])
    #Line chart
    with cols[0]:
        fig = px.line(df_line, x="year", y="gdpPercap"
            , text="country"
            , markers=True                        
            , line_shape='spline'#linear
            , color="country"
            , color_discrete_sequence=Common.color_palette_1
            #, line_dash='country'
            #, line_dash_sequence=['solid', 'dash', 'dot']
            #, symbol="country"
            #, symbol_sequence=['circle', 'square', 'diamond']
        )
        fig.update_traces(
            textposition="bottom right",
            mode="markers+lines", 
            hovertemplate = '<b>Quốc gia : %{text}</b><br><b>Năm : %{x}</b><br><b>GDP: %{y:$,.0f}</b><extra></extra>',
            hoverlabel=dict(
                align="left"
            )
        )
        fig.update_layout(
            title_text="GDP per Capita by Year"
            #,hovermode="x unified"
            ,legend=dict(
                    title='Quốc gia',
                    orientation='h',
                    x=0,
                    y=-0.15
            )
            ,showlegend=True
            ,xaxis= dict(
                title='Năm'
                ,showgrid=False
                ,tickmode='array'
                ,tickvals=df_line['year'].tolist()
                ,ticktext=df_line['year'].tolist()
                ,tickangle=0
                ,ticklen=5
                ,tickcolor='black'
                ,tickfont=dict(
                    size=12,
                    color='black'
                )
                ,layer='above traces'
            )
            ,yaxis=dict(
                title='GDP đầu người'
                ,side="left"
                ,showgrid=True
                ,tickformat=',.0f'
                ,tickfont=dict(
                    size=12,
                    color='black'
                )
            )

        )
        st.plotly_chart(fig,use_container_width=True)
    #Pie chart
    with cols[1]:        
        # Create the doughnut chart
        fig = px.pie(
            df_sum, 
            values='population', 
            names='continent', 
            custom_data=['population_formatted'],
            color='continent',
            title='Distribution of World Population by Continent in 2007',
            color_discrete_sequence=Common.color_palette_2,            
        )

        # Update the chart layout
        fig.update_layout(
            title_font=dict(size=17, color='black'),
            margin = dict(t=80, l=20, r=20, b=0),
            uniformtext_minsize=8, 
            uniformtext_mode='hide',
            legend_title_text='Continents',
            legend=dict(
                orientation='v',
                x=-0.3,
                y=0,
                traceorder='normal',
                font=dict(
                    family='sans-serif',
                    size=12,
                    color='black'
                ),
                bgcolor='white',
                bordercolor='black',
                borderwidth=0
            ),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        fig.update_traces(
            opacity=1,
            pull=Common.list_pull(7,1,0.1),
            domain={
                'y': [0, 1],
                'x': [0.05, 0.95]
            },
            hole=.5,
            textinfo='percent+label+value',
            textfont_size=13, 
            textfont_color='black', 
            textposition='outside', 
            texttemplate='%{label}<br>%{customdata[0]}<br>%{percent}',
            hoverinfo='percent+label+value',
            hovertemplate ='Continent : %{label}<br>Percent : %{percent}',
        )
        st.plotly_chart(fig,use_container_width=True)
    
    cols = st.columns([1,1])
    #Bar Stacked
    with cols[0]:
        long_df = px.data.medals_long()       
        # Create the stacked bar chart
        fig = px.bar(long_df, x='count', y='nation', color='medal'
            , barmode='stack'
            , color_discrete_sequence=Common.color_palette_4
            , orientation='h'
            )

        fig.update_traces(
            texttemplate='%{x}',
            textposition='inside',
            hovertemplate='<b>%{x}</b>',
            #text=long_df.groupby(['nation'])['count'].apply(lambda x: f"{x.name}<br>{x.sum()}")
        )

        annotations=[]
        for i, nation in enumerate(long_df['nation'].unique()):
            total = long_df[long_df['nation'] == nation]['count'].sum()
            annotations.append(dict(x=total + 4, y=i, text='Total: ' + str(total), showarrow=False, font=dict(color='black')))

        # Customize the chart by adding a title, axis labels, and grid lines
        fig.update_layout(
            title='Count of Medal by Nation',
            xaxis=dict(
                title='Count of Medal',
                tickfont=dict(size=10),
                showgrid=True, 
            ),
            yaxis=dict(
                title='Nations',
                showgrid=False, 
                gridwidth=0.5
            ),
            legend=dict(title='Medal'),
            paper_bgcolor='white',
            plot_bgcolor='white',
            hovermode='y unified',
            annotations=annotations,
        )
        st.plotly_chart(fig,use_container_width=True)
    #Bar and Line
    with cols[1]:
        # Load the gapminder data
        df_world = px.data.gapminder()

        # Filter the data to only include China
        df_china = df_world[df_world['country'] == 'China']

        # Group the data by year to get the total population of the world in each year
        df_grouped = df_world.groupby('year').sum(numeric_only=True).reset_index()

        # Merge the two DataFrames to get a DataFrame with year, population of China, and total population of the world in each year
        df_result = df_china.merge(df_grouped, on='year')        

        # Calculate the percentage of the total population represented by China's population
        df_result['percent'] = df_result['pop_x'] / df_result['pop_y']
        df_result['pop_x'] = df_result['pop_x'].apply(lambda x: Common.divide_number(x,"M"))   
        # Keep only the columns we're interested in
        df_result = df_result[['year', 'pop_x', 'percent']]

        # Rename the columns for clarity
        df_result = df_result.rename(columns={'pop_x': 'pop_china'})
        fig = go.Figure(            
            data=go.Bar(
                x=df_result["year"],
                y=df_result["pop_china"],
                name="Population",
                marker=dict(color="#1877F2"),
            )            
        )
        fig.add_trace(
            go.Scatter(
                x=df_result["year"],
                y=df_result["percent"],
                yaxis="y2",
                name="Percentage (%)",
                line=dict(width=2, color='#FFBE31'),
                mode='markers+lines'
            )
        )
        fig.update_layout(
            title_text="Population and percentage of China<br>(Millions | %)",            
            legend=dict(
                orientation='h',
                x=0,
                y=-0.15
            ),
            showlegend=True,
            xaxis= dict(
                title='Year'
                ,showgrid=False
                ,tickmode='array'
                ,tickvals=df_result["year"].tolist()
                ,ticktext=df_result["year"].tolist()
                ,tickangle=0
                ,ticklen=5
                ,tickcolor='black'
                ,tickfont=dict(
                    size=12,
                    color='black'
                )
                ,layer='above traces'
            ) ,
            yaxis=dict(
                side="left",
                showgrid=True,
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
        
    cols = st.columns([1])
    #Sankey
    with cols[0]:
        # Define the data for the Sankey diagram
        sankey_data = dict(
            type='sankey',
            node=dict(
                pad=15,
                thickness=20,
                line=dict(
                    color="black",
                    width=0
                ),
                label=["iPhone<br>$42.6B", "MacBook<br>$11.5B", "iPad<br>$7.2B", "Watch,AirPods<br>$9.7B", "Products<br>$71B"
                , "Services<br>$19.2B", "Revenue<br>$90.2B", "Gross profit<br>$38.1B", "Cost of revenue<br>$52.1B"
                , "Operating profit<br>$24.9B", "Operating expenses<br>$13.2B", "Net profit<br>$20.7B", "Tax<br>$3.9B", "Other<br>$0.2B", "R&D<br>$6.8B", "SG&A<br>$6.4B", "Products Cost<br>$46.4B", "Services Cost<br>$5.7B"],         
                x = [0.1, 0.1, 0.1, 0.1, 0.28, 0.2, 0.45, 0.6, 0.6, 0.75, 0.75, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.7],
                y = [0.05, 0.35, 0.7, 0.9, 0.3, 1.1, 0.55, 0.2, 0.85, 0.05, 0.4, -0.1, 0.3, 0.4, 0.6, 0.8, 0.9, 1.2],
                color=['#0063c7','#0063c7','#0063c7','#0063c7','#0063c7','#0063c7','#0063c7','#00cc07','#fa2e00','#00cc07','#fa2e00','#00cc07','#fa2e00','#fa2e00','#fa2e00','#fa2e00','#fa2e00','#fa2e00'],
                hovertemplate='%{label}<extra></extra>'
            ),
            link=dict(
                source=[0, 1, 2, 3, 4, 5, 6, 6, 7, 7, 9, 9, 9, 10, 10, 8, 8],
                target=[4, 4, 4, 4, 6, 6, 7 ,8, 9, 10, 11, 12, 13, 14, 15, 16, 17] ,
                value=[42.6, 11.5, 7.2, 9.7, 71.0, 19.2, 38.1, 52.1, 24.9, 13.2, 20.7, 3.9, 0.2, 6.8, 6.4, 46.4, 5.7],
                color=['#99c7ff','#99c7ff','#99c7ff','#99c7ff','#99c7ff','#99c7ff','#ccffcf','#ffac99','#ccffcf','#ffac99','#ccffcf','#ffac99','#ffac99','#ffac99','#ffac99','#ffac99','#ffac99'],
                hovertemplate='source:%{source.label}<br>target:%{target.label}<extra></extra>',
            )
        )
        # Define the layout for the Sankey diagram
        layout = dict(
            title="Apple Q4 FY2022 Income Statement", 
            font=dict(size=12),
            title_font=dict(size=16),              
        )

        # Create the figure and plot the data
        fig = dict(data=[sankey_data], layout=layout)
        
        st.plotly_chart(fig,use_container_width=True)

    cols = st.columns([1])
    #Heatmap
    with cols[0]:
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hours_of_day = [22, 23, 0, 1] * 7 + [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] * 7

        visitor_1 = [np.random.randint(1000, 6000) for i in range(24 * 7 - 4 * 7)]
        visitor_2 = [np.random.randint(6000, 10000) for i in range(4 * 7)]
        visitor = visitor_2 + visitor_1

        df_visitor = pd.DataFrame({'day_of_week': np.tile(days_of_week, 24),
                        'hour_of_day': hours_of_day,
                        'visitor': visitor})
        fig = px.density_heatmap(
            df_visitor, 
            x='hour_of_day', 
            y='day_of_week', 
            z='visitor',
            nbinsx=24, 
            nbinsy=7,
            title='Density Heatmap of Visitor Counts by Hour and Day',
            text_auto=False
        )
        fig.update_layout(
            xaxis=dict(
                tickmode='linear', 
                tick0=0, 
                dtick=1,
                title='Hour of Day',
            ),
            yaxis=dict(
                tickmode='linear', 
                title='Day of Week'
            )
        )
        st.plotly_chart(fig,use_container_width=True)

    cols = st.columns([1])
    #Animation Bubble
    with cols[0]:
        df_bubble = px.data.gapminder()
        fig = px.scatter(
            df_bubble, 
            x="gdpPercap", 
            y="lifeExp", 
            animation_frame="year", 
            animation_group="country",
            size="pop", 
            color="continent", 
            color_discrete_sequence=['#fa2e00','#4675ed','black','#FFC93C','#70e000'],
            hover_name="country",
            custom_data=["country","pop","year","continent"],
            log_x=True, 
            size_max=55, 
            range_x=[100,100000], 
            range_y=[25,90]
        )
        fig.update_traces(
            hovertemplate='<b>%{customdata[3]} | %{customdata[0]}</b><br>Year: %{customdata[2]}<br>Population: %{customdata[1]:,.0f}<br>GDP per cap: $%{x:,.0f}<br>Life Exp: %{y:.1f}<extra></extra>',
        )
        fig.update_layout(
            title_text="Populations, Life exp and GDP per cap by Year and Country"
            #,hovermode="x unified"
            ,legend=dict(
                    title='Continents',
                    orientation='v',
                    x=1,
                    y=1
            )
            ,showlegend=True
            ,xaxis= dict(
                title='GDP per cap'
                ,showgrid=False
                ,tickmode='array'
                ,tickangle=0
                ,ticklen=5
                ,tickcolor='black'
                ,tickfont=dict(
                    size=12,
                    color='black'
                )
                ,layer='above traces'
            )
            ,yaxis=dict(
                title='Life Exp'
                ,side="left"
                ,showgrid=True
                #,tickformat=',.0f'
                ,tickfont=dict(
                    size=12,
                    color='black'
                )
            )

        )
        
        config = {'displaylogo': False}
        #fig.show(config=config)
        st.plotly_chart(fig,use_container_width=True)

    cols = st.columns([1])    
    #Radar
    with cols[0]:
        # Define the data for Messi and Ronaldo's statistics
        data_siro = {
            'Name': ['Store A', 'Store B'],
            'Doanh Số': np.random.randint(1, 20, size=2),
            '% Đạt Mục Tiêu': np.random.randint(1, 50, size=2),
            'GTTB Đơn': np.random.randint(1, 50, size=2),
            'Chiết khấu': np.random.randint(1, 50, size=2),
            'Tỷ trọng NH Xanh': np.random.randint(1, 50, size=2),
            'Tỷ trọng NH Vàng': np.random.randint(1, 50, size=2),
            'Khách hàng mới': np.random.randint(1, 20, size=2)
        }
        df_siro = pd.DataFrame(data_siro)

        # Create subplots with shared polar axis
        fig = make_subplots(rows=1, cols=2, subplot_titles=df_siro['Name'], specs=[[{'type': 'polar'}]*2])
        

        # Loop through each row in the DataFrame and create a trace for each player
        for i, row in df_siro.iterrows():
            fig.add_trace(
                go.Scatterpolar(
                    r=row[1:],
                    theta=df_siro.columns[1:],
                    fill='toself',
                    name=row['Name'],
                    line=dict(color=Common.color_palette_2[i]),
                    hovertemplate='%{theta}<br>Xếp hạng: %{r}<extra></extra>'
                ),
                row=1,
                col=i+1
            )
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[100, 1],
                    tickvals=[100,80,60,40,20]
                )
            ),
            polar2=dict(
                radialaxis=dict(
                    visible=True,
                    range=[100, 1],
                    tickvals=[100,80,60,40,20]
                )
            ),
            showlegend=True
        )
            
        
        st.plotly_chart(fig,use_container_width=True)    
        
    st.header('**Nivo**')
    cols = st.columns([1,1])   
    
    with cols[0]:        
        with elements("nivo_line_chart"):            
            with mui.Box(sx={"height": 400}):
                st.write('GDP đầu người theo Năm')
                nivo.Line(
                    data=data_line,
                    theme="light",
                    margin={"top": 10, "right": 15, "bottom": 60, "left": 60},
                    lineWidth=2,
                    curve="monotoneX",
                    colors=Common.color_palette_1,
                    axisTop=None,
                    axisRight=None,
                    enableGridX=False,
                    enableGridY=True,
                    axisBottom={
                        "orient": "bottom", 
                        "tickSize": 5, 
                        "tickPadding": 5, 
                        "tickRotation": 0, 
                        "legend": "Năm", 
                        "legendOffset": 36, 
                        },
                    axisLeft={
                        "orient": "left", 
                        "tickSize": 5, 
                        "tickPadding": 5, 
                        "tickRotation": 0, 
                        "legend": "GDP đầu người", 
                        "legendOffset": -45,
                        "format": ",.0f"},
                    yFormat=">-$,.0f",
                    enableSlices='x',
                    enablePointLabel=False,
                    pointSize=4,
                    pointBorderWidth=2,
                    pointBorderColor={"from": "serieColor"},
                    pointLabel="y",
                    pointLabelYOffset=-12,
                    useMesh=True,
                    legends=[
                        {
                            "anchor": "bottom",
                            "direction": "row",
                            "justify": False,
                            "translateX": 0,
                            "translateY": 56,
                            "itemsSpacing": 0,
                            "itemWidth": 100,
                            "itemHeight": 18,
                            "itemTextColor": "#999",
                            "itemDirection": "left-to-right",
                            "itemOpacity": 1,
                            "symbolSize": 18,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ]
                )
    
    with cols[1]:
        data = df_sum.to_dict('records')
        DEFAULT_DATA = [{"id": record['continent'], "label": record['continent'],
                  "value": record['population'], "formatted":record['population_formatted']} for record in data]
        with elements("nivo_bar_charts"):
            with mui.Box(sx={"flex": 1, "minHeight": 0, "height": 400}):
                st.write('**Distribution of World Population by Continent in 2007**')
                nivo.Pie(
                    data=DEFAULT_DATA,
                    isInteractive=True,
                    theme="light",
                    margin={ "top": 30, "right": 20, "bottom": 60, "left": 20 },
                    innerRadius=0.5,
                    padAngle=1.25,
                    cornerRadius=3,
                    colors=Common.color_palette_2,                    
                    sortByValue = True,
                    borderWidth=1,
                    borderColor={
                        "from": "color",
                        "modifiers": [
                            [
                                "darker",
                                0.2,
                            ]
                        ]
                    },
                    activeInnerRadiusOffset=4,
                    activeOuterRadiusOffset=8,
                    valueFormat='>-.4s',
                    enableArcLabels=True,
                    arcLabel='formattedValue',
                    arcLabelsRadiusOffset=0.5,
                    arcLinkLabel='id',
                    arcLinkLabelsSkipAngle=0,
                    arcLinkLabelsTextColor="grey",
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsDiagonalLength=16,
                    arcLinkLabelsStraightLength=24,
                    arcLinkLabelsTextOffset=6,
                    arcLinkLabelsColor={ "from": "color" },
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor={
                        "from": "color",
                        "modifiers": [
                            [
                                "darker",
                                2
                            ]
                        ]
                    },
                    defs=[
                        {
                            "id": "dots",
                            "type": "patternDots",
                            "background": "inherit",
                            "color": "rgba(255, 255, 255, 0.3)",
                            "size": 4,
                            "padding": 1,
                            "stagger": True
                        },
                        {
                            "id": "lines",
                            "type": "patternLines",
                            "background": "inherit",
                            "color": "rgba(255, 255, 255, 0.3)",
                            "rotation": -45,
                            "lineWidth": 6,
                            "spacing": 10
                        }
                    ],                    
                    legends=[
                        {
                            "anchor": "bottom",
                            "direction": "row",
                            "justify": False,
                            "translateX": 0,
                            "translateY": 56,
                            "itemsSpacing": 0,
                            "itemWidth": 100,
                            "itemHeight": 18,
                            "itemTextColor": "#999",
                            "itemDirection": "left-to-right",
                            "itemOpacity": 1,
                            "symbolSize": 18,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ]
                )

if __name__ == "__main__":
    try:
        logger = get_logger(__name__)
        main()
    except Exception as e:
        # Print the exception message
        logger.error(f'An error occurred: {e}')

    