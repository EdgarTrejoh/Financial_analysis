import streamlit as st 

def main():
    
    pg = st.navigation([
        st.Page("pages/home.py", title="Home", icon="🏚️"),
        st.Page("pages/TechnicalAnalysis.py", title="Technical Analysis", icon="💻"),
        st.Page("pages/FundamentalAnalysis.py", title="Fundamental Analysis", icon="📈"),
        st.Page("pages/Additional.py", title="Additional Information", icon="📕")
    ])

    pg.run()

if __name__ == "__main__":
    main()