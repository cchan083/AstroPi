import streamlit as st


def main():
    selected = st.navigation(
        [
            st.Page("pages/home_page.py", title="Home", icon='🏠'),
            st.Page("pages/gallery_page.py", title="Gallery", icon="🖼️"),
            st.Page("pages/graphs_page.py", title="Dashboard", icon="📊"),
            st.Page("pages/process_page.py", title="Development Process", icon="⚙️")
        ]
    )
    selected.run()

    
    

    
if __name__ == "__main__":
    main()