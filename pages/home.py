import streamlit as st 

st.set_page_config(page_title="Stocks Dashboard", page_icon="💹", layout="wide")

st.markdown("# :green[Welcome to Financials analysis for the main stocks in the S&P 500 🚀]")

st.markdown("##### :green[v3.0 Technical & Fundamental Anaylsis]")

st.markdown("""
        #### :green[Developed by:]     
        """
)

col_1, col_2, col_3 = st.columns([0.5,1.5,5])

with col_1:
    st.image('.\images\icons8-linkedin.svg', width=60)
with col_2:
    st.markdown(""" 
                [**Edgar Trejo**](https://www.linkedin.com/in/edgar-trejo-03077748)
                """)
    st.html('<a target="_blank" href="https://icons8.com/icon/13930/linkedin">LinkedIn</a> icono de <a target="_blank" href="https://icons8.com">Icons8</a>')

with col_3:
    st.write("")

col_1, col_2, col_3 = st.columns([0.5,1.5,5])

with col_1:
    st.image('.\images\icons8-twitterx.svg', width=60)
with col_2:
    st.markdown(""" 
                [**@EconoDataMx**](https://x.com/EconoDataMx)
                """)
    st.html('<a target="_blank" href="https://icons8.com/icon/phOKFKYpe00C/twitterx">X</a> icono de <a target="_blank" href="https://icons8.com">Icons8</a>')

with col_3:
    st.write("")

st.markdown("""
             
        🐢 :green[**More info:** ] [![EconoDataMx Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://econodatamx-v1.streamlit.app/)  
        """
        
)

st.markdown(
    """

    **This demo shows the use of *Streamlit* 
    for data analysis and data visualization with Python code, 
    powered with libraries such as:

    - **St-Gsheets-Connection:**

     ```sh
    pip install st-gsheets-connection
    ```

    [**gsheets-connection**](https://github.com/streamlit/gsheets-connection)
    
    - **yfinance:**
     ```sh
    pip install yfinance
    ```   
    [**yfinance**](https://pypi.org/project/yfinance/)

    - **Plotly:**

     ```sh
    $ pip install plotly==5.22.0
    ```

    [**Plotly**](https://plotly.com/python/)

    And others.**
    
    """
)
"----------"

st.markdown(
    """
    >> ### :red[Important Information] ✅
    """
    )

"----------"

st.markdown(
    """
    The information provided below has been prepared for academic and  informational purposes. 
    
    Any opinions, analyses, prices, or other content do not constitute investment advice and do not represent an investment recommendation. 
    
    Past performance is not indicative of future results, and anyone acting on this information does so at their own risk. 
    
    For a specific evaluation, it is essential to consider aspects such as:
    
    - Investor profile
    - Investment goals
    - Risk management approach: appetite, tolerance, unacceptable levels
    - Liquidity needs
    - Investment timeframe
    - And other relevant factors. 
    
    Undertaking any form of investment is not recommended without specialized guidance and without having conducted a thorough analysis and assessment, including the investment instrument and market conditions (macro and microeconomic analysis), among other relvant indicators.



    >> ### :red[Key Features]

    

    | Technical Analysis | Fudamental Analysis |
    |-----------|-----------|
    |MACD| Profitability Ratios|
    |SMA| Profit Margin|
    |EMA| Turnover-control ratios|
    |Bollinger Bands| Leverage and liquity ratios|

    ### And more
    
    """
    ) 