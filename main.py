import streamlit as st

def main():
    
    pg = st.navigation([
        st.Page("modulos/home.py", title="Home", icon="🏚️"),
        st.Page("modulos/TechnicalAnalysis.py", title="Technical Analysis", icon="💻"),
        st.Page("modulos/FundamentalAnalysis.py", title="Fundamental Analysis", icon="📈"),
        st.Page("modulos/Additional.py", title="Additional Information", icon="📕")
    ])

    pg.run()

if __name__ == "__main__":
    main()