import streamlit as st
from Functions import functions as fc     
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("# :green[2. Fundamental Analysis 📊]")

def cargar_datos(filtrar_datos_func, sheet_name, columns, company_selected):
    try:
        data = filtrar_datos_func(sheet_name, columns, company_selected)
        if data is None or data.empty:
            raise ValueError(f"No data available for {company_selected}; Please select another company")
        return data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def safe_access(df, index, column):
    try:
        return df.iloc[index][column]
    except IndexError:
        st.error("Index out of bounds,Please select another company")
        return None

list_1 = [i for i in range(14)]
list_2 = [i for i in range(39)]

company_selected = st.session_state["selected_company"]            

income_statement = cargar_datos(fc.filtrar_datos,'IS_001', list_1, company_selected)
income_statement_current = cargar_datos(fc.filtrar_datos,'IS_002', list_1, company_selected)   
balance_sheet = cargar_datos(fc.filtrar_datos,'BS_001', list_2, company_selected)
balance_sheet_current = cargar_datos(fc.filtrar_datos,'BS_002', list_2, company_selected)

# CAGR Variables
# Income Statement
final_revenues = income_statement['Revenues'].iloc[-1]
initial_revenues = income_statement['Revenues'].iloc[0]
final_CoR = income_statement['Cost of revenues'].iloc[-1]
initial_CoR = income_statement['Cost of revenues'].iloc[0]
final_TCE = income_statement['Total costs and expenses'].iloc[-1]
initial_TCE = income_statement['Total costs and expenses'].iloc[0]
final_Net_Income = income_statement['Net income'].iloc[-1]
initial_Net_Income = income_statement['Net income'].iloc[0]

# Balance Sheeet
final_current_assets = balance_sheet['TotalCurrentAssets'].iloc[-1]
initial_current_assets = balance_sheet['TotalCurrentAssets'].iloc[0]
final_total_assets = balance_sheet['TotalAssets'].iloc[-1]
initial_total_assets = balance_sheet['TotalAssets'].iloc[0]
final_current_liabilities = balance_sheet['TotalCurrentLiab'].iloc[-1]
initial_current_liabilities = balance_sheet['TotalCurrentLiab'].iloc[0]
final_total_liabilities = balance_sheet['TotalLiab'].iloc[-1]
initial_total_liabilities = balance_sheet['TotalLiab'].iloc[0]

years = len(income_statement['Revenues'])-1
years_balance = len(balance_sheet['TotalCurrentAssets'])-1 #cambio

# CAGR Calculate
CAGR_Revenues = fc.CAGR_calculate(final_revenues, initial_revenues, years)
CAGR_CoR = fc.CAGR_calculate(final_CoR, initial_CoR, years)
CAGR_TCE = fc.CAGR_calculate(final_TCE, initial_TCE, years)
CAGR_Net_Income = fc.CAGR_calculate(final_Net_Income, initial_Net_Income, years)
CAGR_Current_Asets = fc.CAGR_calculate(final_current_assets, initial_current_assets, years_balance)
CAGR_Total_Asets = fc.CAGR_calculate(final_total_assets, initial_total_assets, years_balance)
CAGR_Current_Liabilities = fc.CAGR_calculate(final_current_liabilities, initial_current_liabilities, years_balance)
CAGR_Total_Liabilities = fc.CAGR_calculate(final_total_liabilities, initial_total_liabilities, years_balance)

#************************************
        # Financial Ratios
#************************************
# ROE Return on Equity 
Profit_margin, Profit_margin_current, Asset_turnover, Asset_turnover_current, Financial_leverage, Financial_leverage_current = fc.calculate_financial_ratios(income_statement, income_statement_current, balance_sheet, balance_sheet_current)

# ROE
ROE_components = pd.DataFrame({
    'Periodo': Financial_leverage['Periodo'],
    "Financial Leverage": Financial_leverage['Financial Leverage'],
    "Asset Turnover":Asset_turnover['Asset Turnover'],
    "Profit Margin" : Profit_margin["Profit Margin"]
})

ROE_components['ROE'] = ROE_components['Financial Leverage'] * ROE_components['Asset Turnover'] * ROE_components['Profit Margin']
ROE_components['ROE'] = ROE_components['ROE'].map('{:.2%}'.format)

ROE_components_current = pd.DataFrame({
    'Period': Financial_leverage_current['Periodo'],
    "Financial Leverage": Financial_leverage_current['Financial Leverage'],
    "Asset Turnover":Asset_turnover_current['Asset Turnover'],
    "Profit Margin" : Profit_margin_current["Profit Margin"]
})

ROE_components_current['ROE'] = ROE_components_current['Financial Leverage'] * ROE_components_current['Asset Turnover'] * ROE_components_current['Profit Margin']
ROE_components_current['ROE'] = ROE_components_current['ROE'].map('{:.2%}'.format)

# ROA
ROE_components['ROA'] = ROE_components['Asset Turnover'] * ROE_components['Profit Margin']
ROE_components['ROA'] = ROE_components['ROA'].map('{:.2%}'.format)

ROE_components_current['ROA'] = ROE_components_current['Asset Turnover'] * ROE_components_current['Profit Margin']
ROE_components_current['ROA'] = ROE_components_current['ROA'].map('{:.2%}'.format)

# Balance Sheet Ratios
Debt_to_assets_ratio_current = (balance_sheet_current['TotalLiab'].iloc[0])/(balance_sheet_current['TotalAssets'].iloc[0])
Debt_to_equity_ratio_current = (balance_sheet_current['TotalLiab'].iloc[0])/(balance_sheet_current['Total_Sth_Equity'].iloc[0])

# Liquidity Ratios
current_ratio = balance_sheet_current['TotalCurrentAssets'].div(balance_sheet_current['TotalCurrentLiab'])
acid_test = (balance_sheet_current['TotalCurrentAssets'] -balance_sheet_current['Inventory']).div(balance_sheet_current['TotalCurrentLiab'])
df_liquidity = pd.DataFrame(current_ratio, columns=["Current Ratio"]) 
df_liquidity["Acid Test"] = pd.DataFrame(acid_test)

# CAGR Dataframe 

CAGR_data = {
    "Revenues":[str(CAGR_Revenues) + "%"],
    "Current Assets": [str(CAGR_Current_Asets) + "%"],
    "Total Assets": [str(CAGR_Total_Asets) + "%"],
    "Current Liabilities": [str(CAGR_Current_Liabilities) + "%"],
    "Total Liabilities": [str(CAGR_Total_Liabilities) + "%"],
    "Cost of Revenues": [str(CAGR_CoR) + "%"] ,
    "Total Cost and Expenses": [str(CAGR_TCE) + "%"],
    "Net Income": [str(CAGR_Net_Income) + "%"]
}

resume_financial = pd.DataFrame(CAGR_data) 
resume_financial = resume_financial.T.reset_index()
resume_financial = resume_financial.rename(columns= {"index": "Component", 0: "CAGR"})

# Visualization 

#************************************************
        
        # GRÁFICOS

#************************************************

# Crear el Gráfico: 

empresa = st.session_state["selected_company"]

figura = make_subplots(rows=2, cols=2,
                        row_heights=[0.8, 0.8],
                        shared_xaxes=False,
                        subplot_titles=("1. Profit Margin", 
                                        "2. Asset Turnover", 
                                        "3. Financial Leverage", 
                                        "ROE"
                                        ),
                        vertical_spacing=0.3,
                        horizontal_spacing=0.2,
                        print_grid=True
                        )

# Primer Gráfico:

figura.add_trace(
    go.Scatter(
        x =ROE_components['Periodo'], 
        y = ROE_components['Profit Margin'],
        mode= "markers+lines",
        line=dict(color='#15C463', width=3)
        ),
    row=1, col=1  
    )

figura.update_yaxes(title_text="<b>%</b>", row=1, col=1)

# Segundo Gráfico:

figura.add_trace(
    go.Scatter(
        x =ROE_components['Periodo'], 
        y = ROE_components['Asset Turnover'],
        mode= "markers+lines",
        line=dict(color='#08781D', width=3)), #dash options include 'dash', 'dot', and 'dashdot'
    row=2, col=1  
    )

figura.update_yaxes(title_text="Times", row=2, col=1)

# Tercer Gráfico:

figura.add_trace(
    go.Scatter(
        x =ROE_components['Periodo'], 
        y = ROE_components['Financial Leverage'],
        mode= "markers+lines",
        line=dict(color='#4CA25C ', width=3)
        ),        
    row=1, col=2 
    )

figura.update_yaxes(title_text="Times", row=1, col=2)

# Cuarto Gráfico:

figura.add_trace(
    go.Scatter(
        x =ROE_components['Periodo'], 
        y = ROE_components['ROE'],
        mode= "markers+lines", # lines  - markers
        line=dict(color='#5CA57D', width=3)),
    row=2, col=2  
    )

figura.update_yaxes(title_text="<b>%</b>", row=2, col=2)

# Personalizar Gráfico:

figura.update_xaxes(title_text="Year")

figura.update_layout(showlegend=False,
                    #row_span=[1, 2, 3], col_span=[1, 1, 2],
                    height=600,
                    width=800,
                    title_text =f"<b>{empresa}</b> - Three Determinants of ROE",
                    title_font=dict(
                        color="#027034",
                        size=22),
                    annotations=[
                        dict(xref='paper', yref='paper',
                            x=0, y=1.05,
                            xanchor='left', yanchor='middle',
                            text='<b>1. Profit Margin</b>',
                            font=dict(color='#6376F3', size=16)),
                        dict(
                            xref='paper', yref='paper',
                            x=0.5, y=1.05,
                            xanchor='center', yanchor='middle',
                            text='<b>2. Asset Turnover</b>',
                            font=dict(color='#6376F3', size=16)
                        ),
                        dict(
                            xref='paper', yref='paper',
                            x=0, y=0.48,
                            xanchor='left', yanchor='middle',
                            text='<b>3. Financial Leverage</b>',
                            font=dict(color='#6376F3', size=16)
                        ),
                        dict(
                            xref='paper', yref='paper',
                            x=0.5, y=0.48,
                            xanchor='center', yanchor='middle', #top - bottom
                            text='<b>4. ROE</b>',
                            font=dict(color='#6376F3', size=16)
                        ),
                        ]
                    )


#***************************************
    # CAGR Chart
#***************************************
selection = ["Revenues", "Total Assets", 
            "Total Liabilites", "Cost of Revenues", 
            "Net Income"]

CAGR_datachart = resume_financial.loc[resume_financial["Component"].isin(selection)].copy()

#***********************************
    # Revenues Chart
#***********************************

revenues_chart = go.Figure()

years = income_statement['Periodo']
Revenues  = income_statement['Revenues']
CostOfRevenues = income_statement['Cost of revenues']

CostOfRevenues = CostOfRevenues*-1 
#go.Bar 
revenues_chart.add_trace(go.Scatter(
    x=years,
    y=CostOfRevenues,
    #base=0,
    mode= 'lines',
    marker_color='red',
    name='Cost of Revenues'))

revenues_chart.add_trace(go.Scatter(
    x=years, 
    y= Revenues,
    mode='lines',
    #base=0,
    marker_color='green',
    name='Revenues'
    ))

revenues_chart.update_layout(title_text=f"{empresa} - Revenues - Cost of Revenues",
                            title_font=dict(
            color="#027034",
            size=20
            ),
            xaxis_title="Year",
            yaxis_title="Amount",
            legend_title="Components",
            #barmode='stack',  # 'stack' apilará las barras
            #yaxis=dict(range=[100, max(Revenues.max(), -CostOfRevenues.min())]),  # Ajusta el rango del eje y
    )

#*************************************
        # CAGR Chart
#*************************************

CAGR_chart = px.bar(
    CAGR_datachart, 
    x ="Component",
    y = "CAGR",
    color="Component",
    color_discrete_sequence=["#163266", 
                            "#0f3c90", 
                            "#376ac9", 
                            "#789de1"],
    title = f"{empresa} - CAGR",
)

CAGR_chart.update_xaxes(title_text="Components")

CAGR_chart.update_yaxes(
        title_text="CAGR (%)")

CAGR_chart.update_layout(
        height = 380,
        width=480,
        showlegend = False,
        title_font=dict(
            color="#027034",
            size=20
            )
        )

#************************************************
        # VISUALIZATION
#************************************************

current_year, historical_data, resume_CAGR = st.tabs([":date: Current Year", 
                                                                ":clipboard: Historical Data", 
                                                                ":chart_with_upwards_trend: CAGR", 
                                                                ])

with current_year:

    container =st.container(border=True)
    
    with container:

        st.markdown(f"### :green[{empresa} - 1Q2024 :pushpin:    ]")
        st.markdown(f":blue[(in millions)]")

        v1, m1, m2, m3, v2 = st.columns(5)

        total_costs = income_statement_current['Revenues'].iloc[0]-income_statement_current['Net income'].iloc[0]
    
        
        st.html(f'<span class="st-emotion-cache-1wivap2"></span>')

        v1.write("")
        m1.metric(":blue[Revenues]", value=f"{int(income_statement_current['Revenues'].iloc[0]):,}")
        m2.metric(':blue[Total Costs]', value=f"{int(total_costs):,}")
        m3.metric(':blue[Net Income]', value=f"{int(income_statement_current['Net income'].iloc[0]):,}")
        v2.write("")
        
        c1, n1, n2, n3, c2 = st.columns(5)

        c1.write("")
        n1.metric(":blue[Revenues]", '{:.1f}%'.format((income_statement_current['Revenues'].iloc[0]/income_statement_current['Revenues'].iloc[0])*100), label_visibility="hidden")
        n2.metric(':blue[Total Costs]', '{:.1f}%'.format((total_costs/income_statement_current['Revenues'].iloc[0])*100),label_visibility="hidden")
        n3.metric(':blue[Net Income]', '{:.1f}%'.format((income_statement_current['Net income'].iloc[0]/income_statement_current['Revenues'].iloc[0])*100),label_visibility="hidden")
        c2.write("")
    
    with st.expander(" :green[Return on Equity]"):
        
        st.markdown("### :green[The Three Determinants of ROE]")

        column_roe_1, column_roe_2, column_roe_3, column_roe_4, column_roe_5 = st.columns(5) 

        column_roe_1.write("")
        column_roe_2.metric(":blue[Profit Margin]", '{:,.2f}'.format(ROE_components_current['Profit Margin'].iloc[0]))
        column_roe_3.metric(':blue[Assets Turnover]', '{:,.2f}'.format(ROE_components_current['Asset Turnover'].iloc[0]))
        column_roe_4.metric(':blue[Financial Leverage]', '{:,.2f}'.format(ROE_components_current['Financial Leverage'].iloc[0]))
        column_roe_5.write("")

        roe_1, roe_2, roe_3, roe_4 = st.columns(4) 

        roe_1.write("")
        roe_2.metric(":blue[ROE]", ROE_components_current['ROE'].iloc[0])
        roe_3.metric(':blue[ROA]', ROE_components_current['ROA'].iloc[0])
        roe_4.write("")

        st.divider()

        st.latex(
            r'''

            ROE = (\frac{Net Income}{Sales})x (\frac{Sales}{Assets})x (\frac{Assests}{Shareholder´s Equity})                       
            
            '''
        )

        st.divider()
            
        st.latex(
            r'''

            ROA = ({Profit Margin})x ({Asset Turnover})   
            '''
        )

    with st.expander(" :green[Balance Sheet Ratios]"):
        balance_1, balance_2, balance_3, balance_4 = st.columns(4)

        balance_1.write("") 
        balance_2.metric(":blue[Debt-to-assets-ratio]",'{:,.2%}'.format(Debt_to_assets_ratio_current))
        balance_3.metric(":blue[Debt-to.equity-ratio]",'{:,.2%}'.format(Debt_to_equity_ratio_current))
        balance_4.write("")

        st.divider()

        st.latex(
            r'''

            Debt-to-assets-ratio = (\frac{Total-Liabilities}{Total-Assets})                      
            
            '''
        )

        st.divider()
            
        st.latex(
            r'''

            Debt-to-equity-ratio = (\frac{Total-Liabilities}{Total-Stockholders’-Equity})

            '''
        )
    
    with st.expander(" :green[Liquidity Rarios]"):
        
        #st.markdown("### :green[The Three Determinants of ROE]")
        column1, column2, column3, column4 = st.columns(4)

        column1.write("")
        column2.metric(":blue[Current Ratio]", '{:,.2f}'.format(df_liquidity['Current Ratio'].iloc[0]))
        column3.metric(':blue[Acid Test]', '{:,.2f}'.format(df_liquidity['Acid Test'].iloc[0]))
        column4.write("")

        st.divider()

        st.latex(
            r'''

            Current-Ratio = (\frac{Current Assets}{Current Liabilities})                      
            
            '''
        )

        st.divider()
            
        st.latex(
            r'''

            Acid-Test = (\frac{Current Assets - Inventory}{Current Liabilities})

            '''
        )

    st.markdown(":blue[Source: Financial Statements]")

#************************************************
        # Tres Determinantes del ROE
#************************************************

with historical_data:

    with st.expander(" :green[Revenues]"):
        
        st.markdown("### :green[Historical Revenues]")

        st.plotly_chart(revenues_chart, use_container_width=True)

    with st.expander(" :green[Return on Equity]"):
        
        st.markdown("### :green[The Three Determinants of ROE]")

        st.plotly_chart(figura, use_container_width=True)

with resume_CAGR:

    st.markdown("## :green[Compound Annual Growth Rate]")

    chart, data = st.columns([2,1])

    with chart:
        st.plotly_chart(CAGR_chart)

    with data:
        st.markdown("### :green[Data]")
        st.dataframe(resume_financial, hide_index=True, width=150)