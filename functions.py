import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st 
import yfinance as yf
import numpy as np
from streamlit_gsheets import GSheetsConnection

@st.cache_resource(ttl=6000)  # Almacena en caché los resultados durante 1 hora (3600 segundos)
def cargar_datos_gsheets(worksheet_name: str, columns: list= None):
    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df = conn.read(worksheet=worksheet_name,usecols=columns, ttl=2).dropna()
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos de la hoja de cálculo '{worksheet_name}': {str(e)}")
        return None

@st.cache_resource(ttl=6000)
def cargar_datos_yfinance(symbol: str, period: str):
    try:
        df = yf.download(symbol, period=period)
        df = df.reset_index()
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos de Yahoo Finance para el símbolo '{symbol}': {str(e)}")
        return None

def CAGR_calculate(final_value,initial_value, years):
        CAGR = round(((final_value/initial_value)**(1/years)-1)*100,2)
        return CAGR

def calcular_estadisticas(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')

    # Cálculos de estadisticas
    start = data['Date'].iloc[0]
    end = data['Date'].iloc[-1]
    data['DailyReturn'] = data.Close.pct_change(1)
    standard_deviation = (data['DailyReturn'].std()* np.sqrt(252))*100  # Daily return
    standard_deviation_price = data['Close'].std()  # Close price
    data['LogReturn'] = np.log(data['Close'] / data['Close'].shift(1))
    data['LogReturn'] = data['LogReturn'].dropna() 
    log_return = (data['LogReturn'].mean() * 252) * 100
    rendimiento_anual_simple = round(data['DailyReturn'].mean() * 252, 2) * 100
    CAGR_return = round(CAGR_calculate(data['Close'].iloc[-1],(data['Close'].iloc[0]),252 ),2)
    rolling_max = data['Close'].cummax()
    daily_drawdown = data['Close'] / rolling_max - 1
    max_drawdown = (daily_drawdown.cummin().iloc[-1])*100

    # Calcular valores agregados
    mean = round(data['Close'].mean(), 2)
    max_val = round(data['Close'].max(), 2)
    min_val = round(data['Close'].min(), 2)
    count = data['Close'].count()
    standard_deviation = round(standard_deviation, 2)
    standard_deviation_price = round(standard_deviation_price, 2)
    log_return = round(log_return, 2)

    # Crear un DataFrame con los resultados
    results = {
        'Start Date' : [start],
        'End Date': [end],
        'Period (days)': [count],
        'Avg. Close Price': [mean],
        'Max. Close Price': [max_val],
        'Min. Close Price': [min_val],
        'Std. (Close Price)': [standard_deviation_price],
        'RoR (%)': [str(round(rendimiento_anual_simple,2 ))+"%"],
        'Log. Return (%)': [str(round(log_return,2))+"%"],
        'CAGR': [str(round(CAGR_return,2))+"%"],
        'Volatility': [str(round(standard_deviation,2))+"%"],
        'Maximum Drawdown': [str(round(max_drawdown,2))+"%"],

    }

    resultados_df = pd.DataFrame(results, index=["Valor"])
    resultados_df = resultados_df.T

    return resultados_df

def plot_time_series(data, x_col, y_col, title, x_title, y_title, chart_type='line', line_color='black', title_color="#027034"):
    if chart_type =='area':
        fig = px.area(
        data,
        x = x_col,
        y = y_col,
        title = title,
        )
    else:
        fig = px.line(
            data,
            x = x_col,
            y = y_col,
            title= title, 
        )

    fig.update_xaxes(title_text=x_title)

    fig.update_yaxes(
        title_text=y_title,
    )

    fig.update_layout(
        title_font=dict(
            color=title_color,
            size=20
        )
    )

    fig.update_traces(line=dict(color=line_color))

    st.plotly_chart(fig, use_container_width=True)

def calculate_financial_ratios(income_statement, income_statement_current, balance_sheet, balance_sheet_current):
    # A. Profit Margin
    Profit_margin = pd.DataFrame({
        'Periodo': income_statement['Periodo'],
        'Profit Margin': income_statement['Net income'] / income_statement['Revenues']
    })

    Profit_margin_current = pd.DataFrame({
        'Periodo': income_statement_current['Periodo'],
        'Profit Margin': income_statement_current['Net income'] / income_statement_current['Revenues']
    })

    # B. Asset Turnover
    Asset_turnover = pd.DataFrame({
        'Periodo': income_statement['Periodo'],
        'Asset Turnover': income_statement['Revenues'] / balance_sheet['TotalAssets']
    })

    Asset_turnover_current = pd.DataFrame({
        'Periodo': income_statement_current['Periodo'],
        'Asset Turnover': income_statement_current['Revenues'] / balance_sheet_current['TotalAssets']
    })

    # C. Financial Leverage
    Financial_leverage = pd.DataFrame({
        'Periodo': income_statement['Periodo'],
        'Financial Leverage': balance_sheet['TotalAssets'] / balance_sheet['Total_Sth_Equity']
    })

    Financial_leverage_current = pd.DataFrame({
        'Periodo': income_statement_current['Periodo'],
        'Financial Leverage': balance_sheet_current['TotalAssets'] / balance_sheet_current['Total_Sth_Equity']
    })

    return Profit_margin, Profit_margin_current, Asset_turnover, Asset_turnover_current, Financial_leverage, Financial_leverage_current

def filtrar_datos(sheet_name, columns, company):
    df = cargar_datos_gsheets(sheet_name, columns)
    if df is not None:
        df = df[df["Empresa"] == company]
        df['Periodo'] = df['Periodo'].astype(str)
    return df