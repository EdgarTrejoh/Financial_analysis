import streamlit as st 
from Functions import functions as fc 
import numpy as np 
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
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

st.markdown("# :green[1. Technical Analysis 📈]")

#1. Definir las variables
catalogo = fc.cargar_datos_gsheets('CAT_001', [0,1]) 
stocks = catalogo['Empresa']

empresa =st.selectbox(":blue[***Please select an option:***]", stocks, help = 'Filter report to show only one Stock') 

benchmark = "^GSPC"
ticker = catalogo[catalogo['Empresa']==empresa]['Ticker'].values[0]     

if 'selected_company' not in st.session_state:
    st.session_state["selected_company"] = None

st.session_state["selected_company"] = empresa

#2. Generar la información:
data_load_state = st.markdown(":red[Loading data...]")

data = fc.cargar_datos_yfinance(ticker, '5Y')
data_benchmark = fc.cargar_datos_yfinance(benchmark,'5Y')

data_load_state.markdown(':blue[Loading data... done!]')

current_data = data.loc[data['Date'] > "07-2023"]
current_data.reset_index(inplace=True)

"----------"

#3. Realizar los modelos:
#3.1 Modelo de Regresión lineal:
data['Numbers']  = list(range(0, len(data)))
X = np.array(data[['Numbers']])
Y = data["Close"].values
lin_model = LinearRegression().fit(X ,Y)
#print ('Intercept:', lin_model.intercept_)
#print ('Slope:' , lin_model.coef_)
y_pred = lin_model.coef_ * X + lin_model.intercept_
data['Pred'] = y_pred

#3.2 Crecimiento base - 5Y
data['IncBase5Y'] = data.Close.div(data.Close.iloc[0]).mul(100)
data_benchmark['IncBase5Y'] = data_benchmark.Close.div(data_benchmark.Close.iloc[0]).mul(100)

#3.3 SMA
SMA10 = 10
SMA50 = 50
data['SMA10'] = data['Close'].rolling(SMA10).mean()
data['SMA50'] = data['Close'].rolling(SMA50).mean()
data_SMA = data.loc["2022":]
    
#3.4 MACD (Moving Average Convergence Divergence)
exponential_small = data['Close'].ewm(span=8, adjust= False).mean() # ewm = Provide exponentially weighted (EW) calculations.
exponental_large =  data['Close'].ewm(span=17, adjust= False).mean()
data['MACD'] = exponential_small - exponental_large 
data['MACD_Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

#3.5 Bollinger Bands
data['TypicalPrice'] =(data['Close'] + data['High']+ data['Low']) / 3 
data['Std'] = data['TypicalPrice'].rolling(20).std(ddof=0)
data['MA-Close'] = data['TypicalPrice'].rolling(20).mean()
data['BOLU'] = data['MA-Close'] + 2 * data['Std'] 
data['BOLD'] = data['MA-Close'] - 2 * data['Std']

#4. Visualización de resultados
#4.1 Estadísticas
st.markdown(f"### :green[{empresa}]")

st.markdown(
    """
    > ### 📊 :green[Statistics]

    """
    )

resultados_df = fc.calcular_estadisticas(data)
st.dataframe(resultados_df, hide_index= False, width=340, height=455)
st.text(len(data)* "*")

#4.2 Gráficos:
#4.2.1 Time Series
st.markdown(
    """
    > ### 📈 :green[Charts]
    >
    >> ### :green[1. Time Series]

    """
    )

config = {
    'modeBarButtonsToRemove': ['zoom', 'pan'],
    }

fc.plot_time_series(data, 'Date','Close', f" {empresa} - Time Series", "Date", "Price USD($)","area","black", "#027034",  )

fc.plot_time_series(data, 'Date','DailyReturn', f" {empresa} - Daily Return","Date", "Daily RoR (%)","area","blue", "#027034",  )

#4.2.2 Crecimiento en 5Y
st.markdown(
    """
            
    >> ### :green[2. Stock price growth over the past five years (%)]

    """
    )

grafica_5Y = go.Figure()

grafica_5Y.add_trace(
    go.Scatter(
        x=data['Date'],
        y=data['IncBase5Y'],
        mode="lines",
        name=empresa,
        line=dict(color='#196FEC'),
        )
    )

grafica_5Y.add_trace(
    go.Scatter(
        x=data_benchmark['Date'],
        y=data_benchmark['IncBase5Y'],
        mode="lines",
        name="S&P500",
        line=dict(color='#07582B')
        #fill= 'toself'     ,
        )
    )

grafica_5Y.update_xaxes(title_text="Date")

grafica_5Y.update_yaxes(title_text="Stock price growth (%)")

grafica_5Y.update_layout(
    title_text=f"{empresa} - S&P500",
    title_font=dict(
        color="#027034", 
        size=20
        )
    )

st.plotly_chart(grafica_5Y, use_container_width=True)

#4.2.3 Gráfico de Vela Candlesticks
st.markdown(
    """   
    >> ### :green[3. Candlestick]
    
    """
    )

figura  = go.Figure(
    data = [go.Candlestick(
        x=current_data['Date'], 
        open = current_data['Open'],
        high = current_data['High'],
        low = current_data['Low'],
        close = current_data['Close']
        )
    ]
)

figura.update_layout(
    title_text=f"{empresa} - Candlestick",
    title_font=dict(
        color="#027034", 
        size=20
        )
    )

st.plotly_chart(figura, use_container_width = True)

#4.2.4 Histogramas
st.markdown(
    """
    
    >> ### :green[4. Histograms]

    """
    
    )

#4.2.4.1 Histograma precio de cierre
histogram_price = px.histogram(
    data, 
    x=data['Close'], 
    nbins=150,
    color_discrete_sequence=['indianred'],
    marginal='box'
    )

histogram_price.update_layout(
    title_text=f"{empresa} : Close Price",
    title_font=dict(
        color="#027034", 
        size=20
        )
    )

st.plotly_chart(histogram_price, use_container_width = True)

#4.2.4.2 Histograma rendimiento diario
histogram = px.histogram(
    data, 
    x=data['DailyReturn'], 
    nbins=30,
    color_discrete_sequence=['indianred'],
    marginal='box'
    )

histogram.update_layout(
    title_text=f"{empresa} : Daily RoR",
    title_font=dict(
        color="#027034", 
        size=20
        )
    )

st.plotly_chart(histogram, use_container_width = True)

#4.2.5 Moving Average
st.markdown(
    """
        
    >> ### :green[5. Simple Moving Average]

    """
    )

periods = st.slider(":red[**Select the number of periods (days)**]", 10 ,100, step=10)

data['MA'] = data['Close'].rolling(periods).mean()

fig_MA =  px.line(
    data, 
    x='Date',
    y=['Close', 'MA'],
    color_discrete_sequence= px.colors.sequential.GnBu_r, 
    #px.colors.sequential.Plasma_r,
    title=f"{empresa} : Moving Average. Periods: {periods} days."
    )

fig_MA.update_layout(
    title_font=dict(
        color="#027034", 
        size=20
        )
    )

st.plotly_chart(fig_MA)

fig_SMA =  px.line(
    data, 
    x = 'Date',
    y=['Close', 'SMA10','SMA50'],
    title=f"{empresa}: SMA"
    )

fig_SMA.update_layout(
    title_font=dict(
        color="#027034", 
        size=20
        )
    )

st.plotly_chart(fig_SMA)

#st.line_chart(data_SMA, x= 'Date', y=['Close', 'SMA_S','SMA_L'])

#4.2.6 MACD (Moving Average Convergence Divergence)

st.markdown(
    """
    
    >> ### :green[6. MACD (Moving Average Convergence Divergence)]
    
    """
    )

fig_MACD = make_subplots(specs= [[{"secondary_y": True}]])

fig_MACD.add_trace(
    go.Scatter(
        x=data['Date'], 
        y=data['MACD'], 
        name = "MACD"
        ),
        secondary_y =False, 
    )

fig_MACD.add_trace(
    go.Scatter(
        x=data['Date'], 
        y=data['MACD_Signal_Line'], 
        name = "Signal Line"
        ),
        secondary_y =False, 
    )
    #AQui modifique jeje
fig_MACD.add_trace(
    go.Scatter(
        x= data['Date'], 
        y=data['Close'], 
        name = "Close Price"
        ),
        secondary_y =True, 
    )

fig_MACD.update_layout(
    title_text = f"{empresa}: MACD",
    title_font=dict(
        color="#027034",
        size=20
        )
    )

fig_MACD.update_xaxes(title_text="Date")

#fig_MACD.update_yaxes(title_text="<b>Close</b> Price ($)", secondary_y=False)
fig_MACD.update_yaxes(title_text="<b>Close</b> Price ($)", secondary_y=True)

st.plotly_chart(fig_MACD)

#4.2.7 Bollinger bands
st.markdown(
    """
    
    >> ### :green[7. Bollinger Bands]
    
    """
    )

fig_bollinger_band = go.Figure()

fig_bollinger_band.add_trace(
    go.Scatter(
        x=data['Date'], 
        y=data['TypicalPrice'],
        fill=None,
        mode='lines',
        line_color='#EA6E43',
        name = "Close"
        )
    )

fig_bollinger_band.add_trace(
    go.Scatter(
        x=data['Date'], 
        y=data['BOLU'],
        fill = 'tonexty',
        #fill="toself",
        mode = "lines",
        line_color= "#4380EA",
        name= "BOLU"
        )
    )

fig_bollinger_band.add_trace(
    go.Scatter(
        x=data['Date'], 
        y=data['BOLD'],
        fill = 'tonexty',
        #fill='tozeroy',
        mode = "lines",
        line_color= "#4380EA",
        name= "BOLD"
        )
    )

fig_bollinger_band.update_xaxes(title_text="Date")

fig_bollinger_band.update_yaxes(
    title_text="Price",
    tickprefix="$"
    )

fig_bollinger_band.update_layout(
    title_text=f"{empresa} - Bollinger Bands",
    title_font=dict(
    color="#027034",
    size=20
    )
)

st.plotly_chart(fig_bollinger_band, use_container_width=True)

#6 Gráfico Tendencia precio de cierre
st.markdown(
    """
    
    > ### :blue[Trending - Close Price]
    
    """
    )

trending_close_price =  px.line(
    data, 
    x='Date',
    y=['Pred', 'Close'],
    color_discrete_sequence= px.colors.sequential.GnBu_r, 
    #px.colors.sequential.Plasma_r,
    title=f"{empresa} : Trending close price."
    )

trending_close_price.update_layout(
    title_font=dict(
        color="#027034", 
        size=20
        )
    )

st.plotly_chart(trending_close_price)