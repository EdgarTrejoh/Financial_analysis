import streamlit as st 

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

st.markdown("## :green[3. Additional Information Resources :nerd_face:]")
st.markdown("### Web-Pages :globe_with_meridians:")

st.write(
    """
    Whether you're an investor, student, or financial enthusiast, 
    these websites offer additional information to help you stay 
    informed and make well-informed decisions. 
    Explore the following references to enhance your understanding of 
    various financial topics:
    """

)

"----------"

columna_1, columna_2 = st.columns(2)

with columna_1:
    #Rate of Return
    st.markdown(
    """   
    **:green[1. RoR - Rate Of Return]**

    """)
    
    st.latex(
    r'''

        RoR = (\frac{V_f -V_{init}}{V_{init}})-1         
        
        '''
    )
    st.markdown(
        """
        
        - $V_{init}$: Initial value
        - $V_f$: Final value
        - $n$: number of period
        
        
        [Source: Investopedia](https://www.investopedia.com/terms/r/rateofreturn.asp)
        
        """
    )

    "----------"
    
    #CAGR
    st.markdown(
        """
        **:green[3. Compound Annual Growth Rate]**
        """
    )
    
    st.latex(
        r'''

        CAGR = (\frac{V_f}{V_{init}})^\frac{1}{n}-1         
        
        '''
    )
    st.markdown(
        """   
        - $V_{init}$: Initial value
        - $V_f$: Final value
        - $n$: number of period

        [Source: Investopedia](https://www.investopedia.com/terms/c/cagr.asp)
    """
    )
    
    "----------"
    
    
#Bollinger Bands
st.markdown(
        """
        **:green[5. Bollinger Bands]**
        """
    )
st.markdown(
        """
        **Bollinger Band®** formula:
        
        BOLU=MA(TP,n) + m ∗ σ[TP,n]

        BOLD=MA(TP,n) − m ∗σ[TP,n]

        where:

        BOLU=Upper Bollinger Band

        BOLD=Lower Bollinger Band

        MA=Moving average
        
        TP (typical price)=(High+Low+Close)÷3

        n=Number of days in smoothing period (typically 20)

        m=Number of standard deviations (typically 2)

        σ[TP,n]=Standard Deviation over last n periods of TP
        
        [Source: Investopedia](https://www.investopedia.com/terms/b/bollingerbands.asp)
        
        """
    )
    

"----------"

with columna_2:
    #Log Return
    st.markdown(
    """   
    **:green[2. Logarithmic Return]**
    """
    )
    
    st.latex(r"""
            R_log = ln(\frac{V_t}{V_{t-1}}) 
            """    
    )

    st.markdown(
        """
        - $V_t$: The price of an asset at time: *t*
        - $V_{t-1}$: The price of an asset at time: *t-1*
        - $ln$: The natural logarithm log is the inverse of the exponential function. 
        
        [Source: Wikipedia](https://en.wikipedia.org/wiki/Rate_of_return)
        [Numpy](https://numpy.org/doc/stable/reference/generated/numpy.log.html)

        """
    )

    "----------"

    #Desviación Estándar
    st.markdown(
        """
        **:green[4. Standard Deviation - Volatility]**
        """
    )
    st.markdown(
        """
        $vol = \sigma\sqrt{252}$

        """
    )
    st.markdown(
        """
        [Source: Investopedia](https://www.investopedia.com/terms/s/standarddeviation.asp)
        [Volatility](https://www.investopedia.com/terms/v/volatility.asp)
        """
    )


st.subheader(":green[Additional Web Pages:]")

st.markdown(
    """
    1. [Simple Moving Average (SMA): Investopedia](https://www.investopedia.com/terms/s/sma.asp)
    2. [Damodaran ONLINE](https://pages.stern.nyu.edu/~adamodar/)
    3. [yfinance](https://pypi.org/project/yfinance/)
    4. [Plotly](https://plotly.com/python/)

    """
)

"----------"

st.subheader(":green[Books:]")

st.markdown("""
        1. Technical Analysis for the Trading Professional 2E (PB). (s. f.). (https://www.mhprofessional.com/technical-analysis-for-the-trading-professional-2e-pb-9781265905873-usa)
        
        """
        )

st.markdown("""
        2. Analysis for Financial Management. (2022, 21 enero). (https://www.mheducation.com/highered/product/analysis-financial-management-higgins-koski/M9781260772364.html)
        
        """
        )